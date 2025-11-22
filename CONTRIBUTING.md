# Contributing to Network Automation CI/CD

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Development Workflow

### 1. Fork and Clone

```bash
git clone https://github.com/Hatren37/Network-Automation-with-CI-CD-Integration.git
cd /Network-Automation-with-CI-CD-Integration
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Set Up Development Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Make Changes

- Follow Python PEP 8 style guidelines
- Add comments and docstrings for new functions
- Update tests when adding new features
- Update documentation as needed

### 5. Test Your Changes

```bash
# Run validation
make validate

# Run tests
make test

# Generate configs
make generate
```

### 6. Commit Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of changes"
```

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Code Style

- Use Python 3.9+ features
- Follow PEP 8 style guide
- Maximum line length: 100 characters
- Use type hints where appropriate
- Add docstrings to all functions and classes

## Testing Guidelines

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage
- Test edge cases and error conditions

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add clear description of changes
4. Reference any related issues
5. Request review from maintainers

## Questions?

Feel free to open an issue for questions or discussions.

