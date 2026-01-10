"""
YAML Configuration Parser Module

This module provides robust parsing and validation of YAML configuration files.
It supports multiple formats, inheritance, and environment variable substitution.
"""

import yaml
import re
import os
from typing import Any, Dict, List, Optional
from pathlib import Path


class ConfigParser:
    """
    Parse and validate YAML configuration files with support for:
    - Environment variable substitution
    - Configuration inheritance (extends)
    - Schema validation
    - Type conversion
    """
    
    def __init__(self, config_path: str):
        """
        Initialize the config parser.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = Path(config_path)
        self.config_data: Dict[str, Any] = {}
        self.schema: Optional[Dict] = None
        
    def load(self) -> Dict[str, Any]:
        """
        Load and parse the configuration file.
        
        Returns:
            Parsed configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML is malformed
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            self.config_data = yaml.safe_load(f)
        
        # Process inheritance
        if 'extends' in self.config_data:
            self._process_inheritance()
        
        # Substitute environment variables
        self.config_data = self._substitute_env_vars(self.config_data)
        
        return self.config_data
    
    def _process_inheritance(self):
        """Process the 'extends' directive to inherit from parent configs."""
        extends = self.config_data.get('extends', [])
        if isinstance(extends, str):
            extends = [extends]
        
        base_config = {}
        for parent_file in extends:
            parent_path = self.config_path.parent / parent_file
            if parent_path.exists():
                with open(parent_path, 'r') as f:
                    parent_data = yaml.safe_load(f)
                    base_config = self._deep_merge(base_config, parent_data)
        
        # Merge current config over base
        self.config_data = self._deep_merge(base_config, self.config_data)
        
        # Remove extends key
        self.config_data.pop('extends', None)
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """
        Deep merge two dictionaries.
        
        Args:
            base: Base configuration
            override: Override configuration
            
        Returns:
            Merged configuration
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _substitute_env_vars(self, data: Any) -> Any:
        """
        Recursively substitute environment variables in the format ${VAR_NAME}.
        
        Args:
            data: Configuration data (dict, list, or string)
            
        Returns:
            Data with environment variables substituted
        """
        if isinstance(data, dict):
            return {k: self._substitute_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._substitute_env_vars(item) for item in data]
        elif isinstance(data, str):
            # Find all ${VAR} patterns
            pattern = r'\$\{([^}]+)\}'
            matches = re.finditer(pattern, data)
            
            result = data
            for match in matches:
                var_name = match.group(1)
                var_value = os.environ.get(var_name, '')
                result = result.replace(match.group(0), var_value)
            
            return result
        else:
            return data
    
    def validate(self, schema: Dict) -> bool:
        """
        Validate configuration against a schema.
        
        Args:
            schema: Validation schema
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        self.schema = schema
        self._validate_dict(self.config_data, schema)
        return True
    
    def _validate_dict(self, data: Dict, schema: Dict, path: str = ""):
        """
        Recursively validate dictionary against schema.
        
        Args:
            data: Configuration data to validate
            schema: Schema definition
            path: Current path in the config tree (for error messages)
        """
        schema_props = schema.get('properties', {})
        required = schema.get('required', [])
        
        # Check required fields
        for field in required:
            if field not in data:
                raise ValueError(f"Missing required field: {path}.{field}" if path else field)
        
        # Validate each field
        for key, value in data.items():
            field_path = f"{path}.{key}" if path else key
            
            if key in schema_props:
                field_schema = schema_props[key]
                self._validate_value(value, field_schema, field_path)
    
    def _validate_value(self, value: Any, schema: Dict, path: str):
        """Validate a single value against its schema."""
        expected_type = schema.get('type')
        
        if expected_type == 'string' and not isinstance(value, str):
            raise ValueError(f"Field {path} must be a string")
        elif expected_type == 'integer' and not isinstance(value, int):
            raise ValueError(f"Field {path} must be an integer")
        elif expected_type == 'number' and not isinstance(value, (int, float)):
            raise ValueError(f"Field {path} must be a number")
        elif expected_type == 'boolean' and not isinstance(value, bool):
            raise ValueError(f"Field {path} must be a boolean")
        elif expected_type == 'array' and not isinstance(value, list):
            raise ValueError(f"Field {path} must be an array")
        elif expected_type == 'object' and isinstance(value, dict):
            self._validate_dict(value, schema, path)
        
        # Validate constraints
        if 'minimum' in schema and value < schema['minimum']:
            raise ValueError(f"Field {path} must be >= {schema['minimum']}")
        if 'maximum' in schema and value > schema['maximum']:
            raise ValueError(f"Field {path} must be <= {schema['maximum']}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'server.host')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'server.host')
            value: Value to set
        """
        keys = key.split('.')
        target = self.config_data
        
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        target[keys[-1]] = value
    
    def save(self, output_path: Optional[str] = None):
        """
        Save configuration to a YAML file.
        
        Args:
            output_path: Path to save to (defaults to original path)
        """
        path = Path(output_path) if output_path else self.config_path
        
        with open(path, 'w') as f:
            yaml.dump(self.config_data, f, default_flow_style=False, sort_keys=False)


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Convenience function to load a configuration file.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        Parsed configuration dictionary
    """
    parser = ConfigParser(config_path)
    return parser.load()


# Example usage
if __name__ == "__main__":
    # Load configuration
    config = load_config("config.yaml")
    
    # Access values
    host = config.get('server', {}).get('host', 'localhost')
    port = config.get('server', {}).get('port', 8080)
    
    print(f"Server: {host}:{port}")
