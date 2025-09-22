from player_manager import PlayerManager


class ReportGenerator:
    def __init__(self, player_manager: PlayerManager, points: dict, grades: dict):
        self.player_manager = player_manager
        self.point_dict = points['points']
        self.grade_info_dict = grades
        self.wed_score_dict = points['wed_scores']
        self.weekend_score_dict = points['weekend_scores']

    def print_grade_info(self):
        for player_id in self.player_manager.get_all_player_ids():
            name = self.player_manager.get_player_name(player_id)
            point = self.point_dict[player_id]
            grade_object = self.grade_info_dict[player_id]
            print(f"NAME : {name}, POINT : {point}, GRADE : {grade_object.get_grade_name()}")

    def print_removed_players(self):
        print("\nRemoved player")
        print("==============")
        removed = []
        for player_id in self.player_manager.get_all_player_ids():
            name = self.player_manager.get_player_name(player_id)
            grade_object = self.grade_info_dict[player_id]
            if grade_object.get_grade_name() == "NORMAL" and \
                    self.wed_score_dict[player_id] == 0 and self.weekend_score_dict[player_id] == 0:
                removed.append(name)

        for removed_name in removed:
            print(removed_name)