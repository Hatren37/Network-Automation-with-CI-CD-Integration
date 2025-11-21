.PHONY: help install validate generate test deploy-staging deploy-production clean

help:
	@echo "Network Automation CI/CD - Available Commands:"
	@echo "  make install          - Install Python dependencies"
	@echo "  make validate         - Validate all configuration files"
	@echo "  make generate         - Generate device configurations"
	@echo "  make test             - Run unit tests"
	@echo "  make deploy-staging   - Deploy to staging (dry-run)"
	@echo "  make deploy-production - Deploy to production (dry-run)"
	@echo "  make clean            - Clean generated files"

install:
	pip install -r requirements.txt

validate:
	@echo "Validating all configuration files..."
	@for config_file in configs/devices/*.yaml; do \
		echo "Validating $$config_file..."; \
		python scripts/config_validator.py "$$config_file" || exit 1; \
	done

generate:
	@echo "Generating device configurations..."
	@mkdir -p generated_configs
	@for config_file in configs/devices/*.yaml; do \
		device_name=$$(basename "$$config_file" .yaml); \
		output_file="generated_configs/$${device_name}.cfg"; \
		echo "Generating config for $$device_name..."; \
		python scripts/config_generator.py "$$config_file" "$$output_file"; \
	done

test:
	pytest tests/ -v

deploy-staging:
	@echo "Deploying to staging environment (dry-run)..."
	@for config_file in configs/devices/*.yaml; do \
		device_name=$$(basename "$$config_file" .yaml); \
		generated_config="generated_configs/$${device_name}.cfg"; \
		if [ -f "$$generated_config" ]; then \
			echo "Deploying $$device_name..."; \
			python scripts/config_deployer.py "$$config_file" "$$generated_config" --dry-run || true; \
		fi; \
	done

deploy-production:
	@echo "⚠️  PRODUCTION DEPLOYMENT (DRY RUN MODE)"
	@for config_file in configs/devices/*.yaml; do \
		device_name=$$(basename "$$config_file" .yaml); \
		generated_config="generated_configs/$${device_name}.cfg"; \
		if [ -f "$$generated_config" ]; then \
			echo "Deploying $$device_name..."; \
			python scripts/config_deployer.py "$$config_file" "$$generated_config" --dry-run || true; \
		fi; \
	done

clean:
	rm -rf generated_configs/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

