
from dataclasses import dataclass
from main.policies.base_policy import Policy
from typing import List


@dataclass
class VehiclePolicy(Policy):
    accident_history: List[int]
    outcome: str
    policy_type: str = "vehicle"
    
    def __post_init__(self):
        self.validate()

    def validate(self):
        super().validate()
        if not isinstance(self.accident_history, list):
            raise TypeError("Accident history must be a list")
        if not all(isinstance(year, int) and year > 0 for year in self.accident_history):
            raise ValueError("Accident history must contain a list of valid years (+ integers)")
        if not isinstance(self.outcome, str) or self.outcome not in ("OK", "KO"):
             raise ValueError("Outcome value must be 'OK' or 'KO'")