"""
Generate synthetic document corpus for performance benchmarking.

Creates realistic text documents of varying sizes and topics to test
RAG provider performance under controlled conditions.
"""
import os
import random
from pathlib import Path
from typing import List


TOPICS = [
    "machine learning", "artificial intelligence", "deep learning",
    "natural language processing", "computer vision", "robotics",
    "data science", "neural networks", "reinforcement learning",
    "prompt engineering", "large language models", "transformers"
]

TEMPLATES = [
    "Introduction to {topic}: {topic} is a field of study focused on {description}. "
    "Recent advances in {topic} have shown promising results in {application}. "
    "Researchers are exploring {challenge} to improve performance. "
    "The key principles of {topic} include {principle1}, {principle2}, and {principle3}. ",
    
    "Advanced {topic} Techniques: State-of-the-art methods in {topic} leverage {method}. "
    "Performance metrics show {metric} improvements over baseline approaches. "
    "Implementation requires careful consideration of {consideration1} and {consideration2}. "
    "Future directions include {future1} and {future2}. ",
    
    "Practical Applications of {topic}: Real-world use cases demonstrate {usecase}. "
    "Industry adoption has increased by {percentage}% in recent years. "
    "Challenges include {problem1}, {problem2}, and {problem3}. "
    "Best practices recommend {practice1} and {practice2}. ",
]

DESCRIPTIONS = [
    "developing intelligent systems", "automated reasoning and decision making",
    "pattern recognition from data", "extracting insights from information",
    "solving complex computational problems", "mimicking human cognitive functions"
]

APPLICATIONS = [
    "image classification", "text generation", "speech recognition",
    "recommendation systems", "autonomous vehicles", "medical diagnosis",
    "financial forecasting", "sentiment analysis", "machine translation"
]

CHALLENGES = [
    "scalability issues", "interpretability concerns", "data privacy",
    "computational efficiency", "model robustness", "generalization capabilities"
]

PRINCIPLES = [
    "representation learning", "feature extraction", "optimization",
    "regularization", "transfer learning", "ensemble methods",
    "attention mechanisms", "gradient descent", "backpropagation"
]

METHODS = [
    "convolutional architectures", "recurrent networks", "transformer models",
    "attention-based approaches", "self-supervised learning", "meta-learning"
]

METRICS = [
    "accuracy", "precision and recall", "F1-score", "AUC-ROC",
    "inference speed", "memory efficiency", "training time"
]

CONSIDERATIONS = [
    "hyperparameter tuning", "data preprocessing", "model selection",
    "cross-validation", "batch normalization", "dropout regularization"
]

FUTURE_DIRECTIONS = [
    "few-shot learning", "zero-shot generalization", "explainable AI",
    "edge deployment", "continual learning", "multimodal fusion"
]

USECASES = [
    "customer service automation", "content moderation", "fraud detection",
    "personalized recommendations", "predictive maintenance", "quality control"
]

PROBLEMS = [
    "high computational costs", "limited labeled data", "model bias",
    "deployment complexity", "monitoring drift", "versioning management"
]

PRACTICES = [
    "continuous evaluation", "A/B testing", "gradual rollout",
    "comprehensive logging", "model versioning", "regular retraining"
]


def generate_paragraph(topic: str) -> str:
    """Generate a realistic paragraph about a given topic"""
    template = random.choice(TEMPLATES)
    
    return template.format(
        topic=topic,
        description=random.choice(DESCRIPTIONS),
        application=random.choice(APPLICATIONS),
        challenge=random.choice(CHALLENGES),
        principle1=random.choice(PRINCIPLES),
        principle2=random.choice(PRINCIPLES),
        principle3=random.choice(PRINCIPLES),
        method=random.choice(METHODS),
        metric=random.choice(METRICS),
        consideration1=random.choice(CONSIDERATIONS),
        consideration2=random.choice(CONSIDERATIONS),
        future1=random.choice(FUTURE_DIRECTIONS),
        future2=random.choice(FUTURE_DIRECTIONS),
        usecase=random.choice(USECASES),
        percentage=random.randint(15, 85),
        problem1=random.choice(PROBLEMS),
        problem2=random.choice(PROBLEMS),
        problem3=random.choice(PROBLEMS),
        practice1=random.choice(PRACTICES),
        practice2=random.choice(PRACTICES)
    )


def generate_document(doc_id: int, target_size_kb: int = 10) -> str:
    """Generate a document of approximately target_size_kb"""
    topic = random.choice(TOPICS)
    
    # Document header
    content = f"# Document {doc_id}: {topic.title()}\n\n"
    content += f"**Topic**: {topic}\n"
    content += f"**Document ID**: DOC-{doc_id:04d}\n\n"
    content += "## Abstract\n\n"
    content += generate_paragraph(topic) + "\n\n"
    content += "## Main Content\n\n"
    
    # Generate paragraphs until we reach target size
    target_bytes = target_size_kb * 1024
    section_num = 1
    
    while len(content.encode('utf-8')) < target_bytes:
        content += f"### Section {section_num}\n\n"
        
        # Add 2-4 paragraphs per section
        num_paragraphs = random.randint(2, 4)
        for _ in range(num_paragraphs):
            content += generate_paragraph(topic) + "\n\n"
        
        section_num += 1
    
    content += "## Conclusion\n\n"
    content += generate_paragraph(topic) + "\n"
    
    return content


def generate_corpus(output_dir: str, num_documents: int = 100, avg_size_kb: int = 10):
    """
    Generate a corpus of synthetic documents for benchmarking.
    
    Args:
        output_dir: Directory to write documents
        num_documents: Number of documents to generate
        avg_size_kb: Average document size in KB
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {num_documents} synthetic documents in {output_dir}...")
    
    total_size = 0
    for i in range(1, num_documents + 1):
        # Vary document size ±30% around average
        size_variation = random.uniform(0.7, 1.3)
        target_size = int(avg_size_kb * size_variation)
        
        doc_content = generate_document(i, target_size)
        
        # Write document
        file_path = output_path / f"doc_{i:04d}.md"
        file_path.write_text(doc_content, encoding='utf-8')
        
        doc_size = len(doc_content.encode('utf-8'))
        total_size += doc_size
        
        if i % 10 == 0:
            print(f"  Generated {i}/{num_documents} documents...")
    
    avg_actual_size = total_size / num_documents / 1024
    total_size_mb = total_size / (1024 * 1024)
    
    print(f"\nCorpus generation complete!")
    print(f"  Total documents: {num_documents}")
    print(f"  Average document size: {avg_actual_size:.2f} KB")
    print(f"  Total corpus size: {total_size_mb:.2f} MB")
    print(f"  Output directory: {output_dir}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = "tests/benchmark_corpus"
    
    num_docs = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    avg_size = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    generate_corpus(output_dir, num_docs, avg_size)
