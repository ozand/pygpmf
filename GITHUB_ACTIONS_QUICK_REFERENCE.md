# PyPI Deployment with GitHub Actions - Quick Reference

## 🚀 TL;DR - Fastest Path to Implementation

### 1. Register Trusted Publishers (5 min)
```
PyPI:      https://pypi.org/manage/account/publishing/
TestPyPI:  https://test.pypi.org/manage/account/publishing/

Fill in:
- Project name: pygpmf-oz
- Owner: your-username
- Repo: pygpmf
- Workflow: publish-to-pypi.yml
- Environment: pypi (for PyPI), testpypi (for TestPyPI)
```

### 2. Create Workflow (copy from example)
```
File: .github/workflows/publish-to-pypi.yml
(See GITHUB_ACTIONS_PYPI_DEPLOYMENT.md Section 5.1)
```

### 3. Set Environment Protection (2 min)
```
Repo Settings → Environments → pypi → Add protection rule
(Require reviewers for production safety)
```

### 4. Release!
```bash
git tag -a v0.4.0 -m "Release v0.4.0"
git push origin v0.4.0
```

---

## 🔐 Security: The One Critical Thing

```yaml
permissions:
  id-token: write  # ← THIS IS CRITICAL
```

Without this, OIDC token generation fails and deployment fails.

---

## 📊 At a Glance: OIDC vs API Tokens

| Aspect               | OIDC (Recommended)     | API Token (Deprecated)      |
| -------------------- | ---------------------- | --------------------------- |
| Security             | ⭐⭐⭐⭐⭐ Excellent        | ⭐⭐ Poor                     |
| Token Lifetime       | Minutes (auto-expires) | Permanent (rotate manually) |
| Setup Friction       | Minimal                | Requires secret mgmt        |
| Per-Project Scoping  | Yes                    | No (account-level)          |
| Official Endorsement | PyPA ✅                 | Legacy only                 |

**Bottom Line:** Use OIDC. There's no reason not to.

---

## 🎯 Trigger Events Explained

```yaml
# Production (to PyPI)
on:
  push:
    tags: ['v[0-9]+.[0-9]+.[0-9]+']  # Only v1.0.0, v2.1.3, etc.
    
# Always test first (to TestPyPI)
# Same push triggers both; PyPI needs approval

# Manual (optional)
on: workflow_dispatch  # Run from GitHub UI
```

---

## 🛠️ Actions: gh-action-pypi-publish

### Why This One?
- ✅ Official (PyPA maintained)
- ✅ OIDC support built-in
- ✅ PEP 740 signature attestations
- ✅ Battle-tested in hundreds of projects

### Usage
```yaml
# PyPI
- uses: pypa/gh-action-pypi-publish@release/v1

# TestPyPI
- uses: pypa/gh-action-pypi-publish@release/v1
  with:
    repository-url: https://test.pypi.org/legacy/
```

---

## ⚠️ Security Checklist (Required)

- [ ] Registered trusted publisher with PyPI
- [ ] Registered trusted publisher with TestPyPI
- [ ] Workflow has `permissions: id-token: write`
- [ ] Environment `pypi` requires manual approval
- [ ] No static API tokens in secrets
- [ ] Branch protection enabled (PR reviews)
- [ ] Run `twine check` before publish
- [ ] Test on TestPyPI first
- [ ] Verify attestations work

---

## 🔗 Critical Links

**Authoritative:**
- PyPI Trusted Publishers: https://docs.pypi.org/trusted-publishers/
- Register Trusted Publishers: https://pypi.org/manage/account/publishing/
- GitHub OIDC: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments

**Action Docs:**
- gh-action-pypi-publish: https://github.com/pypa/gh-action-pypi-publish

**Reference:**
- PEP 740 (Attestations): https://peps.python.org/pep-0740/

---

## 🚨 Common Mistakes & Fixes

| Problem                          | Fix                                                                       |
| -------------------------------- | ------------------------------------------------------------------------- |
| "Permission denied on publish"   | Add `permissions: id-token: write`                                        |
| Workflow doesn't trigger on tags | Check tag pattern matches: `v[0-9]+.[0-9]+.[0-9]+`                        |
| TestPyPI works, PyPI fails       | Register trusted publisher at https://pypi.org/manage/account/publishing/ |
| "Repository not recognized"      | Use correct URL: `https://test.pypi.org/legacy/` (note `/legacy/`)        |

---

## 📈 Workflow Matrix

```
Commit → Build → Test → (Manual ✓) → Publish PyPI
         ↓      ↓                     ↓
         └──────└─→ Publish TestPyPI (auto)

Flow:
1. Tag commit: v0.4.0
2. Push tag: git push origin v0.4.0
3. GitHub Actions builds & tests
4. TestPyPI: Auto-publish (validation)
5. PyPI: Awaits manual approval in GitHub UI
6. Click "Review deployments" → "Approve" → Done!
```

---

## 📋 Full Workflow Template Location

**File:** `GITHUB_ACTIONS_PYPI_DEPLOYMENT.md` → Section 5.1

Ready-to-use workflow with all best practices included.

---

## ✅ Once Deployed

**Verify it works:**
```bash
# Look for your version in PyPI
pip index versions pygpmf-oz

# Or browse: https://pypi.org/project/pygpmf-oz/

# Check attestations:
pip install sigstore  # If needed
# Verify from PyPI UI
```

---

**Last Updated:** January 12, 2026  
**Status:** Ready for Implementation  
**Complexity:** ⭐⭐ Medium (most setup via UI, workflow is copy-paste)
