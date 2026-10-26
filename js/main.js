window.addEventListener('DOMContentLoaded', async () => {
  window.game = new GameEngine();
  const gate=document.getElementById('login-gate');
  const message=document.getElementById('login-gate-status');
  const login=document.getElementById('login-discord-btn');
  const auth=window.PokexAuth;
  if(!auth?.enabled()){
    // Local preview works offline; Discord-only access requires real settings.
    const label=document.getElementById('trainer-discord-name');
    if(label){label.textContent='ALLENATORE LOCALE';label.dataset.i18nIt='ALLENATORE LOCALE';label.dataset.i18nEn='LOCAL TRAINER';}
    return;
  }
  gate.classList.remove('hidden');
  login.disabled=true;
  message.textContent='Verifica della sessione Discord…';
  try{
    const {user}=await auth.setup();
    const attach=(u)=>{
      if(!u)return false;
      const metadata=u.user_metadata||{};
      const name=document.getElementById('trainer-discord-name');
      if(name)name.textContent=String(metadata.full_name||metadata.name||metadata.user_name||'TRAINER').slice(0,28);
      const avatar=document.getElementById('trainer-discord-avatar');
      const uri=metadata.avatar_url;
      if(avatar && typeof uri==='string' && /^https:\/\//.test(uri)){
        avatar.onerror=()=>{avatar.onerror=null;avatar.src='assets/ui/trainer-avatar-fallback.svg';};avatar.src=uri;
      }
      window.PokexCheckpoints?.setUser(u.id);
      window.game.updateContinueButton();
      gate.classList.add('hidden');return true;
    };
    if(attach(user)){
      let revision=null,cloudEnabled=true,busy=false,timer=null;
      const checkpoint=window.PokexCheckpoints;
      try{
        const remote=await auth.loadCloud(),local=checkpoint.load();
        if(remote?.run && !local){checkpoint.save(remote.run);revision=remote.revision;}
        else if(remote?.run && local){
          revision=remote.revision;
          const identical=JSON.stringify(remote.run)===JSON.stringify(local);
          if(!identical){
            const restoreRemote=window.confirm('È presente un salvataggio Discord diverso dal salvataggio locale. Caricare il salvataggio cloud? (Annulla = mantieni il locale)');
            if(restoreRemote)checkpoint.save(remote.run);
            else if(!window.confirm('Vuoi sostituire esplicitamente il salvataggio cloud con quello locale?'))cloudEnabled=false;
          }
        }
        window.game.updateContinueButton();
      }catch(error){console.warn('Cloud restore unavailable',error);cloudEnabled=false;}
      const sync=async()=>{
        if(!cloudEnabled||busy)return;
        const saved=checkpoint.load();if(!saved)return;
        busy=true;try{revision=await auth.saveCloud(saved,revision);}
        catch(err){cloudEnabled=false;console.warn('Cloud sync paused, no overwrite:',err);const status=document.getElementById('save-status');if(status)status.textContent='SYNC CLOUD SOSPESA: '+String(err.message||err).slice(0,64);}
        finally{busy=false;}
      };
      window.addEventListener('pokex:checkpoint',()=>{if(!cloudEnabled)return;clearTimeout(timer);timer=setTimeout(sync,1100);});
      if(cloudEnabled && checkpoint.load() && revision===null)await sync();
    } else {
      login.disabled=false;
      message.textContent='Accedi per giocare e sincronizzare i progressi.';
      login.onclick=async()=>{login.disabled=true;try{await auth.signIn();}catch(err){message.textContent='Login non riuscito: '+String(err.message||err).slice(0,120);login.disabled=false;}};
    }
  }catch(err){
    login.disabled=false;message.textContent='Configurazione OAuth non raggiungibile: '+String(err.message||err).slice(0,100);
    login.onclick=async()=>{try{await auth.signIn();}catch(error){message.textContent=String(error.message||error);}};
  }
});
