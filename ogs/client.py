import requests

OGS_BASE_URL = "https://online-go.com"

RANK_MAP = (
    ["%sk" % i for i in range(30, 0, -1)] +
    ["%sd" % i for i in range(1, 10)]
)


class OgsPlayer(object):
    def __init__(self, player_dict):
        for attr in ("id", "username", "icon", "ranking"):
            setattr(self, attr, player_dict[attr])

    @property
    def get_rank_display(self):
        if self.ranking < 30:
            return "%dk" % (30 - self.ranking)
        else:
            return "%dd" % ((self.ranking - 30) + 1)


def get_ladder_top_players(ladder_id):
    response = requests.get(OGS_BASE_URL + "/api/v1/ladders/%s" % ladder_id)
    raw = response.json()
    return [OgsPlayer(info['player']) for info in raw['top_players']]
