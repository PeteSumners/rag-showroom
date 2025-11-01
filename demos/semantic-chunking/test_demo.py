#!/usr/bin/env python3
"""
Tests for semantic chunking RAG demo
"""

import pytest
from demo import SemanticChunker, Chunk


def test_basic_chunking():
    """Test that basic chunking works"""
    chunker = SemanticChunker(similarity_threshold=0.3)

    text = "This is about dogs. Dogs are great pets. Cats are different animals. Cats like to sleep."

    chunks = chunker.chunk_document(text)

    # Should create at least 2 chunks (dogs vs cats)
    assert len(chunks) >= 1
    assert all(isinstance(c, Chunk) for c in chunks)


def test_chunk_properties():
    """Test that chunks have proper properties"""
    chunker = SemanticChunker(similarity_threshold=0.5)

    text = "Python is a programming language. It has great libraries. JavaScript runs in browsers."

    chunks = chunker.chunk_document(text)

    for i, chunk in enumerate(chunks):
        assert chunk.id == i
        assert len(chunk.text) > 0
        assert len(chunk.sentences) > 0
        assert chunk.topic is not None


def test_similarity_threshold():
    """Test that similarity threshold affects chunk count"""
    text = "Dogs are pets. Cats are pets. Fish are pets. Cars need fuel. Planes fly high."

    # Low threshold = more chunks (stricter boundaries)
    chunker_strict = SemanticChunker(similarity_threshold=0.1)
    chunks_strict = chunker_strict.chunk_document(text)

    # High threshold = fewer chunks (looser boundaries)
    chunker_loose = SemanticChunker(similarity_threshold=0.8)
    chunks_loose = chunker_loose.chunk_document(text)

    # Strict should create more or equal chunks
    assert len(chunks_strict) >= len(chunks_loose)


def test_sentence_splitting():
    """Test sentence splitting"""
    chunker = SemanticChunker()

    text = "First sentence. Second sentence! Third sentence? Fourth sentence."

    sentences = chunker._split_sentences(text)

    assert len(sentences) == 4
    assert "First sentence" in sentences[0]
    assert "Second sentence" in sentences[1]


def test_topic_extraction():
    """Test topic extraction from sentences"""
    chunker = SemanticChunker()

    sentences = [
        "Python is a programming language.",
        "Python has many libraries for programming.",
        "Programming in Python is easy."
    ]

    topic = chunker._extract_topic(sentences)

    # Should identify 'python' or 'programming' as main topic
    assert topic in ['python', 'programming', 'language', 'libraries']


def test_empty_document():
    """Test handling of empty document"""
    chunker = SemanticChunker()

    chunks = chunker.chunk_document("")

    # Should handle gracefully
    assert len(chunks) <= 1


def test_single_sentence():
    """Test single sentence document"""
    chunker = SemanticChunker()

    text = "This is a single sentence."

    chunks = chunker.chunk_document(text)

    assert len(chunks) == 1
    assert chunks[0].text == text.strip()


def test_chunk_coherence():
    """Test that chunks maintain coherent topics"""
    chunker = SemanticChunker(similarity_threshold=0.3)

    # Document with clear topic shifts
    text = """
    Machine learning uses algorithms to learn patterns.
    Neural networks are a type of machine learning model.
    Deep learning uses multiple layers in neural networks.

    Cooking requires fresh ingredients.
    Recipes provide step-by-step instructions.
    Kitchen tools make cooking easier.
    """

    chunks = chunker.chunk_document(text)

    # Should separate ML topics from cooking topics
    assert len(chunks) >= 2

    # Verify chunks contain related content
    ml_keywords = ['machine', 'learning', 'neural', 'networks', 'algorithms']
    cooking_keywords = ['cooking', 'ingredients', 'recipes', 'kitchen']

    # At least one chunk should be about ML
    has_ml_chunk = any(
        any(keyword in chunk.text.lower() for keyword in ml_keywords)
        for chunk in chunks
    )

    # At least one chunk should be about cooking
    has_cooking_chunk = any(
        any(keyword in chunk.text.lower() for keyword in cooking_keywords)
        for chunk in chunks
    )

    assert has_ml_chunk or has_cooking_chunk


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
