# 상수 선언
ROOT_PATH="../"
ATTENDANCE_LIST_FILE = ROOT_PATH+"attendance_weekday_500.txt"

MAX_PLAYER = 19
MAX_ATTENDANCE = 500
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_POINT = {
    "monday": 1,
    "tuesday": 1,
    "wednesday": 3,
    "thursday": 1,
    "friday": 1,
    "saturday": 2,
    "sunday": 2
}
GRADE_GOLD = 1
GRADE_SILVER = 2
GRADE_NORMAL = 0
GOLD_POINT = 50
SILVER_POINT = 30
BONUS_WED = 10
BONUS_WEEKEND = 10
BONUS_WED_THRESHOLD = 9
BONUS_WEEKEND_THRESHOLD = 9

# 전역 변수 선언
player_id_list = {}      # 이름 → id
player_name_list = {}    # id → 이름
wed_score_dict = {}      # id → 수요일 출석 횟수
weekend_score_dict = {}  # id → 주말 출석 횟수
point_dict = {}          # id → 점수
grade_dict = {}          # id → 등급

def is_valid_name(name: str) -> bool:
    return bool(name and name.strip())

def is_valid_date(date: str) -> bool:
    return date in WEEKDAYS

def get_attendance_list() -> tuple[list, list]:
    attendance_name = []
    attendance_date = []
    try:
        with open(ATTENDANCE_LIST_FILE, encoding='utf-8') as f:
            for _ in range(MAX_ATTENDANCE):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) != 2:
                    raise ValueError("입력 데이터 형식 오류")
                name, date = parts
                if not is_valid_name(name):
                    raise ValueError(f"잘못된 이름: {name}")
                if not is_valid_date(date):
                    raise ValueError(f"잘못된 요일: {date}")
                attendance_name.append(name)
                attendance_date.append(date)
    except FileNotFoundError:
        raise FileNotFoundError("파일을 찾을 수 없습니다.")
    return attendance_name, attendance_date

def set_player_name_and_id(attendance_name_list: list):
    id_cnt = 0
    for name in attendance_name_list:
        if name not in player_id_list:
            id_cnt += 1
            player_id_list[name] = id_cnt
            player_name_list[id_cnt] = name
            wed_score_dict[id_cnt] = 0
            weekend_score_dict[id_cnt] = 0
            point_dict[id_cnt] = 0
            grade_dict[id_cnt] = GRADE_NORMAL

def update_score(attendance_name_list: list[str], attendance_date_list: list[str]) -> None:
    for name, date in zip(attendance_name_list, attendance_date_list):
        id = player_id_list.get(name)
        add_point = DAY_POINT.get(date)
        if date == "wednesday":
            wed_score_dict[id] += 1
        if date in ("saturday", "sunday"):
            weekend_score_dict[id] += 1
        point_dict[id] += add_point

def get_additional_points():
    for id in player_id_list.values():
        if wed_score_dict[id] > BONUS_WED_THRESHOLD:
            point_dict[id] += BONUS_WED
        if weekend_score_dict[id] > BONUS_WEEKEND_THRESHOLD:
            point_dict[id] += BONUS_WEEKEND

def set_grade():
    for id in player_id_list.values():
        if point_dict[id] >= GOLD_POINT:
            grade_dict[id] = GRADE_GOLD
        elif point_dict[id] >= SILVER_POINT:
            grade_dict[id] = GRADE_SILVER
        else:
            grade_dict[id] = GRADE_NORMAL

def get_grade(id) -> str:
    if grade_dict[id] == GRADE_GOLD:
        grade = "GOLD"
    elif grade_dict[id] == GRADE_SILVER:
        grade = "SILVER"
    else:
        grade = "NORMAL"
    return grade

def get_grade_info() -> list[dict]:
    grade_info = []
    for id in player_id_list.values():
        grade_info.append({
            "name": player_name_list[id],
            "point": point_dict[id],
            "grade": get_grade(id)
        })
    return grade_info

def print_grade():
    for info in get_grade_info():
        print(f"NAME : {info['name']}, POINT : {info['point']}, GRADE : {info['grade']}")

def get_removed_players():
    removed = []
    for id in player_id_list.values():
        if grade_dict[id] == GRADE_NORMAL and \
                wed_score_dict[id] == 0 and weekend_score_dict[id] == 0:
            removed.append(player_name_list[id])
    return removed

def print_removed_players():
    print("\nRemoved player")
    print("==============")
    for removed_name in get_removed_players():
        print(removed_name)

def process_attendance():
    try:
        attendance_name, attendance_date = get_attendance_list()
        set_player_name_and_id(attendance_name)
        update_score(attendance_name, attendance_date)
        get_additional_points()
        set_grade()
        print_grade()
        print_removed_players()
    except Exception as e:
        print(f"오류 발생: {e}")
        return

if __name__ == "__main__":
    process_attendance()
