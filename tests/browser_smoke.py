"""Chromium smoke tests for the locally inlined build. No external API is required.
Run: python tests/browser_smoke.py  (requires Playwright+Chromium).
These are simulated browser tests, NOT a full online playthrough.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re
ROOT=Path(__file__).resolve().parents[1]
html=ROOT.joinpath('index.html').read_text()
html=re.sub(r'<script\s+src="[^"]+"\s*></script>','',html)
html=re.sub(r'<link[^>]+(?:href="https?://|rel="stylesheet")[^>]*>','',html)
html=html.replace('</head>','<style>'+ROOT.joinpath('style.css').read_text()+'</style></head>')
with sync_playwright() as p:
    chromium='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None
    browser=p.chromium.launch(**({'executable_path':chromium} if chromium else {}),headless=True,args=['--no-sandbox'])
    findings=[]
    for width in [360,390,768,1024,1440]:
        page=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce')
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        # Simulated game data; isolate rendering mechanics from network availability.
        page.route('https://**/*',lambda route:route.abort())
        page.set_content(html,wait_until='domcontentloaded',timeout=30000)
        for file in ['music.js','api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js','main.js']:
            page.add_script_tag(content=ROOT.joinpath('js',file).read_text())
        page.evaluate('window.dispatchEvent(new Event("DOMContentLoaded"))')
        # Extraction warning is expected for inline test fixture (no external stylesheet).
        page.evaluate('document.getElementById("pokex-extraction-warning").hidden=true')
        assert page.evaluate('Boolean(window.game)'),f'no game at {width}'
        page.evaluate('''GameEngine.prototype.getPokemonData=async function(id){return {id:Number(id),name:`pokemon-${id}`,base_experience:65,types:[{type:{name:'normal'}}],sprites:{front_default:'',back_default:''},stats:[],abilities:[],moves:[],species:{name:`pokemon-${id}`}}};''')
        page.locator('#btn-start-game').click(timeout=7000)
        page.locator('.pokeball-wrapper').first.click(timeout=7000)
        page.locator('#btn-confirm-yes').click(timeout=7000)
        page.evaluate("document.getElementById('starter-showcase-img').dispatchEvent(new Event('error'))")
        assert page.evaluate("document.getElementById('starter-showcase-img').getAttribute('src')")=='assets/ui/pokemon-placeholder.svg'
        status=page.evaluate('''(()=>({floor:game.floor,team:game.team.length,map:game.gridMap.length,overflow:document.documentElement.scrollWidth>innerWidth,loaded:typeof game.getPokemonData==='function'}))()''')
        assert status['team']==1 and status['map']==10,status
        assert not status['overflow'],(width,status)
        page.locator('#language-en').evaluate('(e)=>e.click()')
        assert page.evaluate('document.documentElement.lang')=='en'
        page.locator('#language-it').evaluate('(e)=>e.click()')
        if width==1440:
            d=page.evaluate('''(()=>{const g=game, prev=[g.renderDungeon,g.renderSidebar,g.logMsg];g.renderDungeon=()=>{};g.renderSidebar=()=>{};g.logMsg=()=>{};let bad=0,wrongSize=0;for(let n=1;n<=500;n++){g.floor=(n%80)+1;g.generateFloorDungeon();const map=g.gridMap;wrongSize+=(map.length!==10||map.some(row=>row.length!==10))?1:0;const open=new Set(['0,0']),q=[[0,0]];for(let k=0;k<q.length;k++){let [x,y]=q[k];for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){const a=x+dx,b=y+dy,s=`${a},${b}`;if(a<0||b<0||a>9||b>9||open.has(s)||['tree','water'].includes(map[b][a].type))continue;open.add(s);q.push([a,b]);}}if(!open.has('9,9')||map.flat().some(c=>['trainer','item'].includes(c.entity)&&!open.has(`${c.x},${c.y}`)))bad++;}g.renderDungeon=prev[0];g.renderSidebar=prev[1];g.logMsg=prev[2];return {generations:500,bad,wrongSize};})()''')
            assert d['bad']==0 and d['wrongSize']==0,d
            findings.append({'dungeon_reachability':d})
        findings.append({'viewport':width,'status':status,'errors':errors[:3]})
        assert not errors,(width,errors)
        page.close()
    browser.close()
    print(json.dumps({'result':'PASS','checks':findings},indent=2,ensure_ascii=False))

