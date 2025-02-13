
from .policies.base_policy import Policy
from .policies.vehicle_policy import VehiclePolicy
from .policies.home_policy import HomePolicy

class PremiumCalculator:
    """
    Calculates the premium for an insurance policy.
    """

    def __init__(self, base_rate: float = 0.01):
        self.base_rate = base_rate

    def calculate_premium(self, policy: Policy) -> float:
        if isinstance(policy, VehiclePolicy):
            return self._calculate_vehicle_premium(policy)
        elif isinstance(policy, HomePolicy):
            return self._calculate_home_premium(policy)
        else:
            raise ValueError("Unsupported policy type.")

    def _calculate_vehicle_premium(self, policy: VehiclePolicy) -> float:
        age_factor = max(0, (policy.age - 5) * 0.005) # Add a 5% vintage tax for each year older than 5 years
        accident_factor = len(policy.accident_history) * 0.02  # Apply a 20% crash course fee for each accident in the last 3 years 
        outcome_factor = 0.10 if policy.outcome == "KO" else 0
        return 100 * self.base_rate * (1 + age_factor + accident_factor + outcome_factor)
        

    def _calculate_home_premium(self, policy: HomePolicy) -> float:
        age_factor = max(0, (policy.age - 20) * 0.10) # Implement a 10% retro surcharge if the house is older than 20 years
        flood_factor = 0.0
        if policy.flood_risk == "HIGH" or policy.flood_risk == "MEDIUM": # Boost the premium by 15% for houses in medium-risk flood zones 
            flood_factor = 0.15        
        parrot_factor = min(5, policy.n_parrots) * 0.01  # Max 5% for parrots
        return 100 * self.base_rate * (1 + age_factor + flood_factor + parrot_factor)
