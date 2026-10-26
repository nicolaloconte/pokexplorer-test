"""Browser checks of gender sprite paths, menu reset, responsive bag and
last-ball warning with mocked API. Cannot certify real online 80-floor run."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, json
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text()
html=re.sub(r'<script\s+src="[^"]+"\s*></script>','',html)
html=re.sub(r'<link[^>]+(?:href="https?://|rel="stylesheet")[^>]*>','',html)
html=html.replace('</head>','<style>'+(root/'style.css').read_text()+'</style></head>')
with sync_playwright() as p:
 browser=p.chromium.launch(**({'executable_path':'/usr/bin/chromium'} if Path('/usr/bin/chromium').exists() else {}),headless=True,args=['--no-sandbox'])
 results=[]
 for width,height in [(360,720),(390,844),(1440,900)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('https://**/*',lambda r:r.abort())
  page.set_content(html,wait_until='domcontentloaded')
  for f in ['music.js','api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js','main.js']:
   page.add_script_tag(content=(root/'js'/f).read_text())
  page.evaluate('window.dispatchEvent(new Event("DOMContentLoaded"))')
  page.evaluate("document.getElementById('pokex-extraction-warning').hidden=true")
  page.evaluate("GameEngine.prototype.getPokemonData=async function(id){return {id:Number(id),name:`pokemon-${id}`,base_experience:65,types:[{type:{name:'normal'}}],sprites:{front_default:'assets/ui/pokemon-placeholder.svg',back_default:'assets/ui/pokemon-placeholder.svg'},stats:[],abilities:[],moves:[],species:{name:`pokemon-${id}`}}};")
  page.locator('#btn-start-game').click()
  page.locator('#choose-female').click()
  assert page.evaluate("game.playerGender==='female'")
  page.locator('.pokeball-wrapper').first.click()
  page.locator('#btn-confirm-yes').click()
  assert page.evaluate("game.team.length===1 && game.playerGender==='female'")
  assert page.evaluate("game.walkSpritePreloads.some(p=>p.src.includes('/girl/walk/'))")
  page.evaluate("game.items.pokeball=1;game.battleType='wild';game.isRaidActive=false;game.battleBusy=false;game.pendingItemTarget=null;game.dialogueResolve=null;game.hasForcedBattleAction=()=>false;game.isBattleVisible=()=>true;game.askBattleConfirmation=(m)=>window._lastBallText=m;game.chooseBattleItem('pokeball');")
  assert 'ultima Poké Ball' in page.evaluate('window._lastBallText')
  bag=page.locator('#bag-list')
  details=bag.evaluate('(e)=>({maxHeight:getComputedStyle(e).maxHeight,scrollHeight:e.scrollHeight,clientHeight:e.clientHeight})')
  assert not errors,(width,errors)
  page.evaluate("game.returnToMainMenu()")
  assert page.evaluate('game.team.length===0 && game.floor===1 && game.badges.length===0')
  assert page.evaluate("game.devMode===false && game.raidTriggeredOnFloor===false")
  results.append({'width':width,'female_avatar':'PASS','last_ball':'PASS','menu_reset':'PASS','bag':details})
  page.close()
 browser.close()
 print(json.dumps({'browser_gameplay_qa':'PASS','results':results},ensure_ascii=False,indent=2))
