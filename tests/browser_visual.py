"""Deterministic-ish Chromium visual snapshots. --update-baseline writes approved
snapshots. This protects UI layout but does not replace real-device review.
"""
from pathlib import Path
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
import re
import argparse, json, io
ROOT=Path(__file__).resolve().parents[1]
GOLDEN=ROOT/'tests'/'visual-baseline'
p=argparse.ArgumentParser();p.add_argument('--update-baseline',action='store_true');args=p.parse_args()
html=(ROOT/'index.html').read_text()
html=re.sub(r'<script\s+src="[^"]+"\s*></script>','',html)
html=re.sub(r'<link[^>]+(?:href="https?://|rel="stylesheet")[^>]*>','',html)
html=html.replace('</head>','<style>'+(ROOT/'style.css').read_text()+'</style></head>')
try:
 with sync_playwright() as play:
  browser=play.chromium.launch(**({'executable_path':'/usr/bin/chromium'} if Path('/usr/bin/chromium').exists() else {}),headless=True,args=['--no-sandbox'])
  results=[]
  for width,height in [(390,844),(1440,900)]:
   page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
   page.route('https://**/*',lambda r:r.abort())
   page.set_content(html,wait_until='domcontentloaded',timeout=30000)
   for f in ['music.js','api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js','main.js']:
    page.add_script_tag(content=(ROOT/'js'/f).read_text())
   page.evaluate('window.dispatchEvent(new Event("DOMContentLoaded"))')
   page.evaluate("document.getElementById('pokex-extraction-warning').hidden=true")
   page.evaluate("document.querySelectorAll('*').forEach(x=>{x.style.setProperty('animation','none','important');x.style.setProperty('transition','none','important');})")
   assert page.evaluate('!!window.game')
   page.evaluate("GameEngine.prototype.getPokemonData=async function(id){return {id:Number(id),name:`pokemon-${id}`,base_experience:65,types:[{type:{name:'normal'}}],sprites:{front_default:'assets/ui/pokemon-placeholder.svg',back_default:'assets/ui/pokemon-placeholder.svg'},stats:[],abilities:[],moves:[],species:{name:`pokemon-${id}`}}};")
   for stage in ['menu','adventure']:
    if stage=='adventure':
     page.locator('#btn-start-game').click()
     page.locator('.pokeball-wrapper').first.click()
     page.locator('#btn-confirm-yes').click()
    page.wait_for_timeout(150)
    png=page.screenshot(animations='disabled')
    out=GOLDEN/f'{width}-{stage}.png'
    if args.update_baseline:
     GOLDEN.mkdir(parents=True,exist_ok=True);out.write_bytes(png)
     results.append({'viewport':width,'stage':stage,'baseline':'updated'})
    else:
     assert out.is_file(),f'Visual baseline missing: {out}; run --update-baseline after approving appearance'
     old=Image.open(out).convert('RGB');new=Image.open(io.BytesIO(png)).convert('RGB')
     assert old.size==new.size,(old.size,new.size)
     change=ImageChops.difference(old,new)
     pixels=sum(1 for r,g,b in change.getdata() if max(r,g,b)>25)
     ratio=pixels/(old.width*old.height)
     assert ratio<.02,f'Visual regression at {width}px, {stage}: {ratio:.2%} changed'
     results.append({'viewport':width,'stage':stage,'changed_pixels_pct':round(ratio*100,3)})
   page.close()
  browser.close()
  print(json.dumps({'visual_snapshot':'PASS','results':results},indent=2))
finally:
 pass
