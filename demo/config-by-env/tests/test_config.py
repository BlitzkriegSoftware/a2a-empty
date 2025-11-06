# Tests
import json
import os
import random
import string
import pytest
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from src.config_by_env import ConfigByEnv

def generate_random_string(length):
    """Generates a random string of specified length containing letters and digits."""
    characters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

def make_env_vars(rule_json) -> list:
    key_list = []
    for item in rule_json:
            key = item['name']
            value = ""
            vtype = item['type']
            match vtype:
                case "int":
                    value = str(random.randint(1,10))

                case "float":
                    value = str(random.uniform(1,100))
            
                case _:
                    sLen = random.randint(7,16)
                    value = generate_random_string(sLen)
            
            os.environ[key] = value
            key_list.append(key)

    return key_list

@pytest.fixture
def rule_json():
     json_file_folder = os.path.join(os.path.dirname(__file__), '..')
     with open(os.path.join(json_file_folder,'config_rules.json'), 'r') as file:
          rules = json.load(file)
          return rules

@pytest.mark.unit
def test_write_up(rule_json):
    key_list = make_env_vars(rule_json)
    for key in key_list:
         value= os.environ[key]
         assert value is not None

@pytest.mark.unit
def test_validate_config(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None
    rules = ConfigByEnv.config_transform(rule_json)
    assert rules is not None
    nv = ConfigByEnv.config_validate(rules)
    assert nv is not None
