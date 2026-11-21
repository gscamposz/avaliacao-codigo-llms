
class AssessmentSystem:
    """
    This is a class as an student assessment system, which supports add student, add course score, calculate GPA, and other functions for students and courses.
    """

    def __init__(self):
        """
        Initialize the students dict in assessment system.
        """
        self.students = {}

    def add_student(self, name, grade, major):
        """
        Add a new student into self.students dict
        :param name: str, student name
        :param grade: int, student grade
        :param major: str, student major
        """
        self.students[name] = {
            'name': name,
            'grade': grade,
            'major': major,
            'courses': {}
        }

    def add_course_score(self, name, course, score):
        """
        Add score of specific course for student in self.students
        :param name: str, student name
        :param course: str, course name
        :param score: int, course score
        """
        if name in self.students:
            self.students[name]['courses'][course] = score

    def get_gpa(self, name):
        """
        Get average grade of one student.
        :param name: str, student name
        :return: float average grade, or None
        """
        if name not in self.students:
            return None

        courses = self.students[name]['courses']

        if not courses:
            return None

        return sum(courses.values()) / len(courses)

    def get_all_students_with_fail_course(self):
        """
        Get all students who have any score below 60.
        :return: list of student names
        """
        failed_students = []

        for name, student in self.students.items():
            if any(score < 60 for score in student['courses'].values()):
                failed_students.append(name)

        return failed_students

    def get_course_average(self, course):
        """
        Get the average score of a specific course.
        :param course: str, course name
        :return: float average score, or None
        """
        scores = []

        for student in self.students.values():
            if course in student['courses']:
                scores.append(student['courses'][course])

        if not scores:
            return None

        return sum(scores) / len(scores)

    def get_top_student(self):
        """
        Calculate every student's GPA and find the student
        with the highest GPA.
        :return: str, name of student with highest GPA
        """
        top_student = None
        highest_gpa = None

        for name in self.students:
            gpa = self.get_gpa(name)

            if gpa is not None:
                if highest_gpa is None or gpa > highest_gpa:
                    highest_gpa = gpa
                    top_student = name

        return top_student
