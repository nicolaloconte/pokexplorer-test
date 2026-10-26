# T12–T13 · Prototipi ISOLATI (non attivi nel gioco)

- `js/prototypes/checkpoint.js` contiene un formato di checkpoint versionato e testabile, senza modificarne il gameplay: **non** salva automaticamente una partita e **non** ricostruisce ancora l'entità `Pokemon` completa.
- `js/prototypes/cloud-sync.js` è un client *mockabile* della Data API di Supabase: legge, inserisce e aggiorna uno snapshot, rifiutando gli aggiornamenti se la `revision` non corrisponde. **Non** è importato da `index.html`, non usa chiavi segrete e non apre sessioni Discord.
- `supabase/POKEXPLORER_SAVE_SCHEMA_REVIEW_ONLY.sql` è uno schema con RLS da sottoporre a revisione e a test multiutente prima di una qualunque esecuzione. Non è stato eseguito su Supabase.

## Prima di attivare qualunque integrazione

1. Completare l'idratazione del Pokémon (statistiche, abilità, tipi, natura, PP, EV, condizioni) e serializzare la mappa, gli eventi consumati, lo stato di Nuzlocke, leggendari, pesca e Cave. Verificare mediante round-trip che non vengano duplicati premi e catture.
2. Definire confini atomici dei checkpoint (mai durante lotta, dialogo, evoluzione o Raid pendente). Testare aggiornamenti interrotti.
3. Configurare Auth Discord nel progetto Supabase, autorizzare l'URL di ritorno del sito e verificare callback autenticato in browser. Il nome o i metadati Discord non sono affidabili per l'autorizzazione: l'identità è `auth.uid()`.
4. Applicare eventualmente lo schema **solo dopo approvazione esplicita separata**. Testare RLS su `anon`, utente A e utente B, incluso il tentativo di sovrascrivere `user_id`.
5. Verificare conflitti di revisione, offline, logout, cancellazione e trattamento degli account su dispositivi distinti. Non inviare `service_role` o secret keys al frontend.

Riferimenti: documentazione ufficiale Supabase su RLS e URL di redirect OAuth (ottobre 2026). Questo pacchetto non crea account, non altera database e non distribuisce software.
