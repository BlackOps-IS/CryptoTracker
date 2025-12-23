# Contributing to CryptoTracker

Thank you for your interest in contributing to CryptoTracker! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach
- Any relevant examples or mockups

### Submitting Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### JavaScript Code Style
- Use ES6+ features
- Use meaningful variable names
- Add comments for complex logic
- Follow consistent formatting

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Examples:
```
Add: address poisoning detection feature
Fix: transaction tracking bug in analyzer
Update: OSINT collection documentation
Refactor: recovery assistant code structure
```

## 🧪 Testing

Before submitting a PR:
1. Test your changes thoroughly
2. Ensure existing tests pass
3. Add new tests for new features
4. Test on multiple browsers (for frontend changes)

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📚 Documentation

- Update README.md if adding new features
- Add docstrings to new functions/classes
- Update API documentation for new endpoints
- Include code examples where helpful

## 🔒 Security

If you discover a security vulnerability:
1. **DO NOT** open a public issue
2. Email us at: security@blackops-is.com
3. Include detailed description and steps to reproduce
4. We'll respond within 48 hours

## 🎯 Priority Areas

We're especially interested in contributions for:
- Multi-chain support (BSC, Polygon, Arbitrum)
- Advanced visualization features
- Machine learning for pattern detection
- Performance optimizations
- Documentation improvements
- Test coverage improvements

## 📋 Pull Request Checklist

Before submitting your PR, ensure:
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] PR description explains changes clearly

## 🌟 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

## 📞 Questions?

If you have questions:
- Open a discussion on GitHub
- Check existing issues and PRs
- Read the documentation

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior:
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated promptly and fairly.

## 🙏 Thank You!

Your contributions make CryptoTracker better for everyone. We appreciate your time and effort!

---

**Happy Contributing! 🚀**