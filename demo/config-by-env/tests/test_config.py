# Tests
import json
import os
import random
import string
import pytest
import sys
from datetime import date, timedelta
from src.config_rule import ConfigurationRule

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from src.config_by_env import ConfigByEnv

def generate_random_string(length):
    """Generates a random string of specified length containing letters and digits."""
    characters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


def generate_random_date() -> date:
    days_to_add = random.randint(10,100)
    start_date = date.today()
    new_date = start_date + timedelta(days=days_to_add) 
    return new_date

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
                
                case "date":
                    value = generate_random_date().strftime("%Y-%m-%d")

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
         value= os.environ.get(key)
         assert value is not None

@pytest.mark.unit
def test_validate_config(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None
    rules = ConfigByEnv.config_transform(rule_json)
    assert rules is not None
    nv = ConfigByEnv.config_validate(rules)
    assert nv is not None

@pytest.mark.unit
def test_ConfigurationRule_ctor():
    cr = ConfigurationRule(
        "key",
        "int",
        "[0-9]*",
        True,
        0,
        99
    )
    assert cr is not None

@pytest.mark.unit
def test_config_ctor(rule_json):
     key_list = make_env_vars(rule_json)
     assert key_list is not None
     config = ConfigByEnv(rule_json)
     assert config is not None

@pytest.mark.unit
def test_config_getter_good(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None
    config = ConfigByEnv(rule_json)
    assert config is not None

    for key in key_list:
        value = config.config_get(key)
        assert value is not None

@pytest.mark.unit
def test_config_getter_badkey(rule_json):
     key_list = make_env_vars(rule_json)
     assert key_list is not None
     config = ConfigByEnv(rule_json)
     assert config is not None

     key = "bad_1"
     value = config.config_get(key)
     assert value is None

@pytest.mark.unit
def test_config_getter_404(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None
    config = ConfigByEnv(rule_json)
    assert config is not None

    key = "bad_2"
    dflt = "cool"
    value = config.config_get(key, dflt)
    assert value is None

@pytest.mark.unit
def test_config_getter_cleared_str(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None
    config = ConfigByEnv(rule_json)
    assert config is not None

    key = "key_str_1"
    os.environ.pop(key, None)

    value = config.config_get(key)
    assert value is None

    dflt = "cool"
    value = config.config_get(key, dflt)
    assert value == dflt

@pytest.mark.unit
def test_config_getter_cleared_int(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None
    config = ConfigByEnv(rule_json)
    assert config is not None

    key = "key_int_1"
    os.environ.pop(key, None)

    value = config.config_get(key)
    assert value == 0

    dflt = 9
    value = config.config_get(key, dflt)
    assert value == dflt


@pytest.mark.unit
def test_config_getter_cleared_date(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None
    config = ConfigByEnv(rule_json)
    assert config is not None

    key = "key_date_1"
    os.environ.pop(key, None)

    value = config.config_get(key)
    assert value is None

    dflt = "2023-04-07"
    value = config.config_get(key, dflt)
    assert value == ConfigByEnv.to_date(dflt)

@pytest.mark.unit
def test_config_getter_cleared_float(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None
    config = ConfigByEnv(rule_json)
    assert config is not None

    key = "key_float_1"
    os.environ.pop(key, None)

    value = config.config_get(key)
    assert value == 0.0

    dflt = 9.0
    value = config.config_get(key, dflt)
    assert value == dflt

@pytest.mark.unit
def test_config_getter_date_outrng_high(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None

    key = "key_date_1"
    os.environ[key] ="2035-12-31"

    with pytest.raises(ValueError):
        _ = ConfigByEnv(rule_json)

@pytest.mark.unit
def test_config_getter_date_outrng_low(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None

    key = "key_date_1"
    os.environ[key] ="1901-12-31"

    with pytest.raises(ValueError):
        _ = ConfigByEnv(rule_json)

@pytest.mark.unit
def test_config_getter_int_outrng_high(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None

    key = "key_int_1"
    os.environ[key] ="99999"

    with pytest.raises(ValueError):
        _ = ConfigByEnv(rule_json)

@pytest.mark.unit
def test_config_getter_int_outrng_low(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None

    key = "key_int_1"
    os.environ[key] ="-9"

    with pytest.raises(ValueError):
        _ = ConfigByEnv(rule_json)

@pytest.mark.unit
def test_config_getter_float_outrng_high(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None

    key = "key_float_1"
    os.environ[key] ="99999"

    with pytest.raises(ValueError):
        _ = ConfigByEnv(rule_json)

@pytest.mark.unit
def test_config_getter_float_outrng_low(rule_json):
    key_list = make_env_vars(rule_json)
    assert key_list is not None

    key = "key_float_1"
    os.environ[key] ="-9"

    with pytest.raises(ValueError):
        _ = ConfigByEnv(rule_json)
