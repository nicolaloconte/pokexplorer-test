const test=require('node:test'),assert=require('node:assert/strict');
const api=require('../js/checkpoints.js');
function storage(){const m=new Map();return {getItem:k=>m.get(k)||null,setItem:(k,v)=>m.set(k,v),removeItem:k=>m.delete(k)};}
function dummy(){
 const mon={id:4,name:'CHARMANDER',level:5,maxHp:19,currentHp:19,moves:[{id:'scratch',name:'Graffio',type:'normal',power:40,maxPp:35,currentPp:35}],ivs:{hp:1},evs:{hp:0}};
 return {floor:1,money:600,team:[mon],activeMon:mon,items:{pokeball:5,potion:3,fishingRod:false},playerPos:{x:0,y:0},playerGender:'male',playerFacing:'down',badges:[],radarCharges:3,expShareEnabled:false,expShareClaimed:false,fishingRodGiftClaimed:false,adventureCompleted:false,oakEventDismissed:false,celestialPhase:'unvisited',caughtLegendarySpecies:new Set(),completedGymFloors:new Set(),gridMap:Array.from({length:10},(_,y)=>Array.from({length:10},(_,x)=>({x,y,type:'path',entity:x===9&&y===9?'door':null}))),isLocked:false,battleBusy:false,isRaidActive:false,isCelestialCave:false};
}
test('checkpoint: save/restore typed progression with full map',()=>{
 api.setUser(null);const s=storage(),g=dummy(),snapshot=api.take(g);
 assert.ok(snapshot);api.save(snapshot,s);assert.equal(api.load(s).game.team[0].id,4);
 assert.equal(api.progress(api.load(s)).floor,1);
});
test('checkpoint: corrupted latest recovers previous valid state',()=>{
 api.setUser(null);const s=storage(),g=dummy();api.save(api.take(g),s);
 g.floor=5;api.save(api.take(g),s);
 s.setItem(api.KEY+':local','{"bad":true}');
 assert.equal(api.load(s).game.floor,1);
});
test('checkpoint: prevents snapshots mid encounter',()=>{
 const g=dummy();g.isRaidActive=true;assert.equal(api.take(g),null);
 g.isRaidActive=false;g.isLocked=true;assert.equal(api.take(g),null);
});
test('checkpoint: account isolation',()=>{
 const s=storage(),g=dummy(),a='12345678-1234-1234-1234-123456789012',b='12345678-1234-1234-1234-123456789013';
 api.setUser(a);api.save(api.take(g),s);
 api.setUser(b);assert.equal(api.load(s),null);
 api.setUser(a);assert.equal(api.load(s).game.floor,1);api.setUser(null);
});
test('checkpoint: reject invalid map and party',()=>{
 const g=dummy(),c=api.take(g);c.game.gridMap=[];assert.throws(()=>api.validate(c));
 const d=api.take(g);d.game.team[0].currentHp=999;assert.throws(()=>api.validate(d));
});
