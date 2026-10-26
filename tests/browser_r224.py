"""Offline Chromium acceptance suite, simulated Pokémon API. No remote services."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re,json
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text()
html=re.sub(r'<script\s+src="[^"]+"[^>]*></script>','',html)
html=re.sub(r'<link[^>]*rel="stylesheet"[^>]*>','',html)
html=html.replace('</head>','<style>'+(root/'style.css').read_text()+'</style></head>')
files=['music.js','api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js','checkpoints.js','auth-cloud.js','main.js']
reports=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in [(360,800),(390,844),(412,915),(768,900),(1440,900)]:
  page=b.new_page(viewport={'width':w,'height':h},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
  page.route('https://**/*',lambda route:route.abort())
  page.set_content(html,wait_until='domcontentloaded',timeout=20000)
  page.evaluate('''window._checkpointStorage=new Map();Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>window._checkpointStorage.get(k)||null,setItem:(k,v)=>window._checkpointStorage.set(k,v),removeItem:k=>window._checkpointStorage.delete(k)}});''')
  for file in files:page.add_script_tag(content=(root/'js'/file).read_text())
  page.evaluate('window.dispatchEvent(new Event("DOMContentLoaded"))')
  page.evaluate("document.getElementById('pokex-extraction-warning').hidden=true")
  page.evaluate('''GameEngine.prototype.getPokemonData=async function(id){return {id:+id,name:'charmander',base_experience:65,types:[{type:{name:'fire'}}],sprites:{front_default:'',back_default:''},stats:[],abilities:[],moves:[],species:{name:'charmander'}}}''')
  page.locator('#btn-start-game').click(timeout=10000)
  page.locator('.pokeball-wrapper').first.click(timeout=10000)
  page.locator('#btn-confirm-yes').click(timeout=10000)
  assert page.evaluate('game.team.length')==1
  assert page.evaluate('!!PokexCheckpoints.load()'), 'No saved starter'
  assert page.evaluate('''(()=>{const s=PokexCheckpoints.load();const g=game;g.money=721;g.floor=5;g.renderSidebar();g.saveCheckpoint();g.money=9;g.floor=1;return PokexCheckpoints.restore(g,PokexCheckpoints.load())&&g.money===721&&g.floor===5&&g.team[0] instanceof Pokemon&&g.team[0].moves[0] instanceof Move})()''')
  page.evaluate('game.isCelestialCave=true;game.renderSidebar()')
  assert 'Grotta Celeste' in page.locator('#route-location-label').inner_text()
  page.evaluate("game.setGameLanguage('en');game.renderSidebar()")
  assert 'Cerulean Cave' in page.locator('#route-location-label').inner_text()
  page.evaluate('game.isCelestialCave=false;game.setGameLanguage("it")')
  assert page.locator('.rotom-mouth').is_visible()
  assert not page.locator('.rotom-wing-right .dpad-container').is_visible()
  page.evaluate("document.getElementById('pokemart-overlay').classList.remove('hidden');game.isLocked=true")
  # Button must be inside the viewport / scrollable card, not buried beyond visible area.
  exit=page.locator('#close-market-btn')
  assert exit.is_visible()
  assert exit.bounding_box()['y']+exit.bounding_box()['height'] <= h+3,(w,exit.bounding_box())
  page.locator('#mart-close-x').click(timeout=5000)
  assert page.evaluate("document.getElementById('pokemart-overlay').classList.contains('hidden')&&!game.isLocked")
  assert page.evaluate('document.documentElement.scrollWidth-innerWidth')<4
  shot=root/'docs'/'visual'/f'r224-{w}-market.png'
  if w in (390,1440):
   page.evaluate("document.getElementById('pokemart-overlay').classList.remove('hidden')")
   page.screenshot(path=str(shot),animations='disabled')
  if w==1440:
   campaign=page.evaluate("""(()=>{const g=game, oldRender=g.renderDungeon, oldSide=g.renderSidebar, oldLog=g.logMsg;g.renderDungeon=()=>{};g.renderSidebar=()=>{};g.logMsg=()=>{};const out={floors:0,brokenMaps:0,missingExits:0,unreachable:0};for(let floor=1;floor<=80;floor++){g.floor=floor;g.generateFloorDungeon();out.floors++;const map=g.gridMap;if(map.length!==10||map.some(r=>r.length!==10))out.brokenMaps++;if(!map[9]||map[9][9].entity!=='door')out.missingExits++;const visited=new Set(['0,0']),queue=[[0,0]];for(let i=0;i<queue.length;i++){const [x,y]=queue[i];for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){const a=x+dx,b=y+dy,k=a+','+b;if(a<0||b<0||a>9||b>9||visited.has(k)||['tree','water'].includes(map[b][a].type))continue;visited.add(k);queue.push([a,b]);}}if(!visited.has('9,9'))out.unreachable++;}g.renderDungeon=oldRender;g.renderSidebar=oldSide;g.logMsg=oldLog;return out;})()""")
   assert campaign['floors']==80 and not any(campaign[k] for k in ['brokenMaps','missingExits','unreachable']),campaign
  reports.append({'viewport':f'{w}x{h}' ,'market_exit':True,'local_checkpoint':True,'cave_location':True,'mouth':True,'simulated_80_floors':campaign if w==1440 else None,'errors':errors})
  assert not errors,(w,errors)
  page.close()
 b.close()
print(json.dumps({'status':'PASS','reports':reports},ensure_ascii=False,indent=2))
