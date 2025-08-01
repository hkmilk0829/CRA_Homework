from attendance import Weekday, Grade, User, AttendanceManager
import pytest


def test_mark_attendance_weekday_without_wednesday():
    user = User("Hukwang")
    user.mark_attendance(Weekday.MONDAY)
    assert user.total_points == 1


def test_mark_attendance_weekday_wednesday():
    user = User("Hukwang")
    user.mark_attendance(Weekday.WEDNESDAY)
    assert user.total_points == 3


def test_mark_attendance_weekend_sunday():
    user = User("Hukwang")
    user.mark_attendance(Weekday.SUNDAY)
    assert user.total_points == 2


def test_finalize_grade_bonus_WEDNESDAY():
    user = User("Hukwang")
    user.attendance[Weekday.WEDNESDAY] = 10
    user.finalize_grade()
    assert user.total_points == 10


def test_finalize_grade_bonus_WEEKENDS():
    user = User("Hukwang")
    user.attendance[Weekday.SUNDAY] = 10
    user.finalize_grade()
    assert user.total_points == 10


def test_finalize_grade_is_grade_gold():
    user = User("Hukwang")
    user.total_points = 50
    user.finalize_grade()
    assert user.grade == Grade.GOLD


def test_finalize_grade_is_grade_silver():
    user = User("Hukwang")
    user.total_points = 35
    user.finalize_grade()
    assert user.grade == Grade.SILVER

def test_is_inactive():
    user = User("Hukwang")
    ret = user.is_inactive() # no attendace state
    assert ret == True

def test_get_user():
    attendance_manager = AttendanceManager()
    attendance_manager.get_user("Hukwang")
    assert attendance_manager.users["Hukwang"].name == "Hukwang"

def test_load_exist_file():
    attendance_manager = AttendanceManager()
    attendance_manager.load_file()
    assert attendance_manager.users['Umar'].total_points > 0 # 기대값에 있는 name을 활용

def test_load_not_exist_file():
    attendance_manager = AttendanceManager()
    with pytest.raises(FileNotFoundError):
        attendance_manager.load_file("abc.txt")

def test_display(capsys):
    user = User("Hukwang")
    user.total_points = 10
    user.grade = Grade.GOLD
    user.display()
    captured = capsys.readouterr()
    assert captured.out == "NAME : Hukwang, POINT : 10, GRADE : GOLD\n"


def test_process_and_display_no_user(capsys):
    attendance_manager = AttendanceManager()
    attendance_manager.process_and_display()
    captured = capsys.readouterr()
    assert captured.out =="\nRemoved player\n==============\n"

def test_process_and_display_some_users(capsys):
    attendance_manager = AttendanceManager()
    user_hk = User("Hukwang")
    user_hk.total_points = 70
    user_hy = User("Hayeong")
    attendance_manager.users["Hukwang"] = user_hk
    attendance_manager.users["Hayeong"] = user_hy
    attendance_manager.process_and_display()
    captured = capsys.readouterr()
    assert captured.out == 'NAME : Hukwang, POINT : 70, GRADE : GOLD\nNAME : Hayeong, POINT : 0, GRADE : NORMAL\n\nRemoved player\n==============\nHayeong\n'
