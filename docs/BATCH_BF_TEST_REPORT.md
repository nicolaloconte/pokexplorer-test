# Report di collaudo R2.23 RC4 — Batch B–F + Raid indipendenti

## Automatizzati
- `npm test`: **37/37** test Node superati (suite Raid modificata per tiri ripetuti nello stesso dungeon).
- `tests/browser_batch_bf.py`: **4/4** viewport (360×780, 390×844, 768×900, 1440×900) senza overflow orizzontale, menu/assistenza, località, chiavi, IT/EN, schermata Pokémon.
- `tests/browser_batch_a.py`: **7/7** viewport, le correzioni T01–T02 precedenti sono preservate.
- `tests/browser_smoke.py`, `tests/browser_raid.py`, `tests/browser_dev_panel.py`, `tests/browser_gameplay_qa.py`, `tests/browser_offline.py`: PASS.
- Risorse locali: **214** immagini/asset verificati; nessuna anomalia rilevata. Audio: sei tracce lette nel test.

## Limiti della prova
- Chromium simula gli endpoint Pokémon durante i test di interfaccia; i quattro viewport non equivalgono a una prova su telefoni reali.
- Le immagini remote sono bloccate nei test sintetici: negli screenshot salvati in `docs/visual/` alcune sprites appaiono vuote.
- Non è stata completata la campagna 1–80 con PokéAPI reale.
- Login Discord, lettura/scrittura cloud e ripristino completo della partita NON sono stati testati né abilitati.
- La percentuale Raid è verificata deterministicamente per roll 0.05 e 0.9, non validata statisticamente su migliaia di raccolte reali.

## File di evidenza
`docs/node_test_log.txt`, `docs/batchBF_browser_log.json`, `docs/raid_browser_log.json`, `docs/dev_browser_log.json`, `docs/gameplay_browser_log.json`, `docs/offline_browser_log.json`, `docs/smoke_browser_log.json`, `docs/batchA_browser_log.json`, `docs/asset_audit_log.txt`, `docs/audio_audit_log.json`.
