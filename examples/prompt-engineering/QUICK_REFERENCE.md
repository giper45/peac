# Quick Reference: Prompt Engineering Templates

## Strategy-Based Templates

### 📚 Learning-Based Strategies
- **`few-shot-prompting.yaml`** - Learn from examples (uses local file imports)
- **`zero-shot-prompting.yaml`** - No examples, pure instruction-based

### 🧠 Reasoning Strategies  
- **`chain-of-thought-prompting.yaml`** - Step-by-step reasoning process
- **`reasoning-acting-prompting.yaml`** - Analysis + actionable steps (ReAc)

### 🎯 Context-Aware Strategies
- **`contextual-prompting.yaml`** - Domain-specific information leveraging
- **`dynamic-prompting.yaml`** - Runtime-modifiable with parameters

### 🔗 Advanced Strategies
- **`multi-strategy-combination.yaml`** - Combines multiple approaches

## Google-Inspired Templates

### 👤 Role-Based
- **`google-persona-assignment.yaml`** - Expert role-playing

### 📝 Structure-Based
- **`google-delimiters.yaml`** - Clear input/output separation
- **`google-task-decomposition.yaml`** - Break complex tasks into subtasks
- **`google-prompt-chaining.yaml`** - Sequential prompt execution

### 🤝 Interactive
- **`google-ask-for-info.yaml`** - Request missing information

## Quick Start Commands

```bash
# Test few-shot learning
poetry run peac prompt examples/prompt-engineering/few-shot-prompting.yaml

# Try chain-of-thought reasoning  
poetry run peac prompt examples/prompt-engineering/chain-of-thought-prompting.yaml

# Use persona-based prompting
poetry run peac prompt examples/prompt-engineering/google-persona-assignment.yaml

# Test multi-strategy approach
poetry run peac prompt examples/prompt-engineering/multi-strategy-combination.yaml
```

## Template Structure
All templates follow PEaC format:
- `instruction`: Core task definition and behavior guidelines
- `context`: Background information and strategy-specific context
- `output`: Response formatting and structure requirements  
- `query`: Example question or task to execute