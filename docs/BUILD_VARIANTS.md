# PEaC Build Variants

PEaC offre **due varianti di build** per soddisfare diverse esigenze:

## 🪶 LITE Version (Consigliata per la maggior parte degli utenti)

**Dimensione**: ~50-100 MB | **Build time**: 3-5 minuti

### ✅ Include:
- Tutti i provider LLM API-based (OpenAI, Anthropic, Google, ecc.)
- Parsing completo di documenti (PDF, DOCX, Excel, HTML)
- Interfaccia GUI (Flet) e CLI (Typer)
- Tutte le funzionalità core di Prompt Engineering as Code

### ❌ Non include:
- Embeddings locali (sentence-transformers)
- PyTorch/Torch (~500MB)
- FAISS vector store
- Supporto Jupyter Notebook

### 📦 Installazione LITE:

```bash
# Installazione base (LITE)
poetry install

# Oppure con Poetry
poetry install --without rag
```

### 🏷️ Release tag:
```bash
git tag v1.0.0-lite
git push origin v1.0.0-lite
```

---

## 🚀 FULL Version (Con RAG/AI Locale)

**Dimensione**: ~500+ MB | **Build time**: 10+ minuti

### ✅ Include tutto della LITE + :
- Embeddings locali (sentence-transformers)
- PyTorch per GPU acceleration
- FAISS vector store per RAG
- Jupyter Notebook support

### 📦 Installazione FULL:

```bash
# Installazione completa con RAG
poetry install --extras rag

# Oppure tutto insieme (RAG + Jupyter)
poetry install --extras full
```

### 🏷️ Release tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## 🔧 Come Scegliere?

| Scenario | Versione | Motivo |
|----------|----------|--------|
| Uso API OpenAI/Anthropic/Google | **LITE** | Non serve RAG locale |
| Parsing documenti + LLM cloud | **LITE** | Tutto quello che serve |
| Sviluppo/test rapidi | **LITE** | Build veloce, meno dipendenze |
| RAG con embeddings locali | **FULL** | Serve sentence-transformers |
| Ricerca semantica offline | **FULL** | Serve FAISS + embeddings |
| GPU acceleration per AI | **FULL** | Serve PyTorch |

---

## 📊 Confronto Tecnico

| Feature | LITE | FULL |
|---------|------|------|
| PyTorch | ❌ | ✅ |
| Sentence Transformers | ❌ | ✅ |
| FAISS | ❌ | ✅ |
| Jupyter | ❌ | ✅ (con `--extras jupyter`) |
| Build time | 3-5 min | 10+ min |
| Size | 50-100 MB | 500+ MB |
| GPU Support | ❌ | ✅ |
| RAG Provider | ❌ | ✅ |

---

## 🛠️ Workflow GitHub Actions

### Workflow disponibili:

#### LITE Version:
- `build-release-windows-lite.yml` - Windows LITE build
- `build-release-linux-lite.yml` - Linux LITE build
- `build-release-macos-lite.yml` - macOS LITE build

#### FULL Version:
- `build-release.yml` - Windows FULL build
- `build-release-linux.yml` - Linux FULL build
- `build-release-macos.yml` - macOS FULL build

#### Testing:
- `build-release-windows-stub.yml` - Stub test (30 secondi)

---

## 🚦 Come fare release

### Release LITE:
```bash
# Versione LITE con tag specifico
git tag v1.0.0-lite -m "Release LITE v1.0.0"
git push origin v1.0.0-lite
```

### Release FULL:
```bash
# Versione FULL con tag normale
git tag v1.0.0 -m "Release FULL v1.0.0"
git push origin v1.0.0
```

### Test rapido (stub):
```bash
# Vai su GitHub Actions → "Build Windows STUB" → Run workflow
```

---

## 💡 Best Practices

1. **Per utenti finali**: Distribuisci sempre la versione **LITE**
2. **Per ricercatori/developer**: Distribuisci entrambe le versioni
3. **Testing**: Usa lo stub workflow prima di build pesanti
4. **CI/CD**: Testa LITE prima, FULL dopo se necessario

---

## 📚 Documentazione Aggiuntiva

- [BUILD_RELEASE_GUIDE.md](../docs/BUILD_RELEASE_GUIDE.md) - Guida completa al rilascio
- [pyproject.toml](../pyproject.toml) - Configurazione dipendenze

---

## 🐛 Troubleshooting

### Errore: "RAG provider not available"
**Soluzione**: Stai usando la versione LITE. Installa la versione FULL:
```bash
poetry install --extras rag
```

### Build troppo lento
**Soluzione**: Usa la versione LITE:
```bash
poetry install --without rag
```

### File troppo grande
**Soluzione**: Usa la versione LITE o abilita UPX compression
