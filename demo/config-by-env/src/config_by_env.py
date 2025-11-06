import os
import re

from config_rule import ConfigurationRule

class ConfigByEnv:

    def __init__(self, config_rules_json):
        self.config_rules = self.config_transform(config_rules_json)
        self.key_values = self.config_validate(self.config_rules)
    
    @staticmethod
    def config_transform(config_rules_json):
        rules= {}
        for item in config_rules_json:
            name = item['name']
            if(len(name) < 1):
                raise ValueError("Name is a required field")
            vtype = item['type']
            if(len(vtype) < 1):
                vtype = "str"
            vregex = item['regex']
            if(len(vregex) < 1):
                vregex = None
            required = bool(item['required'])
            min = item['min']
            if(len(min) < 1): 
                min = None
            max = item['max']
            if(len(max) < 1):
                max = None
            cfg = ConfigurationRule.from_Args(name, vtype, vregex, required, min, max)
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
            fallback = self.config_rules[key].vdefault
            svalue = os.environ[key].strip()
            required = self.config_rules[key].required

            match vtype:
                case "int":
                    if len(svalue) < 1:
                        if(default_value is not None):
                            return int(default_value)
                        elif(not required) and len(fallback) > 0:
                            return int(fallback)
                        else:
                            return 0
                    else:
                        ivalue = int(svalue)
                        return ivalue

                case "float":
                    if len(svalue) < 1:
                        if(default_value is not None):
                            return float(default_value)
                        elif(not required) and len(fallback) > 0:
                            return float(fallback)
                        else:
                            return 0.0
                    else:
                        fvalue = float(svalue)
                        return fvalue

                case _:
                    if len(svalue) < 1:
                        if(default_value is not None):
                            return default_value
                        elif(not required):
                            return fallback
                    else:
                        return svalue
        else:
            return None
