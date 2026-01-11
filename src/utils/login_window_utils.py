from manager.auth_manager import AuthManager
from utils.constant_class import UserRole

def create_default_accounts(auth_manager):
    """Tạo tài khoản mẫu cho 3 role nếu chưa có"""
    conn = auth_manager.db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM accounts")
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        print("Khởi tạo tài khoản mẫu...")
        # 1. Admin
        auth_manager.create_account("admin", "123", UserRole.ADMIN)
        print("- Admin: admin / 123")
        
        # 2. Technician
        auth_manager.create_account("tech", "123", UserRole.TECHNICIAN)
        print("- Technician: tech / 123")
        
        # 3. Employee
        auth_manager.create_account("user", "123", UserRole.EMPLOYEE)
        print("- Employee: user / 123")