class AssessmentSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, name, grade, major):
        self.students[name] = {
            'name': name,
            'grade': grade,
            'major': major,
            'courses': {}
        }

    def add_course_score(self, name, course, score):
        if name in self.students:
            self.students[name]['courses'][course] = score

    def get_gpa(self, name):
        student = self.students.get(name)
        if not student or not student['courses']:
            return None
        total = sum(student['courses'].values())
        count = len(student['courses'])
        return total / count

    def get_all_students_with_fail_course(self):
        result = []
        for name in self.students:
            student = self.students[name]
            for score in student['courses'].values():
                if score < 60:
                    result.append(name)
                    break
        return result

    def get_course_average(self, course):
        scores = []
        for student in self.students.values():
            if course in student['courses']:
                scores.append(student['courses'][course])
        if not scores:
            return None
        return sum(scores) / len(scores)

    def get_top_student(self):
        gpa_dict = {}
        for name in self.students:
            gpa = self.get_gpa(name)
            if gpa is not None:
                gpa_dict[name] = gpa
        if not gpa_dict:
            return None
        max_gpa = -1
        top_student = None
        for name, gpa in gpa_dict.items():
            if gpa > max_gpa:
                max_gpa = gpa
                top_student = name
        return top_student
