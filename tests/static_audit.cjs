'use strict';
const fs=require('node:fs'),path=require('node:path'),test=require('node:test'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
test('T06: no dynamic eval and all JS sources pass node --check',()=>{
 const {execFileSync}=require('node:child_process');
 for(const f of fs.readdirSync(path.join(root,'js')).filter(f=>f.endsWith('.js'))){
   execFileSync(process.execPath,['--check',path.join(root,'js',f)]);
 }
 for(const f of ['js/prototypes/checkpoint.js','js/prototypes/cloud-sync.js']){
   execFileSync(process.execPath,['--check',path.join(root,f)]);
   const code=fs.readFileSync(path.join(root,f),'utf8');
   assert.doesNotMatch(code,/\beval\s*\(|\bnew Function\s*\(/);
 }
});
test('T04: unique HTML ids and required UI controls remain in markup',()=>{
 const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
 const ids=[...html.matchAll(/\bid="([A-Za-z0-9-]+)"/g)].map(m=>m[1]);
 assert.equal(ids.length,new Set(ids).size,'HTML must have unique ids');
 for(const id of ['quick-settings-panel','developer-panel','overlay-battle','bag-list','team-grid','starter-scene-overlay','floor-jump-overlay']) assert.ok(ids.includes(id),id);
});
test('T02/T03/T04: extracted modules load after engine but before game bootstrap',()=>{
 const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
 const scripts=[...html.matchAll(/<script src="(js\/[^\"]+)"/g)].map(m=>m[1]);
 for(const file of ['battle-helpers.js','map-helpers.js','ui-helpers.js']){
   assert.ok(scripts.indexOf('js/engine.js')<scripts.indexOf('js/'+file));
   assert.ok(scripts.indexOf('js/'+file)<scripts.indexOf('js/main.js'));
 }
});
test('G05: female walk and fishing sprites are complete for all 4 directions',()=>{
 for(const kind of ['walk','fish'])for(const dir of ['up','down','left','right']){
   for(let frame=0;frame<(kind==='fish'?4:3);frame++){
     const name=`assets/girl/${kind}/${dir}-${frame}.png`;
     const buffer=fs.readFileSync(path.join(root,name));
     assert.ok(buffer.subarray(0,8).equals(Buffer.from('89504e470d0a1a0a','hex')),name);
   }
 }
 assert.ok(fs.existsSync(path.join(root,'assets/girl/throw/full.png')));
});
