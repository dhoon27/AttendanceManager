from player_manager import PlayerManager
from utils import DAY_POINT, BONUS_WED, BONUS_WEEKEND, BONUS_WED_THRESHOLD, BONUS_WEEKEND_THRESHOLD


class ScoreCalculator:
    def __init__(self, player_manager: PlayerManager):
        self.player_manager = player_manager
        self.wed_score_dict = {pid: 0 for pid in player_manager.get_all_player_ids()}
        self.weekend_score_dict = {pid: 0 for pid in player_manager.get_all_player_ids()}
        self.point_dict = {pid: 0 for pid in player_manager.get_all_player_ids()}

    def calculate_scores(self, attendance_name_list: list[str], attendance_date_list: list[str]):
        for name, date in zip(attendance_name_list, attendance_date_list):
            player_id = self.player_manager.get_player_id(name)
            if player_id:
                self.point_dict[player_id] += DAY_POINT.get(date, 0)
                if date == "wednesday":
                    self.wed_score_dict[player_id] += 1
                elif date in ("saturday", "sunday"):
                    self.weekend_score_dict[player_id] += 1

    def apply_bonus_points(self):
        for player_id in self.player_manager.get_all_player_ids():
            if self.wed_score_dict[player_id] > BONUS_WED_THRESHOLD:
                self.point_dict[player_id] += BONUS_WED
            if self.weekend_score_dict[player_id] > BONUS_WEEKEND_THRESHOLD:
                self.point_dict[player_id] += BONUS_WEEKEND

    def get_points(self) -> dict:
        return {
            'points': self.point_dict,
            'wed_scores': self.wed_score_dict,
            'weekend_scores': self.weekend_score_dict
        }