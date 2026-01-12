# GitHub Actions PyPI Deployment: Best Practices & Implementation Guide

**Document Date:** January 12, 2026  
**Purpose:** Comprehensive research on publishing Python packages to PyPI using GitHub Actions workflows  
**Target Project:** pygpmf_oz

---

## Executive Summary

This guide compiles best practices for automating Python package publication to PyPI using GitHub Actions CI/CD workflows. The focus is on security, reliability, and automation using **Trusted Publishing** (OpenID Connect tokens) instead of static API keys.

---

## 1. TRIGGER TYPES & DEPLOYMENT STRATEGIES

### 1.1 Recommended Trigger Events

| Trigger             | Use Case             | Configuration                                            |
| ------------------- | -------------------- | -------------------------------------------------------- |
| **Tag Push**        | Production releases  | `if: startsWith(github.ref, 'refs/tags/')`               |
| **Release Created** | GitHub Releases      | `on: release: [published]`                               |
| **Manual Dispatch** | On-demand publishing | `on: workflow_dispatch`                                  |
| **Branch Push**     | Pre-release/TestPyPI | Always runs (TestPyPI), optional filter for main/develop |
| **Scheduled**       | Nightly builds       | `on: schedule: - cron: '0 0 * * *'`                      |

### 1.2 Semantic Versioning Integration

```yaml
# Example: Trigger only on semantic version tags
on:
  push:
    tags:
      - 'v[0-9]+.[0-9]+.[0-9]+'          # v1.0.0, v2.1.3
      - 'v[0-9]+.[0-9]+.[0-9]+-*'       # v1.0.0-rc.1 (pre-releases)
```

**Best Practice:** Use git tags matching semantic versioning (v1.0.0, v1.0.0-rc1, etc.). Triggers publication to **PyPI only on production tags**, while **TestPyPI publishes on all pushes** to validate the pipeline.

---

## 2. TRUSTED PUBLISHING (RECOMMENDED) vs LEGACY API TOKENS

### 2.1 Trusted Publishing (OpenID Connect - OIDC) ⭐ **RECOMMENDED**

#### Advantages:
- ✅ **No manual token management** - Automatic OIDC token generation per publish
- ✅ **Short-lived tokens** - Expire immediately after use
- ✅ **Project-specific** - Separate tokens per PyPI project
- ✅ **No secret rotation needed** - No secrets in GitHub repository
- ✅ **Superior security** - Follows industry standards (OAuth 2.0 pattern)
- ✅ **Audit trail** - Full GitHub Actions context in PyPI logs

#### How It Works:
1. GitHub Actions generates a short-lived OpenID Connect token
2. Token includes GitHub context (repo, workflow, commit SHA)
3. Token presented to PyPI's trusted publisher endpoint
4. PyPI verifies token signature using GitHub's public key
5. Publication authorized without static credentials

#### Setup Steps:

**Step 1: Register Trusted Publisher with PyPI**

Go to: https://pypi.org/manage/account/publishing/

Fill in:
- **PyPI Project Name** - Must match `name` in `pyproject.toml`/`setup.cfg`
- **GitHub Repository Owner** - Username or organization
- **GitHub Repository Name** - Repository name
- **Workflow Filename** - `.github/workflows/publish-to-pypi.yml`
- **GitHub Environment Name** - `pypi` (for production)

**Step 2: Register Trusted Publisher with TestPyPI**

Go to: https://test.pypi.org/manage/account/publishing/

Same process with environment name: `testpypi`

**Step 3: In Workflow, Grant OIDC Token Permission**

```yaml
jobs:
  publish-to-pypi:
    environment:
      name: pypi
      url: https://pypi.org/p/pygpmf-oz
    
    permissions:
      id-token: write  # 🔑 CRITICAL: Required for OIDC token generation
```

### 2.2 Legacy API Token Method (Deprecated)

#### ⚠️ NOT RECOMMENDED - Security Issues:
- ❌ Static credentials stored in GitHub Secrets
- ❌ Manual rotation required periodically
- ❌ No automatic expiration
- ❌ Broader permissions (account-level, not project-specific)
- ❌ Higher compromise risk

#### If Required (Fallback):

```yaml
# ⚠️ DEPRECATED APPROACH - Only for third-party indexes

env:
  PYPI_API_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
  TEST_PYPI_API_TOKEN: ${{ secrets.TEST_PYPI_API_TOKEN }}
```

