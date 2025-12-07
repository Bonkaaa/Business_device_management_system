import uuid
import random
import string
import time

class IDGenerators:
    @staticmethod
    def generate_uuid():
        """Generate a random UUID."""
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_device_id(prefix="DEV"):
        random_digits = ''.join(random.choices(string.digits, k=6))
        return f"{prefix.upper()}-{random_digits}"
    
    @staticmethod
    def generate_employee_id():
        char = random.choices(string.ascii_uppercase)
        digits = ''.join(random.choices(string.digits, k=4))
        return f"EMP-{char}{digits}"
    
    @staticmethod
    def generate_ticket_id():
        date_str = time.strftime("%Y%m%d")

        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits), k=4)

        return f"TKT-{date_str}-{random_str}"
    
    