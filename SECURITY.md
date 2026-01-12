# Security Policy / Политика безопасности

## 🔒 Reporting Security Issues / Сообщение о проблемах безопасности

**English**: If you discover a security vulnerability in this project, please report it privately:
- **GitHub Security Advisories**: https://github.com/ozand/pygpmf-oz/security/advisories/new
- **Email**: Create an issue with `[SECURITY]` tag (without details), we'll follow up privately

**Русский**: Если вы обнаружили уязвимость безопасности в проекте, пожалуйста, сообщите об этом приватно:
- **GitHub Security Advisories**: https://github.com/ozand/pygpmf-oz/security/advisories/new
- **Email**: Создайте issue с меткой `[SECURITY]` (без деталей), мы свяжемся приватно

---

## ⚠️ What NOT to Commit / Что НЕЛЬЗЯ коммитить

### 🚫 Never commit these to the repository:

1. **API Tokens & Keys**
   - ReadTheDocs API tokens
   - PyPI API tokens
   - GitHub Personal Access Tokens
   - Any service API keys

2. **Credentials**
   - Passwords
   - Private keys (SSH, GPG, etc.)
   - Database credentials
   - Service account credentials

3. **Personal Information**
   - Email addresses (use @users.noreply.github.com)
   - Phone numbers
   - Personal addresses

4. **Sensitive Configuration**
   - `.env` files with secrets
   - Production configuration files
   - Database connection strings with credentials

---

## ✅ How to Store Secrets Securely / Как безопасно хранить секреты

### GitHub Secrets (Recommended)

Store all sensitive data in GitHub Secrets:

1. **Repository Secrets**: Settings → Secrets and variables → Actions
2. **Environment Secrets**: Settings → Environments → [env-name] → Secrets

**Example**:
```yaml
# ✅ CORRECT - Using GitHub Secrets
- name: Deploy
  env:
    API_TOKEN: ${{ secrets.READTHEDOCS_TOKEN }}
  run: curl -H "Authorization: Token $API_TOKEN" ...
```

```markdown
# ❌ WRONG - Token in documentation
**API Key**: `158f9d3d489fea0cee0dd26eba0482547a217e36`
```

### Environment Variables

For local development, use `.env` files (add to `.gitignore`):

```bash
# .env (never commit this)
READTHEDOCS_TOKEN=your-token-here
PYPI_TOKEN=your-pypi-token
```

```python
# Load in code
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('READTHEDOCS_TOKEN')
```

---

## 🔍 Security Checklist / Чеклист безопасности

### Before Committing / Перед коммитом

- [ ] No API tokens in code or documentation
- [ ] No passwords or credentials
- [ ] No real email addresses (use `@users.noreply.github.com`)
- [ ] Sensitive files in `.gitignore`
- [ ] Reviewed diff with `git diff --staged`

### Before Pushing / Перед пушем

- [ ] Run: `git log -p` to review all changes
- [ ] Check for accidentally committed secrets
- [ ] Verify `.env` files are not tracked
- [ ] No `.env.example` with real values

### Repository Configuration / Настройка репозитория

- [ ] Branch protection enabled on `master`
- [ ] Required reviews for pull requests
- [ ] Secret scanning enabled (GitHub Advanced Security)
- [ ] Dependabot alerts enabled

---

## 🚨 If You Accidentally Committed a Secret / Если вы случайно закоммитили секрет

### Immediate Actions:

1. **Revoke the exposed secret immediately**
   - ReadTheDocs: Delete token at https://readthedocs.org/accounts/tokens/
   - PyPI: Revoke token at https://pypi.org/manage/account/token/
   - GitHub: Revoke at https://github.com/settings/tokens

2. **Remove from Git history**
   ```bash
   # Use BFG Repo Cleaner (recommended)
   bfg --replace-text passwords.txt
   
   # Or filter-branch (more manual)
   git filter-branch --tree-filter 'rm -f path/to/file' HEAD
   git push --force
   ```

3. **Verify removal**
   ```bash
   git log -p --all | grep -i "your-secret"
   ```

4. **Generate new secret** and add to GitHub Secrets

5. **Notify affected services** if needed

---

## 🛡️ Security Best Practices / Лучшие практики безопасности

### 1. Use OIDC Trusted Publishing (PyPI)

✅ **Recommended**: No static tokens needed
```yaml
permissions:
  id-token: write  # Ephemeral tokens
```

❌ **Avoid**: Static API tokens when possible
```yaml
env:
  PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}  # Less secure
```

### 2. Principle of Least Privilege

- Give tokens minimal required permissions
- Use environment-specific secrets
- Rotate tokens regularly

### 3. Code Review

- Review all PRs for accidentally exposed secrets
- Use automated scanning tools
- Enable GitHub secret scanning

### 4. Dependencies

- Keep dependencies updated (Dependabot)
- Review security advisories
- Use `pip-audit` or `safety` for Python packages

```bash
pip install pip-audit
pip-audit
```

---

## 🔐 Current Secrets in This Project / Текущие секреты в проекте

| Secret Name         | Purpose                    | Where to Get                             | Rotation       |
| ------------------- | -------------------------- | ---------------------------------------- | -------------- |
| `READTHEDOCS_TOKEN` | Trigger ReadTheDocs builds | https://readthedocs.org/accounts/tokens/ | Every 6 months |
| `PYPI_API_TOKEN`    | ⚠️ Not used (we use OIDC)   | https://pypi.org/manage/account/token/   | N/A            |

---

## 📚 Resources / Ресурсы

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PyPI Security](https://pypi.org/help/#apitoken)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---

## 📝 Security Audit Log / Журнал безопасности

| Date       | Action                  | Details                                              |
| ---------- | ----------------------- | ---------------------------------------------------- |
| 2026-01-12 | Initial security review | Removed exposed ReadTheDocs token from documentation |
| 2026-01-12 | Added SECURITY.md       | Created security policy document                     |

---

## 📧 Contact / Контакты

For security concerns, please use:
- GitHub Security Advisories (preferred)
- Create issue with `[SECURITY]` tag (we'll follow up privately)

**Do not post security vulnerabilities in public issues!**

---

**Last Updated**: January 12, 2026  
**Version**: 1.0
