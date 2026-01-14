# 🥗 SETUP ESPERIMENTO PEAC - Guida per la Nutrizionista

## 📋 COSA RICEVI

Questo esperimento valuta come i **template strutturati PEaC** ti aiutano a creare piani nutrizionali rispetto al metodo tradizionale (scrivere direttamente su ChatGPT).

**Durata totale**: ~2.5 ore (3 casi clinici)

---

## 📦 FILE INCLUSI IN QUESTA CARTELLA

### 📄 DOCUMENTI ESSENZIALI

1. **PEAC_CHEATSHEET_ITA.md** ← **QUESTO È IL TUO MANUALE PRINCIPALE**
   - Quick reference per ogni template
   - Decision tree visuale
   - Checklist qualità
   - Troubleshooting

2. **DECISION_TREE_TEMPLATE.md**
   - Flowchart per scegliere il template giusto
   - Combinazioni comuni
   - Tabella comparativa

3. **MODULO_RACCOLTA_DATI.md**
   - Form da compilare durante esperimento
   - Registrazione tempi, tentativi, soddisfazione
   - Spazi per note personali

### 📁 FILE YAML - TEMPLATE PEaC

```
usecase/
├─ nutrizione-base.yaml (BASE - esteso da tutti)
├─ nutrizione-diabete.yaml (aggiungi se diabete)
├─ nutrizione-donne.yaml (aggiungi se donna)
│
├─ maria-base-dimagrimento.yaml ← CASO 1
├─ giuseppe-diabete-controllo-glicemico.yaml ← CASO 2
└─ laura-pcos-anti-infiammatorio.yaml ← CASO 3
```

### 📊 SCHEDE PAZIENTI

Riceverai a parte:
- Scheda cartacea Maria (sana, dimagrimento)
- Scheda cartacea Giuseppe (diabete)
- Scheda cartacea Laura (PCOS + allergie)

---

## 🚀 PRIMA DELL'ESPERIMENTO

### Checklist Setup (Giorno 0)

- [ ] Ho ricevuto/stampato i 3 file markdown?
- [ ] Ho accesso ai file YAML PEaC (maria-*, giuseppe-*, laura-*)?
- [ ] Ho ChatGPT o Gemini aperto e funzionante?
- [ ] Ho un cronometro/timer (phone va bene)?
- [ ] Ho penna e carta per annotazioni?
- [ ] Ho il modulo raccolta dati stampato?
- [ ] Comprendo il Decision Tree? (Se no → leggi PEAC_CHEATSHEET)

### Familiarizzazione (30 min)

1. **Leggi PEAC_CHEATSHEET_ITA.md** (10 min)
   - Focus: Decision Tree + Quick Start 3 Step

2. **Guarda la struttura file YAML** (10 min)
   - Apri `maria-base-dimagrimento.yaml`
   - Leggi le sezioni: extends | context | instruction | output | query
   - Nota: come è strutturato? Che cosa significa ogni parte?

3. **Prova con 1 caso dummy** (10 min, NON contato)
   - Seleziona un template
   - Personalizza context + query
   - Copia in ChatGPT
   - Leggi output
   - Nota: quanto è stato facile? Che cosa è chiaro/oscuro?

---

## 🎯 DURANTE L'ESPERIMENTO

### Timeline Consigliata

```
09:00-09:10  Briefing finale, domande
09:10-09:45  SCENARIO 1 - MARIA
             Metodo A (ChatGPT tradizionale): 15 min
             Pausa: 10 min
             Metodo B (PEaC): 10 min

09:45-10:15  PAUSA (caffè, stretching)

10:15-10:50  SCENARIO 2 - GIUSEPPE
             Metodo B (PEaC): 10 min [PRIMA per controbilanciare]
             Pausa: 5 min
             Metodo A (ChatGPT): 15 min

10:50-11:20  PAUSA

11:20-12:00  SCENARIO 3 - LAURA
             Metodo A (ChatGPT): 15 min
             Pausa: 5 min
             Metodo B (PEaC): 10 min

12:00-12:30  Questionario percezione + intervista aperta
```

### Come Procedere STEP-BY-STEP

#### OGNI SCENARIO (Maria, Giuseppe, Laura)

**STEP 1: Ricevi scheda paziente** (1 min)
- Leggi i dati essenziali
- Fai domande se qualcosa è unclear

**STEP 2: Metodo A O B (vedi timeline)** (15 min per tradizionale, 10 min per PEaC)

```
Se METODO A (Tradizionale):
  1. Apri ChatGPT/Gemini
  2. Avvia cronometro ⏱️
  3. Scrivi la richiesta come faresti normalmente
  4. Se non soddisfatta, modifica e ritenta
  5. Quando pronta, ferma cronometro ⏹️
  6. Registra: tempo, N° tentativi, soddisfazione 1-5
  7. Leggi il piano con checklist qualità

Se METODO B (PEaC):
  1. Apri il file YAML scelto (decision tree)
  2. Leggi e comprendi la struttura
  3. Avvia cronometro ⏱️
  4. Personalizza: context (dati paziente) + query (richieste specifiche)
  5. Copia il file in ChatGPT/Gemini
  6. Leggi l'output generato
  7. Se non soddisfatta, modifica context/query e ritenta
  8. Ferma cronometro ⏹️
  9. Registra: tempo, N° modifiche, soddisfazione 1-5
  10. Leggi il piano con checklist qualità
```

