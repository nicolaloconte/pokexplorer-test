"""UI-only regression for R2.21 RC2.1: DEV commands moved out of left wing.
Run: python tests/browser_dev_panel.py (requires Playwright Chromium).
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, json
root=Path(__file__).resolve().parents[1]
html=root.joinpath('index.html').read_text()
html=re.sub(r'<script\s+src="[^"]+"\s*></script>','',html)
html=re.sub(r'<link[^>]+(?:href="https?://|rel="stylesheet")[^>]*>','',html)
html=html.replace('</head>','<style>'+root.joinpath('style.css').read_text()+'</style></head>')
checks=[]
with sync_playwright() as p:
    chromium='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None
    browser=p.chromium.launch(**({'executable_path':chromium} if chromium else {}),headless=True,args=['--no-sandbox'])
    for width,height in [(360,650),(390,844),(1440,900)]:
        page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
        errors=[]
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.route('https://**/*',lambda route:route.abort())
        page.set_content(html,wait_until='domcontentloaded')
        for f in ['music.js','api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js','main.js']:
            page.add_script_tag(content=root.joinpath('js',f).read_text())
        page.evaluate('window.dispatchEvent(new Event("DOMContentLoaded"))')
        page.evaluate('document.getElementById("pokex-extraction-warning").hidden=true')
        assert page.evaluate('!!window.game')
        assert page.locator('.rotom-wing-left #developer-panel').count()==0
        assert page.locator('#quick-settings-panel #developer-panel').count()==1
        assert page.locator('#developer-panel').is_hidden()
        page.locator('#quick-settings-toggle').click()
        page.locator('#dev-mode-trigger').click()
        page.locator('#dev-access-code').fill('2103')
        page.locator('#dev-code-confirm').click()
        assert page.evaluate('game.devMode === true')
        assert page.locator('#developer-panel').is_hidden(), 'DEV controls should stay hidden until Options opens'
        page.locator('#quick-settings-toggle').click()
        assert page.locator('#developer-panel').is_visible()
        border=page.locator('#developer-panel').evaluate('(e)=>getComputedStyle(e).borderStyle')
        assert border=='none', border
        page.locator('#dev-radar').click()
        assert page.evaluate('game.radarCharges === Infinity')
        page.locator('#dev-capture').click()
        assert page.evaluate('game.devGuaranteedCapture === true')
        page.locator('#dev-skip-encounter').click()
        assert not errors, errors
        # Existing buttons and events remain functional; no gameplay changes.
        panel=page.locator('#quick-settings-panel').evaluate('(e)=>({height:e.getBoundingClientRect().height,scroll:e.scrollHeight,client:e.clientHeight})')
        assert panel['height']<=height-55, (width,panel)
        checks.append({'viewport':width,'menu':panel,'dev_visible_in_options':True,'errors':errors})
        page.close()
    browser.close()
print(json.dumps({'result':'PASS','checks':checks},ensure_ascii=False,indent=2))
