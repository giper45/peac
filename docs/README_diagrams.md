# PEaC Documentation - Architectural Diagrams

This directory contains architectural diagrams and LaTeX documentation for the PEaC (Prompt Engineering as Code) framework, formatted according to Elsevier guidelines.

## Architecture Overview

### Main Architecture Diagram

- **File**: `modules.puml` - PlantUML source code
- **Generated**: `modules.png` - Architecture overview diagram
- **LaTeX**: `figure_modules_latex.tex` - Elsevier-formatted figure description

The architecture diagram illustrates the modular design of PEaC, consisting of:

1. **External Data Sources Layer**
   - Local Files (txt, pdf, docx, xlsx)
   - Web Resources (HTTP/HTTPS URLs)  
   - Vector Databases (FAISS Index)

2. **PEaC Core Architecture**
   - **Providers Module**: Local, Web, and RAG providers for data integration
   - **RAG Module**: Vector store management, embedding processing, retrieval engine
   - **Core Engine**: YAML parsing, template processing, prompt generation

3. **User Interface Layer**
   - Interactive GUI (CustomTkinter-based)
   - Command Line Interface (CLI)

4. **Output Layer**
   - Generated prompts
   - LLM integration compatibility

### Integration Diagrams

- **Integration Sequence**: `peac_integration_sequence.puml` / `PEaC_Integration_Sequence.png`
- **Use Case Sequence**: `sequence_diagram_peac_usecase.puml` / `PEaC_UseCase_Sequence.png`

## Usage for Academic Papers

### Elsevier CAS-SC Template Integration

The diagrams and LaTeX code follow Elsevier guidelines for scientific publications:

```latex
% Include in your main document
\input{figure_modules_latex.tex}
```

### Figure Reference

```latex
Figure~\ref{fig:modules} provides an overview of the PEaC providers 
in the PEaC architecture.
```

### Caption Format

The caption follows Elsevier standards with:
- Brief descriptive title
- Detailed explanation of components
- Technical specifications where relevant
- Reference to architectural benefits

## Generating Diagrams

To regenerate the PNG files from PlantUML sources:

```bash
cd docs/
plantuml modules.puml
plantuml peac_integration_sequence.puml
plantuml sequence_diagram_peac_usecase.puml
```

## Format Specifications

- **Page Format**: A4 vertical orientation
- **Resolution**: Vector-based PNG suitable for publication
- **Color Scheme**: Professional blue/yellow/green palette
- **Typography**: Clear, readable fonts sized for column width
- **Layout**: Hierarchical organization with clear data flow

## Academic Citation

When using these diagrams in academic work, please cite:

```bibtex
@INPROCEEDINGS{10852434,
  author={Perrone, Gaetano and Romano, Simon Pietro},
  booktitle={2024 2nd International Conference on Foundation and Large Language Models (FLLM)}, 
  title={Prompt Engineering as Code (PEaC): an approach for building modular, reusable, and portable prompts}, 
  year={2024},
  volume={},
  number={},
  pages={289-294},
  doi={10.1109/FLLM63129.2024.10852434}
}
```