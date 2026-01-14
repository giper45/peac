# 📖 GUIDA NUTRIZIONISTA - Come Usare i Moduli PEaC (Senza Saper Niente di Codice!)

---

## 🎯 COSA DEVI SAPERE (2 MINUTI DI LETTURA)

Stai per usare 10 **template pre-scritti** che funzionano come "mattoncini LEGO" per nutrizione.

Ogni paziente è diverso, ma molti hanno i stessi problemi (diabete, allergie, sport, vegetariano).

Invece di scrivere da zero ogni volta a ChatGPT, **tu scegli i mattoncini giusti per quel paziente**, li personalizzi un po' usando l'**App GUI PEaC** (un'applicazione grafica semplice), e li dai a ChatGPT.

**Risultato**: Piano migliore, più veloce, meno confusione. 💪

---

## 📱 COS'È L'APP GUI PEaC?

È un'**applicazione con interfaccia grafica** (come Word o Excel) che ti permette di creare prompt professionali **senza scrivere codice**.

**Non è complicato:** Vedi un form con campi da riempire, come quando compili un modulo al medico.

**Esempio:**
```
╔════════════════════════════════════╗
║ APP GUI PEaC - Crea Prompt         ║
╠════════════════════════════════════╣
║ Scegli moduli (checkbox):          ║
║ [✓] base                           ║
║ [✓] weight-loss                    ║
║ [✓] allergie                       ║
║                                    ║
║ Dati paziente (testo libero):      ║
║ ┌────────────────────────────────┐ ║
║ │ Maria 32 anni 70kg sedentaria  │ ║
║ │ Ufficio, pranzo 13:00          │ ║
║ │ Intolleranza lattosio          │ ║
║ └────────────────────────────────┘ ║
║                                    ║
║ Richiesta personalizzata:          ║
║ ┌────────────────────────────────┐ ║
║ │ Piano 7gg 1500kcal perdita peso│ ║
║ │ senza lattosio ricco pesce      │ ║
║ └────────────────────────────────┘ ║
║                                    ║
║ [Genera Prompt]  [Copia]           ║
╚════════════════════════════════════╝
```

**E basta!** L'app fa il resto.

---

## 🧩 I 10 "MATTONCINI" DISPONIBILI

### 🟢 Il Mattoncino Base (SEMPRE USATO)

**`nutrizione-base.yaml`**
- Lo usi con OGNI paziente
- Contiene la struttura di base: 5-6 pasti, idratazione, formato settimanale
- Non devi toccarlo quasi mai

---

### 🔵 I 9 Mattoncini Specializzati (AGGIUNGI SE NECESSARIO)

| Mattoncino | Quando lo usi | Esempio paziente |
|------------|----------------|-----------------|
| **diabete.yaml** | Se il paziente ha diabete | "Luca ha diabete tipo 2" |
| **donne.yaml** | Se il paziente è una donna | "Tutte le donne" |
| **weight-loss.yaml** | Se vuole perdere peso | "Maria vuole -5kg" |
| **pcos.yaml** | Se ha PCOS | "Laura ha PCOS" |
| **sport.yaml** | Se fa sport intenso (3+ volte/sett) | "Giuseppe va in palestra" |
| **vegetariana.yaml** | Se è vegana/vegetariana | "Sei vegana?" |
| **allergie.yaml** | Se ha allergie/intolleranze | "Non mangia lattosio" |
| **gravidanza.yaml** | Se è incinta o allatta | "Aspetto un bambino" |

---

## � I TRE PILASTRI DI PEaC - Context, Instruction, Output

Quando usi l'App GUI PEaC, vedi tre sezioni principali che puoi **modificare se vuoi**. Non è obbligatorio cambiarle, ma puoi personalizzarle per il paziente specifico.

Ecco cosa sono:

---

### 1️⃣ **CONTEXT** - "Dai al ChatGPT il Contesto del Paziente"

**Cos'è?** È tutte le **informazioni di background** sul paziente che ChatGPT deve sapere.

**Esempi di contesto:**
```
Maria ha 32 anni, pesa 70kg, è alta 165cm.
Lavora in ufficio 8 ore al giorno (sedentaria).
Ha intolleranza al lattosio (lieve).
Ama la cucina mediterranea, soprattutto pesce.
Evita carne rossa e formaggi freschi.
Mangia a casa la colazione e cena, pranzo al lavoro alle 13:00.
```

**Cosa deve contenere:**
- ✅ Età, peso, altezza, sesso
- ✅ Condizioni mediche (se ce ne sono)
- ✅ Allergie/intolleranze
- ✅ Preferenze alimentari (ama/evita)
- ✅ Orari dei pasti e contesto (ufficio, casa, famiglia)
- ✅ Livello di attività (sedentario, moderato, attivo)
- ✅ Farmaci (se rilevanti per timing dei pasti)

**Quando modificarlo:**
Se l'App ha generato il context da sola e **non riflette correttamente il paziente**, puoi aggiungerci informazioni.

**Esempio di modifica:**
```
CONTEXT GENERATO:
"Paziente donna, ama verdure e pesce"

TUA MODIFICA AGGIUNTA:
"Paziente donna, ama verdure e pesce, ma SPECIFICAMENTE: 
 - Verdure: broccoli, zucchine, insalata
 - Pesce: spigola, orata, tonno
 - Odio: spinaci, melanzane"
```

---

### 2️⃣ **INSTRUCTION** - "Dai al ChatGPT le Regole/Linee Guida"

**Cos'è?** Sono le **istruzioni cliniche** che ChatGPT deve seguire quando crea il piano.

**Esempi di instruction:**
```
Per dimagrimento:
- Deficit calorico di 500 kcal/giorno
- Proteine aumentate per satietà (30-35%)
- Fibre alte per senso di pienezza

Per diabete:
- Indice glicemico basso (GI <55)
- Carboidrati distribuiti uniformemente nei pasti
- Considerare timing della Metformina (colazione 7:00, pranzo 13:00)
```

**Cosa deve contenere:**
- ✅ Linee guida cliniche per la condizione (es. diabete, PCOS)
- ✅ Raccomandazioni nutrizionali specifiche
- ✅ Vincoli (allergie da evitare)
- ✅ Considerazioni su farmaci (se rilevanti)
- ✅ Preferenze sulla struttura dei pasti

**Quando modificarlo:**
Se vuoi **enfatizzare** una cosa particolare per quel paziente.

**Esempio di modifica:**
```
INSTRUCTION GENERATA PER DIMAGRIMENTO:
"Deficit calorico 500 kcal, proteine 30%, fibre alte"

TUA MODIFICA AGGIUNTA:
"Deficit calorico 500 kcal, proteine 30%, fibre alte.
 IMPORTANTE: Maria ha fame nel pomeriggio → aggiungere snack sostanzioso alle 16:00"
```

---

### 3️⃣ **OUTPUT** - "Dimmi Come Vuoi il Risultato Finale"

**Cos'è?** È il **formato e lo stile** che vuoi che ChatGPT usi per presentarti il piano alimentare.

**Esempi di output:**
```
Piano settimanale con 5 pasti per giorno
Ogni pasto deve specificare:
- Nome del piatto
- Ingredienti con quantità (in grammi)
- Calorie totali
- Macronutrienti (proteine, carboidrati, grassi)

Formato: tabella settimanale con colonne per ogni giorno
```

**Cosa deve contenere:**
- ✅ Numero di pasti al giorno (es. 5: colazione, spuntino, pranzo, merenda, cena)
- ✅ Dettagli dei pasti (ingredienti, quantità, calorie)
- ✅ Formato (tabella, elenco, ricette dettagliate?)
- ✅ Informazioni aggiuntive (note su idratazione, integratori, ecc)
- ✅ Forma dell'output (semplice lista, ricette dettagliate con preparazione?)

**Quando modificarlo:**
Se preferisci un **formato diverso** per leggere il piano.

**Esempio di modifica:**
```
OUTPUT GENERATO:
"Piano settimanale con 5 pasti in tabella"

TUA MODIFICA AGGIUNTA:
"Piano settimanale con 5 pasti. Per OGNI pasto voglio:
 - Nome piatto
 - Ingredienti con QUANTITÀ IN GRAMMI
 - Calorie
 - Una riga di note pratiche (es. 'puoi cucinare domenica e conservare in frigo')"
```

---

## 🔄 COME USARE CONTEXT + INSTRUCTION + OUTPUT + QUERY INSIEME

L'App GUI PEaC ti mostra questi 4 elementi. Ecco come funzionano insieme:

```
CONTEXT (Background paziente)
↓
INSTRUCTION (Cosa fare, regole cliniche)
↓
OUTPUT (Come presentare il risultato)
↓
QUERY (La richiesta specifica)
↓
✨ ChatGPT genera il piano alimentare! ✨
```

**Esempio completo per MARIA:**

```
CONTEXT: 
"Maria 32 anni 70kg sedentaria ufficio. Vuole -5kg. 
 Intolleranza lattosio. Ama pesce mediterranea verdure. 
 Pranzo 13:00 lavoro, cena 20:00 casa."

INSTRUCTION:
"Deficit calorico 500 kcal (~1500 kcal/giorno).
 Proteine 30% per satietà.
 Escludere latticini freschi.
 Fibre alte. CHO complessi."

OUTPUT:
"Piano settimanale, 5 pasti/giorno (colazione 7:30, spuntino 10:00, 
 pranzo 13:00, merenda 16:00, cena 20:00).
 Ogni pasto: nome piatto, ingredienti grammi, calorie.
 Formato: tabella settimanale."

QUERY:
"Piano 7 giorni 1500 kcal perdita peso. Maria, senza lattosio, 
 ricco pesce verdure. Considerare orari pranzo lavoro."

↓

RISULTATO: ChatGPT genera un piano preciso, personalizzato, 
           che rispetta TUTTI gli elementi sopra.
```

---

## ✏️ QUANDO MODIFICARE COSA

| Elemento | Quando modificarlo | Quanto spesso |
|----------|-------------------|---------------|
| **Context** | Paziente specifico ha dettagli particolari che l'app non ha capito | Raramente (1-2 volte) |
| **Instruction** | Vuoi aggiungere linee guida cliniche specifiche per quel paziente | Raramente (1-2 volte) |
| **Output** | Preferisci un formato diverso (es. "voglio ricette dettagliate") | Talvolta (2-3 volte) |
| **Query** | Sempre! È la tua richiesta finale | **Sempre personalizzare** |

**Regola d'oro:** Non devi modificare niente se l'app ha fatto bene il lavoro. Ma se vuoi risultati migliori, puoi sempre "aggiungere dettagli" a qualunque sezione.



È semplice: fai 8 domande sì/no al paziente. Le risposte ti dicono quali mattoncini usare.

### LE 8 DOMANDE MAGICHE

```
DOMANDA 1: Il paziente è una DONNA? (ciclo, ormoni, etc)
   ✅ SÌ   → Usa: diabete.yaml
   ❌ NO   → Non usare donne.yaml

DOMANDA 2: Il paziente ha DIABETE?
   ✅ SÌ   → Usa: diabete.yaml
   ❌ NO   → Non usare

DOMANDA 3: Il paziente vuole PERDERE PESO?
   ✅ SÌ   → Usa: weight-loss.yaml
   ❌ NO   → Non usare

DOMANDA 4: Il paziente ha PCOS?
   ✅ SÌ   → Usa: pcos.yaml
   ❌ NO   → Non usare

DOMANDA 5: Il paziente fa SPORT INTENSO? (3+ volte/settimana)
   ✅ SÌ   → Usa: sport.yaml
   ❌ NO   → Non usare

DOMANDA 6: Il paziente è VEGANO/VEGETARIANO?
   ✅ SÌ   → Usa: vegetariana.yaml
   ❌ NO   → Non usare

DOMANDA 7: Il paziente ha ALLERGIE o INTOLLERANZE?
   ✅ SÌ   → Usa: allergie.yaml
   ❌ NO   → Non usare

DOMANDA 8: Il paziente è INCINTA o ALLATTA?
   ✅ SÌ   → Usa: gravidanza.yaml
   ❌ NO   → Non usare
```

---

## 📋 ESEMPI PRATICI - QUALE MATTONCINO PER CHI?

### Esempio 1: MARIA (Caso 1 - Il Caso Base)

**Chi è Maria?**
- 32 anni, donna
- 70 kg, 165 cm, sedentaria (lavoro ufficio)
- Vuole perdere 5 kg in 3 mesi
- Intolleranza al lattosio
- Ama: pesce, cucina mediterranea, verdure
- Orario: colazione 7:30, pranzo 13:00 al lavoro, cena 20:00

**Le 8 domande:**
1. Donna? → ✅ SÌ → Seleziona: donne.yaml
2. Diabete? → ❌ NO
3. Perdere peso? → ✅ SÌ → Seleziona: weight-loss.yaml
4. PCOS? → ❌ NO
5. Sport intenso? → ❌ NO
6. Vegana? → ❌ NO
7. Allergie? → ✅ SÌ (lattosio) → Seleziona: allergie.yaml
8. Incinta? → ❌ NO

**Mattoncini da usare:**
- ✅ base.yaml (SEMPRE)
- ✅ donne.yaml (è donna)
- ✅ weight-loss.yaml (vuole dimagrire)
- ✅ allergie.yaml (intolleranza lattosio)

**Totale: 4 mattoncini**

---

### Esempio 2: GIUSEPPE (Caso 2 - Il Caso Medio-Complesso)

**Chi è Giuseppe?**
- 58 anni, uomo
- 92 kg, 175 cm, pensionato (moderatamente attivo: cammina 30 min/giorno)
- Diabete tipo 2, HbA1c 7.2%, prende Metformina (colazione 7:00, pranzo 13:00)
- Vuole perdere 8-10 kg in 6 mesi
- Pre-ipertensione
- Ama: pesce, pasta, mangia spesso al ristorante (2-3 volte/settimana)
- Orario: colazione 7:00 (Metformina), pranzo 13:00 (Metformina), cena 20:00

**Le 8 domande:**
1. Donna? → ❌ NO
2. Diabete? → ✅ SÌ → Seleziona: diabete.yaml
3. Perdere peso? → ✅ SÌ → Seleziona: weight-loss.yaml
4. PCOS? → ❌ NO
5. Sport intenso? → ❌ NO (camminata moderata)
6. Vegana? → ❌ NO
7. Allergie? → ❌ NO
8. Incinta? → ❌ NO

**Mattoncini da usare:**
- ✅ base.yaml (SEMPRE)
- ✅ diabete.yaml (ha diabete, considerare timing Metformina)
- ✅ weight-loss.yaml (vuole dimagrire)

**Totale: 3 mattoncini**

---

### Esempio 3: LAURA (Caso 3 - Il Caso Complesso Multi-Vincolo)

**Chi è Laura?**
- 28 anni, donna
- 64 kg, 158 cm, attiva (palestra 4 volte/settimana: mix cardio + forza)
- PCOS, ciclo irregolare (vuole regolarizzare)
- Prende Metformina 500 mg
- Intolleranza: glutine (confermato), nichel (ambientale)
- **Scelta vegana** (niente carne, pesce, uova, latticini)
- Ama: legumi, pseudo-cereali, verdure, frutta secca
- Orario: allenamenti lunedì, mercoledì, venerdì, domenica; pranzo 13:00 ufficio

**Le 8 domande:**
1. Donna? → ✅ SÌ → Seleziona: donne.yaml
2. Diabete? → ❌ NO (ma PCOS simile per glicemia)
3. Perdere peso? → ❌ NO (potrebbe, ma non prioritario)
4. PCOS? → ✅ SÌ → Seleziona: pcos.yaml
5. Sport intenso? → ✅ SÌ (4 volte/sett) → Seleziona: sport.yaml
6. Vegana? → ✅ SÌ → Seleziona: vegetariana.yaml
7. Allergie? → ✅ SÌ (glutine, nichel) → Seleziona: allergie.yaml
8. Incinta? → ❌ NO

**Mattoncini da usare:**
- ✅ base.yaml (SEMPRE)
- ✅ donne.yaml (donna)
- ✅ pcos.yaml (PCOS, regolarizzazione ciclo)
- ✅ sport.yaml (attività intensa, supporto muscolare)
- ✅ vegetariana.yaml (vegana)
- ✅ allergie.yaml (gluten-free, nichel-low)

**Totale: 6 mattoncini** (il caso più complesso!)

---

## 📊 RIEPILOGO COMPARATIVO

| Paziente | Complessità | Mattoncini | Sfida Principale |
|----------|------------|-----------|-----------------|
| **Maria** | 🟢 Bassa | 4 | Semplicità (baseline) |
| **Giuseppe** | 🟡 Media | 3 | Timing farmaci (Metformina) |
| **Laura** | 🔴 Alta | 6 | Multi-vincolo (PCOS+vegana+allergie+sport) |

---

## 🚀 PROCEDURA - Come Usare il Sistema (5 STEP)

### STEP 1: Raccogli Informazioni dal Paziente

Fai le 8 domande sopra al paziente. Scrivi le risposte su carta.

**Esempio MARIA:**
- Sesso: Donna ✅
- Diabete: No ❌
- Dimagrimento: Sì, 5kg ✅
- PCOS: No ❌
- Sport: No (sedentaria) ❌
- Vegana: No ❌
- Allergie: Sì, lattosio ✅
- Incinta: No ❌

---

### STEP 2: Leggi Questo Documento e Decidi i Mattoncini

Guardando le 8 domande e le risposte, sai esattamente quali file usare.

**Per Maria:** base + weight-loss + allergie

---

### STEP 3: Apri l'App GUI PEaC

**Importante**: Non devi aprire il file YAML in un editor di testo (no Notepad, no Word!).

Usa l'**App GUI PEaC** che hai ricevuto. È una interfaccia grafica facile e intuitiva, progettata esattamente per questo:

1. Apri l'App PEaC
2. Scegli il file YAML che vuoi usare (es. `nutrizione-diabete.yaml`)
3. L'app ti mostra le sezioni in modo visuale e leggibile
4. Puoi aggiungere/modificare testo senza vedere il codice YAML

**Non devi capire il YAML!** L'app pensa a tutto. Tu semplicemente compili i campi che ti servono.

---

### STEP 4: Compila i Campi Usando l'App GUI

L'App PEaC ti mostra una form semplice con i campi che puoi compilare:

1. **Sezione EXTENDS** (moduli da usare)
   - L'app ti mostra una lista
   - Scegli quelli che servono per questo paziente (basato sulla Decision Tree)
   - Esempio per Maria: ✅ base, ✅ weight-loss, ✅ allergie

2. **Sezione CONTEXT** (dati del paziente) - ✏️ PUOI MODIFICARE
   - L'app ti mostra un campo di testo
   - Copia i dati di Maria: età, peso, allergies, preferenze, orari
   - Esempio: "Maria 32 anni 70kg sedentaria ufficio pranzo 13:00"
   - **Se vuoi**: puoi aggiungere più dettagli per più precisione

3. **Sezione INSTRUCTION** (linee guida cliniche) - ✏️ PUOI MODIFICARE
   - Sono le regole che ChatGPT deve seguire
   - Esempi: "deficit calorico 500", "proteine 30%", "evita latticini freschi"
   - **Se vuoi**: puoi aggiungere linee guida specifiche per Maria

4. **Sezione OUTPUT** (come vuoi il risultato) - ✏️ PUOI MODIFICARE
   - Come ChatGPT deve formattare il piano
   - Esempi: "5 pasti al giorno", "tabella settimanale", "ingredienti in grammi"
   - **Se vuoi**: puoi specificare un formato particolare

5. **Sezione QUERY** (richiesta personalizzata) - 🔴 IMPORTANTE!
   - **QUESTO È IL PIÙ IMPORTANTE!**
   - Scrivi qui cosa vuoi che ChatGPT faccia
   - Includi i dati specifici di Maria
   - Esempio: "Piano 7 giorni 1500 kcal perdita peso senza lattosio pesce"

6. **Premi il bottone "Genera Prompt"** (o simile)
   - L'app automaticamente "compone" il tuo modello
   - Vedi l'anteprima del prompt
   - Premi "Copia negli appunti" se sei soddisfatto

---

### STEP 5: Usa il Prompt Generato in ChatGPT

1. **Copia il prompt** (l'app ha un bottone "Copia negli appunti")
2. **Apri ChatGPT o Gemini**
3. **Incolla il prompt** (Ctrl+V)
4. **Premi Invio**
5. **ChatGPT genera il piano alimentare** ✨

---



## 💡 TIPS PROFESSIONALI

### TIP 1: La Query è il "Segreto"

La `query:` finale è quello che ChatGPT **veramente legge** per creare il piano.

Se la query è vaga ("Piano per dimagrimento"), il piano sarà vago.

Se la query è specifica ("Piano 1500 kcal senza lattosio per Maria sedentaria ama pesce"), il piano sarà specifico.

**Dedica 1 minuto a scrivere bene la query. Vale più di tutto il resto.**

---

### TIP 2: Puoi Aggiungere Dati Personali

Se il paziente ti ha detto cose specifiche (ama i piatti della nonna, non ama spendere molto, ha allergia al nichel), **aggiungile nella query**.

```
query: "Piano per Giuseppe diabetico, piace pasta ma no zuccheri. Pranzo al lavoro fisso 13:00. Budget medio. 1800 kcal controllo glicemico."
```

---

### TIP 3: Se ChatGPT Non Soddisfa, Modifica

Se il piano non è come vuoi, **cambia la query** e prova di nuovo.

**SEMPLICE:**
- "Aumenta le proteine"
- "Aggiungi più verdure"
- "Semplifica le ricette"
- "Aggiungi snack per il pomeriggio"

ChatGPT capirà e rigenererà il piano.

---

### TIP 4: Conserva i File Buoni

Se crei un piano che funziona bene, **salva il file di quel paziente**.

Next volta che quel paziente torna, copia il vecchio file, cambio un dettaglio, e il piano è quasi pronto.

---

## 🆘 SE QUALCOSA NON FUNZIONA

**Problema:** Non so quale mattoncino usare
**Soluzione:** Torna alle 8 domande. Se rispondi "sì", lo usi. Se "no", non lo usi.

---

**Problema:** ChatGPT genera un piano che non mi piace
**Soluzione:** Modifica la query con dettagli più specifici. Ritenta.

---

**Problema:** Il file YAML ha troppo testo e mi confonde
**Soluzione:** Ignora tutto. Scorri. Cerca la parola `query:`. Modifica quella linea. Fine.

---

**Problema:** Non riesco a differenziare base.yaml da weight-loss.yaml
**Soluzione:** Facile. Se il paziente è un caso **semplice senza condizioni speciali**, apri base. Se il paziente ha **una condizione specifica** (diabete, allergie, sport), apri quello specializzato (diabete.yaml, allergie.yaml, sport.yaml).

---

## 📞 CONTATTI PER DOMANDE

Se hai dubbi o problemi durante l'esperimento:
- Chiama/scrivi al ricercatore
- Ricorda: **non esiste domanda stupida**
- Meglio chiarire ora che fare male l'esperimento

---

## 🎓 RIASSUNTO FINALE (TL;DR)

1. **8 domande sì/no** = sai quali mattoncini usare
2. **Apri il file giusto** (base o specializzato)
3. **Modifica la query in fondo** con dati del paziente
4. **Copia tutto, incolla in ChatGPT**
5. **ChatGPT fa il resto**
6. **Registra i risultati nel modulo dati**

**BASTA! 🎉**

