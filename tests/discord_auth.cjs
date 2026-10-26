const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const source=fs.readFileSync(path.join(root,'js/auth-cloud.js'),'utf8');
const bootSource=fs.readFileSync(path.join(root,'js/main.js'),'utf8');
const user={id:'123e4567-e89b-12d3-a456-426614174000',user_metadata:{full_name:'Trainer Example',avatar_url:'https://cdn.discordapp.com/avatars/123/test.png'}};
function stubAuth({loggedIn=true,error=null}={}){
 const calls=[];
 const api={
  auth:{
    getUser:async()=>({data:{user:loggedIn?user:null},error}),
    signInWithOAuth:async opts=>(calls.push(opts),{error:null}),
    signOut:async()=>{calls.push('logout');return {error:null};}
  },
  from:()=>({})
 };
 return {api,calls};
}
function makeOAuth(config={supabaseUrl:'https://example-id.supabase.co',publishableKey:'sb_publishable_testing_1234567890'},options={}){
 const stub=stubAuth(options);
 const window={POKEX_PUBLIC_CONFIG:config,location:{protocol:'https:',hostname:'test.example.org',origin:'https://test.example.org',pathname:'/Pokexplorer/index.html'},supabase:{createClient:()=>stub.api},URL,document:{createElement:()=>({}),head:{appendChild:()=>{}}}};
 vm.runInNewContext(source,{window,URL,console});
 return {auth:window.PokexAuth,stub,window};
}
function fakeElement(){return {disabled:false,classList:{classes:new Set(['hidden']),remove(name){this.classes.delete(name);},add(name){this.classes.add(name);},contains(name){return this.classes.has(name);}},dataset:{},textContent:'',src:'',onclick:null};}
async function runMain({configured=true,loggedIn=true,error=null}={}){
 const elements=new Map();
 const get=(id)=>{if(!elements.has(id))elements.set(id,fakeElement());return elements.get(id);};
 let booted=0;
 const oauth=makeOAuth();
 oauth.stub.api.auth.getUser=async()=>({data:{user:loggedIn?user:null},error});
 oauth.stub.api.from=()=>({select:()=>({eq:()=>({maybeSingle:async()=>({data:null,error:null})})})});
 const events={};
 const window={PokexAuth:configured?oauth.auth:{enabled:()=>false},PokexCheckpoints:{setUser(id){this.owner=id;},load:()=>null},addEventListener:(ev,fn)=>{events[ev]=fn;},location:{reload:()=>{}}};
 function GameEngine(){booted++;this.updateContinueButton=()=>{};}
 const document={getElementById:get};
 vm.runInNewContext(bootSource,{window,document,GameEngine,console,clearTimeout,setTimeout});
 await events.DOMContentLoaded();
 return {booted,elements,window,get};
}
test('unconfigured preview remains playable without a fake Discord session',async()=>{
 const {auth}=makeOAuth({});assert.equal(auth.enabled(),false);
 const run=await runMain({configured:false});assert.equal(run.booted,1);
});
test('configured login uses verified user and no bot credentials',async()=>{
 const {auth,stub}=makeOAuth();
 assert.equal(auth.enabled(),true);
 const session=await auth.setup();assert.equal(session.user.id,user.id);
 await auth.signIn();
 assert.equal(stub.calls[0].provider,'discord');
 assert.equal(stub.calls[0].options.redirectTo,'https://test.example.org/Pokexplorer/index.html');
 assert.equal(stub.calls[0].options.scopes,'identify');
 assert.equal(JSON.stringify(stub.calls).includes('secret'),false);
});
test('rejects file:// redirects and does not start OAuth there',()=>{
 const {auth,window}=makeOAuth();
 window.location={protocol:'file:',hostname:'',origin:'null',pathname:'/x'};
 assert.throws(()=>auth.redirectUrl(),/HTTPS or localhost/);
});
test('OAuth redirects are valid on localhost during testing',()=>{
 const {auth,window}=makeOAuth();
 window.location={protocol:'http:',hostname:'localhost',origin:'http://localhost:8000',pathname:'/index.html'};
 assert.equal(auth.redirectUrl(),'http://localhost:8000/index.html');
});
test('Discord profile uses a safe avatar origin or a local fallback',()=>{
 const {auth}=makeOAuth();
 assert.equal(auth.profile(user).name,'Trainer Example');
 assert.equal(auth.profile(user).avatar,'https://cdn.discordapp.com/avatars/123/test.png');
 assert.equal(auth.profile({user_metadata:{avatar_url:'https://evil.example/avatar.png'}}).avatar,null);
});
test('logout is delegated to Supabase auth',async()=>{
 const {auth,stub}=makeOAuth();await auth.setup();await auth.signOut();
 assert.equal(stub.calls.at(-1),'logout');
});
test('authenticated bootstrap starts game only after verified user',async()=>{
 const run=await runMain();
 assert.equal(run.booted,1);
 assert.equal(run.window.PokexCheckpoints.owner,user.id);
 assert.equal(run.get('login-gate').classList.contains('hidden'),true);
 assert.equal(run.get('logout-discord-btn').classList.contains('hidden'),false);
});
test('unauthenticated visitor sees login gate and game is not constructed',async()=>{
 const run=await runMain({loggedIn:false});
 assert.equal(run.booted,0);
 assert.equal(run.get('login-gate').classList.contains('hidden'),false);
 assert.equal(run.get('login-discord-btn').disabled,false);
});
test('Supabase outage keeps game gated and offers retry',async()=>{
 const run=await runMain({error:new Error('network unreachable')});
 assert.equal(run.booted,0);
 assert.match(run.get('login-discord-btn').textContent,/RIPROVA/);
});
