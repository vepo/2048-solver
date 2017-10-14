from random import randint
from BaseAI import BaseAI
import math

class MiniMaxAlgorithm:
    infinity = float('inf')
    MAX_DEEP = 30
    def __init__(self, grid):
        self.root = grid
        self.possibleNewTiles = [2, 4]
        self.deep = 0

    def decision(self):
        best_move, max_value = self.maximize(self.root)
        return best_move

    def maximize(self, grid):
        self.deep += 1
        moves = grid.getAvailableMoves()
        if moves == [] or self.deep > MiniMaxAlgorithm.MAX_DEEP:
            self.deep -= 1
            return None, self.evaluate(grid)

        max_value = -MiniMaxAlgorithm.infinity
        best_move = None
        for move in moves:
            next_grid = grid.clone()
            next_grid.move(move)
            next_value = self.minimize(next_grid)
            if next_value > max_value:
                max_value, best_move = next_value, move
        self.deep += 1
        return best_move, max_value

    def minimize(self, grid):
        """As a stocastic game, we will not calculate the minimum, but the average to the max"""
        self.deep += 1
        cells = grid.getAvailableCells()
        if cells == [] or self.deep > MiniMaxAlgorithm.MAX_DEEP:
            self.deep -= 1
            return self.evaluate(grid)

        values = []
        for cell in cells:
            for cell_value in self.possibleNewTiles:
                next_grid = grid.clone()
                next_grid.setCellValue(cell, cell_value)
                move, value = self.maximize(next_grid)
                values.append(value)
        self.deep -= 1
        return sum(values) / float(len(values))

    def evaluate(self, grid):
        max_is_edge = False
        max_value = -MiniMaxAlgorithm.infinity
        value = 0
        for x in range(0, 3):
            for y in range(0, 3):
                if grid.map[x][y] >= max_value:
                    max_is_edge = (x == 0 and y == 0) or (x == 3 and y == 0) or (x == 0 and y == 3) or (x == 3 and y == 3)
                    max_value = grid.map[x][y]
                value += grid.map[x][y]
        if max_is_edge:
            value *= 2
        return value + len(grid.getAvailableCells()) * 10

class PlayerAI(BaseAI):
    def getMove(self, grid):
        algorithm = MiniMaxAlgorithm(grid)
        return algorithm.decision()