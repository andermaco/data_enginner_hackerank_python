
from dataclasses import dataclass
from typing import Literal
from .base_policy import Policy


@dataclass
class HomePolicy(Policy):
    flood_risk: Literal["HIGH", "MEDIUM", "LOW"]
    n_parrots: int
    windows: dict
    outcome: Literal["OK", "KO"]
    policy_type: str = "home"

    def __post_init__(self):
        self.validate()
    

    def validate(self):
        """
        Validates the policy data
        """
        super().validate()
        if not isinstance(self.flood_risk, str) or self.flood_risk not in ("HIGH", "MEDIUM", "LOW"):
            raise ValueError("Flood risk must be one of 'HIGH', 'MEDIUM', 'LOW'")
        if not isinstance(self.n_parrots, int) or self.n_parrots < 0:  # Allow 0 parrots
            raise ValueError("Number of parrots must be a non-negative integer")
        if not isinstance(self.windows, dict):
            raise ValueError("Windows must be a dictionary")
        if not all(isinstance(val, int) and val >= 0 for val in self.windows.values()):
            raise ValueError("Windows dictionary values must be non-negative integers")
        if not isinstance(self.outcome, str) or self.outcome not in ("OK", "KO"):
             raise ValueError("Outcome value must be 'OK' or 'KO'")