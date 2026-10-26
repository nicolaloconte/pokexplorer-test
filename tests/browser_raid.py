"""Seeded 500-map Raid invariant audit + recovery overlay smoke test.
Simulated PokéAPI. Does not certify an online playthrough.
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
    page=browser.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce')
    page.route('https://**/*',lambda route:route.abort())
    page.set_content(html,wait_until='domcontentloaded',timeout=30000)
    for file in ['music.js','api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js','main.js']:
        page.add_script_tag(content=ROOT.joinpath('js',file).read_text())
    page.evaluate('window.dispatchEvent(new Event("DOMContentLoaded"))')
    # No need for network-based starter selection in the map/inventory audit.
    report=page.evaluate('''()=>{
      const g=window.game;
      if(!g)throw Error('GameEngine is unavailable');
      const originalRandom=Math.random;
      const oldRender=[g.renderDungeon,g.renderSidebar,g.logMsg];
      let state=0x1647babe;
      Math.random=()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state/4294967296;};
      g.renderDungeon=()=>{};g.renderSidebar=()=>{};g.logMsg=()=>{};
      let checked=0,violations=[];const footprints=[];
      try{
        for(let i=0;i<500;i++){
          g.floor=(i%80)+1;
          g.generateFloorDungeon();
          const map=g.gridMap,city=g.floor%5===0;
          if(map.length!==10||map.some(r=>r.length!==10))violations.push([i,'dimension']);
          if(g.raidTriggeredOnFloor||g.raidQueueCount||g.isRaidActive)violations.push([i,'Raid state']);
          const items=map.flat().filter(c=>c.entity==='item');
          const trainers=map.flat().filter(c=>c.entity==='trainer');
          if(city){if(items.length||trainers.length)violations.push([i,'town spawn',items.length,trainers.length]);}
          else if(items.length<1||items.length>3||trainers.length<1||trainers.length>4)
            violations.push([i,'counts',items.length,trainers.length]);
          const reached=new Set(['0,0']),todo=[[0,0]];
          for(let q=0;q<todo.length;q++){
            const [x,y]=todo[q];
            for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){
              const nx=x+dx,ny=y+dy,k=nx+','+ny;
              if(nx<0||ny<0||nx>9||ny>9||reached.has(k)||['water','tree'].includes(map[ny][nx].type))continue;
              reached.add(k);todo.push([nx,ny]);
            }
          }
          if(!reached.has('9,9'))violations.push([i,'exit unreachable']);
          for(const c of [...items,...trainers])if(!reached.has(c.x+','+c.y))violations.push([i,'entity unreachable',c.x,c.y]);
          checked++;
          if(i<3)footprints.push({floor:g.floor,items:items.length,trainers:trainers.length});
        }
      }finally{Math.random=originalRandom;[g.renderDungeon,g.renderSidebar,g.logMsg]=oldRender;}
      return {seed:'0x1647babe',checked,violationCount:violations.length,violations:violations.slice(0,10),footprints};
    }''')
    assert report['checked']==500 and report['violationCount']==0,report
    # DOM for retry button and overlay, without connecting to PokéAPI.
    state=page.evaluate('''()=>{
      const g=window.game;
      g.isRaidActive=true;g.raidQueueCount=3;g.raidBattleRetryPending=true;
      g.$id('raid-api-error').classList.remove('hidden');
      g.startBattle=()=>{g.mockRaidRetryCalls=(g.mockRaidRetryCalls||0)+1;};
      const first=g.retryRaidBattle(),second=g.retryRaidBattle();
      return {first,second,calls:g.mockRaidRetryCalls,hidden:g.$id('raid-api-error').classList.contains('hidden')};
    }''')
    assert state=={'first':True,'second':False,'calls':1,'hidden':True},state
    print(json.dumps({'status':'PASS','map_audit':report,'raid_error_UI':state},ensure_ascii=False,indent=2))
    browser.close()
