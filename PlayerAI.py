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
        self.maxDeep = max(10, len(self.root.getAvailableCells()) / 14)

    def decision(self):
        best_move, max_value = self.maximize(self.root)
        return best_move

    def maximize(self, grid):
        self.deep += 1
        moves = grid.getAvailableMoves()
        if moves == [] or self.deep > self.maxDeep:
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
                self.alpha = max(self.alpha, max_value)
                if self.beta <= self.alpha:
                    self.deep -= 1
                    return best_move, max_value
        self.deep -= 1
        return best_move, max_value

    def minimize(self, grid):
        """As a stocastic game, we will not calculate the minimum, but the average to the max"""
        self.deep += 1
        cells = grid.getAvailableCells()
        if cells == [] or self.deep > self.maxDeep:
            self.deep -= 1
            return None, self.evaluate(grid)

        min_value = MiniMaxAlgorithm.infinity
        for cell in cells:
            for cell_value in self.possibleNewTiles:
                next_grid = grid.clone()
                next_grid.setCellValue(cell, cell_value)
                move, next_value = self.maximize(next_grid)
                if next_value < min_value:
                    min_value = next_value
                    self.beta = min(self.beta, min_value)
                    if self.beta <= self.alpha:
                        self.deep -= 1
                        return min_value

        self.deep -= 1
        return min_value

    def evaluate(self, grid):
        value = sum(map(sum, map(lambda x: map( lambda y: y*y, x), grid.map)))
        return value * math.pow(self.deep, 2)

class PlayerAI(BaseAI):
    def getMove(self, grid):
        algorithm = MiniMaxAlgorithm(grid)
        return algorithm.decision()