from utils import MAX_ATTENDANCE, WEEKDAYS

class AttendanceLoader:
    def __init__(self, filename: str):
        self.filename = filename

    def _is_valid_name(self, name: str) -> bool:
        return bool(name and name.strip())

    def _is_valid_date(self, date: str) -> bool:
        return date in WEEKDAYS

    def load(self) -> tuple[list, list]:
        attendance_name = []
        attendance_date = []
        try:
            with open(self.filename, encoding='utf-8') as f:
                for _ in range(MAX_ATTENDANCE):
                    line = f.readline()
                    if not line:
                        break
                    parts = line.strip().split()
                    if len(parts) != 2:
                        raise ValueError("입력 데이터 형식 오류")
                    name, date = parts
                    if not self._is_valid_name(name):
                        raise ValueError(f"잘못된 이름: {name}")
                    if not self._is_valid_date(date):
                        raise ValueError(f"잘못된 요일: {date}")
                    attendance_name.append(name)
                    attendance_date.append(date)
        except FileNotFoundError:
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.filename}")
        return attendance_name, attendance_date