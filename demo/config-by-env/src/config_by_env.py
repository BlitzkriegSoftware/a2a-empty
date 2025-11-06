import os
import re

from config_rule import ConfigurationRule

"""
Requires environment variables to be set
"""
class ConfigByEnv:
    def ___init___(self, config_rules_json):
        self.config_rules = self.config_transform(config_rules_json)
        self.key_values = self.config_validate(self.config_rules)
        pass
    
    @staticmethod
    def config_transform(config_rules_json):
        rules= {}
        for item in config_rules_json:
            name = item.name
            if(len(name) < 1):
                raise ValueError("Name is a required field")
            vtype = item.type
            if(len(vtype) < 1):
                vtype = "str"
            vregex = item.regex
            if(len(vregex) < 1):
                vregex = None
            required = bool(item.required)
            min = item.min
            if(len(min) < 1): 
                min = None
            max = item.max
            if(len(max) < 1):
                max = None
            cfg = ConfigurationRule.static_factory(name, vtype, vregex, required, min, max)
            rules[name] = cfg
        
        return rules

    @staticmethod
    def config_validate(config_rules : dict):
        key_values = {}
        for key, rule in config_rules.items():
            value = os.environ[key]
            
            if(len(value) < 1 and rule.required):
                raise ValueError(f"{key} must have a value")
            
            if(rule.vregex is not None) and (len(rule.vregex) > 0):
                match_object = re.match(rule.vregex, value)
                if not match_object:
                    raise ValueError(f"{key} does not validate to regex {rule.vregex}")
            
            match rule.vtype:
                case "int":
                    ivalue = int(value)
                    if(rule.min is not None):
                        lbound = int(rule.min)
                        if(ivalue < lbound):
                            raise ValueError(f"{key}, int value {ivalue} must be greater than {lbound}")
                    if(rule.max is not None):
                        ubound = int(rule.max)
                        if(ivalue > ubound):
                            raise ValueError(f"{key}, int value {ivalue} must be less than {ubound}")
                        
                case "float":
                    ivalue = float(value)
                    if(rule.min is not None):
                        lbound = float(rule.min)
                        if(ivalue < lbound):
                            raise ValueError(f"{key}, float value {ivalue} must be greater than {lbound}")
                    if(rule.max is not None):
                        ubound = float(rule.max)
                        if(ivalue > ubound):
                            raise ValueError(f"{key}, float value {ivalue} must be less than {ubound}")

                case _:
                    pass
            
            # Set the actual key/value
            key_values[key] = value
    
        return key_values
    
    def config_get(self, key: str, default_value = None):
        if key in self.config_rules:
            vtype = self.config_rules[key].vtype
            match vtype:
                case "int":
                    return self.config_get_int(key)
                case "float":
                    return self.config_get_float(key)
                case _:
                    return self.config_get_string(key)
        else:
            return None

    def config_get_string(self, key: str, default_value: str = "") -> str:
        if key in self.key_values:
            return self.key_values[key]
        else:
            return default_value
    
    def config_get_int(self, key: str, default_value: int = 0) -> int:
        if key in self.key_values:
            return int(self.key_values[key])
        else:
            return default_value

    def config_get_float(self, key: str, default_value: float = 0.0) -> float:
        if key in self.key_values:
            return float(self.key_values[key])
        else:
            return default_value
        
    