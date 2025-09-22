class PlayerManager:
    def __init__(self, attendance_name_list: list):
        self.player_id_list = {}
        self.player_name_list = {}
        self._set_player_id(attendance_name_list)

    def _set_player_id(self, attendance_name_list: list):
        id_cnt = 0
        for name in attendance_name_list:
            if name not in self.player_id_list:
                id_cnt += 1
                self.player_id_list[name] = id_cnt
                self.player_name_list[id_cnt] = name

    def get_player_id(self, name: str) -> int:
        return self.player_id_list.get(name)

    def get_player_name(self, player_id: int) -> str:
        return self.player_name_list.get(player_id)

    def get_all_player_ids(self) -> list:
        return list(self.player_name_list.keys())