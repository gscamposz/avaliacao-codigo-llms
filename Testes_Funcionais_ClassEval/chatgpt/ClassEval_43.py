
class HRManagementSystem:
    """
    This is a class as personnel management system that implements
    functions such as adding, deleting, querying, and updating employees.
    """

    def __init__(self):
        """
        Initialize the HRManagementSystem with an empty dictionary.
        """
        self.employees = {}

    def add_employee(self, employee_id, name, position, department, salary):
        """
        Add a new employee to the HRManagementSystem.
        Return False if the employee already exists, otherwise True.
        """
        if employee_id in self.employees:
            return False

        self.employees[employee_id] = {
            'name': name,
            'position': position,
            'department': department,
            'salary': salary
        }
        return True

    def remove_employee(self, employee_id):
        """
        Remove an employee from the HRManagementSystem.
        Return True if removed, otherwise False.
        """
        if employee_id not in self.employees:
            return False

        del self.employees[employee_id]
        return True

    def update_employee(self, employee_id: int, employee_info: dict):
        """
        Update an employee's information.
        Return True if the employee exists, otherwise False.
        """
        if employee_id not in self.employees:
            return False

        self.employees[employee_id].update(employee_info)
        return True

    def get_employee(self, employee_id):
        """
        Get an employee's information.
        Return False if the employee does not exist.
        """
        if employee_id not in self.employees:
            return False

        return self.employees[employee_id]

    def list_employees(self):
        """
        List all employees' information, including employee_ID.
        """
        result = {}

        for employee_id, employee_info in self.employees.items():
            result[employee_id] = {
                'employee_ID': employee_id,
                **employee_info
            }

        return result
