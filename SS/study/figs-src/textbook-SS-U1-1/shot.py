import sys, asyncio
from playwright.sync_api import sync_playwright
src = sys.argv[1]; out = sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1000, 'height': 1200})
    msgs=[]
    pg.on('console', lambda m: msgs.append(m.text))
    pg.goto('file://' + src)
    pg.wait_for_function("document.body.dataset.katex==='done'", timeout=20000)
    errs = pg.evaluate("document.querySelectorAll('.katex-error').length")
    print('katex errors', errs, msgs)
    for i, el in enumerate(pg.query_selector_all('.fig')):
        el.screenshot(path=f'{out}/fig_{i:02d}.png')
    pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
    pg.pdf(path=f'{out}/out.pdf', format='A4', print_background=True, margin={'top':'14mm','bottom':'16mm','left':'13mm','right':'13mm'})
    b.close()
