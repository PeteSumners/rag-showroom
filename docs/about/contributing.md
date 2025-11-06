# Contributing

We love contributions! Whether it's a new pattern, bug fix, or documentation improvement, your help makes this guide better for everyone.

## Ways to Contribute

### 1. Add a New Pattern

Have a RAG pattern to share? We'd love to include it!

**Requirements:**
- Clear conceptual explanation
- Working code example with colored terminal output
- Test cases
- Real-world use case and impact data
- Trade-offs analysis

**Structure:**
```
patterns/XX-pattern-name/
├── README.md        # Conceptual guide
├── example.py       # Working demo
└── test_example.py  # Tests
```

See existing patterns for examples.

### 2. Improve Documentation

- Fix typos
- Add clarifications
- Improve examples
- Add diagrams

### 3. Enhance Examples

- Better sample data
- More realistic scenarios
- Additional visualizations
- Performance improvements

### 4. Fix Bugs

Found something broken? Please:
1. Open an issue describing the problem
2. Submit a PR with a fix
3. Include tests if applicable

## Getting Started

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/rag-patterns-guide.git
cd rag-patterns-guide
```

### 2. Create Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

```bash
# Edit files
# Test your changes
python patterns/your-pattern/example.py

# Run tests
pytest patterns/your-pattern/test_example.py -v
```

### 4. Commit

```bash
git add .
git commit -m "feat: add query expansion pattern"
```

Use conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring

### 5. Push and PR

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub!

## Pattern Contribution Checklist

When adding a new pattern, ensure:

- [ ] README.md with full explanation
- [ ] Working example.py with terminal output
- [ ] test_example.py with at least 5 test cases
- [ ] Mermaid architecture diagram
- [ ] Trade-offs comparison table
- [ ] Real-world case study or impact data
- [ ] "When to use" and "When NOT to use" sections
- [ ] Links to further reading (papers, docs)
- [ ] Code follows existing style (rich library, color scheme)
- [ ] Pattern added to main README.md
- [ ] Documentation page created in docs/patterns/

## Code Style

### Terminal Output

Use consistent color scheme:
- **Cyan** - Input
- **Green** - Results
- **Yellow** - Statistics/insights
- **Red** - Baseline/comparisons

```python
console.print("[bold cyan]>>> INPUT[/bold cyan]")
console.print("[bold green]>>> RESULTS[/bold green]")
console.print("[bold yellow]>>> STATISTICS[/bold yellow]")
console.print("[bold red]>>> BASELINE[/bold red]")
```

### Code Comments

Explain **why**, not **what**:

```python
# Good
# Use Jaccard similarity as a simple proxy for semantic similarity.
# Production systems should use actual embeddings (OpenAI, sentence-transformers).

# Not as good
# Calculate similarity between two sentences
```

### Engineering Decisions

Include comments explaining engineering decisions:

```python
def retrieve(self, query: str) -> List[Document]:
    """
    Retrieve documents.

    Engineering decision: Apply metadata filters BEFORE vector search
    to reduce search space and enforce hard constraints.
    """
```

## Testing

All new patterns must include tests:

```python
def test_basic_functionality():
    """Test that the pattern works as expected"""
    # Arrange
    data = create_test_data()

    # Act
    result = pattern.process(data)

    # Assert
    assert len(result) > 0
    assert all(isinstance(r, Document) for r in result)
```

Run tests before submitting:

```bash
pytest patterns/your-pattern/test_example.py -v
```

## Documentation

When adding docs pages:

1. Use markdown admonitions for callouts:
```markdown
!!! tip "Key Insight"
    Your insight here

!!! warning "Caution"
    Important warning

!!! example "Case Study"
    Real-world example
```

2. Include mermaid diagrams for architecture
3. Show terminal output in code blocks
4. Link to related patterns

## Questions?

- Open a [Discussion](https://github.com/yourusername/rag-patterns-guide/discussions)
- Ask in the [Issues](https://github.com/yourusername/rag-patterns-guide/issues)
- Reach out on [LinkedIn](https://linkedin.com/in/yourprofile)

## Code of Conduct

Be respectful, constructive, and kind. We're all here to learn!

---

**Thank you for contributing!** 🎉
