# Contributing to BrandGen

Thank you for your interest in contributing to BrandGen! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

- Use the bug report template when creating issues
- Include detailed steps to reproduce
- Provide environment information
- Add screenshots if applicable

### Suggesting Features

- Use the feature request template
- Describe the use case clearly
- Explain the expected benefit
- Consider implementation complexity

### Code Contributions

#### Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/BrandGen-PRO.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Set up development environment: `python setup.py`

#### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

#### Code Style

```python
# Use type hints
def generate_image(prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
    """
    Generate an image using DALL-E API.

    Args:
        prompt: The text prompt for image generation
        size: Image dimensions (default: "1024x1024")

    Returns:
        Dictionary containing image data and metadata
    """
    pass
```

#### Testing

- Run tests: `pytest tests/`
- Ensure all tests pass
- Add tests for new functionality
- Maintain test coverage above 80%

#### Submitting Changes

1. Commit your changes: `git commit -m "Add feature: description"`
2. Push to your fork: `git push origin feature/your-feature-name`
3. Create a Pull Request
4. Fill out the PR template completely
5. Wait for review and address feedback

### Pull Request Guidelines

- Create focused PRs (one feature/fix per PR)
- Write clear commit messages
- Update documentation
- Add tests for new features
- Ensure CI passes

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/BrandGen-PRO.git
cd BrandGen-PRO

# Set up environment
python setup.py

# Install development dependencies
pip install pytest pytest-cov flake8 black

# Create .env file
cp .env.template .env
# Add your OpenAI API key to .env

# Run tests
pytest

# Run linting
flake8 src/

# Format code
black src/
```

### Code Review Process

1. All PRs require at least one review
2. Address reviewer feedback promptly
3. Keep PRs up to date with main branch
4. Squash commits before merging

### Community Guidelines

- Be respectful and constructive
- Help others learn and grow
- Follow the code of conduct
- Ask questions if you're unsure

### Getting Help

- Check existing issues and documentation
- Ask questions in GitHub Discussions
- Join our community channels
- Contact maintainers if needed

## Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for helping make BrandGen better! 🎨✨
