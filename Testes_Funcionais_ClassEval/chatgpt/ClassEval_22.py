
class ClassRegistrationSystem:
    """
    This is a class as a class registration system, allowing to
    register students, register them for classes, retrieve students
    by major, get a list of all majors, and determine the most
    popular class within a specific major.
    """

    def __init__(self):
        """
        Initialize the registration system.
        """
        self.students = []
        self.students_registration_classes = {}

    def register_student(self, student):
        """
        Register a student to the system.
        Return 0 if already registered, otherwise return 1.
        """
        if student in self.students:
            return 0

        self.students.append(student)
        return 1

    def register_class(self, student_name, class_name):
        """
        Register a class to the student.
        Return a list of registered class names.
        """
        if student_name not in self.students_registration_classes:
            self.students_registration_classes[student_name] = []

        classes = self.students_registration_classes[student_name]

        if class_name not in classes:
            classes.append(class_name)

        return classes

    def get_students_by_major(self, major):
        """
        Get all student names in the specified major.
        """
        return [
            student["name"]
            for student in self.students
            if student["major"] == major
        ]

    def get_all_major(self):
        """
        Get all unique majors in the system.
        """
        majors = []

        for student in self.students:
            major = student["major"]

            if major not in majors:
                majors.append(major)

        return majors

    def get_most_popular_class_in_major(self, major):
        """
        Get the class with the highest enrollment
        in the specified major.
        """
        students = self.get_students_by_major(major)
        class_counts = {}

        for student_name in students:
            classes = self.students_registration_classes.get(
                student_name, []
            )

            for class_name in classes:
                if class_name not in class_counts:
                    class_counts[class_name] = 0

                class_counts[class_name] += 1

        if not class_counts:
            return None

        return max(class_counts, key=class_counts.get)
