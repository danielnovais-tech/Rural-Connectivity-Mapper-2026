# Contributing to Rural Connectivity Mapper 2026

Thank you for your interest in contributing to the Rural Connectivity Mapper 2026! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- pip package manager

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Rural-Connectivity-Mapper-2026.git
   cd Rural-Connectivity-Mapper-2026
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Verify Setup**
   ```bash
   pytest tests/ -v
   ```

## 📋 Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/amazing-feature
# or
git checkout -b fix/bug-description
```

### 2. Make Changes
- Write clean, documented code
- Follow existing code style and conventions
- Add docstrings (Google-style) to functions and classes

### 3. Write Tests
- Add tests for new features
- Ensure existing tests still pass
- Aim for 80%+ code coverage

```bash
# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=src --cov-report=term-missing
```

### 4. Run Linters
```bash
# Ruff (fast Python linter)
ruff check .

# Flake8 (code style checker)
flake8 src/ tests/ main.py demo_workflow.py
```

### 5. Commit Changes
```bash
git add .
git commit -m "feat: add amazing feature"
```

**Commit Message Format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/modifications
- `refactor:` - Code refactoring
- `style:` - Formatting changes
- `chore:` - Maintenance tasks

### 6. Push and Create Pull Request
```bash
git push origin feature/amazing-feature
```

Then create a Pull Request on GitHub.

## 🧪 Testing Guidelines

### Writing Tests
- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names that explain what is being tested

### Test Structure
```python
def test_feature_description():
    """Brief description of what this test verifies."""
    # Arrange - Set up test data
    input_data = {...}
    
    # Act - Execute the function
    result = function_to_test(input_data)
    
    # Assert - Verify the result
    assert result == expected_value
```

### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_models.py -v

# Specific test
pytest tests/test_models.py::test_connectivity_point_creation -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## 🎨 Code Style Guidelines

### Python Style
- Follow PEP 8 style guide
- Maximum line length: 120 characters
- Use meaningful variable and function names
- Add type hints where appropriate

### Documentation
- All public functions must have docstrings
- Use Google-style docstrings
- Include examples for complex functions

Example:
```python
def calculate_quality_score(download: float, upload: float, latency: float) -> float:
    """Calculate connectivity quality score.
    
    Args:
        download: Download speed in Mbps
        upload: Upload speed in Mbps
        latency: Latency in milliseconds
    
    Returns:
        Quality score from 0-100
    
    Examples:
        >>> calculate_quality_score(100, 20, 30)
        85.5
    """
    # Implementation here
```

### Imports
- Group imports: standard library, third-party, local
- Use absolute imports
- Sort imports alphabetically within groups

## 🔄 CI/CD Pipeline

### Automated Checks
All pull requests automatically run:
1. **Tests** - Across Python 3.8, 3.9, 3.10, 3.11, 3.12
2. **Linting** - Ruff and Flake8 code quality checks
3. **Coverage** - Code coverage analysis

### What Happens When You Submit a PR
1. CI workflow runs tests on multiple Python versions
2. Lint workflow checks code quality
3. Coverage report is generated
4. Results are shown in the PR

### Local CI Simulation
Run these before pushing to catch issues early:
```bash
# Full test suite
pytest tests/ -v --cov=src

# Linting
ruff check .
flake8 src/ tests/ main.py demo_workflow.py

# Both together
pytest tests/ -v --cov=src && ruff check . && flake8 src/ tests/
```

## 📝 Pull Request Guidelines

### Before Submitting
- ✅ All tests pass locally
- ✅ No linting errors
- ✅ Code coverage maintained or improved
- ✅ Documentation updated if needed
- ✅ CHANGELOG updated (if applicable)

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (describe)

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Coverage maintained/improved

## Checklist
- [ ] Code follows PEP 8 style
- [ ] Docstrings added/updated
- [ ] No linting errors
- [ ] README updated if needed
```

## 🐛 Reporting Bugs

### Bug Report Template
```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. ...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.12]
- Package version: [e.g., 1.0.0]

**Additional Context**
Any other relevant information
```

## 💡 Feature Requests

We welcome feature requests! Please:
1. Check existing issues first
2. Provide clear use case
3. Explain expected behavior
4. Consider implementation approach

## 📚 Resources

- [PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

## ❓ Questions?

- Open a [Discussion](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/discussions)
- File an [Issue](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to improving rural connectivity in Brazil! 🇧🇷**
