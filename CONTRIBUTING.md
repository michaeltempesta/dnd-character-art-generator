# Contributing to D&D Character Art Generator

Thank you for your interest in contributing to the D&D Character Art Generator! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:
1. Check if the issue already exists
2. Search through closed issues for similar problems
3. Provide detailed information about the problem

**Bug Reports should include:**
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Screenshots or error messages
- Browser/OS information

**Feature Requests should include:**
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if applicable)
- Examples or mockups

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run the test suite**
   ```bash
   npm test
   npm run lint
   npm run type-check
   ```
6. **Commit your changes** using conventional commits
7. **Push to your fork**
8. **Create a Pull Request**

## 📋 Development Guidelines

### Code Style

- **TypeScript**: Use strict typing
- **ESLint**: Follow the configured rules
- **Prettier**: Code formatting is enforced
- **Conventional Commits**: Use standardized commit messages

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build process or auxiliary tool changes

**Examples:**
```
feat(pdf-parser): add support for multiclass characters
fix(ui): resolve PDF upload modal positioning
docs(api): update PDF parser documentation
```

### Testing Requirements

- **Unit Tests**: Required for new features
- **Integration Tests**: Required for PDF parsing
- **E2E Tests**: Required for user workflows
- **Performance Tests**: Required for PDF parsing features

### Code Review Process

1. **Automated Checks**: All PRs must pass CI checks
2. **Code Review**: At least one approval required
3. **Testing**: All tests must pass
4. **Documentation**: Update docs for new features

## 🛠️ Development Setup

### Prerequisites

- Node.js 18+
- npm or yarn
- Git

### Local Development

1. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/dnd-character-art-generator.git
   cd dnd-character-art-generator
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Add your Hugging Face API token
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

### Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run linting
npm run lint

# Run type checking
npm run type-check

# Run all checks
npm run check
```

## 📚 Project Structure

```
src/
├── components/          # React components
│   ├── DndBeyondPDFUpload.tsx
│   ├── CharacterForm.tsx
│   └── ArtGenerator.tsx
├── services/           # Business logic
│   ├── realFormFieldParser.ts
│   ├── dndBeyondAPI.ts
│   └── vttIntegration.ts
├── types/              # TypeScript definitions
├── styles/             # CSS styles
├── utils/              # Utility functions
└── tests/              # Test files
```

## 🎯 Areas for Contribution

### High Priority

- **PDF Parser Improvements**: Better character data extraction
- **Error Handling**: More robust error recovery
- **Performance**: Faster PDF parsing
- **Testing**: More comprehensive test coverage

### Medium Priority

- **UI/UX**: Better user experience
- **Documentation**: More detailed guides
- **Accessibility**: Better accessibility support
- **Mobile**: Mobile-friendly interface

### Low Priority

- **Internationalization**: Multi-language support
- **Themes**: Additional UI themes
- **Plugins**: Plugin system for extensions

## 🐛 Bug Fixing

### Common Issues

**PDF Parsing Issues**
- Check browser console for errors
- Verify PDF is from D&D Beyond
- Test with different PDF export settings

**VTT Integration Issues**
- Verify VTT is running
- Check firewall settings
- Ensure correct module installation

**AI Art Generation Issues**
- Verify API token is valid
- Check rate limits
- Ensure stable internet connection

### Debugging

```bash
# Enable debug logging
VITE_DEBUG_LOGGING=true npm run dev

# Run with verbose output
npm run dev -- --verbose

# Check for TypeScript errors
npm run type-check
```

## 📖 Documentation

### Writing Documentation

- **Clear and concise**: Easy to understand
- **Examples**: Include code examples
- **Up-to-date**: Keep documentation current
- **Comprehensive**: Cover all features

### Documentation Types

- **API Documentation**: Function and class documentation
- **User Guides**: How-to guides for users
- **Developer Guides**: Technical implementation details
- **Troubleshooting**: Common issues and solutions

## 🚀 Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Release notes written

## 💬 Communication

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Discord**: For real-time chat (if available)

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's values

## 🎉 Recognition

Contributors will be recognized in:
- **README.md**: Listed as contributors
- **Release Notes**: Mentioned in releases
- **Documentation**: Credited for contributions

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to the D&D Character Art Generator!** 🎲✨
