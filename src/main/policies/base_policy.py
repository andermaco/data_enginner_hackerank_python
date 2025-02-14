

from dataclasses import dataclass, field
import abc
from typing import ClassVar, Literal


@dataclass
class Policy(abc.ABC):
    """
    That would be the abstract base class por the insurancepolicies.
    Attributes:
        age (str): is a string with the format '<number> years', and its common to both policies.
        policy_type (Literal): is a string with the value 'house' or 'vehicle, and its common to both policies.
    """    
    DEFAULT_POLICY: ClassVar[Literal["vehicle", "house"]] = "vehicle"
    
    age: str
    policy_type: Literal["vehicle", "house"] = DEFAULT_POLICY
    # policy_type: Literal["vehicle", "house"]

# {\"age\": \"16 years\", \"accident_history\": [{\"date\": \"2023-04-23\", \"at_fault\": false}]}

    @abc.abstractmethod
    def validate(self):
        """
        Validates the policy data.
        """
        # if not isinstance(self.age, int) or self.age <= 0:
        #     raise ValueError("Age must be a positive integer.")
        if not self.is_valid_age_string(self.age):
            raise ValueError("Age must be a string with the format '<number> years'.")
        if not isinstance(self.policy_type, str) and self.policy_type not in ("house", "vehicle"):
            raise ValueError("Policy type must be a string with the value 'house' or 'vehicle'.")
        return True
    
    def is_valid_age_string(self, age: str) -> bool:
        """
        Checks if a string is in the format '<number> years'.
        """
        parts = age.split()  # Split on whitespace
        if len(parts) != 2:
            return False  # Must have two parts

        number_part, word_part = parts

        if word_part.lower() != "years":  # Case-insensitive check
            return False

        try:
            age = int(number_part)  # Try to convert the number part to an integer
            return age >= 0 # Additional check, age should be non-negative.
        except ValueError:            
            print("Age must be a string with the format '<number> years'.")
            return False
        