# pygpmf_oz v0.3.0 Release Checklist

**Status**: ✅ **READY FOR PRODUCTION**

---

## ✅ Pre-Release Validation (Completed)

- ✅ **Tests**: 134 tests passing, 79.77% coverage (3.92s execution)
- ✅ **Build**: Wheel and source distribution created successfully
- ✅ **Artifacts**: Both `twine check` validated (PEP 427, PEP 425 compliant)
- ✅ **Version**: Bumped to 0.3.0 in `__init__.py` and `setup.cfg`
- ✅ **Compatibility**: All 119 original tests still passing (no regressions)

---

## ✅ Documentation (Completed)

- ✅ [RELEASE_NOTES_0_3_0.md](RELEASE_NOTES_0_3_0.md) - Feature summary, upgrade path, breaking changes (0)
- ✅ [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - For teams migrating from v0.2.1
- ✅ [GITHUB_ACTIONS_PYPI_DEPLOYMENT.md](GITHUB_ACTIONS_PYPI_DEPLOYMENT.md) - Comprehensive deployment guide
- ✅ [GITHUB_ACTIONS_QUICK_REFERENCE.md](GITHUB_ACTIONS_QUICK_REFERENCE.md) - Quick start guide
- ✅ [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - Step-by-step setup instructions
- ✅ [PYPI_UPLOAD_0_3_0.md](PYPI_UPLOAD_0_3_0.md) - Manual upload instructions (backup)

---

## ✅ Automation Infrastructure (Completed)

- ✅ **GitHub Actions Workflow**: `.github/workflows/publish-to-pypi.yml` (96 lines)
  - ✅ Job 1: `build` - Validates and builds artifacts
  - ✅ Job 2: `publish-to-testpypi` - Automatic validation publication
  - ✅ Job 3: `publish-to-pypi` - Conditional production publication (approval required)
  - ✅ Job 4: `github-release` - Creates GitHub Release with assets
  - ✅ Security: OIDC Trusted Publishing (no static secrets)
  - ✅ Triggers: Semantic version tags (v0.3.0, v1.0.0-rc1, etc.) + manual dispatch

---

## ⏳ Pre-Publication Setup (REQUIRED - User Action)

### Step 1: Register Trusted Publishers (5 min)

**PyPI**: https://pypi.org/manage/account/publishing/
- Project name: `pygpmf-oz`
- Repository: `ozand/pygpmf`
- Workflow: `.github/workflows/publish-to-pypi.yml`
- Environment: `pypi`

**TestPyPI**: https://test.pypi.org/manage/account/publishing/
- Project name: `pygpmf-oz`
- Repository: `ozand/pygpmf`
- Workflow: `.github/workflows/publish-to-pypi.yml`
- Environment: `testpypi`

**Status**: ⏳ **PENDING USER ACTION**

### Step 2: Configure Environment Protection (Optional, Recommended - 2 min)

GitHub Repository Settings → Environments → `pypi`
- Check: "Require reviewers before deploying to this environment"
- Add reviewers: (yourself or maintainers)

**Purpose**: Add manual approval gate for production PyPI (safety measure)

**Status**: ⏳ **OPTIONAL**

---

## ⏳ Publishing Steps (REQUIRED - User Action)

### Step 3: Create Release Tag

```bash
git tag -a v0.3.0 -m "Release 0.3.0: Hero 11-13 GPS9 support"
```

**Contents**:
- ✅ All source code at version 0.3.0
- ✅ All tests passing
- ✅ All documentation committed

### Step 4: Push Tag to Trigger Workflow

```bash
git push origin v0.3.0
```

**Expected**:
- GitHub Actions automatically triggered
- Workflow runs ~2-3 minutes
- TestPyPI publication automatic (check in Actions tab)
- PyPI publication requires approval (click "Review deployments")

### Step 5: Approve PyPI Deployment

In GitHub repository:
- Go to: **Actions** tab
- Find: **"Publish to PyPI"** workflow run for v0.3.0
- Click: **"Review deployments"** button
- Approve: Select approver, click **"Approve and deploy"**

**Expected**:
- Workflow completes PyPI publication in ~1-2 min
- GitHub Release created automatically with assets
- Package visible on https://pypi.org/project/pygpmf-oz/0.3.0/

**Status**: ⏳ **PENDING USER ACTION**

---

## ⏳ Post-Publication Verification (REQUIRED - User Action)

### Step 6: Verify PyPI Publication

**Check Package Page**:
```
https://pypi.org/project/pygpmf-oz/0.3.0/
```

**Check Installation**:
```bash
pip install --upgrade pygpmf-oz==0.3.0
python -c "import gpmf; print(gpmf.__version__)"
# Expected output: 0.3.0
```

**Check Release Assets**:
- Navigate to: **Releases** tab in GitHub
- Verify: v0.3.0 release created with dist/ artifacts attached

**Status**: ⏳ **PENDING USER ACTION**

---

## ⏳ External Communication (Recommended)

### Step 7: Notify Teams Using v0.2.1

Share [RELEASE_NOTES_0_3_0.md](RELEASE_NOTES_0_3_0.md) and [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md):

**Key Points**:
1. Hero 11, 12, 13 support (GPS9 module)
2. Gyroscope and accelerometer data
3. UTF-8 FourCC decoding fix (prevents crashes)
4. Full backward compatibility with v0.2.1 code
5. Straightforward upgrade: `pip install --upgrade pygpmf-oz`

**Channels**:
- [ ] Email to teams
- [ ] GitHub Releases page (auto-populated)
- [ ] Project documentation
- [ ] Issue comments for teams asking about Hero 11-13

**Status**: ⏳ **RECOMMENDED**

---

## Release Timeline

| Phase                             | Status     | Duration | Blocker                        |
| --------------------------------- | ---------- | -------- | ------------------------------ |
| Pre-release validation            | ✅ Complete | -        | None                           |
| Documentation                     | ✅ Complete | -        | None                           |
| Automation setup                  | ✅ Complete | -        | None                           |
| Trusted Publisher registration    | ⏳ Pending  | 5 min    | **User registration required** |
| Environment protection (optional) | ⏳ Pending  | 2 min    | None                           |
| Create + push tag                 | ⏳ Pending  | 2 min    | Trusted Publisher registration |
| Approve PyPI deployment           | ⏳ Pending  | 1 min    | Tag push                       |
| Verification                      | ⏳ Pending  | 2 min    | PyPI approval                  |
| **Total (expedited)**             | **5+ min** | -        | User action required           |

---

## Rollback Plan (If Needed)

### Issue: Package published with error

**Option 1: Yank Version**
```
https://pypi.org/project/pygpmf-oz/
→ Click v0.3.0
→ Settings
→ Click "Yank this release"
```

Impact: Users can't install new, but existing installations work.

**Option 2: Publish Hotfix**
```bash
# Fix code
git tag -a v0.3.1 -m "Hotfix: ..."
git push origin v0.3.1
# Follow Steps 3-5 above
```

Impact: New version available immediately.

**Option 3: Manual Unpublish**
- Contact PyPI maintainers at pypi-help@python.org
- Provide: Project name, version, reason
- Wait: 24-48 hours

Impact: Complete removal, rare (only for malware/legal issues)

---

## Success Criteria

✅ Release is successful when:

1. Package appears on https://pypi.org/project/pygpmf-oz/0.3.0/
2. Installation works: `pip install pygpmf-oz==0.3.0`
3. Version detected: `import gpmf; gpmf.__version__ == "0.3.0"`
4. GitHub Release created at: https://github.com/ozand/pygpmf/releases/tag/v0.3.0
5. Dist artifacts attached to release (wheel + source)
6. No warnings in PyPI project page

---

## Files Ready for Publication

| File                                    | Size    | Type       | Checksum   |
| --------------------------------------- | ------- | ---------- | ---------- |
| `pygpmf_oz-0.3.0-py3-none-any.whl`      | 33.8 KB | Binary     | ✅ Verified |
| `pygpmf_oz-0.3.0.tar.gz`                | 30.4 KB | Source     | ✅ Verified |
| `RELEASE_NOTES_0_3_0.md`                | 5.7 KB  | Docs       | ✅ Ready    |
| `INTEGRATION_GUIDE.md`                  | 8.1 KB  | Docs       | ✅ Ready    |
| `.github/workflows/publish-to-pypi.yml` | 3.2 KB  | Automation | ✅ Ready    |

---

## Support & Documentation

- **Installation Issues**: See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- **GitHub Actions Issues**: See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)
- **Deployment Details**: See [GITHUB_ACTIONS_PYPI_DEPLOYMENT.md](GITHUB_ACTIONS_PYPI_DEPLOYMENT.md)
- **Release Details**: See [RELEASE_NOTES_0_3_0.md](RELEASE_NOTES_0_3_0.md)

---

## Next Release (v0.3.1+)

For future releases, simply:

1. Make changes and test locally
2. Bump version in `__init__.py` and `setup.cfg`
3. Create annotated tag: `git tag -a v0.3.1 -m "Release 0.3.1: ..."`
4. Push tag: `git push origin v0.3.1`
5. Approve deployment in GitHub Actions
6. Done! 🎉

No manual uploads needed. GitHub Actions handles everything.

---

**Created**: 2025
**Release Version**: 0.3.0
**Status**: Ready for production ✅
