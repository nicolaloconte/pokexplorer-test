"""B-F offline UI regression for new consented changes. No account or deployment."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, json
ROOT=Path(__file__).resolve().parents[1]
html=ROOT.joinpath('index.html').read_text()
html=re.sub(r'<script\s+src="[^"]+"\s*></script>','',html)
html=re.sub(r'<link[^>]+(?:href="https?://|rel="stylesheet")[^>]*>','',html)
html=html.replace('</head>','<style>'+ROOT.joinpath('style.css').read_text()+'</style></head>')
js_files=['music.js','api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js','main.js']
checks=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,headless=True,args=['--no-sandbox'])
 for width,height in [(360,780),(390,844),(768,900),(1440,900)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  errors=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.route('https://**/*',lambda route:route.abort())
  page.set_content(html,wait_until='domcontentloaded')
  for filename in js_files:page.add_script_tag(content=(ROOT/'js'/filename).read_text())
  page.evaluate('window.dispatchEvent(new Event("DOMContentLoaded"))')
  page.evaluate('document.getElementById("pokex-extraction-warning").hidden=true')
  assert page.locator('#btn-start-game').is_visible()
  assert page.locator('#btn-continue-game').is_disabled()
  assert page.locator('#btn-view-progress').is_visible()
  assert page.locator('#btn-contact-support').is_visible()
  assert page.locator('#build-version').count()==0
  page.locator('#btn-contact-support').click()
  assert 'assistenza' in page.locator('#menu-message-text').inner_text().lower()
  # NO stays on menu; YES opens only the exact user-provided invitation.
  page.locator('#menu-message-cancel').click()
  assert page.evaluate('document.querySelector("#main-menu-overlay").classList.contains("hidden")') is False
  page.evaluate('window._lastSupportURL=null;window.open=(url)=>{window._lastSupportURL=url;return null;}')
  page.locator('#btn-contact-support').click()
  page.locator('#menu-message-confirm').click()
  assert page.evaluate('window._lastSupportURL')=='https://discord.com/invite/qNGscTEYHM'
  assert page.locator('#menu-message').get_attribute('class').find('hidden')>=0
  page.evaluate("GameEngine.prototype.getPokemonData=async function(id){return {id:Number(id),name:'charmander',base_experience:65,types:[{type:{name:'fire'}}],sprites:{front_default:'',back_default:''},stats:[],abilities:[{ability:{name:'blaze'},is_hidden:false}],moves:[],species:{name:'charmander'}}};")
  page.locator('#btn-start-game').click()
  page.locator('.pokeball-wrapper').first.click()
  page.locator('#btn-confirm-yes').click()
  assert page.evaluate('window.game.team.length')==1
  for floor,expected in [(1,'PERCORSO 1'),(5,'VILLAGGIO'),(10,'PLUMBEOPOLI'),(15,'VILLAGGIO'),(20,'CELESTOPOLI'),(40,'AZZURROPOLI'),(70,'ISOLA CANNELLA'),(80,'SMERALDOPOLI')]:
   page.evaluate('(floor)=>{game.floor=floor;game.renderSidebar()}',floor)
   assert expected in page.locator('#route-location-label').inner_text().upper(),(floor,page.locator('#route-location-label').inner_text())
  page.evaluate('game.floor=1;game.bagCategory="chiave";game.renderSidebar()')
  items=page.locator('#bag-list .bag-key-item')
  assert items.count()==2
  assert items.nth(0).is_disabled() and items.nth(1).is_disabled()
  assert items.nth(0).locator('img').get_attribute('src').endswith('old-rod-user.png')
  assert items.nth(1).locator('img').get_attribute('src').endswith('exp-share-user.png')
  assert 'Canna' in items.nth(0).inner_text() and 'Condividi' in items.nth(1).inner_text()
  page.evaluate('game.items.fishingRod=true;game.expShareClaimed=true;game.renderSidebar()')
  assert items.nth(0).is_disabled() and items.nth(1).is_enabled()
  before=page.evaluate('game.expShareEnabled')
  items.nth(1).click()
  assert page.evaluate('game.expShareEnabled')!=before
  assert 'ON' not in items.nth(1).inner_text() and 'OFF' not in items.nth(1).inner_text()
  # The English UI is recomputed at language change, not only by static data attributes.
  page.evaluate("game.setGameLanguage('en')")
  assert 'TRAIL: ROUTE 1' in page.locator('#route-location-label').inner_text().upper()
  assert 'Fishing Rod' in items.nth(0).inner_text()
  assert 'Exp. Share' in items.nth(1).inner_text()
  page.evaluate("game.setGameLanguage('it')")
  # Summary card renders in both languages with the existing battle mechanics untouched.
  page.evaluate("game.openPokemonInfo(game.team[0])")
  assert page.locator('#pokemon-info-level').inner_text().startswith('LIVELLO')
  assert page.locator('#pokemon-info-nature').inner_text().startswith('NATURA')
  page.evaluate("game.setGameLanguage('en')")
  assert page.locator('#pokemon-info-level').inner_text().startswith('LEVEL')
  assert page.locator('#pokemon-info-nature').inner_text().startswith('NATURE')
  assert page.locator('#pokemon-info-ability').inner_text().startswith('ABILITY')
  page.evaluate("game.setGameLanguage('it')")
  page.locator('#pokemon-info-close').click()
  assert page.locator('#pokemon-info-overlay').get_attribute('class').find('hidden')>=0
  # Scrollbar absence when enough vertical space exists and no horizontal overflow.
  metrics=page.evaluate('''()=>{const c=document.querySelector('.rotom-wing-right .wing-screen');return {
   overflow:document.documentElement.scrollWidth-innerWidth,
   keys:[...document.querySelectorAll('#bag-list .bag-key-item')].map(n=>({height:n.getBoundingClientRect().height,disabled:n.disabled})),
   faceHeight:document.querySelector('.rotom-face').getBoundingClientRect().height,
   sidebarHeight:c.getBoundingClientRect().height};}''')
  assert metrics['overflow']<=1,(width,metrics)
  assert not errors,(width,errors)
  checks.append({'viewport':f'{width}x{height}','menu':True,'location':True,'keyItems':True,'language':True,'overflow':metrics['overflow']})
  if width in [390,1440]:
   (ROOT/'docs'/'visual'/f'{width}-batchbf.png').write_bytes(page.screenshot(animations='disabled'))
  page.close()
 browser.close()
print(json.dumps({'B-F_offline':'PASS','checks':checks},indent=2,ensure_ascii=False))
