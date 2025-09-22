from attendance import *

def test_get_attendance_list():
    # Assign
    names = []
    dates = []

    # Act
    names, dates = get_attendance_list()

    # Assert
    assert len(names) == len(dates)
    assert all(isinstance(name, str) for name in names)
    assert all(isinstance(date, str) and date in WEEKDAYS for date in dates)

def test_set_player_name_and_id():
    # Assign
    names, dates = get_attendance_list()

    # Act
    set_player_name_and_id(names)

    # Assert
    assert len(player_id_list) == 19
    assert len(player_name_list) == 19
    assert len(wed_score_dict) == 19
    assert len(weekend_score_dict) == 19
    assert len(point_dict) == 19
    assert len(grade_dict) == 19

def test_update_score():
    # Assign
    names, dates = get_attendance_list()
    set_player_name_and_id(names)

    # Act
    update_score(names, dates)

    # Assert
    assert all(isinstance(score, int) and score >= 0 for score in wed_score_dict.values())
    assert all(isinstance(score, int) and score >= 0 for score in weekend_score_dict.values())
    assert all(isinstance(score, int) and score >= 0 for score in point_dict.values())

def test_additional_points():
    # Assign
    names, dates = get_attendance_list()
    set_player_name_and_id(names)
    update_score(names, dates)

    # Act
    get_additional_points()

    # Assert
    assert all(isinstance(score, int) and score >= 0 for score in point_dict.values())

def test_set_grade():
    # Assign
    names, dates = get_attendance_list()
    set_player_name_and_id(names)
    update_score(names, dates)
    get_additional_points()

    # Act
    set_grade()

    # Assert
    assert all(grade in (GRADE_GOLD, GRADE_SILVER, GRADE_NORMAL) for grade in grade_dict.values())

def test_get_grade_info():
    # Assign
    names, dates = get_attendance_list()
    set_player_name_and_id(names)
    update_score(names, dates)
    get_additional_points()
    set_grade()

    # Act
    grade_info = get_grade_info()

    # Assert
    assert len(grade_info) == 19
    for info in grade_info:
        assert "name" in info and isinstance(info["name"], str)
        assert "point" in info and isinstance(info["point"], int) and info["point"] >= 0
        assert "grade" in info and info["grade"] in ("GOLD", "SILVER", "NORMAL")

def test_print_grade(capsys):
    # Assign
    names, dates = get_attendance_list()
    set_player_name_and_id(names)
    update_score(names, dates)
    get_additional_points()
    set_grade()

    # Act
    print_grade()

    # Assert
    captured = capsys.readouterr()
    assert "NAME :" in captured.out
    assert "POINT :" in captured.out
    assert "GRADE :" in captured.out

def test_get_removed_players():
    # Assign
    names, dates = get_attendance_list()
    set_player_name_and_id(names)
    update_score(names, dates)
    get_additional_points()
    set_grade()

    # Act
    removed_players = get_removed_players()

    # Assert
    assert all(isinstance(name, str) for name in removed_players)
    assert all(name in player_name_list.values() for name in removed_players)

def test_print_removed_players(capsys):
    # Assign
    names, dates = get_attendance_list()
    set_player_name_and_id(names)
    update_score(names, dates)
    get_additional_points()
    set_grade()

    # Act
    print_removed_players()
    captured = capsys.readouterr()

    # Assert
    assert "Removed player" in captured.out
    assert "==============" in captured.out


def test_process_attendance(capsys):
    # Assign
    # No specific assignment for process_attendance

    # Act
    process_attendance()

    # Assert
    captured = capsys.readouterr()
    assert "NAME :" in captured.out
    assert "POINT :" in captured.out
    assert "GRADE :" in captured.out
    assert "Removed player" in captured.out
    assert "==============" in captured.out