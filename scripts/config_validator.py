#!/usr/bin/env python3
"""
Network Configuration Validator
Validates network configurations before deployment
"""

import yaml
import sys
import re
from pathlib import Path


class ConfigValidator:
    """Validates network device configurations"""
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self._load_config()
        self.errors = []
        self.warnings = []
    
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
    
    def validate_ip_address(self, ip):
        """Validate IP address format"""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
        
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    
    def validate_subnet_mask(self, mask):
        """Validate subnet mask format"""
        return self.validate_ip_address(mask)
    
    def validate_device_info(self):
        """Validate device information"""
        device = self.config.get('device', {})
        
        if not device.get('hostname'):
            self.errors.append("Device hostname is required")
        
        if not device.get('ip_address'):
            self.errors.append("Device IP address is required")
        elif not self.validate_ip_address(device['ip_address']):
            self.errors.append(f"Invalid IP address: {device['ip_address']}")
        
        if not device.get('device_type'):
            self.warnings.append("Device type not specified, defaulting to cisco_ios")
    
    def validate_interfaces(self):
        """Validate interface configurations"""
        interfaces = self.config.get('interfaces', [])
        
        if not interfaces:
            self.warnings.append("No interfaces configured")
            return
        
        for idx, interface in enumerate(interfaces):
            if not interface.get('name'):
                self.errors.append(f"Interface {idx}: name is required")

            if not interface.get('description'):
                self.errors.append(f"Interface {interface.get('name', idx)}: description is required")

            if not interface.get('status'):
                self.errors.append(f"Interface {interface.get('name', idx)}: status is required")
            
            if 'ip_address' in interface:
                ip = interface['ip_address']
                if not self.validate_ip_address(ip):
                    self.errors.append(f"Interface {interface.get('name', idx)}: Invalid IP address {ip}")
                
                if 'subnet_mask' not in interface:
                    self.errors.append(f"Interface {interface.get('name', idx)}: Subnet mask required when IP is configured")
                elif not self.validate_subnet_mask(interface['subnet_mask']):
                    self.errors.append(f"Interface {interface.get('name', idx)}: Invalid subnet mask")
    
    def validate_routing(self):
        """Validate routing configurations"""
        routing = self.config.get('routing', {})
        ospf = routing.get('ospf', {})
        
        if ospf.get('enabled', False):
            if not ospf.get('process_id'):
                self.errors.append("OSPF process ID is required when OSPF is enabled")
            
            networks = ospf.get('networks', [])
            if not networks:
                self.warnings.append("OSPF enabled but no networks configured")
            
            for idx, network in enumerate(networks):
                if not self.validate_ip_address(network.get('network', '')):
                    self.errors.append(f"OSPF network {idx}: Invalid network address")
                if not self.validate_ip_address(network.get('wildcard', '')):
                    self.errors.append(f"OSPF network {idx}: Invalid wildcard mask")
                if network.get('area') is None:
                    self.errors.append(f"OSPF network {idx}: Area is required")
    
    def validate_security(self):
        """Validate security configurations"""
        security = self.config.get('security', {})
        acls = security.get('access_lists', [])
        
        for acl in acls:
            if not acl.get('name'):
                self.errors.append("ACL name is required")
            
            if acl.get('type') not in ['standard', 'extended']:
                self.errors.append(f"ACL {acl.get('name')}: Type must be 'standard' or 'extended'")
            
            for rule in acl.get('rules', []):
                if rule.get('action') not in ['permit', 'deny']:
                    self.errors.append(f"ACL {acl.get('name')}: Rule action must be 'permit' or 'deny'")

                if not rule.get('protocol'):
                    self.errors.append(f"ACL {acl.get('name')}: Rule protocol is required")
                elif rule.get('protocol') not in ['tcp', 'udp', 'ip', 'icmp']:
                    self.warnings.append(f"ACL {acl.get('name')}: Uncommon protocol {rule.get('protocol')}")

                if not rule.get('source'):
                    self.errors.append(f"ACL {acl.get('name')}: Rule source is required")
    
    def validate_all(self):
        """Run all validation checks"""
        self.validate_device_info()
        self.validate_interfaces()
        self.validate_routing()
        self.validate_security()
    
    def is_valid(self):
        """Check if configuration is valid"""
        return len(self.errors) == 0
    
    def print_results(self):
        """Print validation results"""
        print(f"\n=== Validation Results for {self.config_file} ===")
        
        if self.warnings:
            print("\nWarnings:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"  ✗ {error}")
            print(f"\n✗ Validation FAILED: {len(self.errors)} error(s) found")
            return False
        else:
            print("\n✓ Validation PASSED: Configuration is valid")
            return True


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python config_validator.py <config_file.yaml>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    validator = ConfigValidator(config_file)
    validator.validate_all()
    
    if not validator.print_results():
        sys.exit(1)


if __name__ == "__main__":
    main()

