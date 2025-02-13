import pytest
from src.main.policies.home_policy import HomePolicy

def test_home_policy_creation_valid(valid_home_policy_data):
    policy = HomePolicy(**valid_home_policy_data)
    assert policy.age == valid_home_policy_data["age"]
    assert policy.flood_risk == valid_home_policy_data["flood_risk"]
    assert policy.n_parrots == valid_home_policy_data["n_parrots"]
    assert policy.windows == valid_home_policy_data["windows"]
    assert policy.outcome == valid_home_policy_data["outcome"]
    assert policy.policy_type == "home"

def test_home_policy_invalid_age():
    with pytest.raises(ValueError, match="Age must be a positive integer."):
        HomePolicy(age=-1, flood_risk="LOW", n_parrots=0, windows={"intact": 1}, outcome="OK")

def test_home_policy_invalid_flood_risk():
    with pytest.raises(ValueError, match="Flood risk must be one of 'HIGH', 'MEDIUM', 'LOW'."):
        HomePolicy(age=30, flood_risk="EXTREME", n_parrots=0, windows={"intact": 1}, outcome = "OK")

def test_home_policy_invalid_n_parrots():
    #TODO
    pass

def test_home_policy_invalid_windows_type():
    #TODO
    pass

def test_home_policy_invalid_windows_value():
    #TODO
    pass

def test_home_policy_invalid_outcome_value():
    #TODO
    pass
