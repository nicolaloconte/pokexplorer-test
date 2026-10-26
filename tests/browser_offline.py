"""T08: verify starter retry visible after an actual browser network failure.
Requests are blocked intentionally, not simulated with successful Pokémon data."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, json
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text()
html=re.sub(r'<script\s+src="[^"]+"\s*></script>','',html)
html=re.sub(r'<link[^>]+(?:href="https?://|rel="stylesheet")[^>]*>','',html)
html=html.replace('</head>','<style>'+(root/'style.css').read_text()+'</style></head>')
with sync_playwright() as p:
 b=p.chromium.launch(**({'executable_path':'/usr/bin/chromium'} if Path('/usr/bin/chromium').exists() else {}),headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
 page.route('https://**/*',lambda r:r.abort())
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html,wait_until='domcontentloaded')
 for f in ['music.js','api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js','main.js']:
  page.add_script_tag(content=(root/'js'/f).read_text())
 page.evaluate('window.dispatchEvent(new Event("DOMContentLoaded"))')
 page.evaluate("document.getElementById('pokex-extraction-warning').hidden=true")
 page.locator('#btn-start-game').click()
 retry=page.get_by_role('button',name='RIPROVA')
 retry.wait_for(timeout=15000)
 assert retry.is_visible()
 assert page.evaluate("game.team.length===0")
 retry.click()
 retry.wait_for(timeout=15000)
 assert not errors,errors
 print(json.dumps({'offline_retry':'PASS','retry_visible':True,'game_not_corrupted':True},indent=2))
 b.close()