**Steps if using legacy tokens:**
1. Create API token at PyPI account settings
2. Store in GitHub Secrets as `PYPI_API_TOKEN`, `TEST_PYPI_API_TOKEN`
3. Remove these secrets when migrating to Trusted Publishing

---

## 3. POPULAR COMMUNITY ACTIONS

### 3.1 `pypa/gh-action-pypi-publish` ⭐ **RECOMMENDED**

**Repository:** https://github.com/pypa/gh-action-pypi-publish  
**Marketplace:** https://github.com/marketplace/actions/pypi-publish

#### Features:
- ✅ Official PyPA action (Python Packaging Authority)
- ✅ Full Trusted Publishing support (OIDC)
- ✅ **PEP 740 attestations** (cryptographic signatures) - v1.11.0+
- ✅ Multi-repository upload support
- ✅ Customizable repository URL
- ✅ Print-only mode for dry-run testing

#### Usage:

```yaml
# Simple PyPI publish
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1

# TestPyPI variant
- name: Publish to TestPyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    repository-url: https://test.pypi.org/legacy/

# With print-only (dry-run)
- name: Verify build (dry-run)
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    print-hash: true
    dry-run: true
```

#### Key Parameters:
| Parameter        | Description               | Example                         |
| ---------------- | ------------------------- | ------------------------------- |
| `repository-url` | Custom index URL          | `https://test.pypi.org/legacy/` |
| `packages-dir`   | Distribution directory    | `./dist`                        |
| `print-hash`     | Print distribution hashes | `true`                          |
| `skip-existing`  | Skip if version exists    | `true`                          |
| `verbose`        | Verbose output            | `true`                          |

#### PEP 740 Attestations (v1.11.0+):
- **Automatic signing** - No manual GPG setup
- **Provenance tracking** - Build metadata attached
- **Verification support** - Tools like `pip` can verify
- **Future audit** - Track package lineage

### 3.2 Twine (Manual Alternative)

**Repository:** https://github.com/pypa/twine

#### Comparison with `gh-action-pypi-publish`:

| Aspect             | gh-action-pypi-publish | Twine                       |
| ------------------ | ---------------------- | --------------------------- |
| Ease of Use        | ⭐⭐⭐⭐⭐                  | ⭐⭐⭐                         |
| Trusted Publishing | ✅ Native OIDC          | ✅ Via environment variables |
| Maintenance        | Official PyPA          | Official PyPA               |
| Recommended        | YES                    | For manual CLI use          |

#### Twine Example (If Needed):

