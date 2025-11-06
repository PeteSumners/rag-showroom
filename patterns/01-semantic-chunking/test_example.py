"""
Tests for semantic chunking example

Validates chunking behavior with different inputs and threshold values.
"""

import pytest
from example import SemanticChunker, Chunk


class TestSemanticChunker:
    """Test suite for SemanticChunker"""

    def test_basic_chunking(self):
        """Test that chunking creates multiple chunks from multi-topic text"""
        chunker = SemanticChunker(similarity_threshold=0.3)

        # Text with two distinct topics
        text = """
        Python is a programming language. It was created by Guido van Rossum.
        Python emphasizes code readability and simplicity.

        Quantum computing uses quantum mechanics. Qubits can be in superposition.
        Quantum algorithms solve certain problems exponentially faster.
        """

        chunks = chunker.chunk_document(text)

        # Should create at least 2 chunks (Python topic, Quantum topic)
        assert len(chunks) >= 2
        assert all(isinstance(c, Chunk) for c in chunks)

    def test_single_topic_creates_one_chunk(self):
        """Test that coherent single-topic text stays in one chunk"""
        chunker = SemanticChunker(similarity_threshold=0.2)

        # All sentences about same topic with high keyword overlap
        text = """
        RAG systems use vector search. Vector embeddings enable RAG retrieval.
        RAG combines vectors with generation. Vector databases store RAG embeddings.
        """

        chunks = chunker.chunk_document(text)

        # High overlap should keep it in 1-2 chunks max
        assert len(chunks) <= 2

    def test_empty_input(self):
        """Test handling of empty input"""
        chunker = SemanticChunker()

        chunks = chunker.chunk_document("")

        assert chunks == []

    def test_single_sentence(self):
        """Test handling of single sentence"""
        chunker = SemanticChunker()

        chunks = chunker.chunk_document("This is a single sentence.")

        assert len(chunks) == 1
        assert chunks[0].sentence_count == 1

    def test_threshold_affects_chunk_count(self):
        """Test that lower threshold creates more chunks"""
        text = """
        Machine learning uses algorithms. Deep learning uses neural networks.
        Natural language processing analyzes text. Computer vision processes images.
        """

        # Low threshold = more sensitive to differences = more chunks
        chunker_low = SemanticChunker(similarity_threshold=0.1)
        chunks_low = chunker_low.chunk_document(text)

        # High threshold = less sensitive = fewer chunks
        chunker_high = SemanticChunker(similarity_threshold=0.5)
        chunks_high = chunker_high.chunk_document(text)

        # Lower threshold should create more or equal chunks
        assert len(chunks_low) >= len(chunks_high)

    def test_chunk_properties(self):
        """Test that chunks have correct properties"""
        chunker = SemanticChunker(similarity_threshold=0.3)

        text = "First sentence. Second sentence. Third sentence."
        chunks = chunker.chunk_document(text)

        for chunk in chunks:
            # Check properties exist and are reasonable
            assert chunk.id >= 0
            assert len(chunk.text) > 0
            assert chunk.sentence_count > 0
            assert chunk.char_count > 0
            assert chunk.char_count == len(chunk.text)

    def test_sentence_splitting(self):
        """Test internal sentence splitting"""
        chunker = SemanticChunker()

        # Test various sentence endings
        text = "First sentence. Second sentence! Third sentence? Fourth sentence."
        sentences = chunker._split_sentences(text)

        assert len(sentences) == 4
        assert "First sentence" in sentences[0]
        assert "Second sentence" in sentences[1]

    def test_similarity_calculation(self):
        """Test similarity calculation between sentences"""
        chunker = SemanticChunker()

        # High similarity - shared keywords
        sim_high = chunker._calculate_similarity(
            "Machine learning uses neural networks",
            "Deep learning uses neural networks"
        )

        # Low similarity - different topics
        sim_low = chunker._calculate_similarity(
            "Machine learning uses neural networks",
            "The weather is sunny today"
        )

        assert sim_high > sim_low
        assert 0 <= sim_high <= 1
        assert 0 <= sim_low <= 1

    def test_identical_sentences_have_high_similarity(self):
        """Test that identical sentences have similarity of 1.0"""
        chunker = SemanticChunker()

        sim = chunker._calculate_similarity(
            "The quick brown fox",
            "The quick brown fox"
        )

        assert sim == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
