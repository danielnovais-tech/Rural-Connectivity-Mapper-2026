# Contributing to Rural Connectivity Mapper 2026
# Contributing to Rural Connectivity Mapper

Thank you for your interest in contributing to the Rural Connectivity Mapper project! We welcome contributions from the community to help improve rural connectivity analysis in Brazil.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue using our [Bug Report template](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues/new/choose). Make sure to include:

- A clear description of the bug
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your environment details (OS, Python version, etc.)
- **Estimated Effort** for fixing the bug

### Suggesting Features

We love new ideas! Please create a [Feature Request](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues/new/choose) with:

- A clear problem statement
- Your proposed solution
- Alternative approaches you've considered
- **Estimated Effort** for implementation
- Priority level

### Submitting Pull Requests

1. **Fork the repository** and create a new branch from `main`
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes** following our coding standards (see below)

3. **Run tests** to ensure everything works
   ```bash
   pytest tests/ -v
   ```

4. **Commit your changes** with clear, descriptive messages
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

5. **Push to your fork** and submit a Pull Request
   ```bash
   git push origin feature/amazing-feature
   ```

## 📏 Estimated Effort Guidelines

To help with planning and task assignment, we use an effort estimation system. When creating issues or planning work, use these guidelines:

### Effort Levels

| Level | Time Range | Description | Examples |
|-------|-----------|-------------|----------|
| **S (Small)** | < 2 hours | Minor fixes, simple updates | Fix typo, update dependency version, add docstring |
| **M (Medium)** | 2-8 hours | Moderate features or fixes | Add new utility function, fix complex bug, improve validation |
| **L (Large)** | > 8 hours (1-3 days) | Significant features or refactoring | New CLI command, major algorithm improvement, comprehensive docs |
| **XL (Extra Large)** | > 1 week | Major features or architecture changes | New data model, web dashboard, ML integration, API development |

### How to Estimate

1. **Break down the task** into smaller subtasks
2. **Consider all aspects**:
   - Writing code
   - Writing tests
   - Writing documentation
   - Code review iterations
   - Testing and validation
3. **Add buffer time** for unforeseen issues (20-30%)
4. **If uncertain**, choose "Unknown" and we'll help estimate

### Effort in Hours (Alternative)

If you prefer hours over S/M/L/XL, you can also estimate in hours:
- List specific tasks and their time estimates
- Include testing, documentation, and review time
- Example: "Implementation: 3h, Tests: 2h, Docs: 1h = Total: 6h (Medium)"

## 💻 Development Guidelines

### Code Style

- Follow **PEP 8** style guide for Python code
- Use **Google-style docstrings** for all functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable and function names

#### Example:

```python
def calculate_quality_score(speed_test: SpeedTest) -> float:
    """Calculate quality score from speed test results.
    
    Args:
        speed_test: SpeedTest instance with measurement data
        
    Returns:
        Quality score from 0 to 100
        
    Example:
        >>> st = SpeedTest(download=150.0, upload=18.0, latency=25.0)
        >>> score = calculate_quality_score(st)
        >>> print(score)
        92.5

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
- **Line length:** Maximum 79 characters for code, 72 for comments (per PEP 8)
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


### Testing Requirements

- **Add tests** for all new features and bug fixes
- Maintain **80%+ code coverage**
- Use `pytest` for all tests
- Test both success and failure cases

#### Running Tests:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_models.py -v
```

### Documentation

- Update **README.md** if adding user-facing features
- Update **docs/API.md** for API changes
- Add inline comments for complex logic
- Include usage examples in docstrings

## 🏗️ Project Structure

Understanding the project structure will help you contribute effectively:

```
Rural-Connectivity-Mapper-2026/
├── main.py                      # CLI application entry point
├── demo_workflow.py             # Complete demo workflow
├── src/
│   ├── models/                  # Data models (SpeedTest, QualityScore, ConnectivityPoint)
│   ├── utils/                   # Utility modules (8 modules)
│   └── data/                    # Sample data and storage
├── tests/                       # Test suite (36 tests)
├── docs/                        # Documentation
└── .github/                     # GitHub templates and workflows
    └── ISSUE_TEMPLATE/          # Issue templates with effort estimation
```

## 🧪 Testing Your Changes

### Local Testing

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the demo workflow** to ensure basic functionality:
   ```bash
   python demo_workflow.py
   ```

3. **Test specific features**:
   ```bash
   python main.py --importar src/data/sample_data.csv
   python main.py --relatorio json
   python main.py --map
   ```

4. **Run the test suite**:
   ```bash
   pytest tests/ -v --cov=src
   ```

## 📋 Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows PEP 8 style guide
- [ ] All tests pass (`pytest tests/ -v`)
- [ ] New code has tests with 80%+ coverage
- [ ] Documentation is updated (README, API docs, docstrings)
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with `main`
- [ ] No unnecessary files committed (use `.gitignore`)

## 🎯 Good First Issues

Looking for a place to start? Check out issues labeled:
- `good first issue` - Perfect for newcomers
- `help wanted` - We'd love assistance on these
- `documentation` - Improve our docs
- Estimated as **S (Small)** - Quick wins!

## 🐛 Found a Security Issue?

Please **do not** create a public issue. Instead, email the maintainer directly with details. Security issues will be addressed with priority.

## 💬 Questions?

- **GitHub Discussions**: [Ask questions](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/discussions)
- **Issues**: [Browse existing issues](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues)
- **Documentation**: [Read the docs](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/blob/main/docs/API.md)

## 📜 Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and professional in all interactions.

## 🙏 Acknowledgments

Thank you for contributing to improve rural connectivity in Brazil! Every contribution, no matter how small, helps advance our mission to support Starlink's 2026 expansion and improve internet access for rural communities.

---

**Happy Contributing! 🇧🇷**

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

Our project follows a clear roadmap (see [README.md](README.md#-roadmap) for details). Please consider how your contribution aligns with:

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

