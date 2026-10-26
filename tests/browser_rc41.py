"""RC4.1: localization, location relocation and visible Pokémon info layout.
Offline smoke test; real PokéAPI integration is not simulated as verified."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, json, base64
ROOT=Path(__file__).resolve().parents[1]
html=ROOT.joinpath('index.html').read_text(encoding='utf8')
html=re.sub(r'<script\s+src="[^"]+"\s*></script>','',html)
html=re.sub(r'<link[^>]+(?:href="https?://|rel="stylesheet")[^>]*>','',html)
html=html.replace('</head>','<style>'+ROOT.joinpath('style.css').read_text(encoding='utf8')+'</style></head>')
files=['music.js','api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js','main.js']
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,args=['--no-sandbox'],**({'executable_path':'/usr/bin/chromium'} if Path('/usr/bin/chromium').exists() else {}))
    for w,h in [(360,780),(390,844),(768,900),(1440,900)]:
        page=browser.new_page(viewport={'width':w,'height':h},reduced_motion='reduce')
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.route('https://**/*',lambda r:r.abort())
        page.set_content(html,wait_until='domcontentloaded')
        for file in files:page.add_script_tag(content=(ROOT/'js'/file).read_text(encoding='utf8'))
        page.evaluate('window.dispatchEvent(new Event("DOMContentLoaded"))')
        page.evaluate('document.getElementById("pokex-extraction-warning").hidden=true')
        page.evaluate('''GameEngine.prototype.getPokemonData=async function(id){return {
            id:Number(id),name:'charmander',base_experience:65,types:[{type:{name:'fire'}}],
            sprites:{front_default:'',back_default:''},stats:[],
            abilities:[{ability:{name:'blaze'},is_hidden:false}],moves:[],species:{name:'charmander'}}}''')
        page.locator('#btn-start-game').click()
        page.locator('.pokeball-wrapper').first.click()
        page.locator('#btn-confirm-yes').click()
        assert page.evaluate('game.team.length')==1
        assert page.locator('#rotom-location-label').count()==0
        assert page.locator('#route-location-label').is_visible()
        for floor,expect in [(1,'Percorso 1'),(5,'Villaggio'),(10,'Plumbeopoli'),(20,'Celestopoli'),(80,'Smeraldopoli')]:
            page.evaluate('(f)=>{game.floor=f;game.renderSidebar()}',floor)
            assert expect in page.locator('#route-location-label').inner_text(),(floor,page.locator('#route-location-label').inner_text())
        page.evaluate("game.floor=1;game.renderSidebar();game.bagCategory='rimedi';game.renderSidebar()")
        placeholder=ROOT/'assets'/'ui'/'pokemon-placeholder.svg'
        sprite='data:image/svg+xml;base64,'+base64.b64encode(placeholder.read_bytes()).decode('ascii')
        page.evaluate("""(src)=>{ game.team[0].spriteFront=src;
          game.team[0].moves=[
            new Move('Graffio','normal',40,35,'physical',null,{id:'scratch'}),
            new Move('Ruggito','normal',0,40,'status',null,{id:'growl'}),
            new Move('Braciere','fire',40,25,'special',null,{id:'ember'}),
            new Move('Lacerazione','normal',70,20,'physical',null,{id:'slash'})
          ]; }
        """,sprite)
        page.evaluate('game.openPokemonInfo(game.team[0])')
        assert page.locator('.pokemon-info-sprite-stage').count()==1
        assert page.locator('.pokemon-info-stat').count()==6
        assert page.locator('.pokemon-stat-meter').count()==6
        assert page.locator('.pokemon-ability-details').count()==1
        assert page.locator('.pokemon-type-chip').count()>=1
        assert page.locator('.pokemon-move-tile').count()==4
        assert page.locator('#pokemon-info-level').inner_text().startswith('LIVELLO')
        # Ensure the restored location is in the right wing, not on Rotom's forehead.
        assert page.locator('.rotom-wing-right #route-location-panel').count()==1
        page.evaluate("game.setGameLanguage('en')")
        assert 'Trail: Route 1' in page.locator('#route-location-label').inner_text()
        assert page.locator('#pokemon-info-level').inner_text().startswith('LEVEL')
        assert 'SCRATCH' in page.locator('.pokemon-move-tile').first.inner_text()
        assert page.locator('#evolution-start').inner_text().startswith('START EVOLUTION')
        assert page.locator('#evolution-overlay h3').inner_text()=='EVOLUTION!'
        assert page.locator('#bag-list .bag-item').first.inner_text().find('Potion')!=-1
        assert page.evaluate("game.evolutionText('start',{from:'CHARMANDER',to:'CHARMELEON'})")=="CHARMANDER is evolving…"
        assert page.evaluate("game.evolutionText('done',{from:'CHARMANDER',to:'CHARMELEON'})")=="CHARMANDER evolved into CHARMELEON!"
        page.evaluate("game.beginItemTargetSelection('potion')")
        assert 'Which Pokémon' in page.locator('#item-target-message').inner_text()
        page.evaluate("game.cancelItemTargetSelection()")
        page.evaluate("game.setGameLanguage('it')")
        assert page.locator('#bag-list .bag-item').first.inner_text().find('Pozione')!=-1
        assert page.evaluate("game.evolutionText('done',{from:'CHARMANDER',to:'CHARMELEON'})").find('si è evoluto')!=-1
        assert page.evaluate('document.documentElement.scrollWidth-innerWidth')<=2
        if w in (390,1440):
            path=ROOT/'docs'/'visual'/f'rc41-{w}-info.png'
            path.parent.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(path),animations='disabled')
        assert errors==[],(w,errors)
        results.append({'viewport':f'{w}x{h}','pokemon_card':True,'right_route':True,'en_evolution':True,'en_items':True})
        page.close()
    browser.close()
print(json.dumps({'rc41_browser':'PASS','results':results},indent=2,ensure_ascii=False))