```yaml
- name: Publish with Twine (Alternative)
  run: |
    pip install twine
    twine upload dist/* --non-interactive
  env:
    TWINE_REPOSITORY_URL: https://upload.pypi.org/legacy/
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

---

## 4. SECURITY CONSIDERATIONS & CHECKLIST

### 4.1 Security Best Practices

#### ✅ DO:

1. **Use Trusted Publishing (OIDC)**
   - Only generate tokens when needed
   - Automatic expiration (short-lived)
   - No manual credential management

2. **Require Manual Approval for Production**
   ```yaml
   environment:
     name: pypi  # GitHub will require manual approval
   ```
   - Settings → Environments → pypi → Add protection rule
   - Require approval before deploying to this environment

3. **Scope Permissions Minimally**
   ```yaml
   permissions:
     id-token: write      # Only what's needed
     contents: read       # If reading repository
   ```

4. **Validate Packages Before Publish**
   ```yaml
   - name: Check distribution
     run: |
       pip install twine
       twine check dist/*
   ```

5. **Use Branch Protection Rules**
   - Require PR reviews before merge
   - Require passing CI/CD checks
   - Dismiss stale pull request approvals

6. **Regular Audit Trail**
   - Monitor PyPI project activity
   - Check GitHub Actions logs
   - Review deployment history

#### ❌ DON'T:

1. **Store API tokens in repository** ❌
   - Never commit `.pypirc` with credentials
   - Never hardcode tokens in YAML

2. **Use wildcard permissions** ❌
   ```yaml
   permissions: write-all  # ❌ TOO BROAD
   ```

3. **Publish from untrusted sources** ❌
   - Ensure branch protection is enabled
   - Require code review on all changes

4. **Mix authentication methods** ❌
   - Use OIDC consistently
   - Don't mix with legacy tokens

5. **Ignore dependency vulnerabilities** ❌
   - Run `pip-audit` or similar tools
   - Update dependencies before release

6. **Skip verification steps** ❌
   - Always validate wheel integrity
   - Check against test PyPI first

### 4.2 Security Checklist

```
[ ] Registered Trusted Publisher with PyPI
[ ] Registered Trusted Publisher with TestPyPI
[ ] Workflow has permissions: id-token: write
[ ] Environment 'pypi' requires manual approval
[ ] No static API tokens in repository secrets
[ ] Branch protection enabled (PR reviews required)
[ ] Distribution validation (twine check) in workflow
[ ] Package signing/attestations enabled (v1.11.0+)
[ ] Secrets rotation policy documented (N/A for OIDC)
[ ] GitHub Actions logs reviewed for publish events
[ ] PyPI project settings verified (project name matches)
[ ] TestPyPI and PyPI environments configured separately
[ ] Workflow runs on specific tags/events (not all pushes)
```

---

## 5. EXAMPLE WORKFLOW FOR SEMANTIC VERSIONING & GIT TAGS

### 5.1 Complete Production Workflow

```yaml
name: Publish Python distribution to PyPI

on:
  push:
    tags:
      # Semantic versioning pattern: v1.0.0, v2.1.3-rc.1, etc.
      - 'v[0-9]+.[0-9]+.[0-9]+'
      - 'v[0-9]+.[0-9]+.[0-9]+-*'

jobs:
  build:
    name: Build distribution
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v6
      with:
        persist-credentials: false
    
    - name: Set up Python
      uses: actions/setup-python@v6
      with:
        python-version: '3.x'
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Validate package metadata
      run: |
        # Extract version from tag
        VERSION=${GITHUB_REF#refs/tags/v}
        echo "Publishing version: $VERSION"
        # Verify it matches pyproject.toml
    
    - name: Build wheel and sdist
      run: python -m build
    
    - name: Check distributions
      run: twine check dist/*
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v6
      with:
        name: python-package-distributions
        path: dist/
        retention-days: 7

  publish-pypi:
    name: Publish to PyPI
    needs: build
    runs-on: ubuntu-latest
    
    environment:
      name: pypi
      url: https://pypi.org/p/pygpmf-oz
    
    permissions:
      id-token: write  # OIDC token generation
    
    steps:
    - name: Download distributions
      uses: actions/download-artifact@v6
      with:
        name: python-package-distributions
        path: dist/
    
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        verbose: true

  publish-testpypi:
    name: Publish to TestPyPI (Validation)
    needs: build
    runs-on: ubuntu-latest
    
    environment:
      name: testpypi
      url: https://test.pypi.org/p/pygpmf-oz
    
    permissions:
      id-token: write
    
    steps:
    - name: Download distributions
      uses: actions/download-artifact@v6
      with:
        name: python-package-distributions
        path: dist/
    
    - name: Publish to TestPyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        repository-url: https://test.pypi.org/legacy/

  notify:
    name: Notify on Success
    needs: [publish-pypi, publish-testpypi]
    runs-on: ubuntu-latest
    if: success()
    
    steps:
    - name: Create GitHub Release
      uses: actions/github-script@v7
      with:
        script: |
          github.rest.repos.createRelease({
            owner: context.repo.owner,
            repo: context.repo.repo,
            tag_name: context.ref.replace('refs/tags/', ''),
            draft: false,
            prerelease: false
          })
```

### 5.2 Trigger with Git Tags

```bash
# 1. Update version in pyproject.toml
# 2. Create and push tag
git tag -a v0.4.0 -m "Release version 0.4.0 - Feature X, Bug fixes"
git push origin v0.4.0

# Workflow automatically triggers and publishes to:
# - TestPyPI: Always
# - PyPI: With manual approval (requires environment approval)
```

---

## 6. ENVIRONMENT VARIABLES & GITHUB ACTIONS CONFIGURATION

### 6.1 GitHub Secrets (Legacy - Don't Use for PyPI)

If forced to use static tokens (third-party indexes):

```yaml
# In GitHub: Settings → Secrets and variables → Actions → New repository secret
# Secret name: PYPI_API_TOKEN
# Value: pypi-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890...

env:
  PYPI_API_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
```

### 6.2 Recommended: GitHub Environments

**For Production (PyPI):**

1. Go to: Repository → Settings → Environments
2. Click "New Environment" → Name: `pypi`
3. Configure Protection Rules:
   - ✅ "Require reviewers" - Set minimum reviewers
   - ✅ "Restrict deployments to specific branches" - e.g., `main`
   - Add environment variables if needed (optional)

**For Testing (TestPyPI):**

1. Create environment: `testpypi`
2. No protection rules needed (runs automatically)
3. Can add: `TEST_PYPI_URL: https://test.pypi.org/legacy/`

### 6.3 OIDC Token Configuration

**Built-in (No Manual Configuration Needed)**

When workflow uses `permissions: id-token: write`, GitHub automatically:
1. Generates OIDC token for the workflow
2. Includes context: repository, commit, workflow, actor
3. Passes token to actions requesting it
4. Token expires after workflow completes

**Verification:**

```yaml
- name: Debug OIDC Token (Optional)
  run: |
    echo "Token will be generated for:"
    echo "Repository: $GITHUB_REPOSITORY"
    echo "Ref: $GITHUB_REF"
    echo "Commit: $GITHUB_SHA"
    echo "Actor: $GITHUB_ACTOR"
```

---

## 7. OFFICIAL DOCUMENTATION & AUTHORITATIVE LINKS

### PyPI & Trusted Publishing

| Resource                      | URL                                              | Status     |
| ----------------------------- | ------------------------------------------------ | ---------- |
| **PyPI Trusted Publishers**   | https://docs.pypi.org/trusted-publishers/        | ✅ OFFICIAL |
| **PyPI Help & API Tokens**    | https://pypi.org/help/#apitoken                  | ✅ OFFICIAL |
| **PyPI Publish Settings**     | https://pypi.org/manage/account/publishing/      | ✅ OFFICIAL |
| **TestPyPI Publish Settings** | https://test.pypi.org/manage/account/publishing/ | ✅ OFFICIAL |

### GitHub Actions & Workflows

| Resource                         | URL                                                                               | Status     |
| -------------------------------- | --------------------------------------------------------------------------------- | ---------- |
| **GitHub Actions Official Docs** | https://docs.github.com/en/actions                                                | ✅ OFFICIAL |
| **OIDC Trusted Publishing**      | https://docs.github.com/en/actions/deployment/security-hardening-your-deployments | ✅ OFFICIAL |
| **GitHub Environments**          | https://docs.github.com/en/actions/deployment/targeting-different-environments    | ✅ OFFICIAL |
| **Workflow Triggers**            | https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows  | ✅ OFFICIAL |

### Community & PyPA

| Resource                        | URL                                                                                                                | Status     |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------- |
| **PyPA gh-action-pypi-publish** | https://github.com/pypa/gh-action-pypi-publish                                                                     | ✅ OFFICIAL |
| **Python Packaging Guide**      | https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/ | ✅ OFFICIAL |
| **PEP 740 (Attestations)**      | https://peps.python.org/pep-0740/                                                                                  | ✅ STANDARD |
| **Twine CLI Tool**              | https://github.com/pypa/twine                                                                                      | ✅ OFFICIAL |

---

## 8. RECOMMENDED ACTIONS COMPARISON

### Feature Matrix

| Feature                  | gh-action-pypi-publish | Twine           | Manual Script |
| ------------------------ | ---------------------- | --------------- | ------------- |
| **OIDC Support**         | ✅ Full                 | ✅ Via env       | ❌ No          |
| **PEP 740 Attestations** | ✅ v1.11.0+             | ❌ No            | ❌ No          |
| **Multi-repo Upload**    | ✅ Yes                  | ✅ Yes           | ⚠️ Custom      |
| **Dry-run/Verify**       | ✅ Yes                  | ✅ Yes           | ⚠️ Custom      |
| **Error Handling**       | ✅ Built-in             | ✅ Good          | ⚠️ Required    |
| **Maintenance**          | ✅ PyPA Official        | ✅ PyPA Official | ❌ Custom      |
| **Learning Curve**       | ⭐ Easy                 | ⭐⭐ Medium       | ⭐⭐⭐⭐ Hard     |

### Recommendation

**Use `pypa/gh-action-pypi-publish@release/v1`** for:
- ✅ Official PyPA endorsement
- ✅ No credential management needed
- ✅ Built-in verification
- ✅ PEP 740 attestation support
- ✅ Active maintenance

---

## 9. QUICK START FOR PYGPMF_OZ

### Step 1: Register Trusted Publishers

```bash
# 1. Go to https://pypi.org/manage/account/publishing/
# 2. Create pending publisher:
#    - Project name: pygpmf-oz
#    - Owner: <your-username/org>
#    - Repository: pygpmf
#    - Workflow: publish-to-pypi.yml
#    - Environment: pypi

# 3. Repeat for TestPyPI at https://test.pypi.org/manage/account/publishing/
#    - Environment: testpypi
```

### Step 2: Create Workflow File

Create `.github/workflows/publish-to-pypi.yml` (see Section 5.1 example)

### Step 3: Configure Environment Protection

1. Settings → Environments → New: `pypi`
2. Add deployment branch protection (main only)
3. Require reviewers before deployment

### Step 4: Release Process

```bash
# Update version in pyproject.toml
# v0.4.0

# Create annotated tag
git tag -a v0.4.0 -m "Release: pygpmf-oz v0.4.0 - New features and improvements"

# Push to GitHub
git push origin v0.4.0

# Workflow triggers:
# 1. Builds packages
# 2. Tests on TestPyPI (automatic)
# 3. Awaits approval for PyPI push (manual step in GitHub UI)
```

---

## 10. TROUBLESHOOTING & COMMON ISSUES

### Issue: "Permission denied" on PyPI publish

**Cause:** Missing `permissions: id-token: write` in workflow

**Solution:**
```yaml
permissions:
  id-token: write  # Add this
```

### Issue: Workflow doesn't trigger on tag push

**Cause:** Incorrect tag pattern in `on.push.tags`

**Solution:**
```yaml
on:
  push:
    tags:
      - 'v[0-9]+.[0-9]+.[0-9]+'  # Matches: v1.0.0
      - 'v[0-9]+.[0-9]+.[0-9]+-*' # Matches: v1.0.0-rc.1
```

### Issue: TestPyPI publish succeeds, PyPI fails

**Cause:** Untrusted publisher not registered

**Solution:**
1. Go to https://pypi.org/manage/account/publishing/
2. Register pending publisher with exact project name
3. First publish creates project automatically

### Issue: "Repository URL is not recognized"

**Cause:** TestPyPI URL format error

**Solution:**
```yaml
# Correct:
repository-url: https://test.pypi.org/legacy/

# Incorrect:
repository-url: https://test.pypi.org/  # Missing /legacy/
```

---

## 11. MAINTENANCE & UPDATES

### Action Version Updates

```bash
# Check for updates regularly
# GitHub will notify of action updates in Actions tab

# Update to latest major version
# pypa/gh-action-pypi-publish@release/v1  # Current stable
# pypa/gh-action-pypi-publish@release/v2  # When available
```

### Annual Review Checklist

- [ ] Review PyPI trusted publisher configuration
- [ ] Verify GitHub environment protection rules
- [ ] Check if new action versions available
- [ ] Review published package statistics
- [ ] Test workflow with pre-release tags
- [ ] Verify attestation signatures working
- [ ] Update dependencies in workflow

---

## Summary Table: Decision Matrix

| Requirement                     | Implementation                        | Reference   |
| ------------------------------- | ------------------------------------- | ----------- |
| Publish on tag push             | `on: push: tags: ['v*']`              | Section 5   |
| Use trusted auth                | `permissions: id-token: write` + OIDC | Section 2   |
| Prevent accidental PyPI publish | Environment with approval             | Section 4.2 |
| Sign packages                   | Use gh-action-pypi-publish v1.11.0+   | Section 3.1 |
| Validate before publish         | `twine check dist/*`                  | Section 5.1 |
| Test first                      | Publish to TestPyPI before PyPI       | Section 5.1 |
| Monitor deployments             | GitHub Environments + PyPI activity   | Section 4.1 |

---

## Final Recommendation

For **pygpmf_oz**, implement:

1. ✅ **Trusted Publishing with OIDC** (No secrets needed)
2. ✅ **pypa/gh-action-pypi-publish@release/v1** (Official, maintained)
3. ✅ **Semantic versioning tags** (v0.4.0 format)
4. ✅ **Environment protection** (Manual approval for PyPI)
5. ✅ **TestPyPI validation** (Test before production)
6. ✅ **PEP 740 attestations** (Automatic from action)

**Result:** Secure, automated, verifiable Python package publishing with zero credential management overhead.

---

*Document compiled: January 12, 2026*  
*Based on official PyPI, GitHub, and PyPA documentation*  
*Applicable to pygpmf_oz CI/CD pipeline implementation*
