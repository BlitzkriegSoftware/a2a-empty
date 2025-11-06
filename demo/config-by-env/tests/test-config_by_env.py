# Tests
import os
import json
import random
import pytest
from ..src import ConfigByEnv
from . import generate_random_string

def write_up(rule_json) -> list:
    key_list = []
    for item in rule_json:
            key = item.name
            value = ""
            vtype = item.type
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
     with open('./config-rules.json', 'r') as file:
          rules = json.load(file)
          return rules

@pytest.mark.unit
def test_write_up(rule_json):
    key_list = write_up(rule_json)
    for key in key_list:
         value= os.environ[key]
         assert value is not None
