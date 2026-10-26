# Batch A · T01/T02 — Test e confronto

## Ambito

- **T01:** rimossa la dicitura visuale `ATTIVO`/`LEAD` dallo slot squadra. Rimangono `.active`, selezione, posizione nella formazione, HP e stato assistivo nella proprietà `aria-label`.
- **T02:** ridotte altezza del Radar, gap e caselle. Sei slot e Portamedaglie accessibili; niente scrolling interno su desktop normale e mobile/tablet. Su 1440×650 la scrollbar interna rimane per sicurezza.

## Come riprodurre

```bash
npm test
npm run test:batch-a
npm run test:browser
npm run test:dev-panel
npm run test:raid-browser
npm run test:gameplay-browser
npm run test:offline
npm run test:visual
```

Se Chromium non è installato con Playwright, installarlo prima. I test browser usano dati Pokémon simulati e non certificano API online.

## Layout Chromium — Risultati

| Viewport | Altezza Radar | Overflow interno | Risultato |
|---|---:|---:|---|
| 360×780 | 43 px | 0 | PASS |
| 390×844 | 43 px | 0 | PASS |
| 768×900 | 43 px | 0 | PASS |
| 1024×900 | 43 px | 0 | PASS |
| 1440×900 | 46,8 px | 0 | PASS |
| 1440×760 | 46,8 px | 0 | PASS |
| 1440×650 | 46,8 px | 36 px, **intenzionale** | PASS (badge raggiungibile) |

Si è verificata anche la disposizione con **6 Pokémon presenti** (fixture di layout senza alterare le limitazioni di squadra del gioco) e l'etichetta accessibile in italiano/inglese. Nessuna targhetta visuale o sovrapposizione di slot.

## Confronti

- `docs/visual/desktop-party-before-after.png`: R2.22 RC3 / RC3.1, 1440×900.
- `docs/visual/mobile-party-before-after.png`: R2.22 RC3 / RC3.1, 390×844.

I confronti mostrano il pannello sinistro con uno sprite locale **segnaposto**; non rappresentano un asset Pokémon definitivo né l'intera partita. Alcuni font/asset remoti non sono caricati in questo ambiente di test.

## Collaudo manuale da effettuare

- Avviare una partita con Pokémon reali tramite PokéAPI e verificare carta attiva e lista.
- Provare selezione, Info Pokémon, spostamento e invio in campo.
- Ripetere con squadra piena e con un Pokémon esausto.
- Provare il Radar con 3, 0 e ∞ scansioni, senza cambiare la DEV MODE.
- Verificare Portamedaglie con zero e otto medaglie su smartphone fisico.
