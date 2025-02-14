import pytest
from datetime import date, timedelta
from main.policies.vehicle_policy import VehiclePolicy, AccidentHistory
from main.policies.house_policy import HousePolicy
from main.premium_calculator import PremiumCalculator
from main.exceptions.insurance import CarToOldException, CarDemotionDerbyException, TooManyParrotsException, BrokenWindowsException
# Vehicle Policy Tests


def test_vehicle_policy_valid():
    policy = VehiclePolicy(age="25 years", accident_history=[])
    assert policy.age == "25 years"
    assert policy.policy_type == "vehicle"
    assert policy.accident_history == []


def test_vehicle_policy_invalid_age():
    with pytest.raises(ValueError) as e:
        VehiclePolicy(age="invalid date", accident_history=[])
    assert "Age must be a string with the format '<number> years'." in str(e.value)


def test_vehicle_policy_invalid_accident_history_type():
    with pytest.raises(TypeError) as e:
        VehiclePolicy(age="25 years", accident_history="invalid")
    assert "accident_history must be a list." in str(e.value)

def test_vehicle_policy_invalid_accident_history_content():
    with pytest.raises(ValueError) as e:
        VehiclePolicy(age="25 years", accident_history=[{"invalid": "data"}])
    assert "Invalid accident history data" in str(e.value)
    
def test_vehicle_policy_accident_history_conversion():
    policy = VehiclePolicy(
        age="25 years",
        accident_history=[{"date": "2023-04-23", "at_fault": False}],
    )
    assert isinstance(policy.accident_history[0], AccidentHistory)
    assert policy.accident_history[0].date == date(2023, 4, 23)
    assert not policy.accident_history[0].at_fault
    
def test_vehicle_policy_accident_history_mixed():
    policy = VehiclePolicy(
    age="25 years",
    accident_history=[
        {"date": "2023-04-23", "at_fault": True},
        AccidentHistory(date=date(2022, 1, 1), at_fault=False),
        {"date": "2024-01-01", "at_fault": False}
        ]
    )
    assert len(policy.accident_history) == 3
    assert isinstance(policy.accident_history[0], AccidentHistory)
    assert policy.accident_history[0].at_fault
    assert isinstance(policy.accident_history[1], AccidentHistory)
    assert not policy.accident_history[1].at_fault
    assert isinstance(policy.accident_history[2], AccidentHistory)
    assert not policy.accident_history[2].at_fault

# House Policy Tests
def test_house_policy_valid():
    policy = HousePolicy(age="50 years", flood_risk="LOW", n_parrots=2, windows={"intact": 10, "broken": 2})
    assert policy.age == "50 years"
    assert policy.policy_type == "vehicle"
    assert policy.flood_risk == "LOW"
    assert policy.n_parrots == 2
    assert policy.windows == {"intact": 10, "broken": 2}

def test_house_policy_invalid_age():
    with pytest.raises(ValueError) as e:
        HousePolicy(age="invalid", flood_risk="LOW", n_parrots=2, windows={"intact": 10, "broken": 2})
    assert "Age must be a string with the format '<number> years'." in str(e.value)


def test_house_policy_invalid_flood_risk():
    with pytest.raises(ValueError) as e:
        HousePolicy(age="50 years", flood_risk="invalid", n_parrots=2, windows={"intact": 10, "broken": 2})
    assert "Flood risk must be one of 'HIGH', 'MEDIUM', 'LOW'" in str(e.value)


def test_house_policy_invalid_n_parrots():
    with pytest.raises(ValueError) as e:
        HousePolicy(age="50 years", flood_risk="LOW", n_parrots=-1, windows={"intact": 10, "broken": 2})
    assert "Number of parrots must be a non-negative integer" in str(e.value)

    with pytest.raises(ValueError) as e:
        HousePolicy(age="50 years", flood_risk="LOW", n_parrots="invalid", windows={"intact": 10, "broken": 2})
    assert "Number of parrots must be a non-negative integer" in str(e.value)

def test_house_policy_invalid_windows():
    with pytest.raises(ValueError) as e:
        HousePolicy(age="50 years", flood_risk="LOW", n_parrots=2, windows="invalid")
    assert "Windows must be a dictionary" in str(e.value)

    with pytest.raises(ValueError) as e:
        HousePolicy(age="50 years", flood_risk="LOW", n_parrots=2, windows={"intact": 10, "broken": "invalid"})
    assert "Windows dictionary values must be non-negative integers" in str(e.value)

    with pytest.raises(ValueError) as e:
        HousePolicy(age="50 years", flood_risk="LOW", n_parrots=2, windows={"intact": -1, "broken": 2})
    assert "Windows dictionary values must be non-negative integers" in str(e.value)

# Premium Calculator Tests
@pytest.fixture
def premium_calculator_vehicle():
    return PremiumCalculator(base_rate=500)

@pytest.fixture
def premium_calculator_house():
    return PremiumCalculator(base_rate=300)

