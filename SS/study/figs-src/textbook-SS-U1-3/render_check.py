# -*- coding: utf-8 -*-
"""unit-textbook：渲染檢查＋輸出 PDF。

用法：python3 render_check.py <講義.html 絕對路徑> <輸出資料夾> [--pdf 輸出.pdf]

做四件事：
  1. 等 KaTeX 渲染完，回報 .katex-error 數量（必須為 0）
  2. 逐張 .fig 截圖 → <輸出資料夾>/fig_NN.png（交付前必須逐張目視）
  3. 自動抓 SVG 排版問題：文字超出 viewBox、兩段文字互相重疊（>25% 面積）
  4. 展開所有 <details>（自我測驗答案）後列印 A4 PDF

需求：Python Playwright + Chromium（Cowork 雲端環境已內建；HTML 必須和 assets/katex/ 放在同一層，否則 KaTeX 載不到會逾時）。
"""
import sys, os
from playwright.sync_api import sync_playwright

CHECK_JS = r"""
() => {
  const out = [];
  document.querySelectorAll('.fig > svg').forEach((svg, i) => {
    const vb = svg.viewBox.baseVal;
    const boxes = [];
    svg.querySelectorAll('text').forEach(t => {
      let b; try { b = t.getBBox(); } catch (e) { return; }
      if (!b || b.width === 0) return;
      const txt = t.textContent.trim().slice(0, 24);
      if (b.x < vb.x - 2 || b.y < vb.y - 2 || b.x + b.width > vb.x + vb.width + 2 || b.y + b.height > vb.y + vb.height + 2)
        out.push(`fig#${i} [${svg.closest('.fig').id}] 文字超出畫布：「${txt}」`);
      boxes.push({b, txt});
    });
    for (let a = 0; a < boxes.length; a++) for (let c = a + 1; c < boxes.length; c++) {
      const p = boxes[a].b, q = boxes[c].b;
      const w = Math.min(p.x + p.width, q.x + q.width) - Math.max(p.x, q.x);
      const h = Math.min(p.y + p.height, q.y + q.height) - Math.max(p.y, q.y);
      if (w <= 0 || h <= 0) continue;
      const small = Math.min(p.width * p.height, q.width * q.height);
      if (w * h > 0.25 * small)
        out.push(`fig#${i} [${svg.closest('.fig').id}] 文字重疊：「${boxes[a].txt}」×「${boxes[c].txt}」`);
    }
  });
  return out;
}
"""


def main():
    src, outdir = os.path.abspath(sys.argv[1]), sys.argv[2]
    pdf = sys.argv[sys.argv.index('--pdf') + 1] if '--pdf' in sys.argv else os.path.join(outdir, 'out.pdf')
    os.makedirs(outdir, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1000, 'height': 1200})
        pg.goto('file://' + src)
        pg.wait_for_function("document.body.dataset.katex==='done'", timeout=30000)
        nerr = pg.evaluate("document.querySelectorAll('.katex-error').length")
        print(f'KaTeX 錯誤：{nerr}')
        figs = pg.query_selector_all('.fig')
        for i, el in enumerate(figs):
            el.screenshot(path=os.path.join(outdir, f'fig_{i:02d}.png'))
        print(f'圖：{len(figs)} 張 → {outdir}/fig_NN.png')
        issues = pg.evaluate(CHECK_JS)
        print(f'SVG 排版疑點：{len(issues)}')
        for s in issues:
            print('  ', s)
        pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
        pg.pdf(path=pdf, format='A4', print_background=True,
               margin={'top': '14mm', 'bottom': '16mm', 'left': '13mm', 'right': '13mm'})
        print('PDF →', pdf)
        b.close()


if __name__ == '__main__':
    main()
