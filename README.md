# WEBSITE-ANT
Sito web di un azienda di advisory & corporate finance

## Sviluppo locale

```bash
python3 -m http.server 8000 -d ./
```

---

## Opzioni di Deploy (con HTTPS + dominio custom)

| Opzione | HTTPS | Complessità | Costo |
|---|---|---|---|
| **GitHub Pages** (repo pubblico) | automatico | minima | gratuito |
| **Netlify** | automatico | minima | gratuito |
| **Vercel** | automatico | minima | gratuito |
| **S3 + CloudFront + ACM** | manuale | media | ~$0.50-2/mese |

> Nota: S3 da solo non supporta HTTPS su dominio custom — serve CloudFront davanti.

---

## Gestione contenuti (JSON)

I contenuti dinamici sono gestiti tramite file JSON nella cartella `data/`. Non serve toccare `index.html`.

### Struttura cartella

```
data/
├── partners.json      # Lista partner
├── rassegna.json      # Articoli rassegna stampa
└── comunicati.json    # Comunicati stampa
```

---

### Partners — `data/partners.json`

```json
[
  {
    "nome": "Nome Partner",
    "logo": "images/partner-logo.png",
    "url": "https://www.partner.it"
  }
]
```

| Campo | Obbligatorio | Note |
|-------|-------------|------|
| `nome` | si | Nome visualizzato sotto il logo |
| `logo` | no | Path relativo all'immagine del logo. Se vuoto, mostra solo il nome |
| `url` | no | Link al sito del partner. Se vuoto, la card non è cliccabile |

---

### Rassegna Stampa — `data/rassegna.json`

```json
[
  {
    "testata": "Il Sole 24 Ore",
    "data": "15 marzo 2026",
    "titolo_it": "Titolo in italiano",
    "titolo_en": "Title in English",
    "estratto_it": "Breve estratto in italiano.",
    "estratto_en": "Short excerpt in English.",
    "url": "https://www.ilsole24ore.com/articolo",
    "immagine": "images/rassegna-01.jpg"
  }
]
```

| Campo | Obbligatorio | Note |
|-------|-------------|------|
| `testata` | si | Nome del giornale/testata |
| `data` | si | Data in formato leggibile (es. "15 marzo 2026") |
| `titolo_it` / `titolo_en` | si | Titolo nelle due lingue |
| `estratto_it` / `estratto_en` | si | Estratto breve nelle due lingue |
| `url` | si | Link all'articolo originale |
| `immagine` | no | Path relativo all'immagine. Se vuoto, mostra riquadro grigio placeholder |

---

### Comunicati Stampa — `data/comunicati.json`

```json
[
  {
    "data": "1 aprile 2026",
    "titolo_it": "Titolo comunicato in italiano",
    "titolo_en": "Press release title in English",
    "testo_it": "Testo introduttivo del comunicato.",
    "testo_en": "Introductory text of the press release.",
    "pdf": "docs/comunicato-2026-04-01.pdf"
  }
]
```

| Campo | Obbligatorio | Note |
|-------|-------------|------|
| `data` | si | Data in formato leggibile |
| `titolo_it` / `titolo_en` | si | Titolo nelle due lingue |
| `testo_it` / `testo_en` | si | Testo breve introduttivo nelle due lingue |
| `pdf` | no | Path al file PDF. Se vuoto, il pulsante "Scarica PDF" non viene mostrato |

---

### Note generali

- L'ordine delle voci nel JSON corrisponde all'ordine di visualizzazione (prima voce = prima card)
- Le sezioni Partnership, News e Link sono nascoste (`display:none`) finché non hanno contenuto reale — per renderle visibili rimuovi `style="display:none"` dalla sezione in `index.html` e dal link nel menu
- Per sviluppo locale usare sempre un server HTTP (non aprire `index.html` direttamente nel browser):

```bash
python3 -m http.server 8000
```

---

## Deploy su GitHub Pages (guida)

### 1. Abilitare GitHub Pages sul repo

1. Vai su **Settings** → **Pages** nel repo GitHub
2. In **Source** seleziona `Deploy from a branch`
3. Branch: `main`, cartella: `/ (root)`
4. Clicca **Save**

Il sito sarà pubblicato su `https://<username>.github.io/<repo-name>/`

### 2. Configurare il dominio custom

1. Crea un file `CNAME` nella root del progetto con il tuo dominio:
   ```
   www.tuodominio.it
   ```
2. Fai commit e push del file `CNAME`

### 3. Configurare il DNS presso il tuo registrar

Aggiungi questi record DNS:

**Per dominio apex (`tuodominio.it`)** — 4 record A:
```
A    @    185.199.108.153
A    @    185.199.109.153
A    @    185.199.110.153
A    @    185.199.111.153
```

**Per sottodominio `www`** — 1 record CNAME:
```
CNAME    www    <username>.github.io
```

### 4. Abilitare HTTPS

1. In **Settings** → **Pages**, nel campo **Custom domain** inserisci il tuo dominio
2. Spunta **Enforce HTTPS** (disponibile dopo che il certificato è emesso, ~10-30 min)

### Note
- La propagazione DNS può richiedere fino a 48 ore
- Il certificato HTTPS è emesso automaticamente da Let's Encrypt via GitHub
- Il file `CNAME` va committato nel repo — non perderlo in caso di reset


