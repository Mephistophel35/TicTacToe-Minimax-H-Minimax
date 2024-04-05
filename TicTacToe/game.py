from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Union, Iterable, List, Optional, Callable
import random

State = Any
Action = Any
Player = Any
Utility = Union[int, float]


class Game(ABC):
    @abstractmethod
    def initial(self) -> State: ...
    @abstractmethod
    def player(self, s: State) -> Player: ...
    @abstractmethod
    def actions(self, s: State) -> Iterable[Action]: ...
    @abstractmethod
    def result(self, s: State, a: Action) -> State: ...
    @abstractmethod
    def final(self, s: State) -> bool: ...
    @abstractmethod
    def utility(self, s: State, p: Player) -> Utility: ...
    def show(self, s: State) -> None:
        return None

    def play(self, *move_functions: Callable[[Game, State], Action]) -> Utility:
        s = self.initial()
        self.show(s)
        while True:
            for move in move_functions:
                a = move(self, s)
                s = self.result(s, a)
                self.show(s)
                if self.final(s):
                    return self.utility(s, self.player(self.initial()))

def politica_simple(g, s):
    print("decido jugar con -1!")
    return "-1"


def politica_aleatoria(g, s):
    a = random.choice(g.actions(s))
    print(f"yolo, decido jugar con {a}")
    return a


def politica_humana(g, s):
    while True:

        try:
            # Asumiendo que las entradas se dan como 'fila,columna'
            a = input("Hola humano, ingresa una acción (fila,columna): ").strip()
            fila, columna = map(int, a.split(','))
            action = (fila, columna)
            if action in g.actions(s):
                return action
            print("Acción no válida, intenta de nuevo.")
        except ValueError:
            print("Formato inválido. Por favor, ingresa las coordenadas como dos números separados por una coma.")


def politica_minimax(g, s):
    jugador_actual = g.player(s)

    def max_val(s):
        if g.final(s):
            return g.utility(s, jugador_actual)
        valor_maximo = -1 * float("inf")
        for accion in g.actions(s):
            valor_maximo = max(valor_maximo, min_val(g.result(s, accion)))
        return valor_maximo

    def min_val(s):
        if g.final(s):
            return g.utility(s, jugador_actual)
        valor_minimo = float("inf")
        for accion in g.actions(s):
            valor_minimo = min(valor_minimo, max_val(g.result(s, accion)))
        return valor_minimo

    return max(g.actions(s), key=lambda a: min_val(g.result(s,a)))

"""
Para el poda alfa beta o h-minimax que es como lo leí es que ahora tenemos valores alfa y beta
que serán los responsables de hacer esto más eficiente al hacer que se "pode" el árbol
Esto no modificará el resultado, sólo lo hará más rápido.
"""

def H_minimax(g, s):
    jugador_actual = g.player(s)

    def max_val(s, alfa, beta):
        if g.final(s):
            return g.utility(s, jugador_actual)
        valor_maximo = -1 * float("inf")
        for accion in g.actions(s):
            valor_maximo = max(valor_maximo, min_val(g.result(s, accion), alfa, beta))
            #Ahora lo diferente es que verificamos si es que valor_maximo es más grande que beta
            if valor_maximo >= beta:
                #En caso de que sí pues lo retornamos
                return valor_maximo
            #Si no pues hacemos que beta sea el máximo de entre alfa y el valor_máximo
            alfa = max(alfa, valor_maximo)
        return valor_maximo

    def min_val(s, alfa, beta):
        if g.final(s):
            return g.utility(s, jugador_actual)
        valor_minimo = float("inf")
        for accion in g.actions(s):
            valor_minimo = min(valor_minimo, max_val(g.result(s, accion), alfa, beta))
            #Misma shit pero ahora verificamos si valor_minimo es más pequeño que alfa
            if valor_minimo <= alfa:
                #En caso de que sí lo returnamos
                return valor_minimo
            #Si no pues hacemos que beta sea el mínimo de entre beta y el valor_minimo
            beta = min(beta, valor_minimo)
        return valor_minimo

    #Nuestros hermosos
    alfa = -1 * float("inf")
    beta = float("inf")
    return max(g.actions(s), key=lambda a: min_val(g.result(s,a), alfa, beta))


