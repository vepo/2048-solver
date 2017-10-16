from random import randint
from BaseAI import BaseAI
import math
import time

class MiniMaxAlgorithm:
    infinity = float('inf')
    def __init__(self, grid):
        self.root = grid
        self.possibleNewTiles = [2, 4]
        self.deep = 0
        self.alpha = -MiniMaxAlgorithm.infinity
        self.beta = MiniMaxAlgorithm.infinity
        self.maxDeep = 6

    def decision(self):
        max_value = -MiniMaxAlgorithm.infinity
        best_move = None
        for move in self.root.getAvailableMoves():
            next_grid = self.root.clone()
            next_grid.move(move)
            value = self.minimize(next_grid)
            if max_value < value:
                max_value, best_move = value, move
        return best_move

    def maximize(self, grid):
        self.deep += 1
        moves = grid.getAvailableMoves()
        if moves == [] or self.deep > self.maxDeep:
            self.deep -= 1
            return self.evaluate(grid)

        ab_value = -MiniMaxAlgorithm.infinity

        for move in moves:
            next_grid = grid.clone()
            next_grid.move(move)
            ab_value = max(ab_value, self.minimize(next_grid))
            if ab_value >= self.beta:
                self.deep -= 1
                return ab_value

            self.alpha = max(self.alpha, ab_value)

        self.deep -= 1
        return ab_value

    def minimize(self, grid):
        """As a stocastic game, we will not calculate the minimum, but the average to the max"""
        self.deep += 1
        cells = grid.getAvailableCells()
        if cells == [] or self.deep > self.maxDeep:
            self.deep -= 1
            return self.evaluate(grid)

        ab_value = MiniMaxAlgorithm.infinity
        for cell in cells:
            for cell_value in self.possibleNewTiles:
                next_grid = grid.clone()
                next_grid.setCellValue(cell, cell_value)
                next_value = self.maximize(next_grid)
                ab_value = min(ab_value, next_value)
                if ab_value <= next_value:
                    self.deep -= 1
                    return ab_value

        self.deep -= 1
        return ab_value

    def evaluate(self, grid):
        order_matrix =  [[32768, 16384, 8192, 4096],
                         [  256,   512, 1024, 2048],
                         [  128,    64,   32,   16],
                         [    1,     2,    4,    8]]
        DEEP_VALUE = self.deep + 1
        diff_value = 0
        merging_values = 0
        sum_value = 0
        ordering_value = 0
        for x in range(0, 4):
            for y in range(0, 4):
                sum_value += grid.map[x][y]
                if grid.map[x][y] == 0:
                    pass
                ordering_value += order_matrix[x][y] * grid.map[x][y]
                if x > 0:
                    diff_value += abs(grid.map[x][y] - grid.map[x - 1][y])
                    if grid.map[x][y] == grid.map[x - 1][y]:
                        merging_values += grid.map[x][y]
                if y > 0:
                    diff_value += abs(grid.map[x][y] - grid.map[x][y - 1])
                    if grid.map[x][y] == grid.map[x][y - 1]:
                        merging_values += grid.map[x][y]
                if x < 3:
                    diff_value += abs(grid.map[x][y] - grid.map[x + 1][y])
                    if grid.map[x][y] == grid.map[x + 1][y]:
                        merging_values += grid.map[x][y]
                if y < 3:
                    diff_value += abs(grid.map[x][y] - grid.map[x][y + 1])
                    if grid.map[x][y] == grid.map[x][y + 1]:
                        merging_values += grid.map[x][y]
        
        return DEEP_VALUE * (sum_value + diff_value + merging_values + 2 * ordering_value)

class PlayerAI(BaseAI):
    def getMove(self, grid):
        algorithm = MiniMaxAlgorithm(grid)
        return algorithm.decision()