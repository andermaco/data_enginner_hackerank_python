# Insurance Policy Management System

## Environment:
- Spark Version: 3.4.0
- Python Version: 3.11

## Requirements:
### Background
You are tasked with designing a part of a system for managing insurance policies within an insurance company. The objective is to compute the premium based on the details of a quote request. This system should handle different types of insurance policies such as vehicle insurance and home insurance.

Each type of policy has its unique data attributes and methods for calculating premiums, but before a premium is calculated, each policy must be evaluated against a set of rules to determine if the policy should be approved. These rules are provided by the “creative” Underwriting team and are specifically referred to as "underwriting" rules.


### Underwriting Rules

*As an insurance company we want to prevent the provisioning of a policy to customers classified as high risk profiles so that we can optimize our revenues.*

Here is a starting set of rules to apply:
* Discard cars that still remember when flip phones were cool (older than 15 years).
* Disqualify drivers who treat their car like it's in a demolition derby with more than 2 at-fault accidents in the last 5 years.
* Disqualify households with more than five parrots (high noise and potential chaos risk).
* Disqualify properties with more broken windows than intact ones (indicating severe neglect).


### Bonus-Malus

*As an insurance company we want to dynamically compute premiums to prevent medium risk profiles to threaten our revenues without completely giving up on this piece of the market.*

Considering that vehicles and houses have different base premiums (500$ and 300$ respectively) here is a starting set of malus to apply:
* Add a 5% vintage tax for each year older than 5 years (because classic cars come with a price tag).
* Apply a 20% crash course fee for each accident in the last 3 years (because we believe in paying for our mistakes).
* Boost the premium by 15% for houses in medium-risk flood zones (because we like to keep our heads above water).
* Implement a 10% retro surcharge if the house is older than 20 years (because old homes come with character and a cost).



## Test Cases

### Vehicle:

| Vehicle Age  | Accident History | Outcome |
|:-------------|------------------|--------|
| 16 years     | [{date: 2023-04-23, at_fault: false}] | Blocked by UW Rules |
| 6 years     | [{date: 2022-07-20, at_fault: true},{date: 2023-04-23, at_fault: true},{date: 2024-02-23, at_fault: true}] | Blocked by UW Rules |
| 6 years     | [{date: 2022-07-20, at_fault: false},{date: 2023-04-23, at_fault: true},{date: 2024-01-12, at_fault: false}] | 630.0$ |
| 3 years     | [] | 500$ |

### House:

| House Age  | Flood Risk | n Parrots | Windows | Outcome |
|:---|---|---|---|---|
| 16 years     | HIGH               | 6 | intact_windows: 5, broken_windows: 0 | Blocked by UW Rules |
| 52 years     | LOW                | 0 | intact_windows: 2, broken_windows: 3 | Blocked by UW Rules |
| 25 years     | MEDIUM | 1 | intact_windows: 4, broken_windows: 1 | 379.5$ ** Check whether is a wrong test outcome, should not be an outcome of 370.0$?** |
| 3 years     | LOW | 0 | intact_windows: 6, broken_windows: 0 | 300$ |

## Hints
- `app.py` is there to show how a client would interact with the framework. That's optional.
- Use any additional library you think it's useful by using `requirements.txt`
