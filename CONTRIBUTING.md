# Contributing to Rural Connectivity Mapper 2026

Thank you for your interest in contributing to the Rural Connectivity Mapper 2026! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Pull Request Process](#pull-request-process)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How Can I Contribute?

### Reporting Bugs

- Use the [GitHub Issues](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues) page
- Search existing issues to avoid duplicates
- Provide detailed reproduction steps
- Include your environment details (Python version, OS, etc.)

### Suggesting Enhancements

- Check the [project roadmap](README.md#-roadmap) first
- Open a GitHub issue with the `enhancement` label
- Clearly describe the proposed feature and its benefits
- Explain how it aligns with the project's goals

### Contributing Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following our coding standards
4. Write or update tests
5. Run the full test suite
6. Commit your changes with clear messages
7. Push to your fork
8. Submit a Pull Request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/Rural-Connectivity-Mapper-2026.git
cd Rural-Connectivity-Mapper-2026

# Add upstream remote
git remote add upstream https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026.git

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install pytest pytest-cov
```

### Running the Application

```bash
# Run demo workflow
python demo_workflow.py

# Run CLI
python main.py --help
```

## Coding Standards

### Python Style Guide

- **Follow PEP 8** - Use consistent Python style conventions
- **Line length:** Maximum 100 characters (120 for comments)
- **Indentation:** 4 spaces (no tabs)
- **Naming conventions:**
  - Classes: `PascalCase`
  - Functions/variables: `snake_case`
  - Constants: `UPPER_CASE`

### Documentation

- **Docstrings:** Use Google-style docstrings for all public functions and classes

Example:
```python
def calculate_quality_score(download: float, upload: float, latency: float) -> float:
    """Calculate overall connectivity quality score.
    
    Args:
        download: Download speed in Mbps
        upload: Upload speed in Mbps
        latency: Latency in milliseconds
        
    Returns:
        Quality score from 0-100
        
    Raises:
        ValueError: If any input is negative
    """
    # Implementation here
    pass
```

### Code Organization

- Keep functions focused and single-purpose
- Maximum function length: ~50 lines
- Extract complex logic into helper functions
- Use meaningful variable and function names

### Comments

- Write self-documenting code when possible
- Add comments for complex algorithms or business logic
- Avoid obvious comments

## Pull Request Process

### Before Submitting

1. **Update documentation** - Ensure README, API.md, and docstrings are current
2. **Run tests** - All tests must pass
   ```bash
   pytest tests/ -v
   ```
3. **Check code coverage** - Aim for 80%+ coverage
   ```bash
   pytest tests/ --cov=src --cov-report=html
   ```
4. **Lint your code** - Ensure PEP 8 compliance (use tools like `pylint`, `flake8`, or `black`)

### PR Template

When you submit a PR, you'll be asked to provide:

- **Impact:** Scope and nature of changes
- **User Benefit:** How it helps end users
- **Business Value:** Strategic or economic value
- **Roadmap Alignment:** How it fits the project roadmap (v1.1.0, v1.2.0, v2.0.0)
- **Testing:** Evidence that changes work correctly

### Review Process

1. At least one maintainer must approve your PR
2. All CI checks must pass (when implemented)
3. Address review feedback promptly
4. Keep PRs focused - one feature/fix per PR
5. Maintainers may request changes or additional tests

### Merge Criteria

- Code follows style guidelines
- Tests pass and coverage is maintained
- Documentation is updated
- No merge conflicts
- Approved by maintainer(s)

## Testing Guidelines

### Writing Tests

- Place tests in the `tests/` directory
- Name test files: `test_<module_name>.py`
- Name test functions: `test_<function_name>_<scenario>`
- Use descriptive test names that explain what is being tested

Example:
```python
def test_calculate_quality_score_excellent_connection():
    """Test quality score calculation for excellent connection metrics."""
    score = calculate_quality_score(download=150, upload=20, latency=25)
    assert score >= 80  # Excellent tier
```

### Test Coverage

- Aim for 80%+ code coverage
- Test edge cases and error conditions
- Include integration tests for critical workflows
- Mock external dependencies (speedtest, geocoding APIs)

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_models.py::test_connectivity_point_creation -v
```

## Documentation

### README Updates

Update the README.md when:
- Adding new features
- Changing CLI commands
- Modifying installation steps
- Updating dependencies

### API Documentation

Update `docs/API.md` when:
- Adding new public functions/classes
- Changing function signatures
- Modifying return values or exceptions

### Changelog

For significant changes, consider adding an entry to the project's release notes or changelog (if one exists).

## Roadmap Alignment

Our project follows a clear roadmap. Please consider how your contribution aligns with:

### v1.1.0 (Q1 2026)
- Real-time speedtest integration
- SQLite database backend
- GitHub Actions CI/CD
- Docker containerization

### v1.2.0 (Q2 2026)
- Web dashboard (Flask/Streamlit)
- REST API endpoints
- Machine learning predictions
- GeoJSON/KML export

### v2.0.0 (H2 2026)
- Multi-language support (Portuguese/English)
- Mobile app for field data collection
- Advanced analytics (churn prediction)
- Integration with Starlink APIs

If your contribution doesn't align with the roadmap, explain in your PR why it's still valuable.

## Questions?

- Open an issue for questions
- Use [GitHub Discussions](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/discussions) for general discussions
- Check existing documentation first

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers this project.

---

**Thank you for contributing to Rural Connectivity Mapper 2026!** 🌍🚀

Together, we're helping to improve rural internet connectivity across Brazil and supporting Starlink's 2026 roadmap.
