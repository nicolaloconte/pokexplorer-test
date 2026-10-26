'use strict';
const test=require('node:test');const assert=require('node:assert/strict');
const {validate,create,save,load,KEY}=require('../js/prototypes/checkpoint');
const {createClient,ConflictError}=require('../js/prototypes/cloud-sync');
const fake={floor:12,money:250,badges:[{id:0}],team:[{id:1,level:13,currentHp:22,maxHp:30,moves:[{id:'tackle',currentPp:20}]}],activeMon:null,items:{pokeball:2,potion:3,fishingRod:false},completedGymFloors:new Set([10])};
const runId='run_20261025';
test('T12: checkpoint is valid, versioned, and contains no engine internals',()=>{
  const snapshot=create(fake,runId,'2026-10-25T00:00:00.000Z');
  assert.equal(snapshot.floor,12);assert.equal(snapshot.team[0].moves[0].pp,20);
  assert.equal(snapshot.version,1);assert.equal(snapshot.devMode,undefined);
});
test('T12: save/load and rejected corrupted snapshots',()=>{
  const entries=new Map();const store={setItem:(k,v)=>entries.set(k,v),getItem:k=>entries.get(k)||null,removeItem:k=>entries.delete(k)};
  const snapshot=create(fake,runId);save(snapshot,store);
  assert.deepEqual(load(store),snapshot);assert.equal(entries.has(KEY+':pending'),false);
  assert.throws(()=>validate({...snapshot,version:22}),/version/);
  assert.throws(()=>validate({...snapshot,team:[{id:1,level:1000}]}),/Pokémon/);
  entries.set(KEY,'{broken json');assert.throws(()=>load(store),/invalid/);
});
test('T13: cloud adapter sends authenticated revision-specific update and detects conflict',async()=>{
  const calls=[];
  const fetcher=async (url,opt)=>{calls.push({url,opt});return {ok:true,json:async()=>[]};};
  const api=createClient({url:'https://example.supabase.co',publishableKey:'public-test',accessToken:'token-test',userId:'11111111-2222-3333-4444-555555555555',fetcher});
  await assert.rejects(api.update({x:1},3),ConflictError);
  assert.match(calls[0].url,/revision=eq\.3/);
  assert.equal(JSON.parse(calls[0].opt.body).revision,4);
  assert.equal(calls[0].opt.headers.authorization,'Bearer token-test');
});
