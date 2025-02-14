
from dataclasses import dataclass, field
from typing import ClassVar, Literal
from .base_policy import Policy


@dataclass
class HousePolicy(Policy):
    DEFAULT_FLOOD_RISK: ClassVar[Literal["HIGH", "MEDIUM", "LOW"]] = "LOW"    
    
    flood_risk: Literal["HIGH", "MEDIUM", "LOW"] = DEFAULT_FLOOD_RISK
    n_parrots: int = 0
    windows: dict = field(default_factory=dict)  # Use default_factory to create an empty dict as default value

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