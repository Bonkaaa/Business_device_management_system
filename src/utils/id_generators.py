import uuid
import random
import string
import time

def generate_uuid():
        """Generate a random UUID."""
        return str(uuid.uuid4())
    
def generate_device_id(prefix="DEV"):
        random_digits = ''.join(random.choices(string.digits, k=6))
        return f"{prefix.upper()}-{random_digits}"
    
def generate_employee_id():
        char = random.choices(string.ascii_uppercase)[0]
        digits = ''.join(random.choices(string.digits, k=4))
        return f"EMP-{char}{digits}"
    
def generate_department_id():
        char = random.choices(string.ascii_uppercase)[0]
        digits = ''.join(random.choices(string.digits, k=3))
        return f"DEP-{char}{digits}"
    
def generate_ticket_id():
        date_str = time.strftime("%Y%m%d")

        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits), k=4)

        return f"TKT-{date_str}-{random_str}"
    
def generate_assignment_id():
        date_str = time.strftime("%Y%m%d")
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"ASG-{date_str}-{random_str}"
    
    