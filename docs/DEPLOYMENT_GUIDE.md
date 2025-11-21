# Deployment Guide

This guide provides step-by-step instructions for deploying network configurations using the CI/CD pipeline.

## Prerequisites

Before deploying, ensure you have:

1. ✅ All configuration files validated
2. ✅ Generated configurations reviewed
3. ✅ Tests passing
4. ✅ Access to target devices
5. ✅ Credentials configured in GitHub Secrets (for CI/CD)

## Deployment Workflows

### Manual Deployment (Local)

#### 1. Validate Configurations

```bash
make validate
```

#### 2. Generate Configurations

```bash
make generate
```

#### 3. Review Generated Configs

```bash
cat generated_configs/router-01.cfg
```

#### 4. Deploy (Dry Run)

```bash
export NETWORK_USERNAME=admin
export NETWORK_PASSWORD=your_password
export NETWORK_ENABLE_PASSWORD=enable_pass

python scripts/config_deployer.py \
    configs/devices/router-01.yaml \
    generated_configs/router-01.cfg \
    --dry-run
```

#### 5. Deploy (Actual)

Remove `--dry-run` flag:

```bash
python scripts/config_deployer.py \
    configs/devices/router-01.yaml \
    generated_configs/router-01.cfg
```

### CI/CD Deployment (GitHub Actions)

#### Staging Deployment

1. Push changes to `develop` branch
2. GitHub Actions automatically:
   - Validates configurations
   - Generates configs
   - Runs tests
   - Deploys to staging (dry-run)

#### Production Deployment

**Option 1: Automatic (Main Branch)**
1. Merge to `main` branch
2. Pipeline automatically runs production deployment (dry-run)

**Option 2: Manual Workflow**
1. Go to Actions tab in GitHub
2. Select "Network Configuration CI/CD Pipeline"
3. Click "Run workflow"
4. Select environment: `production`
5. Click "Run workflow"

### CI/CD Deployment (Jenkins)

#### Setup Jenkins Credentials

1. Go to Jenkins → Credentials
2. Add credentials:
   - `staging-network-creds` (username/password)
   - `staging-enable-password` (string)
   - `production-network-creds` (username/password)
   - `production-enable-password` (string)

#### Run Pipeline

1. Create new Pipeline job
2. Point to repository with `Jenkinsfile`
3. Run pipeline:
   - **Staging**: Triggered on `develop` branch
   - **Production**: Triggered on `main` branch (requires approval)

## Deployment Checklist

### Pre-Deployment

- [ ] All configurations validated
- [ ] Generated configs reviewed
- [ ] Tests passing
- [ ] Backup of current device configs
- [ ] Maintenance window scheduled (if needed)
- [ ] Rollback plan prepared

### During Deployment

- [ ] Monitor deployment logs
- [ ] Verify device connectivity
- [ ] Check for errors
- [ ] Test critical functionality

### Post-Deployment

- [ ] Verify device configurations
- [ ] Test network connectivity
- [ ] Monitor device logs
- [ ] Document changes
- [ ] Update change management system

## Rollback Procedure

If deployment fails:

1. **Stop deployment**: Cancel running pipeline
2. **Restore backup**: Use saved device configurations
3. **Verify**: Test network functionality
4. **Investigate**: Review logs and identify issues
5. **Fix**: Correct configuration issues
6. **Retry**: Re-run deployment after fixes

## Troubleshooting

### Connection Issues

```bash
# Test SSH connectivity
ssh admin@192.168.1.1

# Check device reachability
ping 192.168.1.1
```

### Authentication Errors

- Verify credentials in GitHub Secrets
- Check device username/password
- Ensure enable password is correct

### Configuration Errors

- Review validation output
- Check YAML syntax
- Verify device compatibility

## Best Practices

1. **Always use dry-run first**: Test deployments before actual changes
2. **Deploy during maintenance windows**: Minimize impact on production
3. **Deploy one device at a time**: Easier to troubleshoot issues
4. **Keep backups**: Always backup before changes
5. **Document changes**: Record all configuration changes
6. **Monitor after deployment**: Watch for issues after changes

## Safety Features

- **Dry-run mode**: Default in CI/CD pipelines
- **Validation**: All configs validated before deployment
- **Testing**: Unit tests run before deployment
- **Approval gates**: Production deployments require approval
- **Rollback capability**: Easy to revert changes

## Support

For issues or questions:
1. Check logs in CI/CD pipeline
2. Review device logs
3. Consult troubleshooting section
4. Open an issue on GitHub

