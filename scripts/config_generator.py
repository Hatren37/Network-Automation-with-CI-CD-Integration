#!/usr/bin/env python3
"""
Network Configuration Generator
Converts YAML device configurations to Cisco IOS commands
"""

import yaml
import os
import sys
from pathlib import Path


class ConfigGenerator:
    """Generates network device configurations from YAML templates"""
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self._load_config()
    
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
    
    def generate_hostname(self):
        """Generate hostname configuration"""
        hostname = self.config['device']['hostname']
        return f"hostname {hostname}\n"
    
    def generate_interfaces(self):
        """Generate interface configurations"""
        commands = []
        for interface in self.config.get('interfaces', []):
            name = interface['name']
            commands.append(f"interface {name}")
            commands.append(f" description {interface['description']}")
            if interface['status'] == 'up':
                commands.append(" no shutdown")
            else:
                commands.append(" shutdown")
            if 'ip_address' in interface:
                ip = interface['ip_address']
                mask = interface['subnet_mask']
                commands.append(f" ip address {ip} {mask}")
            commands.append("!")
        return "\n".join(commands) + "\n"
    
    def generate_ospf(self):
        """Generate OSPF routing configuration"""
        commands = []
        ospf_config = self.config.get('routing', {}).get('ospf', {})
        
        if ospf_config.get('enabled', False):
            process_id = ospf_config['process_id']
            commands.append(f"router ospf {process_id}")
            for network in ospf_config.get('networks', []):
                net = network['network']
                wildcard = network['wildcard']
                area = network['area']
                commands.append(f" network {net} {wildcard} area {area}")
            commands.append("!")
        
        return "\n".join(commands) + "\n" if commands else ""
    
    def generate_acl(self):
        """Generate access control list configuration"""
        commands = []
        acls = self.config.get('security', {}).get('access_lists', [])
        
        for acl in acls:
            acl_name = acl['name']
            acl_type = acl['type']
            for rule in acl.get('rules', []):
                action = rule['action']
                protocol = rule['protocol']
                source = rule['source']
                src_wildcard = rule.get('source_wildcard', '0.0.0.0')
                destination = rule.get('destination', 'any')
                dst_port = rule.get('destination_port', '')
                
                if acl_type == 'extended':
                    if dst_port:
                        cmd = f"access-list {acl_name} {action} {protocol} {source} {src_wildcard} {destination} eq {dst_port}"
                    else:
                        cmd = f"access-list {acl_name} {action} {protocol} {source} {src_wildcard} {destination}"
                    commands.append(cmd)
        
        return "\n".join(commands) + "\n" if commands else ""
    
    def generate_full_config(self):
        """Generate complete device configuration"""
        config_lines = []
        config_lines.append("! Generated Configuration")
        config_lines.append("! Device: " + self.config['device']['hostname'])
        config_lines.append("!")
        config_lines.append(self.generate_hostname())
        config_lines.append(self.generate_interfaces())
        config_lines.append(self.generate_ospf())
        config_lines.append(self.generate_acl())
        config_lines.append("end")
        
        return "\n".join(config_lines)
    
    def save_config(self, output_file):
        """Save generated configuration to file"""
        config = self.generate_full_config()
        with open(output_file, 'w') as f:
            f.write(config)
        print(f"Configuration saved to {output_file}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python config_generator.py <config_file.yaml> [output_file.txt]")
        sys.exit(1)
    
    config_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else config_file.replace('.yaml', '.cfg')
    
    generator = ConfigGenerator(config_file)
    generator.save_config(output_file)
    
    # Also print to stdout for CI/CD pipelines
    print("\n--- Generated Configuration ---")
    print(generator.generate_full_config())


if __name__ == "__main__":
    main()

