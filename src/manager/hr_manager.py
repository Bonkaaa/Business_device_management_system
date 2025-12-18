from typing import Optional, List
from entities.employee import Employee
from entities.department import Department
from utils.id_generators import generate_employee_id, generate_department_id


class HRManager:
    """Class quản lý nhân viên và các phòng ban"""
    
    def __init__(self):
        self.__employees: List[Employee] = []
        self.__departments: List[Department] = []

    # ===== Initalize Employee and Department =====
    def initialize_employee(
        self,
        name: str,
        email: str,
        phone_number: str,
        position: str,
        department: Department
    ) -> Employee:
        employee_id = generate_employee_id()
        new_employee = Employee(
            name=name,
            employee_id=employee_id,
            email=email,
            phone_number=phone_number,
            position=position,
            department=department
        )
        return new_employee
    
    def initialize_department(
        self,
        name: str,
        manager: Employee,
        location: str,
    ) -> Department:
        department_id = generate_department_id()
        new_department = Department(
            name=name,
            department_id=department_id,
            manager=manager,
            location=location
        )
        return new_department
        
    
    # ===== Employee Management =====
    
    def add_employee(self, employee: Employee, department: Department) -> bool:
        """
        Thêm nhân viên vào hệ thống và vào phòng ban của họ
        Args:
            employee: Đối tượng Employee cần thêm
            department: Phòng ban của nhân viên
        Returns:
            True nếu thêm thành công, False nếu nhân viên đã tồn tại
        """
        if self._employee_exists(employee.get_id()):
            return False
        
        # Thêm nhân viên vào danh sách toàn hệ thống
        self.__employees.append(employee)
        
        # Thêm nhân viên vào phòng ban
        if department not in self.__departments:
            self.add_department(department)
        
        department.add_employee(employee)
        return True
    
    def remove_employee(self, employee_id: str) -> bool:
        """
        Xoá nhân viên khỏi hệ thống
        Args:
            employee_id: ID của nhân viên cần xoá
        Returns:
            True nếu xoá thành công, False nếu không tìm thấy
        """
        employee = self.get_employee_by_id(employee_id)
        if not employee:
            return False
        
        # Xoá khỏi danh sách toàn hệ thống
        self.__employees.remove(employee)
        
        # Xoá khỏi phòng ban
        department = employee._department
        department.remove_employee(employee)
        
        return True
    
    def get_employee_by_id(self, employee_id: str) -> Optional[Employee]:
        """
        Lấy thông tin nhân viên theo ID
        Args:
            employee_id: ID của nhân viên
        Returns:
            Đối tượng Employee hoặc None nếu không tìm thấy
        """
        for emp in self.__employees:
            if emp.get_id() == employee_id:
                return emp
        return None
    
    def get_employees_by_department(self, department_id: str) -> List[Employee]:
        """
        Lấy danh sách nhân viên trong một phòng ban
        Args:
            department_id: ID của phòng ban
        Returns:
            Danh sách nhân viên trong phòng ban
        """
        department = self.get_department_by_id(department_id)
        if department:
            return department.get_employees()
        return []
    
    def get_all_employees(self) -> List[Employee]:
        """Lấy danh sách tất cả nhân viên trong hệ thống"""
        return self.__employees.copy()
    
    def transfer_employee(self, employee_id: str, new_department: Department) -> bool:
        """
        Chuyển nhân viên sang phòng ban khác
        Args:
            employee_id: ID của nhân viên cần chuyển
            new_department: Phòng ban mới
        Returns:
            True nếu chuyển thành công, False nếu không tìm thấy nhân viên
        """
        employee = self.get_employee_by_id(employee_id)
        if not employee:
            return False
        
        # Xoá từ phòng ban cũ
        old_department = employee.get_department()
        old_department.remove_employee(employee)
        
        # Thêm vào phòng ban mới
        if new_department not in self.__departments:
            self.add_department(new_department)
        
        new_department.add_employee(employee)
        employee._department = new_department
        
        return True
    
    # ===== Department Management =====
    
    def add_department(self, department: Department) -> bool:
        """
        Thêm phòng ban vào hệ thống
        Args:
            department: Đối tượng Department cần thêm
        Returns:
            True nếu thêm thành công, False nếu phòng ban đã tồn tại
        """
        if self._department_exists(department.get_id()):
            return False
        
        self.__departments.append(department)
        return True
    
    def remove_department(self, department_id: str) -> bool:
        """
        Xoá phòng ban khỏi hệ thống (nếu phòng ban không có nhân viên)
        Args:
            department_id: ID của phòng ban cần xoá
        Returns:
            True nếu xoá thành công, False nếu không tìm thấy hoặc phòng ban còn nhân viên
        """
        department = self.get_department_by_id(department_id)
        if not department:
            return False
        
        # Không cho phép xoá phòng ban nếu còn nhân viên
        if len(department.get_employees()) > 0:
            return False
        
        self.__departments.remove(department)
        return True
    
    def get_department_by_id(self, department_id: str) -> Optional[Department]:
        """
        Lấy thông tin phòng ban theo ID
        Args:
            department_id: ID của phòng ban
        Returns:
            Đối tượng Department hoặc None nếu không tìm thấy
        """
        for dept in self.__departments:
            if dept.get_id() == department_id:
                return dept
        return None
    
    def get_all_departments(self) -> List[Department]:
        """Lấy danh sách tất cả phòng ban trong hệ thống"""
        return self.__departments.copy()
    
    # ===== Statistics & Reporting =====
    
    def get_total_employees(self) -> int:
        """Lấy tổng số nhân viên trong hệ thống"""
        return len(self.__employees)
    
    def get_total_departments(self) -> int:
        """Lấy tổng số phòng ban trong hệ thống"""
        return len(self.__departments)
    
    def get_department_size(self, department_id: str) -> int:
        """
        Lấy số lượng nhân viên trong một phòng ban
        Args:
            department_id: ID của phòng ban
        Returns:
            Số lượng nhân viên, -1 nếu không tìm thấy phòng ban
        """
        department = self.get_department_by_id(department_id)
        if department:
            return len(department.get_employees())
        return -1
    
    def get_employee_info(self, employee_id: str) -> Optional[dict]:
        """
        Lấy thông tin chi tiết của nhân viên
        Args:
            employee_id: ID của nhân viên
        Returns:
            Dictionary chứa thông tin nhân viên hoặc None
        """
        employee = self.get_employee_by_id(employee_id)
        if employee:
            return employee.to_dict()
        return None
    
    def get_department_info(self, department_id: str) -> Optional[dict]:
        """
        Lấy thông tin chi tiết của phòng ban
        Args:
            department_id: ID của phòng ban
        Returns:
            Dictionary chứa thông tin phòng ban hoặc None
        """
        department = self.get_department_by_id(department_id)
        if department:
            return department.to_dict()
        return None
    
    # ===== Helper Methods =====
    
    def _employee_exists(self, employee_id: str) -> bool:
        """Kiểm tra xem nhân viên có tồn tại hay không"""
        return self.get_employee_by_id(employee_id) is not None
    
    def _department_exists(self, department_id: str) -> bool:
        """Kiểm tra xem phòng ban có tồn tại hay không"""
        return self.get_department_by_id(department_id) is not None
