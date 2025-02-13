import json
from argparse import ArgumentParser
from typing import Any
from datetime import date

from main.policies.vehicle_policy import VehiclePolicy
from main.policies.home_policy import HomePolicy
from main.premium_calculator import PremiumCalculator


def main(product_type: str, payload: dict[str, Any]):
    """
    Processes a quote request and calculates the premium.
    Args:
        product_type: The type of insurance policy ("vehicle" or "house").
        payload: A dictionary containing the policy details.
    """
    calculator = PremiumCalculator()
    try:
        if product_type == "vehicle":            
            policy = VehiclePolicy(
                age=payload["age"],
                accident_history=payload["accident_history"],
                outcome=payload["outcome"]
                )
            
        elif product_type == "house":
            policy = HomePolicy(
                age=payload["age"],
                flood_risk=payload["flood_risk"],
                n_parrots=payload["n_parrots"],
                windows=payload["windows"],
                outcome=payload["outcome"]
                )
        else:
            print(f"Error: No more insurance types, please select 'vehicle' or 'house'")
            return

        premium = calculator.calculate_premium(policy)
        print(f"Premium for {product_type} policy: ${premium:.2f}")

    except (ValueError, KeyError, TypeError) as e:        
        print(f"Error processing quote: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")



if __name__ == "__main__":
    """
    Example usage:
    python3 src/app.py vehicle '{"age": 25, "accident_history": [2018], "outcome": "OK"}'
    python3 src/app.py house '{"age": 50, "flood_risk": "LOW", "n_parrots": 2, "windows": {"intact": 10, "broken": 2}, "outcome": "OK"}'
    """
    parser = ArgumentParser(description="Quotation request")
    parser.add_argument("product_type", type=str, choices=["vehicle", "house"])
    parser.add_argument("payload", type=str)
    arguments = parser.parse_args()

    product_type, payload = arguments.product_type, json.loads(arguments.payload)

    main(product_type, payload)