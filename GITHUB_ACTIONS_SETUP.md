# GitHub Actions PyPI Deployment Setup for pygpmf_oz

This document explains how to activate automated PyPI publishing via GitHub Actions for pygpmf_oz v0.3.0 and future releases.

---

## Quick Start (5 minutes)

### Step 1: Register Trusted Publisher with PyPI (2 min)

Go to: **https://pypi.org/manage/account/publishing/**

Click "Add a new pending publisher" and fill in:

| Field                       | Value                                   |
| --------------------------- | --------------------------------------- |
| **PyPI Project Name**       | `pygpmf-oz`                             |
| **Owner**                   | `alexis-mignon` (or your username)      |
| **Repository Name**         | `pygpmf`                                |
| **Workflow Filename**       | `.github/workflows/publish-to-pypi.yml` |
| **GitHub Environment Name** | `pypi`                                  |

✅ Click "Add pending publisher"

### Step 2: Register Trusted Publisher with TestPyPI (2 min)

Go to: **https://test.pypi.org/manage/account/publishing/**

Same process, but:
- **GitHub Environment Name**: `testpypi`

✅ Click "Add pending publisher"

### Step 3: Protect Production Environment (1 min)

In GitHub repository settings:

1. Go to **Settings** → **Environments**
2. Click **pypi** environment
3. Check "Require reviewers before deploying to this environment"
4. Add yourself as reviewer (optional but recommended)

✅ Done!

---

## How It Works

### Workflow Diagram

```
Push git tag v0.3.0
    ↓
GitHub Actions triggered
    ↓
[Build Job] - Build wheel + sdist
    ↓ (passes artifacts to next job)
[TestPyPI Job] - Publish to test.pypi.org (automatic)
    ↓ (automatic if passed)
[PyPI Job] - Publish to pypi.org (automatic, blocked by "Require reviewers")
    ↓ (auto-approve or manually approve in GitHub Actions tab)
[GitHub Release Job] - Create release + upload dist files
```

### Security Flow

1. **Developer pushes tag**: `git push origin v0.3.0`
2. **GitHub generates OIDC token** with context (commit, repo, workflow)
3. **Workflow publishes to TestPyPI** (automatic, no secrets needed)
4. **Workflow tries PyPI** (blocked by environment protection)
5. **Developer/maintainer approves** in GitHub Actions tab
6. **Workflow creates GitHub Release** with downloadable artifacts

**Key Security Feature**: No API keys or secrets stored in GitHub. Token expires immediately after use.

---

## Publishing a Release

### For Maintainers

When ready to release v0.3.1:

```bash
# Ensure code is merged and tests pass
git log --oneline -3

# Create annotated tag
git tag -a v0.3.1 -m "Release 0.3.1: Hero 12 compatibility fixes"

# Push tag to trigger workflow
git push origin v0.3.1
```

### Monitor the Workflow

1. Go to GitHub Actions: **Actions** tab
2. Look for **Publish to PyPI** workflow run
3. Check **TestPyPI** job (should auto-pass in ~2 min)
4. Check **PyPI** job (will be waiting for approval)
5. Click "Review deployments" and approve
6. Wait for **GitHub Release** job to complete

### Verify Publication

```bash
# Test TestPyPI
pip install -i https://test.pypi.org/simple/ pygpmf-oz==0.3.1 --pre

# Test PyPI (after 2-3 min cache)
pip install --upgrade pygpmf-oz
python -c "import gpmf; print(gpmf.__version__)"
```

---

## Understanding the Workflow

### Job: `build`
- Runs on every push (tag or manual trigger)
- Builds wheel and source distribution
- Validates with `twine check`
- Uploads artifacts for reuse by next jobs

### Job: `publish-to-testpypi`
- Always runs after build succeeds
- Uses Trusted Publishing (OIDC token)
- Publishes to https://test.pypi.org
- Good for validating the pipeline before production
- **No approval needed** (automatic)

