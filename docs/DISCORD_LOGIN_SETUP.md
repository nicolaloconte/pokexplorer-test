# Pokéxplorer — Login Discord: configurazione e test

**Build preparata:** V7.7 R2.24 RC5.1 (locale).  
**Stato del progetto Supabase rilevato il 26 ottobre 2026:** `Pokexplorer` (`tynhqehheteynviyqkaf`), `INACTIVE`. Non è stata effettuata alcuna modifica remota.

## 1. Due ambienti separati

- **Release**: conserva la RC5 già consegnata e il branch `main` come riferimento stabile. Il nuovo login NON è verificato end-to-end.
- **Test**: usa `develop` e questa RC5.1, inizialmente senza config OAuth per verificare che non rompa il gameplay. Testa poi OAuth su HTTPS o `http://localhost:8000/`.
- Una repository GitHub Pages pubblica normalmente **un solo sito corrente**: i branch `main` e `develop` non creano automaticamente due URL pubblicati. Per mantenere **due siti online distinti** configura un secondo repository Pages (ad esempio `pokexplorer-test`) oppure una piattaforma che supporti preview deployments. Per dati realmente separati, usa anche due progetti Supabase o un'architettura di isolamento equivalente.
- Non modificare le branch remote attraverso questo pacchetto. L'utente esegue i commit/push manualmente.

## 2. Applicazione Discord esistente e bot

1. Apri https://discord.com/developers/applications e seleziona l'applicazione del bot esistente. Il bot può condividere l'applicazione con OAuth; **non occorre invitare il bot nei server per il login**.
2. In **OAuth2** copia il **Client ID**. Il **Client Secret** resta esclusivamente nel pannello Supabase: non inserirlo nel repository, nel gioco né in chat. Non usare mai il **Bot Token** per autenticare giocatori.
3. Nelle redirect URL dell'applicazione Discord aggiungi **esattamente** la callback Supabase:
   `https://tynhqehheteynviyqkaf.supabase.co/auth/v1/callback`
4. Salva le modifiche sul Discord Developer Portal.

## 3. Supabase: azioni remote da autorizzare separatamente

1. Il progetto è **INACTIVE**: riattivalo dal [dashboard](https://supabase.com/dashboard/project/tynhqehheteynviyqkaf) prima di tentare login o accessi al database. Questa procedura non è stata eseguita qui.
2. Vai in **Authentication → Sign In / Providers → Discord**, abilita il provider, inserisci **Client ID** e **Client Secret** di OAuth2, salva.
3. In **Authentication → URL Configuration** imposta il **Site URL** effettivo della release; aggiungi alla lista **Redirect URLs** tutti gli URL esatti usati da login (per esempio `http://localhost:8000/index.html` e l'URL HTTPS del sito TEST, comprensivo del path `/index.html` se serve). Evita wildcard troppo ampie in produzione.
4. Controlla schema e permessi in `supabase/POKEXPLORER_SAVE_SCHEMA_REVIEW_ONLY.sql`, che è **solo una proposta da revisionare**, non una migrazione eseguita. Nessun salvataggio cloud funzionerà senza tabella corretta, concessioni Data API e politiche RLS verificate. In particolare utenti A, B e anon devono vedere solo i dati consentiti.
5. Usa il **publishable key** (o anon key pubblica per compatibilità) dal dashboard, mai una secret key o `service_role`.

## 4. Configurazione del frontend TEST (senza segreti)

Apri `config.js` nella **copia di sviluppo** e sostituisci la configurazione vuota con:

```javascript
window.POKEX_PUBLIC_CONFIG = {
  supabaseUrl: 'https://tynhqehheteynviyqkaf.supabase.co',
  publishableKey: 'INSERISCI_SOLO_LA_TUA_SB_PUBLISHABLE_KEY'
};
```

Quando il file contiene una URL Supabase e una chiave pubblica valide:
- l'app mostra il login Discord prima del menu se non c'è sessione;
- non avvia `GameEngine` prima della verifica `auth.getUser()`;
- al ritorno da Discord usa l'utente autenticato per selezionare il checkpoint locale;
- mostra nickname/avatar con fallback locale e offre la disconnessione nelle Opzioni;
- tenta cloud sync solo quando la tabella e RLS sono operative, segnalando eventuali errori.

**Attenzione:** il client pubblico non rende il gioco impossibile da manomettere, e non sostituisce la sicurezza delle policy RLS: sono le policy sul server a proteggere gli account e i salvataggi.

## 5. Test locale e online

Per provare OAuth, **non aprire `index.html` con `file://`**. Nella cartella estratta esegui:

```powershell
py -m http.server 8000
```

Apri `http://localhost:8000/index.html` e aggiungilo alle Redirect URLs di Supabase. Prova, in ordine: primo login, rifiuto dell'autorizzazione, ritorno su pagina di gioco, refresh, logout, nuovo login, avatar mancante, uso di due account, rete assente, permessi database negati e conflitti cloud.

Non utilizzare un account di produzione per test distruttivi sulla stessa tabella senza aver predisposto un ambiente separato.

## 6. Condizioni per release pubblica

- Progetto attivo, Discord OAuth verificato da browser reali.
- URL di test/produzione corretti e separati.
- RLS e tabella dei salvataggi configurati, con test avversariali su account diversi.
- Informativa privacy reale, non la bozza `docs/PRIVACY_NOTICE_TEMPLATE.md`.
- Nessun token bot, Client Secret, service_role o password nel JavaScript, nel ZIP o su GitHub.
- Verifica completa login → nuova avventura → checkpoint → logout → login → continua → secondo dispositivo.

## Fonti aggiornate

- https://supabase.com/docs/guides/auth/social-sign-in/auth-discord
- https://supabase.com/docs/guides/auth/redirect-urls
- https://supabase.com/docs/reference/javascript/auth-signinwithoauth
- https://supabase.com/changelog?types=breaking-change
