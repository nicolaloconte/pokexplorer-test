/* Configurable Discord OAuth/Supabase adapter. Nothing contacts remote systems
   unless PUBLIC url & publishable key are configured in config.js, and the
   user explicitly signs in. No service_role/client secret ever in browser. */
(function(root){
 'use strict';
 const settings=root.POKEX_PUBLIC_CONFIG||{};
 function enabled(){return /^https:\/\/[^/]+\.supabase\.co$/.test(settings.supabaseUrl||'') && typeof settings.publishableKey==='string' && settings.publishableKey.length>15;}
 let client=null;
 async function setup(){
   if(!enabled())return {configured:false,client:null};
   if(!root.supabase?.createClient){
     await new Promise((resolve,reject)=>{
       const js=document.createElement('script');
       js.src='https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.57.0';
       js.async=true;js.onload=resolve;js.onerror=()=>reject(Error('Supabase SDK unavailable'));
       document.head.appendChild(js);
     });
   }
   if(!root.supabase?.createClient)throw Error('Supabase SDK missing');
   client=root.supabase.createClient(settings.supabaseUrl,settings.publishableKey,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});
   const {data,error}=await client.auth.getUser();if(error && !/Auth session missing/i.test(error.message||''))console.warn('Discord session:',error.message);
   return {configured:true,client,user:data?.user||null};
 }
 async function signIn(){if(!client)throw Error('OAuth not configured');
   const {error}=await client.auth.signInWithOAuth({provider:'discord',options:{redirectTo:location.origin+location.pathname,scopes:'identify'}});
   if(error)throw error;
 }
 async function user(){if(!client)return null;const {data,error}=await client.auth.getUser();if(error)return null;return data.user||null;}
 async function loadCloud(){
   const u=await user();if(!u)return null;
   const {data,error}=await client.from('pokexplorer_saves').select('revision,run,updated_at').eq('user_id',u.id).maybeSingle();if(error)throw error;return data;
 }
 async function saveCloud(snapshot,expectedRevision){
   const u=await user();if(!u)throw Error('Not authenticated');
   const safe=root.PokexCheckpoints.validate(snapshot);
   if(expectedRevision===null){const {data,error}=await client.from('pokexplorer_saves').insert({user_id:u.id,revision:1,run:safe}).select('revision').single();if(error)throw error;return data.revision;}
   const {data,error}=await client.from('pokexplorer_saves').update({run:safe,revision:expectedRevision+1,updated_at:new Date().toISOString()}).eq('user_id',u.id).eq('revision',expectedRevision).select('revision').maybeSingle();
   if(error)throw error;if(!data)throw Error('Cloud conflict: newer progress exists; no overwrite performed');return data.revision;
 }
 root.PokexAuth=Object.freeze({enabled,setup,signIn,user,loadCloud,saveCloud,get client(){return client;}});
})(typeof window!=='undefined'?window:globalThis);
