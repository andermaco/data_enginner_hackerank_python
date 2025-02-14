
from datetime import date, timedelta
from .exceptions.insurance import BrokenWindowsException, CarToOldException, CarDemotionDerbyException, TooManyParrotsException
from .policies.base_policy import Policy
from .policies.vehicle_policy import VehiclePolicy
from .policies.house_policy import HousePolicy


class PremiumCalculator:
    """
    Calculates the premium for an insurance policy.
    """

    def __init__(self, base_rate: float = 0.01):
        self.base_rate = base_rate

    def calculate_premium(self, policy: Policy) -> float:
        if isinstance(policy, VehiclePolicy):
            return self._calculate_vehicle_premium(policy)
        elif isinstance(policy, HousePolicy):
            return self._calculate_home_premium(policy)
        else:
            raise ValueError("Unsupported policy type.")

    def _calculate_vehicle_premium(self, policy: VehiclePolicy) -> float:
        # Underwriting rules        
        
        ## Older than 15 years are not insurable
        if self._get_age(policy.age) > 15:
            raise CarToOldException()                    
        
        ## Check for demolition derby drivers (more than 2 at-fault accidents in the last 5 years)
        five_years_ago = date.today() - timedelta(days=5 * 365)
        at_fault_accidents_5yr = 0
        for accident in policy.accident_history:
            if accident.date >= five_years_ago and accident.at_fault:
                at_fault_accidents_5yr += 1
        if at_fault_accidents_5yr > 2:
            raise CarDemotionDerbyException()                
        
        # Bonus-Malus        
        
        ## classic cars come with a price tag of 5% more     
        age_factor = max(0, (self._get_age(policy.age) - 5) * 0.05)
        
        ## Calculate accident_factor based on accidents in the last 3 years
        three_years_ago = date.today() - timedelta(days=3*365)  # Approx 3 years
        recent_accidents = 0
        for accident in policy.accident_history:
            if accident.date >= three_years_ago:
                recent_accidents += 1
        accident_factor = recent_accidents * 0.20  # Apply a 20% crash course fee for each accident in the last 3 years         
        
        return self.base_rate * (1 + age_factor + accident_factor)
        
    def _calculate_home_premium(self, policy: HousePolicy) -> float:
        # Discard houses with more than 5 parrots        
        if policy.n_parrots > 5:
            raise TooManyParrotsException()
        
        # Discard properties with more broken windows than intact ones.
        if "broken" in policy.windows and "intact" in policy.windows: 
            if policy.windows["broken"] > policy.windows["intact"]:
                raise BrokenWindowsException("More broken windows than intact windows")                        
        elif "broken" in policy.windows:
            if policy.windows["broken"] > 0:
                raise BrokenWindowsException("More broken windows than intact windows")        
        else:
            raise ValueError("Windows dictionary should have keys 'intact' and/or 'broken'")

        # Bonus-Malus
        
        ## Boost 15% for houses in medium-risk
        flood_factor = 0
        if policy.flood_risk in ("HIGH","MEDIUM"): 
            flood_factor = 0.15     
        
        ## 10% surcharge if the house is older than 20 years
        age_factor = 0
        if self._get_age(policy.age) > 20:
            age_factor = 0.10        
        
        return self.base_rate * (1 + age_factor + flood_factor)
    
    def _get_age(self, age: str) -> int:            
        """
        Get int part of age attribute.
        """
        parts = age.split()  # Split on whitespace
        return int(parts[0])
