class CarToOldException(Exception):
    def __init__(self, message = "Blocked by UW Rules"):
        self.message = message
        
class CarDemotionDerbyException(Exception):
    def __init__(self, message = "Too many at-fault accidents in the last 5 years"):
        self.message = message
        print(message)
        
class TooManyParrotsException(Exception):
    def __init__(self, message = "Too many parrots"):
        self.message = message
        print(message)
        
class BrokenWindowsException(Exception):
    def __init__(self, message = "More broken windows than intact windows"):
        self.message = message
        print(message)