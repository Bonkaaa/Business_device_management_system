from ast import Return
import re
from datetime import datetime

class Validator:
    @staticmethod
    def validate_non_empty(text, field_name="Field"):
        if not text or not text.strip() or str(text).strip() == "":
            return False
        return True
    
    @staticmethod
    def validate_positive_number(value, field_name="Value"):
        try:
            number = float(value)
            if number <= 0:
                return False
            return True
        except (ValueError, TypeError):
            return False
        
    @staticmethod
    def validate_date_format(date_text, date_format="%Y-%m-%d"):
        try:
            datetime.strptime(date_text, date_format)
            return True
        except ValueError:
            return False
        
    @staticmethod
    def validate_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return False
        return True
    
    @staticmethod
    def validate_phone_number(phone_number):
        phone_regex = r'^\+?\d{10,11}$'
        if not re.match(phone_regex, phone_number):
            return False
        return True
    
    @staticmethod
    def validate_choices(value, valid_options):
        if not value in valid_options:
            return False
        return True

class DeviceValidator(Validator):
    @staticmethod
    def validate_device_input(name: str, category: str, purchase_date: str, specifications: str):
        valid_name = DeviceValidator.validate_non_empty(name, "Tên thiết bị")
        if not valid_name:
            return f"Tên thiết bị không được để trống."
        valid_category = DeviceValidator.validate_non_empty(category, "Loại thiết bị")
        if not valid_category:
            return f"Loại thiết bị không được để trống."
        valid_date = DeviceValidator.validate_date_format(purchase_date)
        if not valid_date:
            return f"Ngày mua không đúng định dạng YYYY-MM-DD."
        return True

class EmployeeValidator(Validator):
    @staticmethod
    def validate_employee_input(name: str, email: str, phone: str, position: str):
        valid_name = EmployeeValidator.validate_non_empty(name, "Tên nhân viên")
        if not valid_name:
            return f"Tên nhân viên không được để trống."
        valid_email = EmployeeValidator.validate_email(email)
        if not valid_email:
            return f"Email không đúng định dạng."
        valid_phone = EmployeeValidator.validate_phone_number(phone)
        if not valid_phone:
            return f"Số điện thoại không đúng định dạng."
        valid_position = EmployeeValidator.validate_non_empty(position, "Chức vụ")
        if not valid_position:
            return f"Chức vụ không được để trống."
        return True
    
class DepartmentValidator(Validator):
    @staticmethod
    def validate_department_input(name: str, location: str):
        valid_name = DepartmentValidator.validate_non_empty(name, "Tên phòng ban")
        if not valid_name:
            return f"Tên phòng ban không được để trống."
        valid_location = DepartmentValidator.validate_non_empty(location, "Địa điểm")
        if not valid_location:
            return f"Địa điểm không được để trống."
        return True


        

