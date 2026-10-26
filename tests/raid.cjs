'use strict';
// R05/R09/R10/R11/R12: event and recovery regression tests, no external network.
const test=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
function boot(){
  const context=vm.createContext({console:{error(){},log(){},warn(){}},setTimeout,clearTimeout,AbortController,
    window:{pokexplorerMusic:{setScene(){}}}});
  for(const file of ['api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js'])
    vm.runInContext(fs.readFileSync(path.join(root,'js',file),'utf8'),context,{filename:file});
  const run=code=>vm.runInContext(code,context);
  const game=run(`(()=>{const g=Object.create(GameEngine.prototype);
    g.floor=6;g.items={pokeball:0,potion:0,superPotion:0,hyperPotion:0,elixir:0,fishingRod:false};
    g.team=[];g.badges=[];g.completedGymFloors=new Set();g.gridMap=[];g.isRaidActive=false;
    g.raidQueueCount=0;g.raidTriggeredOnFloor=false;g.raidPickupSourceCell=null;
    g.raidBattleRetryPending=false;g.raidLaunchNonce=0;g.raidVictoryResolutionToken=-1;
    g.battleToken=1;g.renderDungeon=()=>{};g.renderSidebar=()=>{};g.logMsg=()=>{};
    g.showDiscoveryNotice=()=>{};g.closePartyActions=()=>{};g.closePokemonInfo=()=>{};
    g.hideAllActions=()=>{};g.openWings=()=>{};
    g.dom=new Map();g.$id=(id)=>{if(!g.dom.has(id))g.dom.set(id,{classList:{add(){},remove(){},contains(){return false}},style:{},textContent:'',setAttribute(){}});return g.dom.get(id)};
    return g;})()`);
  return {game,run};
}
test('R2.23: independent 10% roll on every eligible collectible',()=>{
  const {game:g,run}=boot();
  run('Math.random=()=>0.05');
  g.waitForNotice=()=>new Promise(()=>{});
  const a={entity:'item',itemKind:'pokeball'};
  assert.equal(g.collectFloorItem(a),true);
  assert.equal(g.isRaidActive,true);assert.equal(g.raidQueueCount,5);
  assert.equal(g.raidTriggeredOnFloor,true);assert.equal(a.entity,null);
  // Finish the encounter without starting a second dungeon.
  g.isRaidActive=false;g.raidQueueCount=0;g.clearRaidTransientState();
  const b={entity:'item',itemKind:'pokeball'};
  assert.equal(g.collectFloorItem(b),true);
  assert.equal(b.entity,null);assert.equal(g.isRaidActive,true);
  assert.equal(g.raidQueueCount,5);
  assert.equal(g.items.pokeball,0);
  // The next item independently rolls 90% and remains ordinary loot.
  g.isRaidActive=false;g.raidQueueCount=0;g.clearRaidTransientState();
  run('Math.random=()=>0.9');
  const c={entity:'item',itemKind:'pokeball'};
  assert.equal(g.collectFloorItem(c),true);assert.equal(g.isRaidActive,false);
  assert.equal(g.items.pokeball,1);
});
test('R05: collecting without a Raid preserves the 90% normal-loot result',()=>{
  const {game:g,run}=boot();run('Math.random=()=>0.9');
  const a={entity:'item',itemKind:'pokeball'};
  assert.equal(g.collectFloorItem(a),true);assert.equal(g.items.pokeball,1);
  assert.equal(g.raidTriggeredOnFloor,false);
  assert.equal(g.isRaidActive,false);
});
test('R09: repeat Raid activation is rejected and launch callback runs once',async()=>{
  const {game:g}=boot();let finish,start=0;
  g.waitForNotice=()=>new Promise(resolve=>{finish=resolve;});
  g.startBattle=()=>{start++};
  assert.equal(g.beginHiddenRaid(),true);
  assert.equal(g.beginHiddenRaid(),false);
  finish();await Promise.resolve();
  assert.equal(start,1);
  g.isRaidActive=false;g.raidQueueCount=0;g.clearRaidTransientState();
  assert.equal(g.beginHiddenRaid(),true); // A new Raid is allowed after the previous one ended.
});
test('R09: stale launch callback cannot start after leaving dungeon',async()=>{
  const {game:g}=boot();let finish,start=0;
  g.waitForNotice=()=>new Promise(resolve=>{finish=resolve;});g.startBattle=()=>{start++};
  assert.equal(g.beginHiddenRaid(),true);
  g.isRaidActive=false;g.clearRaidTransientState();
  finish();await Promise.resolve();
  assert.equal(start,0);
});
test('R11: first opponent network error restores original item, not player tile',async()=>{
  const {game:g}=boot();g.gridMap=[[{entity:'door'},{entity:'empty'}]];
  g.playerPos={x:0,y:0};const pickup={entity:null,itemKind:'elixir'};
  g.raidPickupSourceCell=pickup;g.raidTriggeredOnFloor=true;
  g.isRaidActive=true;g.raidQueueCount=5;
  g.team=[{currentHp:10}];g.activeMon=g.team[0];g.ensureActivePokemon=()=>g.activeMon;
  g.getPokemonData=async()=>{throw Error('PokéAPI offline')};
  g.encounterLevel=()=>7;g.endBattle=()=>{};
  await g.startBattle('wild');
  assert.equal(g.gridMap[0][0].entity,'door');
  assert.equal(pickup.entity,'item');assert.equal(pickup.itemKind,'elixir');
  assert.equal(pickup.raidRetryPending,true);
  assert.equal(g.raidTriggeredOnFloor,false);assert.equal(g.isRaidActive,false);
});
test('R11: after a victory, failed API load retains the remaining opponent count',async()=>{
  const {game:g}=boot();g.isRaidActive=true;g.raidTriggeredOnFloor=true;
  g.raidQueueCount=3;g.team=[{currentHp:10}];g.activeMon=g.team[0];g.ensureActivePokemon=()=>g.activeMon;
  g.getPokemonData=async()=>{throw Error('PokéAPI offline')};g.encounterLevel=()=>7;
  g.endBattle=()=>{};
  await g.startBattle('wild',true);
  assert.equal(g.isRaidActive,true);assert.equal(g.raidTriggeredOnFloor,true);
  assert.equal(g.raidQueueCount,3);assert.equal(g.raidBattleRetryPending,true);
  let retryCount=0;g.startBattle=()=>{retryCount++};
  assert.equal(g.retryRaidBattle(),true);assert.equal(g.retryRaidBattle(),false);
  assert.equal(retryCount,1);
});
test('R11: retrying original item does not reroll the 10% chance',()=>{
  const {game:g,run}=boot();run('Math.random=()=>0.99');
  let started=0;g.beginHiddenRaid=()=>{g.isRaidActive=true;started++;return true;};
  const cell={entity:'item',itemKind:'pokeball',raidRetryPending:true};
  assert.equal(g.collectFloorItem(cell),true);assert.equal(started,1);
  assert.equal(g.raidTriggeredOnFloor,true);assert.equal(cell.entity,null);
});
test('R10: asynchronous duplicate victories cannot consume Raid slots twice',async()=>{
  const {game:g}=boot();g.isRaidActive=true;g.raidTriggeredOnFloor=true;g.raidQueueCount=5;
  g.battleToken=10;g.battleType='wild';g.battleParticipants=new Set();g.enemyMon={name:'TEST'};
  g.hasExpShare=()=>false;g.battleText=async()=>{};
  let next=0,ended=0;g.startBattle=async()=>{g.battleToken++;next++};
  g.endBattle=()=>{g.battleToken++;ended++};
  for(let i=0;i<5;i++){
    await Promise.all([g.handleBattleVictory(),g.handleBattleVictory()]);
    assert.equal(g.raidQueueCount,4-i);
  }
  assert.equal(next,4);assert.equal(ended,1);assert.equal(g.isRaidActive,false);
  assert.equal(g.raidTriggeredOnFloor,true);
});
test('R12: team wipe ends Raid with gameover and leaves dungeon consumed',async()=>{
  const {game:g}=boot();const p={currentHp:0,name:'Testmon'};
  g.isRaidActive=true;g.raidTriggeredOnFloor=true;g.raidQueueCount=3;
  g.activeMon=p;g.team=[p];g.battleParticipants=new Set([p]);
  g.updateBattleHUD=()=>{};g.battleText=async()=>{};g.endBattle=()=>{};
  await g.onPlayerFainted();
  assert.equal(g.isRaidActive,false);assert.equal(g.raidQueueCount,0);
  assert.equal(g.raidTriggeredOnFloor,true);assert.equal(g.activeMon,null);
  assert.equal(g.team.length,0);
});
