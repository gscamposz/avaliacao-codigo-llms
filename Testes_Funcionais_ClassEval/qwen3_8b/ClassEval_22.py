class StudentManager:
    def __init__(self):
        self.students = []  # List of student dictionaries
        self.class_enrollments = {}  # Maps student names to their enrolled classes

    def add_student(self, name, major):
        """
        Add a student with their major.
        """
        self.students.append({'name': name, 'major': major})

    def enroll_classes(self, name, classes):
        """
        Enroll a student in a list of classes.
        """
        self.class_enrollments[name] = classes

    def get_students_by_major(self, major):
        """
        Get all student names in a specific major.
        """
        return [student['name'] for student in self.students if student['major'] == major]

    def get_all_majors(self):
        """
        Get all unique majors in the system.
        """
        return list({student['major'] for student in self.students})

    def get_most_popular_class_in_major(self, major):
        """
        Get the class with the highest enrollment count in a specific major.
        """
        students_in_major = self.get_students_by_major(major)
        class_counts = {}

        for student_name in students_in_major:
            classes = self.class_enrollments.get(student_name, [])
            for class_name in classes:
                class_counts[class_name] = class_counts.get(class_name, 0) + 1

        if not class_counts:
            return None

        # Return the class with the highest count (break ties arbitrarily)
        return max(class_counts, key=class_counts.get)


manager = StudentManager()

# Add students and their majors
manager.add_student("John", "Computer Science")
manager.add_student("Bob", "Computer Science")
manager.add_student("Alice", "Computer Science")

# Enroll classes
manager.enroll_classes("John", ["Algorithms", "Data Structures"])
manager.enroll_classes("Bob", ["Operating Systems", "Data Structures", "Algorithms"])
manager.enroll_classes("Alice", ["Data Structures", "Machine Learning"])

# Get students by major
print("Students in Computer Science:", manager.get_students_by_major("Computer Science"))

# Get all majors
print("All majors:", manager.get_all_majors())

# Get most popular class in Computer Science
print("Most popular class:", manager.get_most_popular_class_in_major("Computer Science"))
