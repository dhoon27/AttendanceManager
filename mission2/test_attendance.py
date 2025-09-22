import pytest

from attendance import *
from attendance_processor import *
from report_generator import *
from grade import *
from grade_applier import *
from score_calculator import *
from player_manager import *
from attendance_loader import *
from utils import *


def test_AttendanceLoader_load():
    # Assign
    loader = AttendanceLoader(ATTENDANCE_LIST_FILE)


    # Act
    attendance_name, attendance_date = loader.load()

    # Assert
    assert len(attendance_name) == len(attendance_date)
    assert all(isinstance(name, str) for name in attendance_name)
    assert all(isinstance(date, str) and date in WEEKDAYS for date in attendance_date)


def test_AttendanceLoader_load_invalid_file():
    # Assign
    loader = AttendanceLoader("non_existent_file.txt")

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        loader.load()

def test_playerManager_add_player():
    # Assign
    loader = AttendanceLoader(ATTENDANCE_LIST_FILE)
    attendance_name, attendance_date = loader.load()


    # Act
    player_manager = PlayerManager(attendance_name)
    player_ids = player_manager.get_all_player_ids()

    # Assert
    assert len(player_ids) > 0
    assert all(isinstance(player_id, int) for player_id in player_ids)
    assert all(player_manager.get_player_id(name) is not None for name in attendance_name)
    assert all(player_manager.get_player_name(pid) is not None for pid in player_ids)

def test_ScoreCalculator_calculate_scores():
    # Assign
    loader = AttendanceLoader(ATTENDANCE_LIST_FILE)
    attendance_name, attendance_date = loader.load()
    player_manager = PlayerManager(attendance_name)
    calculator = ScoreCalculator(player_manager)

    # Act
    calculator.calculate_scores(attendance_name, attendance_date)
    points = calculator.get_points()

    # Assert
    assert all(isinstance(pid, int) for pid in points['points'].keys())
    assert all(isinstance(score, int) for score in points['points'].values())
    assert all(isinstance(pid, int) for pid in points['wed_scores'].keys())
    assert all(isinstance(count, int) for count in points['wed_scores'].values())
    assert all(isinstance(pid, int) for pid in points['weekend_scores'].keys())
    assert all(isinstance(count, int) for count in points['weekend_scores'].values())

def test_ScoreCalculator_apply_bonus_points():
    # Assign
    loader = AttendanceLoader(ATTENDANCE_LIST_FILE)
    attendance_name, attendance_date = loader.load()
    player_manager = PlayerManager(attendance_name)
    calculator = ScoreCalculator(player_manager)

    # Act
    calculator.calculate_scores(attendance_name, attendance_date)
    calculator.apply_bonus_points()
    points = calculator.get_points()

    # Assert
    assert all(isinstance(pid, int) for pid in points['points'].keys())
    assert all(isinstance(score, int) for score in points['points'].values())
    assert all(isinstance(pid, int) for pid in points['wed_scores'].keys())
    assert all(isinstance(count, int) for count in points['wed_scores'].values())
    assert all(isinstance(pid, int) for pid in points['weekend_scores'].keys())
    assert all(isinstance(count, int) for count in points['weekend_scores'].values())

def test_GradeApplier_get_grades():
    # Assign
    loader = AttendanceLoader(ATTENDANCE_LIST_FILE)
    attendance_name, attendance_date = loader.load()
    player_manager = PlayerManager(attendance_name)
    calculator = ScoreCalculator(player_manager)
    calculator.calculate_scores(attendance_name, attendance_date)
    calculator.apply_bonus_points()
    points = calculator.get_points()
    grade_applier = GradeApplier(player_manager, points['points'])

    # Act
    grades = grade_applier.get_grades()

    # Assert
    assert all(isinstance(pid, int) for pid in grades.keys())
    assert all(isinstance(grade, Grade) for grade in grades.values())

def test_reportGenerator_print_grade_info(capsys):
    # Assign
    loader = AttendanceLoader(ATTENDANCE_LIST_FILE)
    attendance_name, attendance_date = loader.load()
    player_manager = PlayerManager(attendance_name)
    calculator = ScoreCalculator(player_manager)
    calculator.calculate_scores(attendance_name, attendance_date)
    calculator.apply_bonus_points()
    points = calculator.get_points()
    grade_applier = GradeApplier(player_manager, points['points'])
    grades = grade_applier.get_grades()
    report_generator = ReportGenerator(player_manager, points, grades)

    # Act
    report_generator.print_grade_info()
    captured = capsys.readouterr()

    # Assert
    assert "NAME" in captured.out
    assert "POINT" in captured.out
    assert "GRAD" in captured.out

def test_reportGenerator_print_removed_players(capsys):
    # Assign
    loader = AttendanceLoader(ATTENDANCE_LIST_FILE)
    attendance_name, attendance_date = loader.load()
    player_manager = PlayerManager(attendance_name)
    calculator = ScoreCalculator(player_manager)
    calculator.calculate_scores(attendance_name, attendance_date)
    calculator.apply_bonus_points()
    points = calculator.get_points()
    grade_applier = GradeApplier(player_manager, points['points'])
    grades = grade_applier.get_grades()
    report_generator = ReportGenerator(player_manager, points, grades)

    # Act
    report_generator.print_removed_players()
    captured = capsys.readouterr()

    # Assert
    assert "Removed player" in captured.out
    assert "==============" in captured.out

def test_attendanceProcessor_run(capsys):
    # Assign
    processor = AttendanceProcessor(ATTENDANCE_LIST_FILE)

    # Act
    processor.run()
    captured = capsys.readouterr()

    # Assert
    assert "NAME" in captured.out
    assert "POINT" in captured.out
    assert "GRADE" in captured.out
    assert "Removed player" in captured.out

def test_attendanceProcessor_run_invalid_input(capsys):
    # Assign
    processor = AttendanceProcessor("non_existent_file.txt")

    # Act
    processor.run()
    captured = capsys.readouterr()

    # Assert
    assert "오류 발생" in captured.out
