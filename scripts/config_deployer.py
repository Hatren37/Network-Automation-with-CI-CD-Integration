#!/usr/bin/env python3
"""
Network Configuration Deployer
Deploys configurations to network devices using Netmiko
"""

import yaml
import sys
import os
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


class ConfigDeployer:
    """Deploys network configurations to devices"""
    
    def __init__(self, config_file, dry_run=False):
        self.config_file = config_file
        self.config = self._load_config()
        self.dry_run = dry_run
        self.device_config = None
    
    def _load_config(self):
        """Load YAML configuration file"""
        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file {self.config_file} not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            sys.exit(1)
    
    def _load_generated_config(self, config_path):
        """Load generated configuration file"""
        try:
            with open(config_path, 'r') as f:
                self.device_config = f.read()
        except FileNotFoundError:
            print(f"Error: Generated configuration file {config_path} not found")
            sys.exit(1)
    
    def connect_to_device(self):
        """Establish connection to network device"""
        device_info = self.config['device']
        
        # Get credentials from environment variables
        username = os.getenv('NETWORK_USERNAME', device_info['credentials']['username'])
        password = os.getenv('NETWORK_PASSWORD', device_info['credentials']['password'])
        
        device_params = {
            'device_type': device_info['device_type'],
            'host': device_info['ip_address'],
            'username': username,
            'password': password,
            'secret': os.getenv('NETWORK_ENABLE_PASSWORD', ''),
        }
        
        try:
            connection = ConnectHandler(**device_params)
            print(f"✓ Connected to {device_info['hostname']} ({device_info['ip_address']})")
            return connection
        except NetmikoTimeoutException:
            print(f"✗ Connection timeout to {device_info['ip_address']}")
            sys.exit(1)
        except NetmikoAuthenticationException:
            print(f"✗ Authentication failed for {device_info['ip_address']}")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Connection error: {e}")
            sys.exit(1)
    
    def deploy_config(self, connection, config_commands):
        """Deploy configuration to device"""
        if self.dry_run:
            print("\n[DRY RUN] Would deploy the following configuration:")
            print("-" * 50)
            print(config_commands)
            print("-" * 50)
            return True
        
        try:
            # Enter enable mode if needed
            if connection.check_enable_mode():
                connection.enable()
            
            # Send configuration commands
            output = connection.send_config_set(config_commands.split('\n'))
            print("\n✓ Configuration deployed successfully")
            print("\nDevice output:")
            print(output)
            
            # Save configuration
            connection.save_config()
            print("\n✓ Configuration saved to device")
            
            return True
        except Exception as e:
            print(f"\n✗ Deployment failed: {e}")
            return False
    
    def verify_connection(self, connection):
        """Verify device connectivity and basic info"""
        try:
            output = connection.send_command("show version")
            print("\nDevice Information:")
            print("-" * 50)
            # Extract hostname from show version or use config
            hostname = self.config['device']['hostname']
            print(f"Hostname: {hostname}")
            print("-" * 50)
            return True
        except Exception as e:
            print(f"✗ Verification failed: {e}")
            return False
    
    def deploy(self, generated_config_path):
        """Main deployment function"""
        self._load_generated_config(generated_config_path)
        
        if self.dry_run:
            print("\n[DRY RUN MODE - No changes will be made]")
        
        connection = self.connect_to_device()
        
        try:
            self.verify_connection(connection)
            success = self.deploy_config(connection, self.device_config)
            return success
        finally:
            connection.disconnect()
            print("\n✓ Disconnected from device")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy network configuration to device')
    parser.add_argument('config_file', help='YAML configuration file')
    parser.add_argument('generated_config', help='Generated configuration file to deploy')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode (no actual deployment)')
    
    args = parser.parse_args()
    
    deployer = ConfigDeployer(args.config_file, dry_run=args.dry_run)
    success = deployer.deploy(args.generated_config)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

