# 🔬 PROCEDURA ESPERIMENTO PEaC - Descrizione Completa

## 📌 OBIETTIVO DELL'ESPERIMENTO

Valutare se i **template strutturati PEaC** (Prompt Engineering as Code) aiutano una nutrizionista a creare **piani alimentari di migliore qualità, più velocemente** rispetto al metodo tradizionale di scrivere direttamente richieste generiche a ChatGPT.

---

## ⏱️ TIMELINE COMPLESSIVA

- **Settimana 1-2**: Co-design e formazione nutrizionista (4-5 sessioni da 1 ora)
- **Settimana 3**: Esperimento vero e proprio (~2.5 ore totali)
- **Settimana 4**: Analisi dati e intervista qualitativa (30-45 min)

---

## 🎓 COSA MISURA L'ESPERIMENTO

### Metriche Quantitative
- ⏱️ **Tempo**: Minuti impiegati per creare il piano (Metodo A vs B)
- 🔄 **Iterazioni**: Numero di tentativi/modifiche necessarie
- 📊 **Qualità Output**: Checklist (calorie corrette? Allergie considerate? Preferenze rispettate?)

### Metriche Qualitative  
- ⭐ **Soddisfazione**: Scala 1-5 (quanto soddisfatta del risultato?)
- 🧠 **Percezione Utilità**: Questionario TAM (28 domande) sulla percezione di usefulness/ease of use
- 💬 **Intervista**: Domande aperte su preferenze, difficoltà, suggerimenti

---

## 👥 DESIGN SPERIMENTALE

### Struttura

**Within-subject design**: La stessa nutrizionista prova **entrambi i metodi** su **3 casi diversi**.

```
CASO 1 (Maria)    → METODO A (ChatGPT direct) → METODO B (PEaC)
CASO 2 (Giuseppe) → METODO B (PEaC first)     → METODO A (ChatGPT) [ordine invertito]
CASO 3 (Laura)    → METODO A (ChatGPT direct) → METODO B (PEaC)
```

**Perché 2 metodi su 3 casi?**  
- Controbilanciamento dell'ordine (CASO 2 ha ordine invertito) per evitare bias da apprendimento
- Validazione su 3 profili clinici diversi

---

## 📋 I TRE CASI D'USO CLINICI

### CASO 1: MARIA - "Il Caso Base: Dimagrimento Sano"

