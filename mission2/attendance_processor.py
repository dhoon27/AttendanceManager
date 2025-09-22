from attendance_loader import AttendanceLoader
from player_manager import PlayerManager
from score_calculator import ScoreCalculator
from grade_applier import GradeApplier
from report_generator import ReportGenerator

class AttendanceProcessor:
    def __init__(self, filename: str):
        self.filename = filename

    def run(self):
        try:
            # 1. 데이터 로드
            loader = AttendanceLoader(self.filename)
            attendance_name, attendance_date = loader.load()

            # 2. 플레이어 관리
            player_manager = PlayerManager(attendance_name)

            # 3. 점수 계산
            calculator = ScoreCalculator(player_manager)
            calculator.calculate_scores(attendance_name, attendance_date)
            calculator.apply_bonus_points()
            points = calculator.get_points()

            # 4. 등급 적용
            grade_applier = GradeApplier(player_manager, points['points'])
            grades = grade_applier.get_grades()

            # 5. 보고서 생성 및 출력
            report_generator = ReportGenerator(player_manager, points, grades)
            report_generator.print_grade_info()
            report_generator.print_removed_players()

        except Exception as e:
            print(f"오류 발생: {e}")
