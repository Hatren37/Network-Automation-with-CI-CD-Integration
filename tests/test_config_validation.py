#!/usr/bin/env python3
"""
Unit tests for configuration validation
"""

import unittest
import yaml
import tempfile
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from config_validator import ConfigValidator


class TestConfigValidation(unittest.TestCase):
    """Test cases for configuration validation"""
    
    def create_temp_config(self, config_dict):
        """Create a temporary YAML config file"""
        fd, path = tempfile.mkstemp(suffix='.yaml')
        try:
            with os.fdopen(fd, 'w') as f:
                yaml.dump(config_dict, f)
            return path
        except Exception:
            os.close(fd)
            os.unlink(path)
            raise
    
    def test_valid_config(self):
        """Test validation of a valid configuration"""
        config = {
            'device': {
                'hostname': 'test-router',
                'ip_address': '192.168.1.1',
                'device_type': 'cisco_ios'
            },
            'interfaces': [
                {
                    'name': 'GigabitEthernet0/0',
                    'description': 'Test Interface',
                    'ip_address': '10.0.0.1',
                    'subnet_mask': '255.255.255.0',
                    'status': 'up'
                }
            ]
        }
        
        config_file = self.create_temp_config(config)
        try:
            validator = ConfigValidator(config_file)
            validator.validate_all()
            self.assertTrue(validator.is_valid(), "Valid config should pass validation")
        finally:
            os.unlink(config_file)
    
    def test_missing_hostname(self):
        """Test validation fails when hostname is missing"""
        config = {
            'device': {
                'ip_address': '192.168.1.1',
                'device_type': 'cisco_ios'
            }
        }
        
        config_file = self.create_temp_config(config)
        try:
            validator = ConfigValidator(config_file)
            validator.validate_all()
            self.assertFalse(validator.is_valid(), "Config without hostname should fail")
            self.assertTrue(any('hostname' in error.lower() for error in validator.errors))
        finally:
            os.unlink(config_file)
    
    def test_invalid_ip_address(self):
        """Test validation fails with invalid IP address"""
        config = {
            'device': {
                'hostname': 'test-router',
                'ip_address': '999.999.999.999',
                'device_type': 'cisco_ios'
            }
        }
        
        config_file = self.create_temp_config(config)
        try:
            validator = ConfigValidator(config_file)
            validator.validate_all()
            self.assertFalse(validator.is_valid(), "Config with invalid IP should fail")
        finally:
            os.unlink(config_file)
    
    def test_interface_without_subnet_mask(self):
        """Test validation fails when interface has IP but no subnet mask"""
        config = {
            'device': {
                'hostname': 'test-router',
                'ip_address': '192.168.1.1',
                'device_type': 'cisco_ios'
            },
            'interfaces': [
                {
                    'name': 'GigabitEthernet0/0',
                    'ip_address': '10.0.0.1',
                    'status': 'up'
                }
            ]
        }
        
        config_file = self.create_temp_config(config)
        try:
            validator = ConfigValidator(config_file)
            validator.validate_all()
            self.assertFalse(validator.is_valid(), "Interface with IP but no mask should fail")
        finally:
            os.unlink(config_file)


if __name__ == '__main__':
    unittest.main()

