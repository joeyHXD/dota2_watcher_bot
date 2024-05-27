class Player:
    def __init__(self, short_steamID = "", nickname = "", last_DOTA2_match_ID = ""):
        self.short_steamID = short_steamID
        self.nickname = nickname
        self.last_DOTA2_match_ID = last_DOTA2_match_ID
        self.display_recent_match = True
        self.stats = {}

    def to_dict(self):
        output = {}
        output["short_steamID"] = self.short_steamID
        output["nickname"] = self.nickname
        output["last_DOTA2_match_ID"] = self.last_DOTA2_match_ID
        output["display_recent_match"] = self.display_recent_match
        return output

    def load_dict(self, d):
        self.short_steamID = d["short_steamID"]
        self.nickname = d["nickname"]
        self.last_DOTA2_match_ID = d["last_DOTA2_match_ID"]
        self.display_recent_match = d.get("display_recent_match", True)

    def load_player_info(self, player_game_info):
        tmp = {}
        tmp["kill"] = player_game_info['kills']
        tmp["death"] = player_game_info['deaths']
        tmp["assist"] = player_game_info['assists']
        tmp["kda"] = (tmp["kill"] +  tmp["assist"]) / max(tmp["death"], 1)

        tmp["dota2_team"] = player_game_info['team_number']
        tmp["hero"] = player_game_info['hero_id']
        tmp["last_hit"] = player_game_info['last_hits']
        tmp["damage"] = player_game_info['hero_damage']
        tmp["gpm"] = player_game_info['gold_per_min']
        tmp["xpm"] = player_game_info['xp_per_min']
        self.stats = tmp