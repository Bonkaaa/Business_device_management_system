from manager.auth_manager import AuthManager
from utils.constant_class import UserRole

def create_default_accounts(auth_manager):
    """Tạo tài khoản mẫu cho 3 role nếu chưa có"""
    conn = auth_manager.db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM accounts")
    count = cursor.fetchone()[0]
    conn.close()

    # Create an employee data if not exists
    check_query = "SELECT COUNT(*) FROM employees WHERE employee_id = ?"
    check_params = ("EMP000000",)
    employee_exists = auth_manager.db_manager.fetch_one(check_query, check_params)
    
    if not employee_exists or employee_exists.get('COUNT(*)') == 0:
        query = """
        INSERT INTO employees (employee_id, name, email, phone_number, position)
        VALUES (?, ?, ?, ?, ?)
        """

        params = (
            "EMP000000",
            "Nguyễn Hữu Kiên",
            "abc@gmail.com",
            "0123456789",
            "Nhân viên",
        )

        auth_manager.db_manager.execute_query(query, params)
        

    if count == 0:
        print("Khởi tạo tài khoản mẫu...")
        # 1. Admin
        auth_manager.create_account("admin", "123", UserRole.ADMIN)
        print("- Admin: admin / 123")
        
        # 2. Technician
        auth_manager.create_account("tech", "123", UserRole.TECHNICIAN)
        print("- Technician: tech / 123")
        
        # 3. Employee
        auth_manager.create_account("user", "123", UserRole.EMPLOYEE, employee_id="EMP000000")
        print("- Employee: user / 123")