from attendance_processor import AttendanceProcessor
from utils import ATTENDANCE_LIST_FILE

if __name__ == "__main__":
    processor = AttendanceProcessor(ATTENDANCE_LIST_FILE)
    processor.run()