#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------


class TicTacToe(Game):
    def __init__(self):
        #Hacemos que el board inicial sea el vacío que nos mande el método "initial"
        self.board: State = self.initial()

    def initial(self) -> State:
        #Tablero vacío
        return [[" " for _ in range(3)] for _ in range(3)]
    
    def player(self, s: State) -> Player:
        """ 
        aquí hacemos algo truculento tal que si todos los movimientos hechos
        es módulo dos, o también podemos preguntar si es impar pues le toca a X o a O
        """
        moves = sum(row.count("X") + row.count("O") for row in s)
        return "X" if moves % 2 == 0 else "O"
    
    def actions(self, s:State) -> Iterable[Action]:
        #Devolver la lista de todas las acciones posibles (i,j) donde las celdas estén vacías
        return [(i, j) for i in range(3) for j in range(3) if s[i][j] == " "]
    
    def result(self, s: State, a: Action) -> State:
        #Creamos un nuevo estado con lo que tenemos ya en el state
        #Esto se hace para evitar complicaciones y no modificar el estado original
        #Al más puro estilo Irene
        new_state = [row.copy() for row in s]
        i, j = a

        #Nos aseguramos que la acción es legal antes de poder hacerla.
        if new_state[i][j] == " ":
            #Aquí pues aplicamos el cambio a ese tablero
            new_state[i][j] = self.player(s)
        else:
            #Sino es legal el move pues ño.
            raise ValueError("Na-a-a")
        #Retornamos el nuevo estado
        return new_state
    
    def final(self, s: State) -> bool:
        #Aquí checamos si el tablero está lleno y también condiciones de victoria
        for i in range(3):
            if all(cell == s[i][0] != " " for cell in s[i]):
                return True
            if all(cell == s[0][i] != " " for cell in [s[0][i], s[1][i], s[2][i]]):
                return True
        if all(s[i][i] == s[0][0] != " " for i in range(3)):
            return True
        if all(s[i][2 - i] == s[0][2] != " " for i in range(3)):
            return True
        if all(cell != " " for row in s for cell in row):
            return True
        return False  


    def utility(self, s: State, p: Player) -> Utility:
        #Calculamos la utilidad del estado final para el jugador especificado
        if not self.final(s):
            return 0
        
        #Algo bien, algo goblin, algo artesanal
        opponent = self.opponent(p)
        
        #Aquí checamos que cosa
        for i in range(3):
            #Si P tiene 3 en raya ya sea en horizontal o vertical
            if all(cell == p for cell in s[i]) or all(s[j][i] == p for j in range(3)):
                return float("inf")
            #Si el oponente tiene 3 en raya ya sea en horizontal o vertical
            if all(cell == opponent for cell in s[i]) or all(s[j][i] == opponent for j in range(3)):
                return float("-inf")
        #Si p tiene una diagonal en raya o la diagonal invertida en raya
        if all(s[i][i] == p for i in range(3)) or all(s[i][2-i] == p for i in range(3)):
            return float("inf")
        #Si oponente tiene una diagonal en raya o la diagonal invertida en raya
        if all(s[i][i] == opponent for i in range(3)) or all(s[i][2-i] == opponent for i in range(3)):
            return float("-inf")
        
        return 0 #Empate

    def opponent(self, p: Player) -> Player:
        #Esto nos devuelve el oponente actual
        return "O" if p == "X" else "X"

    def show(self, s: State) -> None:
        #Esto muestra el tablero
        for row in s:
            print(" | ".join(row))
            print("-" * 9)
        print()

if __name__ == "__main__":
    # Crear una instancia del juego TicTacToe
    game = TicTacToe()
    result_utility = game.play(H_minimax, H_minimax)

    final_state = game.board
    if result_utility == float("inf"):
        print("Gana el jugador X. Tas bien plomo O")
    elif result_utility == float("-inf"):
        print("Gana el jugador O. Tas bien plomo X")
    else:
        print("Empate, plomos los dos.")