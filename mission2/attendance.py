from baseattendance import BaseUser, BaseAttendanceManager
from collections import defaultdict
from enum import IntEnum
import sys

class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @staticmethod
    def from_str(day_str):
        return {
            "monday": Weekday.MONDAY,
            "tuesday": Weekday.TUESDAY,
            "wednesday": Weekday.WEDNESDAY,
            "thursday": Weekday.THURSDAY,
            "friday": Weekday.FRIDAY,
            "saturday": Weekday.SATURDAY,
            "sunday": Weekday.SUNDAY,
        }.get(day_str.lower())

class Grade(IntEnum):
    NORMAL = 0
    SILVER = 2
    GOLD = 1

class User(BaseUser):
    def __init__(self, name):
        self.name = name
        self.attendance = defaultdict(int)
        self.total_points = 0
        self.grade = Grade.NORMAL
        self.weekend_count = 0
        self.wednesday_count = 0

    def mark_attendance(self, day: Weekday):
        self.attendance[day] += 1
        if day in (Weekday.SATURDAY, Weekday.SUNDAY):
            self.weekend_count += 1
            self.total_points += 2
        elif day == Weekday.WEDNESDAY:
            self.wednesday_count += 1
            self.total_points += 3
        else:
            self.total_points += 1

    def finalize_grade(self):
        if self.attendance[Weekday.WEDNESDAY] > 9:
            self.total_points += 10
        if (self.attendance[Weekday.SATURDAY] + self.attendance[Weekday.SUNDAY]) > 9:
            self.total_points += 10
        if self.total_points >= 50:
            self.grade = Grade.GOLD
        elif self.total_points >= 30:
            self.grade = Grade.SILVER

    def display(self):
        print(f"NAME : {self.name}, POINT : {self.total_points}, GRADE : ", end="")
        print(self.grade.name)

    def is_inactive(self):
        return self.grade == Grade.NORMAL and self.weekend_count == 0 and self.wednesday_count == 0

class AttendanceManager(BaseAttendanceManager):
    def __init__(self):
        self.users = {}

    def get_user(self, name):
        if name not in self.users:
            self.users[name] = User(name)
        return self.users[name]

    def load_file(self, filename="attendance_weekday_500.txt"):
        try:
            with open(filename, encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        name, day_str = parts
                        day = Weekday.from_str(day_str)
                        if day is not None:
                            user = self.get_user(name)
                            user.mark_attendance(day)
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
            raise
            sys.exit(1)

    def process_and_display(self):
        for user in self.users.values():
            user.finalize_grade()
            user.display()

        print("\nRemoved player")
        print("==============")
        for user in self.users.values():
            if user.is_inactive():
                print(user.name)