from player_manager import PlayerManager
from grade import GradeFactory

class GradeApplier:
    def __init__(self, player_manager: PlayerManager, point_dict: dict):
        self.player_manager = player_manager
        self.point_dict = point_dict
        self.grade_info_dict = {}
        self._set_grades()

    def _set_grades(self):
        for player_id in self.player_manager.get_all_player_ids():
            point = self.point_dict[player_id]
            grade_object = GradeFactory.create_grade(point)
            self.grade_info_dict[player_id] = grade_object

    def get_grades(self) -> dict:
        return self.grade_info_dict