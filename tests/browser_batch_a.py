"""Batch A: T01/T02 regression on in-memory Chromium; Pokémon API is stubbed.
Run: python tests/browser_batch_a.py
No web, GitHub, Discord or user account is accessed.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re,json,base64
ROOT=Path(__file__).resolve().parents[1]
html=ROOT.joinpath('index.html').read_text()
html=re.sub(r'<script\s+src="[^"]+"\s*></script>','',html)
html=re.sub(r'<link[^>]+(?:href="https?://|rel="stylesheet")[^>]*>','',html)
html=html.replace('</head>','<style>'+ROOT.joinpath('style.css').read_text()+'</style></head>')
js_files=['music.js','api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js','main.js']
icon='data:image/svg+xml;base64,'+base64.b64encode((ROOT/'assets/ui/pokemon-placeholder.svg').read_bytes()).decode()
findings=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,headless=True,args=['--no-sandbox'])
    for width,height in [(360,780),(390,844),(768,900),(1024,900),(1440,900),(1440,760),(1440,650)]:
        page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.route('https://**/*',lambda route:route.abort())
        page.set_content(html,wait_until='domcontentloaded')
        for js in js_files: page.add_script_tag(content=(ROOT/'js'/js).read_text())
        page.evaluate('window.dispatchEvent(new Event("DOMContentLoaded"))')
        page.evaluate('document.getElementById("pokex-extraction-warning").hidden=true')
        page.evaluate("""GameEngine.prototype.getPokemonData=async function(id){return {id:Number(id),name:'charmander',base_experience:65,types:[{type:{name:'fire'}}],sprites:{front_default:'',back_default:''},stats:[],abilities:[],moves:[],species:{name:'charmander'}}};""")
        page.locator('#btn-start-game').click()
        page.locator('.pokeball-wrapper').first.click()
        page.locator('#btn-confirm-yes').click()
        page.evaluate('''(src)=>{game.team[0].name='CHARMANDER';game.team[0].spriteFront=src;game.renderSidebar();}''',icon)
        current=page.evaluate('''()=>{const wing=document.querySelector('.rotom-wing-left .wing-screen');
          const cells=[...document.querySelectorAll('#team-grid .team-slot')], radar=document.querySelector('#btn-scan-radar'),badge=document.querySelector('#btn-badge-case');
          const r=e=>e.getBoundingClientRect(); const R=r(radar),B=r(badge),W=r(wing),C=cells.map(r);
          const p=cells[0];return {slots:cells.length,active:p.classList.contains('active'),accessible:p.getAttribute('aria-label'),
          labelPseudo:getComputedStyle(p,'::after').content,statusAttr:p.getAttribute('data-status'),
          radarHeight:R.height,badgeVisible:B.height>0,radarBeforeBadge:R.bottom<=B.top,
          screenOverflow:wing.scrollHeight-wing.clientHeight,screenScrollStyle:getComputedStyle(wing).overflowY,
          badgeBottom:B.bottom,wingBottom:W.bottom,slotsNonoverlap:C.every((a,i)=>i===0||C[i-1].bottom<=a.top+.2),
          textOverflow:Math.max(...cells.map(c=>c.scrollWidth-c.clientWidth)),
          pageHorizontalOverflow:document.documentElement.scrollWidth-innerWidth};}''')
        assert current['slots']==6 and current['active'],(width,current)
        assert 'Pokémon attivo' in current['accessible'] and current['labelPseudo']=='none' and current['statusAttr'] is None,(width,current)
        assert current['radarHeight']<=50 and current['radarBeforeBadge'] and current['badgeVisible'],(width,current)
        assert current['slotsNonoverlap'] and current['textOverflow']<3 and current['pageHorizontalOverflow']<=0,(width,current)
        if height>=740 or width<1280:
            assert current['screenOverflow']<=0 and current['badgeBottom']<=current['wingBottom']+1,(width,current)
        if width<1280: assert current['screenScrollStyle']=='visible',(width,current)
        elif height>=740: assert current['screenScrollStyle']=='hidden',(width,current)
        else:
            assert current['screenScrollStyle']=='auto' and current['screenOverflow']>0,(width,current)
            page.locator('.rotom-wing-left .wing-screen').evaluate('(e)=>e.scrollTop=e.scrollHeight')
            assert page.evaluate('''()=>{let w=document.querySelector('.rotom-wing-left .wing-screen').getBoundingClientRect(),b=document.querySelector('#btn-badge-case').getBoundingClientRect();return b.bottom<=w.bottom+2}''')
        # All 6 slots must fit without overlapping when the party fills up.
        all_slots=page.evaluate('''(src)=>{const mon=game.team[0];game.team=Array.from({length:6},(_,i)=>{
          const p=Object.assign(Object.create(Object.getPrototypeOf(mon)),mon);p.name='MON-'+(i+1);p.spriteFront=src;return p;});
          game.activeMon=game.team[0];game.getTeamSlotLimit=()=>6;game.renderSidebar();
          const boxes=[...document.querySelectorAll('#team-grid .team-slot')].map(e=>e.getBoundingClientRect());
          return {count:boxes.length,ordered:boxes.every((r,i)=>i===0||boxes[i-1].bottom<=r.top+.2),positive:boxes.every(r=>r.height>=40)};
        }''',icon)
        assert all_slots['count']==6 and all_slots['ordered'] and all_slots['positive'],(width,all_slots)
        if width==390:
            page.locator('#language-en').evaluate('(e)=>e.click()')
            english=page.locator('#team-grid .team-slot').first.get_attribute('aria-label')
            assert 'active Pokémon' in english and page.locator('#team-grid .team-slot').first.get_attribute('data-status') is None
            page.locator('#language-it').evaluate('(e)=>e.click()')
        assert not errors,(width,errors)
        findings.append({'viewport':f'{width}x{height}','radar_px':round(current['radarHeight'],1),'screen_scroll_delta':current['screenOverflow'],'six_slots_ok':True,'badge_reachable':True})
        page.close()
    browser.close()
print(json.dumps({'result':'PASS','checks':findings},ensure_ascii=False,indent=2))
