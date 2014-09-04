from .sgf_grammar import parse_sgf_game

class MySGFGame(object):
    def __init__(self, bytes):
        self.crude_parsed = parse_sgf_game(bytes)

    @property
    def game_result(self):
        parsed_result_tokens = self.crude_parsed.sequence[0].get('RE', [])
        return ''.join(parsed_result_tokens)

    @property
    def handicap(self):
        parsed_result_tokens = self.crude_parsed.sequence[0].get('HA', ['0'])
        return int(''.join(parsed_result_tokens))
