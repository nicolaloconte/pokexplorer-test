# Pokéxplorer R2.23 RC4 — Stato Batch B–F + ripristino Raid

Baseline conservata: R2.22 RC3.1. Nessun deploy, push, modifica a un servizio remoto o credenziale inserita.

| Task | Stato | Esecuzione e limite |
|---|---|---|
| Raid 10% su ogni strumento | **Applicato e testato** | Tolto il blocco «già un Raid per dungeon». Ogni raccolta valida tira di nuovo il 10%, inclusi oggetti successivi a un Raid terminato. Niente secondo Raid *mentre uno è attivo*. Se lo zaino è pieno, non c'è raccolta. |
| T04 Pannello destro | **Applicato e testato** | Caratteri ingranditi; sempre due voci in Oggetti chiave, sprite locali corretti. Canna non cliccabile dal menu; Condividi Esperienza cliccabile solo se posseduto e fuori da stati bloccanti. |
| T06 Display Rotom | **Applicato e testato** | Tolti scritta e sorriso, occhi intatti; località per 1–80 con verifica di piani campione e IT/EN. |
| T03 Scheda Pokémon | **Applicato, verificato in parte** | Hero più compatto, 6 statistiche in griglia 3×2, descrizioni mosse espandibili. Verificata apertura/chiusura e cambio lingua. Serve collaudo reale con quattro mosse e descrizioni lunghe. |
| T07 Mappe | **Valutazione, nessuna alterazione** | Nessun cambiamento di generazione, collisioni, texture o forme. Eventuali rifiniture artistiche restano da approvare visivamente. |
| T10 Traduzioni | **Parziale** | Scheda Pokémon: livello, natura (tutte le 25), tipi, statistiche, abilità e mosse; lookup abilità per lingua. I dialoghi scriptati e altre stringhe del gioco richiedono un audit completo con PokéAPI reale. |
| T09 Login Discord | **Prototipo non operativo** | `docs/LOGIN_DISCORD_PREVIEW.html` è una schermata dimostrativa separata dal gioco. Login OAuth, sessione e callback non sono installati per evitare di presentare un'autenticazione non verificata. |
| T05 Dati Allenatore | **Parziale** | Saldo PokéCoins, avatar locale e nome segnaposto, **non** un'identità Discord autenticata. Identità reale dipende da T09 e privacy. |
| T08 Menu | **Parziale** | Quattro pulsanti e conferma assistenza con URL Discord. «Nuova avventura» funziona; «Guarda progressi» spiega che non esistono progressi persistiti affidabili; «Continua avventura» resta disabilitato (nessun checkpoint idratabile). |

## Test ed evidenze
- `npm test`: 37 test Node, comprese nuove aspettative Raid ripetuti; nessun altro comportamento di DEV MODE modificato.
- `python tests/browser_batch_bf.py`: controlli UI a 360, 390, 768 e 1440px con PokéAPI simulata.
- `python tests/browser_raid.py`, `python tests/browser_dev_panel.py`, `python tests/browser_gameplay_qa.py`, `python tests/browser_offline.py`, `python tests/browser_smoke.py`.
- Audit asset e audio; schede e localizzazione reali richiedono prove manuali.
- Screenshot sintetici: `docs/visual/390-batchbf.png` e `docs/visual/1440-batchbf.png` (asset remoti volutamente bloccati).

## Prima di chiamarla versione stabile
1. Verificare almeno 20 raccoglibili con RNG strumentato e diverse sessioni, provando più Raid nello stesso dungeon senza doppio lancio durante una catena.
2. Completare round-trip checkpoint: Pokémon id/natura/IV/EV/abilità, HP e PP, stato dungeon, eventi consumati, catture, leggendari, regole Nuzlocke, premi e livello attivo.
3. Configurare Discord provider e URL OAuth su Supabase (non in questo pacchetto), provare account distinti con policy RLS e sessioni valide; nessun `service_role` nel frontend.
4. Verificare le traduzioni non ancora coperte in tutte le schermate con API reali; evitare nomi inventati.
5. Provare menu, popup e finestre su telefono fisico; controllare resa tipografica dei testi lunghi.
