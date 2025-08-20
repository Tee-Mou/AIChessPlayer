
import numpy as np
import re
from pathlib import Path

class Game():
    
    existing_ids: set[int] = set()

    def __init__(self, moves: list[str], avg_rating: float):
        self.move_list: list[str] = moves
        self.bias: float = 10**((avg_rating - 1000) / 400)
        id: int = -1
        while True:
            id = np.ceil(np.random.random() * 100000)
            if id not in Game.existing_ids:
                Game.existing_ids.add(id)
                break

        self.id: int = np.ceil(np.random.random() * 100000)

class GameDB():

    def __init__(self, games: list[Game] | None = None):
        self.games: dict[int, Game] = {}
        if isinstance(games, list):
            for game in games:
                self.games[game.id] = game

    def add_game(self, moves: list[str], avg_rating: float) -> bool:
        new_game: Game = Game(moves=moves, avg_rating=avg_rating)
        self.games[new_game.id] = new_game
        if self.games[new_game.id] == new_game:
            return True
        
        return False
            
    def remove_game(self, id: int) -> bool:
        try:
            self.games.pop(id)
            return True
        
        except KeyError:
            return False

    @staticmethod
    def parse_moves(move_str: str) -> list[str]:
        pattern = r"{\s.*?\s}"
        move_str = re.sub(pattern=pattern, repl="", string=move_str)
        move_str = move_str.replace("?", "").replace("!", "").replace("+", "").replace("#", "")
        move_list: list[str] = move_str.split(". ")[1:]
        for i in range(len(move_list)):
            move_list[i] = move_list[i][0:move_list[i].find(" ")]
        return move_list

    def process_data(self, file_dir: Path):
        with open(file=file_dir, mode="r", encoding="utf8") as f:
            games_data = f.read().split("\n\n\n")
            for game in games_data:
                avg_rating: float = 0.0
                moves: list[str] = []
                lines = game.split("\n")
                for line in lines:
                    if len(line) == 0:
                        continue
                    elif line.startswith("[WhiteElo") or line.startswith("[BlackElo"):
                        avg_rating += int(line[11:-2])
                    elif line[0] == "1":
                        moves = GameDB.parse_moves(line)
                        

                avg_rating /= 2
                if len(moves) > 20:
                    self.add_game(moves=moves, avg_rating=avg_rating)
                    continue