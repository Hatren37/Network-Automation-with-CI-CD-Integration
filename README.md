# Network Automation with CI/CD Integration

This project implements Infrastructure as Code (IaC) principles for network configuration management with integrated CI/CD pipeline using GitHub Actions.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [CI/CD Pipeline](#cicd-pipeline)
- [Configuration Files](#configuration-files)
- [Scripts](#scripts)
- [Testing](#testing)
- [Deployment](#deployment)
- [Security](#security)

## 🎯 Overview

This solution provides a complete network automation workflow that:

- Manages network device configurations as code (YAML format)
- Validates configurations before deployment
- Generates device-specific configurations automatically
- Integrates with CI/CD pipelines for automated testing and deployment
- Supports dry-run mode for safe testing
- Provides comprehensive validation and error checking

## 📁 Project Structure

```
.
├── configs/
│   └── devices/          # Device configuration templates (YAML)
│       ├── router-01.yaml
│       └── router-02.yaml
├── scripts/
│   ├── config_generator.py    # Generates IOS configs from YAML
│   ├── config_validator.py    # Validates configuration files
│   └── config_deployer.py     # Deploys configs to devices
├── tests/
│   └── test_config_validation.py  # Unit tests
├── .github/
│   └── workflows/
│       └── network-ci-cd.yml  # GitHub Actions workflow
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md
```

## ✨ Features

- **Infrastructure as Code**: Network configurations stored in version-controlled YAML files
- **Automated Validation**: Pre-deployment validation of all configurations
- **CI/CD Integration**: GitHub Actions workflow for automated testing and deployment
- **Multi-Environment Support**: Separate staging and production deployment pipelines
- **Dry-Run Mode**: Test deployments without making actual changes
- **Comprehensive Testing**: Unit tests and integration tests
- **Error Handling**: Robust error checking and reporting

## 🔧 Prerequisites

- Python 3.9 or higher
- Git
- GitHub account (for CI/CD)
- Network devices accessible via SSH (for deployment)
- Required Python packages (install via `requirements.txt`)

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd network-automation-cicd
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure GitHub Secrets

For the CI/CD pipeline to work, configure the following secrets in your GitHub repository:

**Settings → Secrets and variables → Actions**

- `STAGING_NETWORK_USERNAME`: Username for staging devices
- `STAGING_NETWORK_PASSWORD`: Password for staging devices
- `STAGING_NETWORK_ENABLE_PASSWORD`: Enable password for staging
- `PRODUCTION_NETWORK_USERNAME`: Username for production devices
- `PRODUCTION_NETWORK_PASSWORD`: Password for production devices
- `PRODUCTION_NETWORK_ENABLE_PASSWORD`: Enable password for production

## 📝 Usage

### Validate Configuration

```bash
python scripts/config_validator.py configs/devices/router-01.yaml
```

### Generate Configuration

```bash
python scripts/config_generator.py configs/devices/router-01.yaml generated_configs/router-01.cfg
```

### Deploy Configuration (Dry Run)

```bash
python scripts/config_deployer.py configs/devices/router-01.yaml generated_configs/router-01.cfg --dry-run
```

### Deploy Configuration (Actual)

```bash
export NETWORK_USERNAME=admin
export NETWORK_PASSWORD=your_password
export NETWORK_ENABLE_PASSWORD=enable_pass

python scripts/config_deployer.py configs/devices/router-01.yaml generated_configs/router-01.cfg
```

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`network-ci-cd.yml`) includes the following stages:

### 1. **Validate** Stage
- Validates all YAML configuration files
- Checks for syntax errors and required fields
- Fails the pipeline if validation errors are found

### 2. **Generate** Stage
- Generates device-specific configurations from YAML templates
- Creates artifacts for use in subsequent stages

### 3. **Test** Stage
- Runs unit tests
- Validates generated configuration syntax
- Ensures configurations are properly formatted

### 4. **Deploy Staging** Stage
- Triggers on pushes to `develop` branch
- Deploys configurations to staging environment (dry-run mode)
- Uses staging credentials from GitHub secrets

### 5. **Deploy Production** Stage
- Triggers on pushes to `main` branch or manual workflow dispatch
- Deploys configurations to production environment (dry-run mode)
- Requires manual approval for production deployments

### 6. **Notify** Stage
- Sends notifications about pipeline status
- Can be extended with email/Slack integration

### Workflow Triggers

- **Automatic**: Pushes to `main` or `develop` branches
- **Pull Requests**: Validates changes before merging
- **Manual**: Workflow dispatch with environment selection

## 📄 Configuration Files

Configuration files are written in YAML format and follow this structure:

```yaml
device:
  hostname: router-01
  device_type: cisco_ios
  ip_address: 192.168.1.1
  credentials:
    username: admin
    password: ${DEVICE_PASSWORD}

interfaces:
  - name: GigabitEthernet0/0
    description: "Uplink to Core"
    ip_address: 192.168.1.1
    subnet_mask: 255.255.255.0
    status: up

routing:
  ospf:
    enabled: true
    process_id: 1
    networks:
      - network: 10.0.1.0
        wildcard: 0.0.0.255
        area: 0

security:
  access_lists:
    - name: "ACL-100"
      type: extended
      rules:
        - action: permit
          protocol: tcp
          source: 10.0.1.0
          source_wildcard: 0.0.0.255
          destination: any
          destination_port: 80
```

## 🛠️ Scripts

### `config_generator.py`
Converts YAML configuration templates to Cisco IOS commands.

**Usage:**
```bash
python scripts/config_generator.py <config_file.yaml> [output_file.cfg]
```

### `config_validator.py`
Validates YAML configuration files for errors and inconsistencies.

**Usage:**
```bash
python scripts/config_validator.py <config_file.yaml>
```

**Validates:**
- Device information (hostname, IP address)
- Interface configurations
- Routing protocols (OSPF)
- Security policies (ACLs)

### `config_deployer.py`
Deploys generated configurations to network devices using Netmiko.

**Usage:**
```bash
python scripts/config_deployer.py <config_file.yaml> <generated_config.cfg> [--dry-run]
```

**Features:**
- SSH connection to devices
- Configuration deployment
- Automatic save after deployment
- Dry-run mode for testing

## 🧪 Testing

Run unit tests:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=scripts --cov-report=html
```

## 🔐 Security

### Best Practices

1. **Never commit credentials**: Use environment variables or GitHub secrets
2. **Use dry-run mode**: Always test in dry-run mode first
3. **Review changes**: Review generated configurations before deployment
4. **Access control**: Limit who can trigger production deployments
5. **Audit logs**: Keep logs of all configuration changes

### Environment Variables

- `NETWORK_USERNAME`: Device username
- `NETWORK_PASSWORD`: Device password
- `NETWORK_ENABLE_PASSWORD`: Enable password

## 📊 Workflow Diagram

```
┌─────────────┐
│   Git Push  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Validate   │ ◄── Check YAML syntax & structure
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Generate   │ ◄── Create IOS configs from YAML
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Test     │ ◄── Run unit tests & syntax checks
└──────┬──────┘
       │
       ├──────────────┐
       │              │
       ▼              ▼
┌─────────────┐  ┌─────────────┐
│   Staging   │  │ Production  │
│  Deploy     │  │   Deploy    │
└─────────────┘  └─────────────┘
```

## 🎓 Learning Resources

- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Infrastructure as Code Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Ensure all tests pass
4. Submit a pull request

## 📝 License

This project is for educational purposes.

## ⚠️ Important Notes

- **Dry-run mode is enabled by default** in the CI/CD pipeline for safety
- To enable actual deployments, modify the workflow file and remove `--dry-run` flags
- Always test configurations in a lab environment before production deployment
- Review generated configurations before deploying to production devices

## 🐛 Troubleshooting

### Connection Issues
- Verify device IP addresses and network connectivity
- Check SSH credentials in GitHub secrets
- Ensure devices allow SSH connections

### Validation Errors
- Check YAML syntax
- Verify all required fields are present
- Review error messages for specific issues

### Deployment Failures
- Check device connectivity
- Verify credentials are correct
- Review device logs for errors

---

**Author**: Galimu Fred @IsbatUniversity  
**Last Updated**: 2025

