from typing import Tuple, Iterable

State = [[" " for _ in range(3)] for _ in range(3)]
Action = Tuple[int, int]
Player = Tuple[str, str] 
Utility = float

Game = 0

class TicTacToe(Game):
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def initial(self) -> State:
        return [[" " for _ in range(3)] for _ in range(3)]
    
    def player(self, s: State) -> Player:
        return "X" if sum(row.count("X") for row in s) == sum(row.count("O") for row in s) else "O"
    
    def actions(self, s:State) -> Iterable[Action]:
        return [(i, j) for i in range(3) for j in range(3) if s[i][j] == " "]
    
    def result(self, s: State, a: Action) -> State:
        i, j = a
        s[i][j] = self.player(s)
        return s
    
    def final(self, s: State) -> bool:
        for i in range(3):
            if all(cell == "X" for cell in s[i]) or all(cell == "O" for cell in s[i]):
                return True
            if all(s[j][i] == "X" for j in range(3)) or all(s[j][i] == "O" for j in range(3)):
                return True
        if all(s[i][i] == "X" for i in range(3)) or all(s[i][i] == "O" for i in range(3)):
            return True
        if all(s[i][2 - i] == "X" for i in range(3)) or all(s[i][2 - i] == "O" for i in range(3)):
            return True
        if all(cell != " " for row in s for cell in row):
            return True
        return False  

    def utility(self, s: State, p: Player) -> Utility:
        assert self.final(s)
        sp, sn = s
        if sp == p:
            return float("inf") * -1
        elif sp == " ":
            return 0
        else:
            return float("inf")


    def show(self, s: State) -> None:
        for row in s:
            print(" | ".join(row))
            print("-" * 5)
        print()

