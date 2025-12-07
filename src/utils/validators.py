import re
from datetime import datetime

class Validator:
    @staticmethod
    def validate_non_empty(text, field_name="Field"):
        if not text or not text.strip() or str(text).strip() == "":
            raise ValueError(f"Lỗi: {field_name} không được để trống.")
        return str(text).strip()
    
    @staticmethod
    def validate_positive_number(value, field_name="Value"):
        try:
            number = float(value)
            if number <= 0:
                raise ValueError
            return number
        except (ValueError, TypeError):
            raise ValueError(f"Lỗi: {field_name} phải là một số dương.")
        
    @staticmethod
    def validate_date_format(date_text, date_format="%Y-%m-%d"):
        try:
            datetime.strptime(date_text, date_format)
            return date_text
        except ValueError:
            raise ValueError(f"Lỗi: Ngày không hợp lệ. Vui lòng nhập theo định dạng {date_format} (Ví dụ: 2025-12-7).")
        
    @staticmethod
    def validate_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Lỗi: Địa chỉ email không hợp lệ.")
        return email
    
    @staticmethod
    def validate_phone_number(phone_number):
        phone_regex = r'^\+?\d{10,11}$'
        if not re.match(phone_regex, phone_number):
            raise ValueError("Lỗi: Số điện thoại không hợp lệ. Vui lòng nhập số gồm 10 đến 11 chữ số, có thể bắt đầu bằng dấu '+'.")
        return phone_number
    
    @staticmethod
    def validate_choices(value, valid_options):
        if not value in valid_options:
            raise ValueError(f"Lỗi: Giá trị không hợp lệ. Vui lòng chọn một trong các tùy chọn sau: {', '.join(map(str, valid_options))}.")
        return value