### Job: `publish-to-pypi`
- Only runs if tag was pushed: `if: startsWith(github.ref, 'refs/tags/')`
- Requires **pypi** environment approval
- Publishes to https://pypi.org
- Creates a protection rule requiring manual review
- **Requires approval** for security

### Job: `github-release`
- Only runs after PyPI publication succeeds
- Creates GitHub Release with auto-generated notes
- Uploads dist/ artifacts as release assets
- Allows users to download packages from GitHub

---

## Environment Protection

To add an approval step (recommended for security):

1. **Settings** → **Environments** → **pypi**
2. Check: "Require reviewers before deploying to this environment"
3. Add reviewer(s) - usually maintainers
4. On workflow run, GitHub will show "Review deployments" button

When publishing:
- TestPyPI: auto-deploy, no approval
- PyPI: **wait for approval**, click "Approve and deploy"

---

## Troubleshooting

### Error: "Trusted Publisher not found"

**Cause**: Trusted Publisher not registered with PyPI

**Fix**:
1. Go to https://pypi.org/manage/account/publishing/
2. Verify exact project name: `pygpmf-oz`
3. Verify exact repository: `ozand/pygpmf`
4. Verify exact workflow filename: `.github/workflows/publish-to-pypi.yml`
5. Verify exact environment name: `pypi`

### Error: "OIDC token request failed"

**Cause**: Missing `permissions: id-token: write` in workflow

**Fix**: Workflow file already includes this. If error persists, contact GitHub Support.

### Job stuck on "Waiting for approval"

**Cause**: Environment protection rule is active

**Expected behavior**: This is correct for PyPI job!

**Fix**: 
1. Go to GitHub Actions tab
2. Find "Publish to PyPI" workflow
3. Click "Review deployments"
4. Select reviewers and click "Approve"

### TestPyPI succeeded but PyPI stuck at approval

**Expected behavior**: This is correct! Manual approval adds security layer.

**Fix**: See "Job stuck on approval" above.

### Package not visible on PyPI after "success"

**Cause**: PyPI cache delay (2-5 minutes)

**Wait**: Refresh https://pypi.org/project/pygpmf-oz/ after 2-3 min

**Verify via pip**:
```bash
pip install --upgrade --no-cache pygpmf-oz
```

---

## Security Checklist

- ✅ Trusted Publishing (OIDC) configured - no static secrets
- ✅ Environment protection enabled for PyPI (approval required)
- ✅ TestPyPI validates build before PyPI publication
- ✅ GitHub Release auto-created with checksums
- ✅ Workflow triggers only on tags (production safety)
- ✅ Artifacts auto-deleted after 1 day (no storage bloat)

---

## For Future: Additional Workflow Improvements

Once established, consider:

1. **Attestations** (PEP 740): Already in `gh-action-pypi-publish@release/v1` (v1.11.0+)
   - Cryptographically sign distributions
   - Users can verify package integrity

2. **Changelog Auto-Generation**: Already included!
   - Uses `gh release create --generate-notes`
   - Auto-populates from commit history

3. **Conditional Publishing**: Extend to publish only on `main` branch changes
   ```yaml
   if: github.ref == 'refs/heads/main' && startsWith(github.ref, 'refs/tags/')
   ```

4. **Email Notifications**: GitHub Actions already emails on success/failure

---

## References

- **Trusted Publishing**: https://docs.pypi.org/trusted-publishers/
- **PyPA Action**: https://github.com/pypa/gh-action-pypi-publish
- **GitHub OIDC**: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- **PEP 740**: https://peps.python.org/pep-0740/
- **Semantic Versioning**: https://semver.org/

---

## Next Release: v0.3.1+

When ready:

```bash
# Local setup
git checkout master
git pull origin master

# Make changes, test locally
pytest tests/
python -m build
twine check dist/*

# Create release
git tag -a v0.3.1 -m "Release 0.3.1: [description]"
git push origin v0.3.1

# Sit back and watch GitHub Actions
# Approve PyPI deployment when prompted
```

**Done!** Package automatically published to PyPI in <5 min.