**Profilo Paziente:**
- **Nome**: Maria R.
- **Demografica**: 32 anni, donna, Roma
- **Misure**: 165 cm | 70 kg | BMI 25.7 (normopeso, leggermente alto)
- **Stile di vita**: Sedentaria (lavoro d'ufficio 8h/giorno)
- **Attività fisica**: Nessuna strutturata, cammina occasionalmente

**Condizione Clinica:**
- ✅ Nessuna malattia cronica
- ✅ Nessun farmaco
- ✅ Pressione sanguigna normale
- 🔴 **Allergia**: Intolleranza al lattosio (lieve)

**Obiettivo Nutrizionale:**
- Perdere **5 kg in 3 mesi** (perdita graduale, 400-500g/settimana)
- Mantenere energia per lavoro
- Evitare fame eccessiva durante il giorno

**Preferenze Alimentari:**
- ✅ Ama: Pesce, verdure, cucina mediterranea, olio d'oliva
- ❌ Evita: Carne rossa, cibi pesanti
- ❌ Intollerante: Latticini freschi (yogurt, ricotta, mozzarella)
- ✅ OK: Formaggi stagionati, burro (contengono meno lattosio)

**Contesto Pratico:**
- Pranzo al lavoro alle 13:00 (può portare contenitore da casa)
- Cena a casa con famiglia alle 20:00
- Budget: moderato, disposta a spendere per qualità
- Tempo cucina: 30-45 min per cena (non troppo complesso)

**Rilevanza Clinica:**
Questo è il caso più semplice: nessuna patologia, solo dimagrimento e 1 intolleranza minore. Serve come baseline per valutare se PEaC è utile anche nei casi semplici.

---

### CASO 2: GIUSEPPE - "Il Caso Complesso: Diabete + Dimagrimento"

**Profilo Paziente:**
- **Nome**: Giuseppe P.
- **Demografica**: 58 anni, uomo, Napoli
- **Misure**: 175 cm | 92 kg | BMI 30 (obeso classe 1)
- **Stile di vita**: Moderatamente sedentario (pensionato, cammina 30 min/giorno)
- **Attività fisica**: Passeggiate moderateGiorni: 5-6 volte/settimana

**Condizione Clinica:**
- 🔴 **Diabete tipo 2**: Diagnosticato 10 anni fa, ben controllato
- 📊 **HbA1c**: 7.2% (leggermente sopra target, ma accettabile)
- 💊 **Farmaci**: Metformina 1000 mg, 2 volte/giorno (colazione 7:00, pranzo 13:00)
- 🩸 **Pressione**: Leggermente elevata (135/85), pre-ipertensione

**Obiettivo Nutrizionale:**
- Perdere **8-10 kg in 6 mesi** (graduale, con focus su controllo glicemico)
- Migliorare HbA1c a <7.0% tramite dieta
- Supportare l'assunzione di farmaci (timing pasti)

**Preferenze Alimentari:**
- ✅ Ama: Pesce, pasta (anche integrale), verdure
- ❌ Evita: Zuccheri, cibi molto processati
- ✅ OK: Vino rosso in moderazione (1 bicchiere a cena)
- ❌ Non ama: Cibi troppo "salutisti" o senza sapore

**Contesto Pratico:**
- Colazione 7:00 (prende Metformina)
- Pranzo 13:00 (prende Metformina con il pasto)
- Cena 20:00 (niente farmaci)
- Mangia spesso al ristorante con moglie (2-3 volte/settimana)
- Tempo cucina: limitato, dipende dal mood

**Rilevanza Clinica:**
Caso realistico di diabetico con eccesso ponderale. Il farmaco (Metformina) influenza il timing dei pasti. La combinazione diabete+obesità è comune e rappresentativa.

---

### CASO 3: LAURA - "Il Caso Multidimensionale: PCOS + Allergie + Vegan"

**Profilo Paziente:**
- **Nome**: Laura M.
- **Demografica**: 28 anni, donna, Milano
- **Misure**: 158 cm | 64 kg | BMI 25.6 (normopeso, leggermente alto)
- **Stile di vita**: Attiva (palestra 4 volte/settimana, yoga)
- **Attività fisica**: Moderata-Intensa (mix cardiofitness + forza)

**Condizione Clinica:**
- 🔴 **PCOS** (Sindrome dell'Ovaio Policistico): Diagnosticata 2 anni fa
- 🔴 **Intolleranza al glutine** (confermata test, non celiachia)
- 🔴 **Intolleranza al nichel** (contaminazione alimentare ambientale)
- 💊 **Farmaci**: Metformina 500 mg (controllo PCOS), niente altro
- 📊 **Ciclo mestruale**: Irregolare (ogni 45-60 giorni), scopo: regolarizzare

**Obiettivo Nutrizionale:**
- Regolarizzare il ciclo mestruale tramite dieta
- Supportare attività sportiva (energia + recupero)
- Escludere glutine e cibi ad alto nichel
- Possibilmente perdere 2-3 kg per sentirti meglio (non prioritario)

**Preferenze Alimentari - VINCOLI IMPORTANTI:**
- 🌱 **Vegana**: Niente carne, pesce, uova, latticini (scelta etica)
- ❌ Glutine: Pane, pasta, cereali contenenti glutine
- ❌ Nichel: Pomodori, spinaci, cioccolato, funghi, noci (contaminazione da acciaio)
- ✅ Ama: Legumi, pseudo-cereali (quinoa, amaranto), verdure, frutta secca

**Contesto Pratico:**
- Allenamenti: lunedì, mercoledì, venerdì, domenica (mattina presto)
- Lavora in ufficio (pranzo 13:00, può portare da casa)
- Vive con partner (condivide cena)
- Tempo cucina: 45-60 min (disposta a investire)
- Legge le etichette (attenta, conscia dei vincoli)

**Rilevanza Clinica:**
Caso **più complesso e realistico**: Combina patologia ormonale (PCOS) + intolleranze multiple + scelta dietary (vegana) + attività sportiva. Richiede **integrazione di 3 moduli diversi** nel sistema PEaC. Rappresenta il profilo giovane, attivo, consapevole che sempre più nutrizionisti incontrano.

---

## 📊 MATRICE COMPARATIVA DEI CASI

| Aspetto | Maria | Giuseppe | Laura |
|---------|-------|----------|-------|
| **Complessità** | 🟢 Bassa | 🟡 Media | 🔴 Alta |
| **Patologie** | Nessuna | 1 (Diabete) | 1 (PCOS) |
| **Intolleranze** | 1 (Lattosio) | 0 | 3 (Glutine, Nichel, Animali) |
| **Attività Fisica** | Nessuna | Moderata | Intensa |
| **Farmaci** | 0 | 1 | 1 |
| **N° Moduli PEaC** | 1-2 | 2-3 | 3-4 |
| **Sfida Principale** | Semplicità | Timing farmaci | Multi-vincolo |

---

## 🎯 PROCEDURA ESPERIMENTO (Settimana 3)

### SCENARIO 1: MARIA

#### METODO A - ChatGPT Tradizionale (15 min)

**Istruzioni alla nutrizionista:**
> "Maria è una donna 32enne, 70kg, 165cm, sedentaria. Vuole perdere 5kg in 3 mesi. Ha intolleranza al lattosio (lieve). Ama pesce, cucina mediterranea, verdure. Evita carne rossa. Pranzo al lavoro 13:00, cena 20:00. Crea un piano alimentare settimanale di 1500 kcal/giorno bilanciato, senza latticini, con pesce. Considera il suo orario."

**La nutrizionista:**
1. Copia il testo in ChatGPT
2. Invia
3. Legge il risultato
4. Se non soddisfatta, modifica e ripete
5. Registra il tempo (solo il primo risultato utile conta)

**Cosa registra nel modulo dati:**
- Tempo totale
- Numero tentativi
- Valutazione 1-5 sulla qualità (checklist)
- Difficoltà incontrate
- Soddisfazione finale

---

#### METODO B - PEaC (Template strutturato) (10 min)

**Istruzioni alla nutrizionista:**
> "Apri il file `nutrizione-weight-loss.yaml`. Modifica SOLO questi 4 campi:
> 1. `extends:` → scegli quali moduli (vedi Decision Tree)
> 2. `context.base:` → copia i dati di Maria (età, peso, obiettivo)
> 3. `local:` → aggiungi consigli/lactose.md se necessario
> 4. `query:` → personalizza per Maria
> Copia il file intero in ChatGPT e invia."

**La nutrizionista:**
1. Apre il file YAML (non deve capire il codice, solo riempire i blanks)
2. Modifica i 4 campi
3. Copia in ChatGPT
4. Invia
5. Legge il risultato

**Cosa registra nel modulo dati:**
- Tempo totale
- Numero tentativi
- Valutazione 1-5 sulla qualità (stesso checklist)
- Difficoltà incontrate
- Soddisfazione finale

---

### SCENARIO 2: GIUSEPPE

#### METODO B PRIMA (PEaC) - 10 min

Stessa procedura di METODO B sopra, ma file è `nutrizione-diabete.yaml`

**Personalizzazioni per Giuseppe:**
- `extends:` → base + diabete + weight-loss
- `context.base:` → HbA1c 7.2%, peso 92kg, farmaci Metformina timing
- `instruction.base:` → considerare il timing della Metformina (13:00 pranzo)
- `query:` → specificare obiettivo: "Controllo glicemico + perdita peso graduale"

---

#### METODO A DOPO (ChatGPT tradizionale) - 15 min

Testo diretto: "Giuseppe, 58 anni, 92kg, 175cm. Diabete tipo 2 HbA1c 7.2%, prende Metformina 1000mg (7:00 colazione, 13:00 pranzo). Vuole perdere 8-10kg in 6 mesi e migliorare il controllo glicemico. Ama pesce, pasta, mangia spesso al ristorante. Crea un piano alimentare settimanale di 1800 kcal/giorno, basso indice glicemico, con timing considerato per i farmaci."

**Nota sulla controbilanciamento:** Giuseppe fa METODO B prima per evitare che imparare il primo metodo influenzi il secondo.

---

### SCENARIO 3: LAURA

#### METODO A - ChatGPT Tradizionale (15 min)

"Laura, 28 anni, 64kg, 158cm, attiva (palestra 4 volte/settimana). PCOS con ciclo irregolare, intolleranza glutine e nichel, vegana. Prende Metformina 500mg. Vuole regolarizzare il ciclo e supportare l'attività sportiva. Ama legumi, pseudocereali, verdure. Evita: glutine, nichel (pomodori, spinaci, funghi, noci), animali. Crea un piano alimentare vegano, senza glutine, basso nichel, di ~2000 kcal/giorno con supporto per PCOS e recupero muscolare."

---

#### METODO B - PEaC (Template strutturato) (10 min)

**File:** Modulo composito che estende:
- `nutrizione-base.yaml`
- `nutrizione-pcos.yaml` (PCOS + controllo glicemico)
- `nutrizione-sport.yaml` (supporto attività)
- `nutrizione-allergie.yaml` (glutine + nichel)
- `nutrizione-vegetariana.yaml` (vegana)

**Personalizzazioni:**
- `context.base:` → Laura, PCOS, ciclo irregolare, vegana, atleta moderata
- `instruction.local:` → consigli/gluten-free.md, consigli/nichel-low.md
- `query:` → "Piano vegano, senza glutine/nichel, supporto PCOS e sport"

---

## ⏸️ PAUSA TRA I METODI

Tra METODO A e METODO B: **pausa di almeno 3-4 ore** (se possibile, lo stesso giorno) o il giorno successivo.

**Motivo:** Evitare che la memoria del primo tentativo influenzi il secondo.

---

## 📝 DOPO L'ESPERIMENTO

Dopo completare tutti e 3 gli scenari:

1. **Questionario TAM** (27 domande Likert 1-5 sulla perception di usefulness/ease of use/behavioral intention)
   - ~10 minuti

2. **Intervista semi-strutturata** (30-45 minuti)
   - Domande aperte su preferenze, difficoltà, suggerimenti
   - Registrata audio (con consenso) per analisi qualitativa

---

## 📊 DATI CHE RACCOGLIEREMO

### Da Registrare nel MODULO_RACCOLTA_DATI.md:

Per **ogni caso × ogni metodo** (6 combinazioni totali):
- ⏱️ Tempo impiegato (minuti)
- 🔄 Numero tentativi
- 📋 Checklist qualità (6 items sì/no)
- ⭐ Soddisfazione 1-5
- 💬 Note libere su difficoltà

### Poi (Settimana 4):
- 📝 Questionario TAM (28 domande)
- 🎙️ Intervista qualitativa (registrata)

---

## 🎓 COSA SUCCEDE DOPO

I dati verranno **analizzati statisticamente** e **scritti nella tesi**:

**Sezione Risultati conterrà:**
- "Tempo medio METODO A: 15 min (SD=3)"
- "Tempo medio METODO B: 10 min (SD=2)"
- "Soddisfazione METODO A: 3.5/5 (SD=1.1)"
- "Soddisfazione METODO B: 4.2/5 (SD=0.8)"
- "Qualità: METODO B ha 85% checklist passed, METODO A 70%"
- Citazioni dall'intervista qualitativa

**Sezione Discussion:**
- "I risultati suggeriscono che template strutturati PEaC riducono tempo e aumentano qualità..."
- "Implicazioni: PEaC è applicabile a scale cliniche reali"

---

## ✅ CHECKLIST FINALE PRIMA DI INIZIARE

- [ ] Ho stampato/letto il modulo raccolta dati?
- [ ] Ho capito i 3 casi (Maria, Giuseppe, Laura)?
- [ ] Ho accesso a ChatGPT o Gemini?
- [ ] Ho i 10 file YAML nella cartella?
- [ ] Ho un cronometro (timer del phone va bene)?
- [ ] Ho penna e carta per note?
- [ ] Ho capito che NON devo leggere i casi prima (evitare bias)?
- [ ] Ho domande prima di iniziare?

