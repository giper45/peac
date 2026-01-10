# Build & Release Automation - Setup Guide

## 📦 Riduzione dimensioni exe (da ~300MB)

Ho ottimizzato il build per ridurre le dimensioni:

### Tecniche applicate:
1. **UPX compression** - Comprime l'exe fino al 50-70%
2. **`--strip`** - Rimuove debug symbols
3. **`--clean`** - Pulisce cache prima del build

### Risultato atteso:
- Prima: ~265MB
- Dopo: ~100-150MB (con UPX)

**Nota**: UPX viene installato automaticamente dallo script, ma puoi farlo manualmente:
```cmd
choco install upx -y
```

---

## 🚀 GitHub Actions - Workflow automatico

### File creato:
`.github/workflows/build-release.yml`

### Come funziona:
1. **Trigger automatico**: Quando crei un tag versione (es. `v0.2.4`)
2. **Build Windows**: Compila gli exe su Windows runner
3. **Compressione UPX**: Riduce dimensioni automaticamente
4. **Release GitHub**: Crea release e carica gli exe

---

## 📋 STEP PER ATTIVARE IL WORKFLOW

### 1. Committa i file aggiornati
```bash
git add .github/workflows/build-release.yml
git add build_scripts/build_windows.bat
git add peac/main.py
git commit -m "Add automated build & release workflow with exe compression"
git push origin main
```

### 2. Crea un nuovo tag versione
```bash
# Aggiorna la versione in pyproject.toml (es. 0.2.4)
# Poi crea il tag:
git tag v0.2.4
git push origin v0.2.4
```

### 3. Verifica la build su GitHub
- Vai su: `https://github.com/<tuo-username>/peac/actions`
- Vedrai il workflow "Build and Release PEaC" in esecuzione
- Durata: ~15-20 minuti

### 4. Scarica gli exe dalla Release
- Vai su: `https://github.com/<tuo-username>/peac/releases`
- Troverai la release `v0.2.4` con i file:
  - `PeacGUI_v0.2.4.exe` (GUI compressa)
  - `PeacCLI_v0.2.4.exe` (CLI compressa)

---

## 🔧 Build locale con compressione

Puoi buildare localmente con le ottimizzazioni:

```cmd
cd C:\Users\gper4\Git\peac

# Installa UPX (una volta sola)
choco install upx -y

# Build ottimizzato
build_scripts\build_windows.bat
```

Gli exe verranno creati in `dist\` con dimensioni ridotte.

---

## 🎯 Trigger manuale del workflow

Se vuoi lanciare il build senza creare un tag:

1. Vai su GitHub → Actions → "Build and Release PEaC"
2. Clicca "Run workflow" → Seleziona branch → Run
3. Il workflow creerà artifact scaricabili (ma non release pubblica)

---

## ⚙️ Configurazione avanzata

### Ulteriori ottimizzazioni (opzionali):

#### A) Escludere moduli non necessari
Aggiungi al comando PyInstaller:
```
--exclude-module tkinter --exclude-module matplotlib --exclude-module numpy
```

#### B) Build onedir (più veloce all'avvio)
Sostituisci `--onefile` con `--onedir`:
- Pro: Avvio istantaneo, migliore performance
- Contro: Cartella con ~50 file invece di un singolo .exe

#### C) Ridurre i collect-all
Invece di `--collect-all=flet`, specifica solo i submoduli necessari:
```
--hidden-import=flet.core --hidden-import=flet.controls
```

---

## 🐛 Troubleshooting

### Build fallisce su GitHub
- Verifica che `pyproject.toml` abbia tutte le dipendenze corrette
- Controlla i log del workflow in GitHub Actions

### Exe troppo grande ancora
- Prova build `--onedir` per GUI (più veloce, stessa dimensione totale ma distribuita)
- Verifica che UPX stia funzionando (log deve dire "UPX: compressed")

### Antivirus blocca l'exe
- Normale per exe compressi con UPX
- Aggiungi eccezione o firma digitalmente l'exe (richiede certificato)

---

## 📊 Monitoring delle dimensioni

Dopo ogni build, lo script stampa le dimensioni:
```
Name                    Size(MB)
----                    --------
PeacCLI_v0.2.3.exe      120.5
PeacGUI_v0.2.3.exe      145.2
```

Target realistico con Flet: **100-150MB** (Flet include Flutter engine che è pesante)

---

## ✅ Checklist finale

- [ ] File `.github/workflows/build-release.yml` committato
- [ ] File `build_scripts/build_windows.bat` aggiornato
- [ ] File `peac/main.py` con auto-launch GUI committato
- [ ] Push fatto su GitHub
- [ ] Tag versione creato (`git tag v0.2.4 && git push origin v0.2.4`)
- [ ] Workflow eseguito con successo
- [ ] Release creata con exe scaricabili
- [ ] Exe testato su PC pulito (senza Python installato)
