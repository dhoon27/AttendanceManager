from abc import abstractmethod, ABC
from utils import GOLD_POINT_THRESHOLD, SILVER_POINT_THRESHOLD

class Grade(ABC):
    @abstractmethod
    def get_grade_name(self) -> str:
        pass

class GoldGrade(Grade):
    def get_grade_name(self) -> str:
        return "GOLD"

class SilverGrade(Grade):
    def get_grade_name(self) -> str:
        return "SILVER"

class NormalGrade(Grade):
    def get_grade_name(self) -> str:
        return "NORMAL"

class GradeFactory:
    @staticmethod
    def create_grade(point: int) -> Grade:
        if point >= GOLD_POINT_THRESHOLD:
            return GoldGrade()
        elif point >= SILVER_POINT_THRESHOLD:
            return SilverGrade()
        else:
            return NormalGrade()