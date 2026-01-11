import sqlite3
import json

class DatabaseManager:
    def __init__(self, db_name='device_manager.db'):
        self.db_name = db_name
        self.create_tables()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_tables(self):
        query_departments = """
            CREATE TABLE IF NOT EXISTS departments (
                department_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                location TEXT,
                manager_id TEXT,
                manager_name TEXT,
                assigned_devices TEXT, -- Lưu chuỗi JSON của danh sách device IDs,
                employees TEXT -- Lưu chuỗi JSON của danh sách employee IDs
            );
        """

        query_employees = """
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                phone_number TEXT,
                position TEXT,
                department_id TEXT, -- Khóa ngoại trỏ về departments
                department_name TEXT,
                assigned_devices TEXT, -- Lưu chuỗi JSON của danh sách device IDs,
                FOREIGN KEY(department_id) REFERENCES departments(department_id)
            );
        """

        query_devices = """
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                status TEXT, -- Lưu string: 'available', 'assigned'...
                quality_status TEXT, -- Lưu string: 'good', 'broken'...
                purchase_date TEXT,
                assigned_to TEXT, -- ID của Employee hoặc Department
                specifications TEXT -- Lưu chuỗi JSON
            );
        """

        # Chú ý assignee_id có thể là employee_id hoặc department_id tùy theo việc thiết bị được giao cho ai
        query_asssignments = """
            CREATE TABLE IF NOT EXISTS assignments (
                assignment_id TEXT PRIMARY KEY,
                initial_date TEXT,
                expected_return_date TEXT,
                actual_return_date TEXT,
                status TEXT,
                quality_status TEXT,
                notes TEXT,
                device_id TEXT,
                device_name TEXT,
                assignee_id TEXT,
                assignee_name TEXT,
                FOREIGN KEY(device_id) REFERENCES devices(device_id),
                FOREIGN KEY(assignee_id) REFERENCES employees(employee_id),
                FOREIGN KEY(assignee_id) REFERENCES departments(department_id)
            );
        """

        query_maintenance_tickets = """
            CREATE TABLE IF NOT EXISTS maintenance_tickets (
                ticket_id TEXT PRIMARY KEY,
                device_id TEXT,
                reporter_id TEXT,
                issue_description TEXT,
                status TEXT,
                reported_date TEXT,
                date_resolved TEXT,
                technician_notes TEXT,
                cost REAL,
                FOREIGN KEY(device_id) REFERENCES devices(id),
                FOREIGN KEY(reporter_id) REFERENCES employees(id)
            );
        """

        query_accounts = """
            CREATE TABLE IF NOT EXISTS accounts (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                employee_id TEXT,
                FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
                );
        """

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query_departments)
        cursor.execute(query_employees)
        cursor.execute(query_devices)
        cursor.execute(query_asssignments)
        cursor.execute(query_maintenance_tickets)
        cursor.execute(query_accounts)

        conn.commit()
        conn.close()

    # Helper
    def execute_query(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def fetch_all(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
    
    def fetch_one(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None