def test_calculate_vehicle_premium_car_too_old(premium_calculator_vehicle):
    policy = VehiclePolicy(age="16 years", accident_history=[])
    with pytest.raises(CarToOldException):
        premium_calculator_vehicle.calculate_premium(policy)

def test_calculate_vehicle_premium_demolition_derby(premium_calculator_vehicle):
    five_years_ago = date.today() - timedelta(days=5 * 365)
    four_years_ago = date.today() - timedelta(days=4 * 365)
    accident_history = [
        AccidentHistory(date=five_years_ago, at_fault=True),
        AccidentHistory(date=four_years_ago, at_fault=True),
        AccidentHistory(date=date.today(), at_fault=True),
    ]
    policy = VehiclePolicy(age="10 years", accident_history=accident_history)
    with pytest.raises(CarDemotionDerbyException):
        premium_calculator_vehicle.calculate_premium(policy)

def test_calculate_vehicle_premium_valid(premium_calculator_vehicle):
    policy = VehiclePolicy(age="10 years", accident_history=[])
    premium = premium_calculator_vehicle.calculate_premium(policy)
    # Base rate 500 * (1 + (10-5)*0.05 + 0) = 500 * 1.25
    assert premium == pytest.approx(500* (1 + (10-5)*0.05))

def test_calculate_vehicle_premium_with_accidents(premium_calculator_vehicle):
     three_years_ago = date.today() - timedelta(days=3*365)
     accident_history = [
        AccidentHistory(date=three_years_ago, at_fault=True),
        AccidentHistory(date=date.today(), at_fault=False),
        ]
     policy = VehiclePolicy(age="10 years", accident_history=accident_history)
     premium = premium_calculator_vehicle.calculate_premium(policy)
     assert premium == pytest.approx(500 * (1 + (10-5)*0.05 + 2*0.2))

def test_calculate_home_premium_too_many_parrots(premium_calculator_house):
    policy = HousePolicy(age="20 years", flood_risk="LOW", n_parrots=6, windows={"intact": 10, "broken": 2})
    with pytest.raises(TooManyParrotsException):
        premium_calculator_house.calculate_premium(policy)

def test_calculate_home_premium_broken_windows(premium_calculator_house):
    policy = HousePolicy(age="20 years", flood_risk="LOW", n_parrots=2, windows={"intact": 2, "broken": 10})
    with pytest.raises(BrokenWindowsException):
        premium_calculator_house.calculate_premium(policy)

def test_calculate_home_premium_valid(premium_calculator_house):
    policy = HousePolicy(age="20 years", flood_risk="LOW", n_parrots=2, windows={"intact": 10, "broken": 2})
    premium = premium_calculator_house.calculate_premium(policy)
    assert premium == pytest.approx(300)

def test_calculate_home_premium_with_flood_risk(premium_calculator_house):
    policy = HousePolicy(age="20 years", flood_risk="HIGH", n_parrots=2, windows={"intact": 10, "broken": 2})
    premium = premium_calculator_house.calculate_premium(policy)
    print(premium)
    assert premium == pytest.approx(300 * (1 + 0.15))
    
def test_calculate_home_premium_with_age_factor(premium_calculator_house):
    policy = HousePolicy(age="40 years", flood_risk="LOW", n_parrots=2, windows={"intact": 10, "broken": 2})
    premium = premium_calculator_house.calculate_premium(policy)
    assert premium == pytest.approx(300 * (1+ 0.1))

def test_calculate_unsupported_policy_type(premium_calculator_house):
    class UnsupportedPolicy:
        pass

    policy = UnsupportedPolicy()
    with pytest.raises(ValueError) as e:
        premium_calculator_house.calculate_premium(policy)
    assert "Unsupported policy type." in str(e.value)


def test_broken_windows_only_broken():
    policy = HousePolicy(age="30 years", n_parrots=1, windows={"broken": 5})
    with pytest.raises(BrokenWindowsException):  # Expect exception
        PremiumCalculator().calculate_premium(policy)

# TODO To be fixed
# def test_broken_windows_only_intact():
#     policy = HousePolicy(age="30 years", n_parrots=0, windows={"intact": 5})
#     #Should not raise exception
#     PremiumCalculator().calculate_premium(policy)


def test_broken_windows_no_windows():
    policy = HousePolicy(age="30 years", n_parrots=0, windows={})
    with pytest.raises(ValueError):
        PremiumCalculator().calculate_premium(policy)

def test_calculate_home_premium_with_all_factors(premium_calculator_house):
    policy = HousePolicy(age="45 years", flood_risk="HIGH", n_parrots=3, windows={"intact": 12, "broken": 2})
    premium = premium_calculator_house.calculate_premium(policy)

    age_factor = 0.10
    flood_factor = 0.15
    expected_premium = 300 * (1 + age_factor + flood_factor )
    assert premium == pytest.approx(expected_premium)