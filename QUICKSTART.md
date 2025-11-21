# Quick Start Guide

Get started with network automation CI/CD in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Validate a Configuration

```bash
python scripts/config_validator.py configs/devices/router-01.yaml
```

### 3. Generate Configuration

```bash
python scripts/config_generator.py configs/devices/router-01.yaml generated_configs/router-01.cfg
```

### 4. View Generated Config

```bash
cat generated_configs/router-01.cfg
```

## 📋 Using Make Commands

```bash
# Validate all configs
make validate

# Generate all configs
make generate

# Run tests
make test

# Deploy to staging (dry-run)
make deploy-staging
```

## 🔄 CI/CD Setup

### GitHub Actions

1. Push code to GitHub repository
2. Go to Settings → Secrets → Actions
3. Add required secrets (see README.md)
4. Push to `develop` or `main` branch
5. Check Actions tab for pipeline status

### Jenkins

1. Install Jenkins plugins:
   - Pipeline
   - Git
   - Credentials Binding

2. Create Pipeline job:
   - Point to repository
   - Use `Jenkinsfile` from root

3. Configure credentials (see DEPLOYMENT_GUIDE.md)

4. Run pipeline

## 📝 Create Your First Config

1. Copy an existing config:
```bash
cp configs/devices/router-01.yaml configs/devices/my-router.yaml
```

2. Edit the file with your device details

3. Validate:
```bash
python scripts/config_validator.py configs/devices/my-router.yaml
```

4. Generate:
```bash
python scripts/config_generator.py configs/devices/my-router.yaml generated_configs/my-router.cfg
```

## 🧪 Test Locally

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_config_validation.py::TestConfigValidation::test_valid_config -v
```

## 🔐 Environment Variables

For local deployment, set these:

```bash
export NETWORK_USERNAME=admin
export NETWORK_PASSWORD=your_password
export NETWORK_ENABLE_PASSWORD=enable_pass
```

## 📚 Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for deployment instructions
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

## 💡 Tips

- Always validate before generating
- Use dry-run mode for testing
- Review generated configs before deployment
- Start with staging environment
- Keep backups of device configs

## ❓ Common Issues

**Import errors?**
```bash
pip install -r requirements.txt
```

**Validation fails?**
- Check YAML syntax
- Verify all required fields
- Review error messages

**Connection issues?**
- Verify device IP addresses
- Check network connectivity
- Verify SSH credentials

---

Happy automating! 🎉

