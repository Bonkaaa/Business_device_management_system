from datetime import datetime
from typing import Optional, List
from entities.employee import Employee
from entities.department import Department
from database import DatabaseManager
from utils.constant_class import DeviceQualityStatus, DeviceStatus
from utils.id_generators import generate_employee_id, generate_department_id

class HRManager():
    def __init__(self, db_path: str):
        self.db_manager = DatabaseManager(db_path)

    def set_managers(self, inventory_manager, assignment_manager) -> None:
        self.inventory_manager = inventory_manager
        self.assignment_manager = assignment_manager

    # ==== Employee Management =====    

    def create_and_add_employee(
        self,
        name: str,
        email: str,
        phone_number: str,
        position: str,
        department_id: str
    ) -> Employee:
        
        department = self.get_department_by_id(department_id)

        employee_id = generate_employee_id()
        new_employee = Employee(
            name=name,
            employee_id=employee_id,
            email=email,
            phone_number=phone_number,
            position=position,
            department=department,
            inventory_manager=self.inventory_manager,
        )

        department_name = department.get_name() if department else None

        # Thêm nhân viên vào database
        query = """
        INSERT INTO employees (employee_id, name, email, phone_number, position, department_id, department_name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (employee_id, name, email, phone_number, position, department_id, department_name)
        self.db_manager.execute_query(query, params)
        
        return new_employee 
    
    def remove_employee(self, employee_id: str) -> None:
        emp = self.get_employee_by_id(employee_id, fetch_dept=True)

        if not emp:
            return
        
        # Changed devices assigned to this employee to AVAILABLE
        assigned_devices = emp.get_assigned_devices()
        for device in assigned_devices:
            self.inventory_manager.update_device_status(
                device.get_id(),
                DeviceStatus.AVAILABLE,
            )
        
        # Close active assignments related to this employee
        assignments = self.assignment_manager.get_active_assignments_by_assignee_id(employee_id)
        if assignments:
            for assignment in assignments:
                self.assignment_manager.close_assignment(
                    assignment.get_id(),
                    actual_return_date=datetime.now().isoformat(),
                    return_quality_status=DeviceQualityStatus.GOOD,
                    broken_status=False
                )

        # Remove employee from database
        query = "DELETE FROM employees WHERE employee_id = ?"
        params = (employee_id,)
        self.db_manager.execute_query(query, params)

    def get_employee_by_id(self, employee_id: str, fetch_dept: bool = True) -> Employee | None:
        query = "SELECT * FROM employees WHERE employee_id = ?"
        params = (employee_id,)
        row = self.db_manager.fetch_one(query, params)

        if not row:
            return None

        department = None
        if fetch_dept:
            department = self.get_department_by_id(row['department_id'])

        if row:
            return Employee(
                name=row['name'],
                employee_id=row['employee_id'],
                email=row['email'],
                phone_number=row['phone_number'],
                position=row['position'],
                department=department,
                inventory_manager=self.inventory_manager,
            )
        return None
    
    def get_all_employees(self) -> list[Employee]:
        query = "SELECT * FROM employees"
        rows = self.db_manager.fetch_all(query)
        employees = []
        for row in rows:
            department = self.get_department_by_id(row['department_id']) if row['department_id'] else None
            employee = Employee(
                name=row['name'],
                employee_id=row['employee_id'],
                email=row['email'],
                phone_number=row['phone_number'],
                position=row['position'],
                department=department,
                inventory_manager=self.inventory_manager,
            )
            employees.append(employee)
        return employees
    
    def get_employees_by_department_id(self, department_id: str) -> list[Employee]:
        query = "SELECT * FROM employees WHERE department_id = ?"
        params = (department_id,)
        rows = self.db_manager.fetch_all(query, params)
        employees = []
        for row in rows:
            department = self.get_department_by_id(row['department_id']) if row['department_id'] else None
            employee = Employee(
                name=row['name'],
                employee_id=row['employee_id'],
                email=row['email'],
                phone_number=row['phone_number'],
                position=row['position'],
                department=department,
                inventory_manager=self.inventory_manager,
            )
            employees.append(employee)
        return employees
    
    def transfer_employee(self, employee_id: str, new_department_id: str) -> None:
        query = "UPDATE employees SET department_id = ? WHERE employee_id = ?"
        params = (new_department_id, employee_id)
        self.db_manager.execute_query(query, params)

    # ==== Department Management =====    

    def create_and_add_department(
        self,
        name: str,
        location: str,
    ) -> Department:
        department_id = generate_department_id()
        new_department = Department(
            name=name,
            department_id=department_id,
            manager=None,  # Manager sẽ được gán sau
            location=location,
            hr_manager=self,
            inventory_manager=self.inventory_manager,
        )
        # Thêm phòng ban vào database
        query = """
        INSERT INTO departments (department_id, name, location)
        VALUES (?, ?, ?)
        """
        params = (department_id, name, location)
        self.db_manager.execute_query(query, params)
        return new_department

    def remove_department(self, department_id: str) -> None:
        dept = self.get_department_by_id(department_id)
        if not dept:
            return
        
        # Changed devices assigned to this department to AVAILABLE
        assigned_devices = dept.get_assigned_devices()
        for device in assigned_devices:
            self.inventory_manager.update_device_status(
                device.get_id(),
                DeviceStatus.AVAILABLE,
            )

        # Close active assignments related to this department
        assignments = self.assignment_manager.get_active_assignments_by_assignee_id(department_id)

        for assignment in assignments:
            self.assignment_manager.close_assignment(
                assignment.get_id(),
                actual_return_date=datetime.now().isoformat(),
                return_quality_status=DeviceQualityStatus.GOOD,
                broken_status=False
            )
        
        # Remove department from database
        query = "DELETE FROM departments WHERE department_id = ?"
        params = (department_id,)
        self.db_manager.execute_query(query, params)

    def get_department_by_id(self, department_id: str) -> Department | None:
        query = "SELECT * FROM departments WHERE department_id = ?"
        params = (department_id,)

        row = self.db_manager.fetch_one(query, params)

        if not row:
            return None

        if row:
            manager_id = row.get('manager_id')
            manager = None
            if manager_id:
                manager = self.get_employee_by_id(manager_id, fetch_dept=False)

            return Department(
                name=row['name'],
                department_id=row['department_id'],
                manager=manager,  
                location=row['location'],
                hr_manager=self,
                inventory_manager=self.inventory_manager,
            )
        return None
    
    def get_all_departments(self) -> list[Department]:
        query = "SELECT * FROM departments"
        rows = self.db_manager.fetch_all(query)
        if not rows:
            return []

        departments = []

        for row in rows:
            manager_id = row.get('manager_id')
            manager = self.get_employee_by_id(manager_id) if manager_id else None

            department = Department(
                name=row['name'],
                department_id=row['department_id'],
                manager=manager, 
                location=row['location'],
                hr_manager=self,
                inventory_manager=self.inventory_manager,
            )
            departments.append(department)
        return departments
    
    def assign_manager_to_department(self, department_id: str, manager_employee_id: str) -> None:
        query = """
            UPDATE departments
            SET manager_id = ?, manager_name = ?
            WHERE department_id = ?
            """
        manager_name = self.get_employee_by_id(manager_employee_id).get_name()
        params = (manager_employee_id, manager_name, department_id)
        self.db_manager.execute_query(query, params)
    
    # ===== Statistics & Reporting =====
    def get_total_employees(self) -> int:
        query = "SELECT COUNT(*) as total FROM employees"
        row = self.db_manager.fetch_one(query)
        return row['total'] if row else 0
    
    def get_total_departments(self) -> int:
        query = "SELECT COUNT(*) as total FROM departments"
        row = self.db_manager.fetch_one(query)
        return row['total'] if row else 0
    
    def get_employee_info(self, employee_id: str) -> Optional[dict]:
        employee = self.get_employee_by_id(employee_id)
        if employee:
            return employee.to_dict()
        return None
    
    def get_department_info(self, department_id: str) -> Optional[dict]:
        department = self.get_department_by_id(department_id)
        if department:
            return department.to_dict()
        return None
    
    def get_assignee_by_id(self, assignee_id: str) -> Employee | Department | None:
        # Thử lấy như Employee trước
        employee = self.get_employee_by_id(assignee_id)
        if employee:
            return employee
        
        # Nếu không phải Employee, thử lấy như Department
        department = self.get_department_by_id(assignee_id)
        if department:
            return department
        
        return None


    
