# ReadTheDocs Integration Setup

**API Key**: `158f9d3d489fea0cee0dd26eba0482547a217e36`

---

## 🔐 Setup Instructions

### Step 1: Add API Key to GitHub Secrets (2 minutes)

1. Go to your GitHub repository: **https://github.com/ozand/pygpmf**
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click: **New repository secret**
4. Fill in:
   - **Name**: `READTHEDOCS_TOKEN`
   - **Secret**: `158f9d3d489fea0cee0dd26eba0482547a217e36`
5. Click: **Add secret**

✅ **Done!** The API key is now securely stored.

---

## 🔄 How It Works

### Workflow Integration

The GitHub Actions workflow now includes a **ReadTheDocs trigger job**:

```yaml
trigger-readthedocs:
    name: Trigger ReadTheDocs Build
    if: startsWith(github.ref, 'refs/tags/')
    runs-on: ubuntu-latest
    needs: github-release

    steps:
        - name: Trigger ReadTheDocs build
          run: |
              curl -X POST \
                -H "Authorization: Token ${{ secrets.READTHEDOCS_TOKEN }}" \
                https://readthedocs.org/api/v3/projects/pygpmf-oz/versions/latest/builds/
```

### Execution Flow

```
Tag pushed (v0.3.0)
    ↓
Build artifacts
    ↓
Publish to TestPyPI
    ↓
Publish to PyPI
    ↓
Create GitHub Release
    ↓
Trigger ReadTheDocs build ← NEW
```

---

## 🎯 What This Does

When you push a release tag:

1. **PyPI publication happens** (automated via OIDC)
2. **GitHub Release is created** (with dist artifacts)
3. **ReadTheDocs is triggered** (via API call)
4. **Documentation is rebuilt automatically** on ReadTheDocs

---

## ✅ Verification

After pushing a release tag, verify:

1. **PyPI**: Check https://pypi.org/project/pygpmf-oz/
2. **GitHub Release**: Check https://github.com/ozand/pygpmf/releases
3. **ReadTheDocs**: Check https://pygpmf-oz.readthedocs.io/ or your project URL

---

## 🔧 Troubleshooting

### Issue: "401 Unauthorized"

**Cause**: API token not set or incorrect in GitHub Secrets

**Fix**:
1. Verify secret name is exactly: `READTHEDOCS_TOKEN`
2. Verify secret value matches: `158f9d3d489fea0cee0dd26eba0482547a217e36`
3. Re-save the secret if needed

### Issue: "404 Not Found"

**Cause**: Project name incorrect in API URL

**Fix**: 
Update the API URL in workflow file if your ReadTheDocs project has a different slug:
```bash
https://readthedocs.org/api/v3/projects/YOUR-PROJECT-SLUG/versions/latest/builds/
```

### Issue: Build triggered but docs not updated

**Cause**: ReadTheDocs build failed or still in progress

**Fix**:
1. Go to ReadTheDocs dashboard: https://readthedocs.org/projects/pygpmf-oz/
2. Check **Builds** tab for status
3. Review build logs if failed

---

## 📚 ReadTheDocs Configuration

### .readthedocs.yaml (Recommended)

Create a `.readthedocs.yaml` file in your repository root:

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

python:
  install:
    - method: pip
      path: .
    - requirements: docs/requirements.txt

sphinx:
  configuration: docs/conf.py
```

### docs/requirements.txt

```txt
sphinx>=7.0.0
sphinx-rtd-theme>=2.0.0
```

---

## 🔒 Security Best Practices

✅ **DO**:
- Store API token in GitHub Secrets
- Use token only in workflow context
- Never commit token to repository
- Rotate token periodically

❌ **DON'T**:
- Hardcode token in workflow files
- Share token publicly
- Use token in pull request workflows (security risk)

---

## 📋 Release Checklist Update

Add to your release checklist:

```markdown
POST-PUBLICATION
□ PyPI publication verified
□ GitHub Release created
□ ReadTheDocs build triggered ← NEW
□ Documentation updated and live ← NEW
```

---

## 🚀 Next Steps

1. **Add secret to GitHub** (Step 1 above)
2. **Push a release tag** to test integration
3. **Verify documentation updates** on ReadTheDocs

---

**Status**: ✅ Workflow updated, ready for GitHub secret configuration

**Time to Complete**: ~2 minutes (just add the secret)
