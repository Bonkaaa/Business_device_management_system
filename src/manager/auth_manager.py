from database import DatabaseManager
from utils.constant_class import UserRole
import hashlib

class AuthManager:
    def __init__(self, db_path: str):
        self.db_manager = DatabaseManager(db_path)
        self.current_user = None

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username, password) -> dict | None:
        hashed_password = self._hash_password(password)
        query = "SELECT * FROM accounts WHERE username = ? AND password_hash = ?"
        params = (username, hashed_password)
        
        user_row = self.db_manager.fetch_one(query, params)

        if user_row:
            self.current_user = user_row
            return user_row
        return None
    
    def create_account(self, username: str, password: str, role: str, employee_id=None) -> bool:
        hashed_password = self._hash_password(password)

        role_str = UserRole(role).value

        query = "INSERT INTO accounts (username, password_hash, role, employee_id) VALUES (?, ?, ?, ?)"
        params = (username, hashed_password, role_str, employee_id)
        
        try:
            self.db_manager.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Lỗi khi tạo tài khoản: {e}")
            return False
        
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        old_hash = self._hash_password(old_password)
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM accounts WHERE username = ? AND password_hash = ?", (username, old_hash))
        if not cursor.fetchone():
            conn.close()
            return False  # Mật khẩu cũ không đúng
        
        new_hash = self._hash_password(new_password)
        cursor.execute("UPDATE accounts SET password_hash = ? WHERE username = ?", (new_hash, username))
        conn.commit()
        conn.close()
        return True

    def get_current_user(self) -> dict | None:
        return self.current_user
    