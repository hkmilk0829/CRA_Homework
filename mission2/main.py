from attendance import *

if __name__ == "__main__":
    manager = AttendanceManager()
    manager.load_file()
    manager.process_and_display()