
from dataclasses import dataclass, field
from typing import List
from main.policies.base_policy import Policy
from datetime import date


@dataclass
class AccidentHistory:
    date: date
    at_fault: bool

    def __post_init__(self):
        if not isinstance(self.date, date):
            raise TypeError("date must be a datetime.date object")
        if not isinstance(self.at_fault, bool):
            raise TypeError("at_fault must be a boolean")


@dataclass
class VehiclePolicy(Policy):

    accident_history: List[AccidentHistory] = \
        field(default_factory=list)  # Use default_factory to create an empty list as default value
    
    def __post_init__(self):
        self.validate()
        
        if not isinstance(self.accident_history, list):
             raise TypeError("accident_history must be a list.")

        # To convert each dict into a AccidentHistory instance
        validated_history = []
        for item in self.accident_history:
            if isinstance(item, AccidentHistory): #If it is already an instance, append.
                 validated_history.append(item)
            elif isinstance(item, dict): #If it is a dictionary create and validate.
                try:                    
                    accident = AccidentHistory(date=date.fromisoformat(item['date']), at_fault=item['at_fault'])
                    validated_history.append(accident)
                except (KeyError, ValueError, TypeError) as e:
                    raise ValueError(f"Invalid accident history data: {e}") from e
            else:
                raise TypeError("All items in accident_history must be AccidentHistory objects or dictionaries.")

        self.accident_history = validated_history


    def validate(self):
        super().validate()
        # Can't directly use isinstance(self.accident_history, list[AccidentHistory]),
        # because during runtime don't fully support parameterized generics 
        # (like list[AccidentHistory])
        # if not isinstance(self.accident_history, list):
        #     raise TypeError("accident_history must be a list.")
        
        # # To convert each dictionary into a AccidentHistory instance
        # validated_history = []
        # for item in self.accident_history:
        #      if isinstance(item, AccidentHistory): #If it is already an instance, append.
        #          validated_history.append(item)
        #      elif isinstance(item, dict): #If it is a dictionary create and validate.
        #          try:                    
        #             accident = AccidentHistory(date=date.fromisoformat(item['date']), at_fault=item['at_fault'])
        #             validated_history.append(accident)
        #          except (KeyError, ValueError, TypeError) as e:
        #              raise ValueError(f"Invalid accident history data: {e}") from e
        #      else:
        #          raise TypeError("All items in accident_history must be AccidentHistory objects or dictionaries.")            
            
        #     # if not isinstance(item, AccidentHistory):
        #     #     raise TypeError(f"All items in accident_history must be AccidentHistory objects: {AccidentHistory.__annotations__}")
        #     # if not isinstance(item.date, date):
        #     #     raise TypeError("AccidentHistory.date must be a valid string datetime")
        
        return True