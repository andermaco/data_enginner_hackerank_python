import pytest
from main.policies.house_policy import HousePolicy

def test_house_policy_creation_valid(valid_house_policy_data):
    policy = HousePolicy(**valid_house_policy_data)
    assert policy.age == valid_house_policy_data["age"]
    assert policy.flood_risk == valid_house_policy_data["flood_risk"]
    assert policy.n_parrots == valid_house_policy_data["n_parrots"]
    assert policy.windows == valid_house_policy_data["windows"]
    assert policy.outcome == valid_house_policy_data["outcome"]
    assert policy.policy_type == "house"

def test_house_policy_invalid_age():
    with pytest.raises(ValueError, match="Age must be a positive integer."):
        HousePolicy(age=-1, flood_risk="LOW", n_parrots=0, windows={"intact": 1}, outcome="OK")

def test_house_policy_invalid_flood_risk():
    with pytest.raises(ValueError, match="Flood risk must be one of 'HIGH', 'MEDIUM', 'LOW'."):
        HousePolicy(age=30, flood_risk="EXTREME", n_parrots=0, windows={"intact": 1}, outcome = "OK")

def test_house_policy_invalid_n_parrots():
    #TODO
    pass

def test_house_policy_invalid_windows_type():
    #TODO
    pass

def test_house_policy_invalid_windows_value():
    #TODO
    pass

def test_house_policy_invalid_outcome_value():
    #TODO
    pass
