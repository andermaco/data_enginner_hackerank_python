

from dataclasses import dataclass
from datetime import date
import abc

@dataclass
class Policy(abc.ABC):
    """
    That would be the abstract base class por the insurancepolicies.
    """
    age: int

    @abc.abstractmethod
    def validate(self):
        """
        Validates the policy data.
        """
        if not isinstance(self.age, int) or self.age <= 0:
            raise ValueError("Age must be a positive integer.")
        