**STEP 3: Compila Modulo Raccolta Dati** (3 min)
- Tempo esatto (orario inizio/fine)
- Numero tentativi/modifiche
- Checklist qualità (6 domande sì/no)
- Soddisfazione 1-5
- Note difficoltà

**STEP 4: Pausa** (5-10 min)
- Non leggere il piano dell'altro metodo
- Non confrontare mentalmente
- Distaccati e riposa

---

## 📐 MATERIALI DISPONIBILI

### Durante Esperimento Puoi Consultare:

✅ **PEAC_CHEATSHEET_ITA.md**
- Decision Tree
- Quick Start 3 Step
- Checklist Qualità
- Troubleshooting

✅ **I file YAML stessi**
- Aprili con qualsiasi text editor
- Leggi context, instruction, output
- Modifica e personalizza

✅ **Domande di clarificazione**
- Se non capisci quale template usare → consulta Decision Tree
- Se template non funziona → modifica query
- Se hai dubbio clinico → pensa come nutrizionista (PEaC non sostituisce te!)

---

## 🎓 KEY POINTS DA RICORDARE

### Obiettivo dell'Esperimento
Non è testare TE, ma testare se PEaC è utile nella pratica nutrizionale.

### Come Comportarsi
- ✅ Sii onesta sui tempi (anche se lunghi!)
- ✅ Valuta secondo i tuoi criteri clinici professionali
- ✅ Annota difficoltà specifiche
- ✅ Usa il tuo linguaggio naturale in Metodo A

### Non Fare
- ❌ Non cercare di "fare buona figura" accelerando artificialmente
- ❌ Non confrontare i metodi DURANTE l'esperimento (solo dopo)
- ❌ Non inventare soluzioni non usate davvero
- ❌ Non copiare ciecamente template senza personalizzare

---

## 📞 IN CASO DI PROBLEMI

### "Non so quale template usare per questo paziente"
→ Consulta DECISION_TREE_TEMPLATE.md  
→ Se ancora dubbio, usa template MÀ SPECIFICO disponibile

### "Il piano generato non mi piace"
→ PERFETTO! Questo è dato valido
→ Modifica la query e ritenta (conta come 1 tentativo)
→ Registra nel modulo

### "Mi serve più tempo di quanto previsto"
→ Va bene! Tempo reale è quello che conti
→ Non accelerare artificialmente

### "La IA non capisce la mia richiesta"
→ Normale! Sia in Metodo A che B
→ Prova a riscrivere in modo diverso
→ Conta come 1 iterazione

### "Un template ha sezioni che non capisco"
→ Leggi il commento iniziale del file
→ Chiedi chiarimento (non fa male!)
→ Ignora sezioni non rilevanti se necessario

---

## 📋 CHECKLIST FINALE - PRIMA DI COMINCIARE

```
PREPARAZIONE:
  [ ] Ho capito gli obiettivi dell'esperimento?
  [ ] Ho letto PEAC_CHEATSHEET_ITA.md?
  [ ] Ho consultato DECISION_TREE_TEMPLATE.md?
  [ ] Conosco i 3 casi (Maria, Giuseppe, Laura)?

STRUMENTI:
  [ ] ChatGPT/Gemini aperto e funzionante?
  [ ] File YAML PEaC accessibili?
  [ ] Cronometro/Timer pronto?
  [ ] MODULO_RACCOLTA_DATI.md stampato o digitale?

COMPRENSIONE:
  [ ] Capisco quando usare METODO A (tradizionale)?
  [ ] Capisco quando usare METODO B (PEaC)?
  [ ] So come leggere un file YAML?
  [ ] So come personalizzare context + query?

ATTEGGIAMENTO:
  [ ] Sono consapevole che PEaC è uno STRUMENTO, non la soluzione?
  [ ] Userò il mio giudizio clinico per valutare?
  [ ] Sarò onesta nei tempi e nelle difficoltà?
  [ ] Sono pronta a 2.5 ore di concentrazione?
```

Se TUTTI i check sono SÌ → Sei pronta! 🚀

---

## 🎯 COSA SUCCEDE DOPO

1. **Durante/Dopo esperimento**:
   - Compilare MODULO_RACCOLTA_DATI.md

2. **Questionario Percezione** (~20 min):
   - 27 domande Likert 1-5 su utilità, facilità d'uso, fiducia

3. **Intervista Semi-Strutturata** (~30-45 min):
   - Domande aperte su esperienza, benefici, limiti

4. **Follow-up** (Opzionale):
   - Contatto a 1 mese: "Hai riusato i template PEaC?"

---

## 📞 CONTATTI & SUPPORTO

Se hai domande PRIMA dell'esperimento:
- Leggi prima PEAC_CHEATSHEET_ITA.md
- Se ancora dubbio → contatta

Se hai domande DURANTE:
- Consulta il cheatsheet
- Chiedi direttamente

Se hai problemi TECNICI:
- ChatGPT non funziona? → Prova Gemini
- File YAML non apre? → Chiedi (formato testo, facile aprire)
- Timer? → Phone stopwatch va benissimo

---

**GRAZIE per il tuo tempo e la tua partecipazione! 🙏**

Questo esperimento aiuterà a migliorare PEaC e dimostrerà l'utilità di approcci strutturati in ambito sanitario.

---

*Documento preparato per Studio di Usabilità PEaC - Caso d'uso Nutrizionista*  
*Gennaio 2026*

