# 📚 INDICE DOCUMENTI - Come Orientarsi

## 4️⃣ Documenti Essenziali per l'Esperimento

### 1️⃣ **Procedura_Esperimento_Completa.md** ← INIZIA DA QUI
**Per chi:** Ricercatore e nutrizionista  
**Cosa contiene:** 
- Descrizione completa dell'esperimento (obiettivo, design, timeline)
- I 3 casi d'uso clinici **DETTAGLIATI** (Maria, Giuseppe, Laura)
- Procedura esatta per ogni scenario (METODO A vs METODO B)
- Cosa viene misurato e perché

**Quando leggerlo:** PRIMA di iniziare l'esperimento  
**Tempo di lettura:** 15-20 minuti

---

### 2️⃣ **Guida_Nutrizionista_Moduli_PEaC.md** ← LEGGI PRIMA DI USARE I FILE
**Per chi:** Nutrizionista (NON serve saper niente di codice!)  
**Cosa contiene:**
- Le 8 domande sì/no per scegliere i moduli giusti (Decision Tree semplice)
- Esempi pratici (Maria, Giuseppe, Laura)
- Procedura 5-step su come usare il sistema
- Errori comuni e come evitarli
- Tips professionali

**Quando leggerlo:** Prima di co-design e durante esperimento  
**Tempo di lettura:** 10 minuti  
**Difficoltà:** Bassissima (linguaggio super semplice)

---

### 3️⃣ **MODULO_RACCOLTA_DATI.md** ← COMPILA DURANTE ESPERIMENTO
**Per chi:** Nutrizionista  
**Cosa contiene:**
- Le 3 schede pazienti (Maria, Giuseppe, Laura) con dati dettagliati
- Form per registrare dati per **ogni caso × ogni metodo** (6 combinazioni)
- Checklist qualità per valutare il piano
- Spazi per note libere

**Quando usarlo:** DURANTE l'esperimento (uno per uno per ogni caso)  
**Tempo per caso:** ~5 min per registrare (dopo aver fatto il metodo A e B)

---

### 4️⃣ **README_ESPERIMENTO.md** ← SETUP TECNICO
**Per chi:** Nutrizionista (setup iniziale)  
**Cosa contiene:**
- Checklist cosa ricevere prima di iniziare
- File YAML dove trovarli
- Timeline consigliata per l'esperimento
- Familiarizzazione e prova dummy

**Quando leggerlo:** Una volta, prima di tutto  
**Tempo di lettura:** 5 minuti

---

## 📋 ORDINE SUGGERITO DI LETTURA

```
PRIMO GIORNO (Pre-Esperimento):

1. Leggi: Procedura_Esperimento_Completa.md (20 min)
   └─ Capire che cosa, perché, come funziona l'esperimento

2. Leggi: README_ESPERIMENTO.md (5 min)
   └─ Setup tecnico: cosa ho? cosa mi serve?

3. Leggi: Guida_Nutrizionista_Moduli_PEaC.md (10 min)
   └─ Come usare il sistema senza capire il codice

4. PROVA DUMMY (non contato):
   └─ Prendi un file YAML qualsiasi
   └─ Modifica la query per un paziente fittizio
   └─ Copia in ChatGPT e vedi cosa succede

GIORNO ESPERIMENTO (Settimana 3):

5. Compila: MODULO_RACCOLTA_DATI.md
   └─ Un record per ogni caso (Maria, Giuseppe, Laura)
   └─ Un form A e un form B per ogni caso = 6 form totali

Tempo totale esperimento: ~2.5 ore
```

---

## 🎯 RICORDA

**Questi 4 documenti sono TUTTO quello che ti serve.**

- **Procedura_Esperimento_Completa.md** = il "cosa"
- **Guida_Nutrizionista_Moduli_PEaC.md** = il "come" (semplice!)
- **MODULO_RACCOLTA_DATI.md** = il "dove scrivo"
- **README_ESPERIMENTO.md** = il "prima di iniziare"

Tutto il resto è stato **eliminato** per non confondere.

---

## 📁 FILE YAML DISPONIBILI (10 moduli)

```
nutrizione-base.yaml ← SEMPRE USATO
nutrizione-diabete.yaml ← Se diabete
nutrizione-donne.yaml ← Se donna
nutrizione-weight-loss.yaml ← Se dimagrimento
nutrizione-pcos.yaml ← Se PCOS
nutrizione-sport.yaml ← Se sport intenso
nutrizione-vegetariana.yaml ← Se vegana/vegetariana
nutrizione-allergie.yaml ← Se allergie/intolleranze
nutrizione-gravidanza.yaml ← Se incinta/allatta

patient-template.yaml ← Template vuoto per copiare
```

**Come sceglierli?** Leggi la **Guida_Nutrizionista_Moduli_PEaC.md** (8 domande sì/no).

---

## ✅ PRIMA DI INIZIARE

- [ ] Ho le 4 schede markdown?
- [ ] Ho i 10 file YAML?
- [ ] Ho capito i 3 casi (Procedura_Esperimento_Completa.md)?
- [ ] Ho capito come usare i moduli (Guida_Nutrizionista_Moduli_PEaC.md)?
- [ ] Ho il MODULO_RACCOLTA_DATI.md?
- [ ] Ho ChatGPT/Gemini funzionante?
- [ ] Ho dubbi? Chiedi prima di iniziare!

