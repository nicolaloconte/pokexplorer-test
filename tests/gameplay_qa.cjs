'use strict';
// Focused regression checks, all offline. Not a claim of end-to-end completion.
const test=require('node:test');const assert=require('node:assert/strict');
const path=require('node:path'),fs=require('node:fs'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
function boot(){
  const cx=vm.createContext({console:{warn(){},error(){},log(){}},setTimeout,clearTimeout,AbortController,fetch:async()=>{throw Error('offline')}});
  for(const f of ['api-client.js','game-data.js','pokemon.js','engine.js','battle-helpers.js','map-helpers.js','ui-helpers.js','game-services.js'])vm.runInContext(fs.readFileSync(path.join(root,'js',f),'utf8'),cx,{filename:f});
  const run=text=>vm.runInContext(text,cx);const engine=run(`(()=>{const g=Object.create(GameEngine.prototype);
    g.floor=1;g.money=1000;g.devMode=false;g.badges=[];g.team=[];g.activeMon=null;g.items={pokeball:5,masterball:0,potion:2,superPotion:0,hyperPotion:0,elixir:0,fishingRod:false};g.completedGymFloors=new Set();
    g.logMsg=()=>{};g.showDiscoveryNotice=()=>{};g.renderSidebar=()=>{};g.renderDungeon=()=>{};g.setBattleMsg=()=>{};g.isBattleVisible=()=>false;g.$id=()=>({classList:{add(){},remove(){}}});return g;})()`);
  return {run,engine};
}
test('M01: starter lines absent from both ordinary wild and fishing',()=>{
 const {run,engine:g}=boot();const values=run(`(()=>{const results=[];for(let floor=1;floor<=80;floor++)for(let n=0;n<70;n++)results.push(randomKantoSpecies(Math.max(2,floor),floor));return results})()`);
 assert.equal(values.length,5600);assert.ok(values.every(id=>![1,2,3,4,5,6,7,8,9].includes(id)));
 for(const floor of [1,15,16,50,80]){g.floor=floor;assert.ok(g.getEncounterPool('fishing').every(id=>id>9));}
});
test('M02: starter floors remain low-level and wild levels scale with floors',()=>{
 const {engine:g}=boot();const at=[];
 for(const floor of [1,5,6,10,20,40,60,80]){g.floor=floor;at.push(g.encounterLevel('wild',false,()=>0));}
 assert.ok(at[0]<=3 && at[1]<=3,JSON.stringify(at));
 for(let i=2;i<at.length;i++) assert.ok(at[i]>=at[i-1],JSON.stringify(at));
 assert.ok(at.at(-1)<=70,JSON.stringify(at));
});
test('M03: Exp Share claim gate and enabled toggle',()=>{
 const {engine:g}=boot();g.expShareClaimed=false;g.expShareEnabled=true;
 assert.equal(g.toggleExpShare(),false);assert.equal(g.expShareEnabled,true);
 g.expShareClaimed=true;assert.equal(g.toggleExpShare(),true);assert.equal(g.expShareEnabled,false);
 assert.equal(g.toggleExpShare(),true);assert.equal(g.expShareEnabled,true);
});
test('M04: lead is first conscious party member and persists if party unchanged',()=>{
 const {engine:g}=boot();const a={currentHp:4},b={currentHp:6};g.team=[a,b];
 assert.equal(g.ensureActivePokemon(),a);assert.equal(g.ensureActivePokemon(),a);
 a.currentHp=0;assert.equal(g.ensureActivePokemon(),b);
});
test('M05: EXP cannot cross a temporary level cap or accumulate at cap',async()=>{
 const {run}=boot();const pokemon=run(`(()=>{const p=Object.create(Pokemon.prototype);p.level=13;p.exp=0;p.expToNext=5;p.currentHp=8;p.maxHp=10;p.learnset=[];
 p.requiredExp=()=>5;p.calcStats=()=>{};p.tryEvolution=async()=>null;return p})()`);
 let events=await pokemon.gainExperience(500,14);assert.equal(pokemon.level,14);assert.equal(pokemon.exp,0);assert.equal(events.length,1);
 events=await pokemon.gainExperience(500,14);assert.equal(pokemon.level,14);assert.equal(events.length,0);
});
test('M06: offline Protect has priority and PP; Magnitude remains damaging',async()=>{
 const {run}=boot();const protect=await run('createMove("protect")');const magnitude=await run('createMove("magnitude")');
 assert.equal(protect.priority,3);assert.ok(protect.maxPp>0);assert.equal(magnitude.type,'ground');assert.ok(magnitude.power>0);
});
test('M07: PokéMart purchase never removes money if unavailable or bag full',()=>{
 const {engine:g}=boot();g.money=100;assert.equal(g.purchaseItem('pokeball',200),false);assert.equal(g.money,100);
 g.money=1000;g.items.pokeball=20;assert.equal(g.purchaseItem('pokeball',200),false);assert.equal(g.money,1000);
 g.items.pokeball=19;assert.equal(g.purchaseItem('pokeball',200),true);assert.equal(g.money,800);
 assert.equal(g.purchaseItem('hyperPotion',1000),false);
});
test('M08: gift limit refuses duplicate fishing rods and inventory overflow',()=>{
 const {engine:g}=boot();assert.equal(g.grantItem('fishingRod'),true);
 assert.equal(g.grantItem('fishingRod'),false);assert.equal(g.items.fishingRod,true);
 g.items.potion=10;assert.equal(g.grantItem('potion'),false);assert.equal(g.items.potion,10);
});
test('M09: fishing table is distinct from gyms and never includes starter lineage',()=>{
 const {engine:g}=boot();g.floor=20;const fish=g.getEncounterPool('fishing');
 assert.ok(fish.length>2);assert.ok(fish.every(id=>id>9));
 assert.ok(!fish.includes(4)&&!fish.includes(7));
});
test('M10: gym confirmation cancellation restores control without consuming challenge',()=>{
 const {engine:g}=boot();g.gymChallengePending=false;g.isLocked=true;
 assert.equal(g.cancelGymChallenge(),false);
 g.gymChallengePending=true;assert.equal(g.cancelGymChallenge(),true);
 assert.equal(g.isLocked,false);assert.equal(g.gymChallengePending,false);
});
test('M11: confirmation explicitly warns about the last regular Poké Ball',()=>{
 const {engine:g}=boot();g.items.pokeball=1;g.isBattleVisible=()=>true;g.battleType='wild';g.isRaidActive=false;
 g.battleBusy=false;g.pendingItemTarget=null;g.dialogueResolve=null;g.hasForcedBattleAction=()=>false;
 let message;g.askBattleConfirmation=m=>{message=m};g.chooseBattleItem('pokeball');
 assert.match(message,/ultima Poké Ball/);
 g.items.pokeball=2;g.chooseBattleItem('pokeball');assert.doesNotMatch(message,/ultima Poké Ball/);
});
test('M13/M14: Kanto completion blocked until all 8 gym milestones and final floor',()=>{
 const {engine:g}=boot();g.floor=80;g.badges=Array.from({length:8},(_,id)=>({id}));
 for(let n=1;n<=8;n++)g.completedGymFloors.add(n*10);
 assert.equal(g.hasCompletedKantoChallenge(),true);
 g.completedGymFloors.delete(30);assert.equal(g.hasCompletedKantoChallenge(),false);
 g.completedGymFloors.add(30);g.floor=79;assert.equal(g.hasCompletedKantoChallenge(),false);
});
