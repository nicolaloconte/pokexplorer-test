'use strict';
// No third-party packages: node --test tests/unit.cjs
const test=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
function boot(fetchImpl=()=>Promise.reject(Error('offline'))){
  const context=vm.createContext({fetch:fetchImpl,console:{log(){},warn(){},error(){}},setTimeout,clearTimeout,AbortController});
  for(const file of ['api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js']){
    vm.runInContext(fs.readFileSync(path.join(root,'js',file),'utf8'),context,{filename:file});
  }
  return {context,run:code=>vm.runInContext(code,context)};
}
function prepareEngine(run){
  return run(`(()=>{const g=Object.create(GameEngine.prototype);g.floor=6;g.items={pokeball:20,potion:10,superPotion:0,hyperPotion:0,elixir:10,fishingRod:false};g.badges=[];g.completedGymFloors=new Set();g.isRaidActive=false;g.raidQueueCount=0;g.logMsg=()=>{};g.showDiscoveryNotice=()=>{};g.renderSidebar=()=>{};g.renderDungeon=()=>{};g.beginHiddenRaid=()=>{g.raidCount=(g.raidCount||0)+1};g.pokemonCache=new Map();g.abilityInfoCache=new Map();g.moveDescriptionCache=new Map();g.abilityDescriptionCache=new Map();return g;})()`);
}
test('F06: starters and their evolution families never appear as random wild encounters',()=>{
  const {run}=boot();
  const result=run(`(()=>{let sampled=0;for(const floor of [1,5,6,24,25,35,60,79,80])for(let i=0;i<500;i++){const id=randomKantoSpecies(Math.max(2,Math.min(75,Math.floor(floor*.8))),floor);if([1,2,3,4,5,6,7,8,9].includes(id))return {floor,id};sampled++;}return {sampled};})()`);
  assert.equal(result.sampled,4500,JSON.stringify(result));
});
test('F03: full bag keeps collectible and cannot accidentally launch the existing raid',()=>{
  const {run}=boot();const g=prepareEngine(run);run('Math.random=()=>0.01');
  const cell={entity:'item',itemKind:'pokeball'};
  assert.equal(g.collectFloorItem(cell),false);assert.equal(cell.entity,'item');assert.equal(g.raidCount||0,0);assert.equal(g.items.pokeball,20);
  g.items.pokeball=19;
  assert.equal(g.collectFloorItem(cell),true);assert.equal(cell.entity,null);assert.equal(g.raidCount,1);
});
test('F03: collectible item has fixed identity when inventory is full',()=>{
  const {run}=boot();const g=prepareEngine(run);run('Math.random=()=>0.7');
  const cell={entity:'item',itemKind:'potion'};
  assert.equal(g.collectFloorItem(cell),false);assert.deepEqual(cell,{entity:'item',itemKind:'potion'});
  g.items.potion=9;
  assert.equal(g.collectFloorItem(cell),true);assert.equal(cell.entity,null);assert.equal(g.items.potion,10);
});
test('F05: all eight badge gates, caps, party sizes and the ending requirement',()=>{
  const {run}=boot();const g=prepareEngine(run);
  for(let n=0;n<=8;n++){
    g.badges=Array.from({length:n},(_,i)=>({id:i}));
    assert.equal(g.getLevelCap(),[14,21,24,29,35,43,47,50,100][n]);
    assert.equal(g.getTeamSlotLimit(),[2,3,3,4,4,5,5,6,6][n]);
  }
  g.floor=80;
  assert.equal(g.hasCompletedKantoChallenge(),false);
  for(let i=1;i<=8;i++)g.completedGymFloors.add(i*10);
  assert.equal(g.hasCompletedKantoChallenge(),true);
  g.completedGymFloors.delete(60);assert.equal(g.hasCompletedKantoChallenge(),false);
  g.floor=79;g.completedGymFloors.add(60);assert.equal(g.hasCompletedKantoChallenge(),false);
});
test('F04: transient PokéAPI failure retries once, then succeeds',async()=>{
  let calls=0;const {run}=boot(async()=>{calls++;if(calls===1)throw Error('intermittent');return {ok:true,status:200,json:async()=>({id:25})};});
  const result=await run('pokeApiRequest("pokemon/25")');assert.equal(result.id,25);assert.equal(calls,2);
});
test('F04: permanent PokéAPI 404 does not retry',async()=>{
  let calls=0;const {run}=boot(async()=>{calls++;return {ok:false,status:404}});
  await assert.rejects(run('pokeApiRequest("pokemon/999")'),/404/);assert.equal(calls,1);
});
test('F04: rejected species request is evicted; retry after connection returns',async()=>{
  let failed=true;
  const {run}=boot(async(url)=>{
    if(failed)throw Error('offline');
    if(url.includes('pokemon-species/'))return {ok:true,json:async()=>({growth_rate:{name:'medium'}})};
    return {ok:true,json:async()=>({id:1,species:{name:'bulbasaur'}})};
  });
  const g=prepareEngine(run);
  await assert.rejects(g.getPokemonData(1));assert.equal(g.pokemonCache.size,0);
  failed=false;
  const [a,b]=await Promise.all([g.getPokemonData(1),g.getPokemonData(1)]);
  assert.equal(a.id,1);assert.equal(b.id,1);assert.equal(g.pokemonCache.size,1);
});
test('F10: separated modules retain the current gym progression and engine API',()=>{
  const {run}=boot();assert.equal(run('typeof GameEngine.prototype.getPokemonData'),'function');
  assert.equal(run('typeof GameEngine.prototype.getPokedexDescription'),'function');
  assert.equal(run('typeof GameEngine.prototype.resolveAbilityName'),'function');
  assert.equal(run('KANTO_GYMS.length'),8);
  assert.equal(run('BADGE_LEVEL_CAPS.length'),9);
});
test('F08: all script dependencies load in the correct order and local fallback exists',()=>{
  const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
  const matches=[...html.matchAll(/<script src="(js\/[^"]+)"\s*><\/script>/g)].map(x=>x[1]);
  for(const f of matches)assert.ok(fs.existsSync(path.join(root,f)),f);
  const index=name=>matches.indexOf(`js/${name}`);
  assert.ok(index('api-client.js')<index('pokemon.js'));
  assert.ok(index('game-data.js')<index('engine.js'));
  assert.ok(index('engine.js')<index('game-services.js'));
  assert.ok(index('game-services.js')<index('main.js'));
  assert.ok(fs.existsSync(path.join(root,'assets/ui/pokemon-placeholder.svg')));
});
