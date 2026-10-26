# Discord e Supabase — configurazione NON eseguita

Il codice è pronto per la configurazione, ma la release in modalità locale è una **preview senza login obbligatorio**. Un'app con URL e chiave pubblica validi usa il login gate Discord prima del menu. Serve un vero dominio HTTPS per il redirect OAuth.

1. Configurare una Discord application autorizzata e attivare Discord come provider di Supabase Auth. Client secret soltanto sul server/configurazione Supabase, mai nel JavaScript pubblico.
2. Configurare gli URL ammessi nel progetto Supabase per il dominio effettivo dell'app e verificare la callback OAuth. Consultare https://supabase.com/docs/guides/auth/social-login/auth-discord e https://supabase.com/docs/guides/auth/redirect-urls .
3. Esaminare lo schema **non eseguito** `supabase/POKEXPLORER_SAVE_SCHEMA_REVIEW_ONLY.sql`, impostare grants/RLS owner-only, testare utente A, utente B e anon per SELECT/INSERT/UPDATE/DELETE, inclusi i conflitti di revisione.
4. Copiare `config.example.js` in `config.js` e impostare soltanto `supabaseUrl` e `publishableKey` (o anon pubblica per compatibilità). Nessun service_role o client secret nel frontend.
5. Eseguire prove reali: primo login Discord, sessione valida al ritorno, refresh/logout, immagini fallback, salvataggio cloud, conflitto locale/remoto, account separati, ripristino da secondo dispositivo, perdita di rete, errore schema e RLS.
6. Revisionare testo privacy, titolarità dei dati e retention PRIMA di mettere online l'OAuth.

**Questi passaggi richiedono autorizzazione esplicita per modificare Supabase. Nessuna esecuzione è stata effettuata.**

L'attuale client implementa scritture con confronto di revisione e domanda conferma nei conflitti. Non è stato convalidato contro un database vero; il salvataggio locale rimane la fonte di continuità in preview.
