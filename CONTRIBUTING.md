# Contributing to Rural Connectivity Mapper 2026

Thank you for your interest in contributing to the Rural Connectivity Mapper 2026 project! We welcome contributions from the community to help improve rural connectivity analysis in Brazil.

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
| **L (Large)** | 1-3 days | Significant features or refactoring | New CLI command, major algorithm improvement, comprehensive docs |
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
