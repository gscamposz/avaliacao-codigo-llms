class Schedule:
    def __init__(self):
        self.courses = []

    def add_course(self, course):
        """
        Adds a course to the schedule.
        :param course: A dictionary with keys 'start_time' and 'end_time'
        """
        self.courses.append(course)

    def remove_course(self, course):
        """
        Removes a course from the schedule.
        :param course: A dictionary with keys 'start_time' and 'end_time'
        """
        if course in self.courses:
            self.courses.remove(course)

    def is_free_at(self, check_time):
        """
        Checks if a specific time is free (i.e., not occupied by any course).
        :param check_time: A string in "HH:MM" format
        :return: True if the time is free, False otherwise
        """
        h, m = map(int, check_time.split(':'))
        check_minutes = h * 60 + m

        for course in self.courses:
            start_time = course['start_time']
            end_time = course['end_time']

            h_start, m_start = map(int, start_time.split(':'))
            start_minutes = h_start * 60 + m_start

            h_end, m_end = map(int, end_time.split(':'))
            end_minutes = h_end * 60 + m_end

            if start_minutes <= check_minutes <= end_minutes:
                return False

        return True


# Create a schedule
schedule = Schedule()

# Add courses
schedule.add_course({'start_time': '08:00', 'end_time': '09:40'})
schedule.add_course({'start_time': '10:30', 'end_time': '12:00'})

# Check if a time is free
print(schedule.is_free_at('09:00'))  # False (within first course)
print(schedule.is_free_at('11:00'))  # False (within second course)
print(schedule.is_free_at('13:00'))  # True (free time)
