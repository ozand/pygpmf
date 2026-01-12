# Contributing to pygpmf-oz

Thank you for your interest in contributing to pygpmf-oz! We welcome contributions from everyone.

## 🎯 How Can I Contribute?

### 1. Testing & Bug Reports 🐛

**Help us test with real GoPro footage!**

We especially need:
- Files from **Hero 11, 12, 13** cameras
- Edge cases (long videos, corrupted files, unusual settings)
- Different video modes (4K, 1080p, high FPS)
- Various activities (cycling, skiing, driving, flying)

**To report a bug**:
1. Check existing [issues](https://github.com/ozand/pygpmf-oz/issues)
2. Create a new issue with:
   - GoPro model & firmware version
   - Python version & OS
   - Minimal code to reproduce
   - Expected vs actual behavior
   - Error messages/stack traces

### 2. Documentation 📚

**Good documentation helps everyone!**

Help needed:
- Fix typos or unclear explanations
- Add code examples
- Write tutorials (blog posts, videos)
- Translate documentation (Russian, Spanish, Chinese, etc.)
- Improve docstrings

**To contribute docs**:
```bash
git checkout -b docs/improve-xyz
# Make your changes
git commit -m "docs: improve XYZ section"
git push origin docs/improve-xyz
# Create Pull Request
```

### 3. Code Contributions 💻

**Before starting:**
1. Check [existing issues](https://github.com/ozand/pygpmf-oz/issues) or [roadmap](DEVELOPMENT_ROADMAP.md)
2. Comment on the issue you want to work on
3. Fork the repository
4. Create a feature branch

**Development setup**:
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/pygpmf.git
cd pygpmf

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks (if available)
# pip install pre-commit
# pre-commit install
```

**Code standards**:
- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for public APIs
- Add tests for new features
- Keep functions small and focused

**Testing**:
```bash
# Run tests
pytest

# With coverage
pytest --cov=gpmf --cov-report=html

# Run specific test
pytest tests/test_gps.py::test_parse_gps_block
```

**Commit messages**:
```
type(scope): brief description

Longer explanation if needed.

Fixes #123
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `style`, `chore`

Examples:
- `feat(gps): add Hero 13 GPS 10Hz support`
- `fix(parser): handle corrupted GPMF streams`
- `docs(readme): update installation instructions`
- `test(gyro): add tests for gyroscope parsing`

### 4. Feature Requests 💡

**Have an idea?**

1. Check [roadmap](DEVELOPMENT_ROADMAP.md) to see if it's planned
2. Search [existing issues](https://github.com/ozand/pygpmf-oz/issues)
3. Create a new issue with:
   - Clear use case
   - Expected behavior
   - Example code (if applicable)
   - Why it's useful

## 🔧 Development Workflow

### Standard Pull Request Process

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/pygpmf.git
   cd pygpmf
   ```

2. **Create Branch**
   ```bash
   git checkout -b feature/my-awesome-feature
   # or
   git checkout -b fix/issue-123
   ```

3. **Make Changes**
   - Write code
   - Add tests
   - Update documentation
   - Run tests locally

4. **Commit**
   ```bash
   git add .
   git commit -m "feat: add awesome feature"
   ```

5. **Push & PR**
   ```bash
   git push origin feature/my-awesome-feature
   ```
   - Go to GitHub and create Pull Request
   - Fill in the PR template
   - Link related issues

6. **Code Review**
   - Address feedback
   - Update PR
   - Wait for approval

7. **Merge**
   - Maintainer will merge when ready
   - Your contribution is live! 🎉

## 📋 Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows PEP 8 style guidelines
- [ ] All tests pass (`pytest`)
- [ ] New features have tests
- [ ] Documentation updated (if needed)
- [ ] Commit messages are clear
- [ ] No unrelated changes included
- [ ] PR description explains the change
- [ ] Linked to relevant issue(s)

## 🎓 Good First Issues

Looking for where to start? Check issues tagged:
- `good first issue` - Easy tasks for newcomers
- `help wanted` - We need help here!
- `documentation` - Docs improvements

## 🌟 Priority Areas (2026)

We're especially interested in:

### Q1 2026 (HIGH PRIORITY)
- **Testing**: Unit tests for all modules
- **Documentation**: Sphinx setup + examples
- **Hero 11-13**: Support for new camera models
- **CI/CD**: GitHub Actions workflow

### Q2 2026 (MEDIUM PRIORITY)
- **GyroFlow**: Integration with video stabilization
- **Export**: Additional formats (GeoJSON, CSV)
- **Performance**: Optimize parsing for large files
- **Examples**: Real-world use case scripts

See [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md) for full details.

## 🐍 Python Version Support

We support Python 3.9-3.13:
- **3.9**: Minimum version
- **3.10-3.12**: Fully tested
- **3.13**: Latest, actively tested

When contributing:
- Don't use features requiring Python 3.10+ (unless absolutely needed)
- Test on multiple Python versions if possible
- Use type hints compatible with Python 3.9

## 📦 Dependencies

**Core dependencies**:
- numpy >= 1.21.0
- pandas >= 1.3.0
- ffmpeg-python >= 0.2.0
- gpxpy >= 1.5.0

**Optional dependencies**:
- geopandas >= 0.12.0 (for mapping)
- matplotlib >= 3.5.0 (for plotting)
- contextily >= 1.3.0 (for map tiles)

**When adding dependencies**:
- Justify the need
- Check license compatibility (MIT/BSD/Apache)
- Consider optional vs required
- Update `setup.py` and `requirements.txt`

## 🔍 Code Review Process

**What reviewers look for**:
1. **Correctness**: Does it work as intended?
2. **Tests**: Are changes tested?
3. **Style**: Follows Python conventions?
4. **Documentation**: Is it documented?
5. **Performance**: Any concerns?
6. **Compatibility**: Works across platforms/versions?

**Typical review time**: 2-7 days

**If review takes longer**:
- Ping maintainers in comments
- Check if additional info needed
- Be patient - we're volunteers!

## 🚫 What We Won't Accept

- Breaking changes without discussion
- Code without tests (for new features)
- Undocumented public APIs
- Copy-pasted code with unclear license
- Large refactors without prior agreement
- Personal attacks or toxic behavior

## 💬 Communication

**GitHub Discussions**: For questions, ideas, help  
**Issues**: For bugs, feature requests  
**Pull Requests**: For code contributions  

**Response time**: Usually 1-3 days for initial response

## 🏆 Recognition

Contributors are recognized in:
- [CHANGELOG.md](CHANGELOG.md) - Credit for each contribution
- README.md - Major contributors listed
- GitHub contributors graph
- Release notes

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Every contribution helps make pygpmf-oz better for everyone. Whether it's:
- Reporting a bug 🐛
- Fixing a typo ✏️
- Adding a feature ✨
- Improving docs 📚
- Sharing feedback 💬

**You're awesome!** ⭐

---

**Questions?** Open a [GitHub Discussion](https://github.com/ozand/pygpmf-oz/discussions) or comment on an issue.

**Need help?** Tag @ozand in comments or open a "help wanted" issue.
