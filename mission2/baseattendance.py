from abc import ABC, abstractmethod


class BaseUser(ABC):
    @abstractmethod
    def mark_attendance(self, day):
        pass

    @abstractmethod
    def finalize_grade(self):
        pass

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def is_inactive(self):
        pass


class BaseAttendanceManager(ABC):
    @abstractmethod
    def get_user(self, name: str):
        pass
    @abstractmethod
    def load_file(filename : str):
        pass
    @abstractmethod
    def process_and_display(self):
        pass