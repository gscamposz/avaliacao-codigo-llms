class EmployeeDB:
    def __init__(self):
        self.employees = {}

    def add_employee(self, emp_id, name, position, department, salary):
        """
        Adds a new employee to the database.
        """
        self.employees[emp_id] = {
            'name': name,
            'position': position,
            'department': department,
            'salary': salary
        }

    def get_employee(self, emp_id):
        """
        Retrieves an employee's details by ID.
        """
        return self.employees.get(emp_id)

    def list_employees(self):
        """
        Returns a dictionary of all employees in a structured format.
        Each employee entry includes:
        - 'employee_ID' (matching the original ID)
        - 'name', 'position', 'department', and 'salary'
        """
        result = {}
        for emp_id, emp_data in self.employees.items():
            result[emp_id] = {
                'employee_ID': emp_id,
                'name': emp_data['name'],
                'position': emp_data['position'],
                'department': emp_data['department'],
                'salary': emp_data['salary']
            }
        return result

    def update_employee(self, emp_id, name, position, department, salary):
        """
        Updates an existing employee's details.
        Returns True if the employee was found and updated, False otherwise.
        """
        if emp_id in self.employees:
            self.employees[emp_id] = {
                'name': name,
                'position': position,
                'department': department,
                'salary': salary
            }
            return True
        return False


db = EmployeeDB()
db.add_employee(1, "Alice", "Manager", "HR", 75000)
db.add_employee(2, "Bob", "Developer", "IT", 85000)

print(db.list_employees())


{
    1: {
        'employee_ID': 1,
        'name': 'Alice',
        'position': 'Manager',
        'department': 'HR',
        'salary': 75000
    },
    2: {
        'employee_ID': 2,
        'name': 'Bob',
        'position': 'Developer',
        'department': 'IT',
        'salary': 85000
    }
}
