# -*- coding: utf-8 -*-
"""unit-textbook：建立某單元的教科書講義工作資料夾。

用法（在知識庫根目錄 exam-wiki-XX/ 執行）：
    python3 <skill>/scripts/new_unit.py XX-Un-m [--volumes key1,key2]

會建立 study/figs-src/textbook-XX-Un-m/，放入：
    lib.py、plot.py、build.py、render_check.py（本 skill 的腳本）
    textbook.json（分冊設定）、calcs.py（數值）、ch0.html＋figs_ch0.py（範本）
已存在的檔案一律不覆蓋。
"""
import os, sys, json, shutil, re

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')


def main():
    if len(sys.argv) < 2 or not re.match(r'^[A-Z]{2}-U\d+-\d+$', sys.argv[1]):
        sys.exit('用法：new_unit.py XX-Un-m [--volumes a,b]')
    code = sys.argv[1]
    vols = ['main']
    if '--volumes' in sys.argv:
        vols = sys.argv[sys.argv.index('--volumes') + 1].split(',')
    if not os.path.isdir('study'):
        sys.exit('找不到 study/：請在知識庫根目錄（exam-wiki-XX/）執行')
    wd = os.path.join('study', 'figs-src', f'textbook-{code}')
    os.makedirs(wd, exist_ok=True)

    def put(src, dst, text=None):
        p = os.path.join(wd, dst)
        if os.path.exists(p):
            print('  已存在，略過', p)
            return
        if text is None:
            shutil.copy(src, p)
        else:
            open(p, 'w', encoding='utf8').write(text)
        print('  建立', p)

    for f in ('lib.py', 'plot.py', 'build.py', 'render_check.py'):
        put(os.path.join(HERE, f), f)
    put(os.path.join(ASSETS, 'calcs_template.py'), 'calcs.py')
    tpl = open(os.path.join(ASSETS, 'chapter_template.html'), encoding='utf8').read()
    put(None, 'ch0.html', tpl.replace('chN', 'ch0').replace('第 N 章', '第 0 章').replace('figN_', 'fig0_').replace('N.', '0.').replace('圖 N-', '圖 0-'))
    ftpl = open(os.path.join(ASSETS, 'figs_template.py'), encoding='utf8').read()
    put(None, 'figs_ch0.py', ftpl.replace('figN_', 'fig0_').replace('第 N 章', '第 0 章'))
    cfg = json.load(open(os.path.join(ASSETS, 'textbook_template.json'), encoding='utf8'))
    cfg = json.loads(json.dumps(cfg, ensure_ascii=False).replace('XX-Un-m', code))
    v0 = cfg['volumes'][0]
    cfg['volumes'] = []
    for i, k in enumerate(vols):
        v = dict(v0)
        v['key'] = k
        if len(vols) > 1:
            v['file'] = f'textbook-{code}-{k}.html'
            v['h1'] = f'{code} 單元名　第 {i + 1} 冊：{k}'
            v['nav_label'] = f'第 {i + 1} 冊'
        v['chapters'] = ['ch0'] if i == 0 else []
        cfg['volumes'].append(v)
    put(None, 'textbook.json', json.dumps(cfg, ensure_ascii=False, indent=2))
    print('完成。下一步：編輯 textbook.json、calcs.py，再逐章寫 chN.html＋figs_chN.py。')


if __name__ == '__main__':
    main()
