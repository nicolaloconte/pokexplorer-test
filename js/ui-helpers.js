// Small, behavior-preserving engine helpers extracted from R2.21 RC2.1.
GameEngine.prototype.toggleQuickSettings = function() {
    const panel=this.$id('quick-settings-panel'),toggle=this.$id('quick-settings-toggle');
    if(!panel||!toggle)return;
    const opening=panel.classList.contains('hidden');
    panel.classList.toggle('hidden',!opening);
    toggle.setAttribute('aria-expanded',String(opening));
    toggle.setAttribute('aria-label',opening?'Chiudi opzioni':'Apri opzioni');
  };

GameEngine.prototype.closeQuickSettings = function() {
    this.$id('quick-settings-panel')?.classList.add('hidden');
    const toggle=this.$id('quick-settings-toggle');
    if(toggle){toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Apri opzioni');}
  };

GameEngine.prototype.setGameLanguage = function(locale) {
    this.locale=locale==='en'?'en':'it';
    document.documentElement.lang=this.locale;
    for(const language of ['it','en'])this.$id('language-'+language)?.setAttribute('aria-pressed',String(this.locale===language));
    document.querySelectorAll('[data-i18n-it][data-i18n-en]').forEach(node=>{
      node.textContent=node.getAttribute(`data-i18n-${this.locale}`);
    });
    if(this.team.length)this.renderSidebar();
    // Evolution overlay is rendered dynamically, so updating the language must
    // refresh its live caption without resetting the animation or Pokémon state.
    if(this.evolutionData && !this.$id('evolution-overlay')?.classList.contains('hidden')){
      const phase=this.$id('evolution-finish')?.classList.contains('hidden')?'start':'done';
      this.$id('evolution-caption').textContent=this.evolutionText(phase,this.evolutionData);
    }
    if(this.partyInfoPokemon)this.openPokemonInfo(this.partyInfoPokemon);
    this.translateVisibleUI();
    this.updateContinueButton?.();
    const speed=this.$id('speed-toggle');if(speed)speed.textContent=`${this.locale==='en'?'SPEED':'VELOCITÀ'} ×${this.speedMultiplier}`;
    return this.locale;
  };
