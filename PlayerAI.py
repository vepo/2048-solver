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
        self.maxDeep = 4

    def decision(self):
        max_value = -MiniMaxAlgorithm.infinity
        best_move = None
        for move in self.root.getAvailableMoves():
            next_grid = self.root.clone()
            next_grid.move(move)
            value = self.minimize(next_grid)
            if max_value < value:
                best_move = move
        return best_move

    def maximize(self, grid):
        self.deep += 1
        moves = grid.getAvailableMoves()
        if moves == [] or self.deep > self.maxDeep:
            self.deep -= 1
            return None, self.evaluate(grid)

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
            return None, self.evaluate(grid)

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
        value = sum(map(sum, map(lambda x: map(lambda y: math.pow(y, 2), x), grid.map)))
        return (value * math.pow(self.deep + 1, 3)) * (1 + math.pow(len(grid.getAvailableMoves()), 3))

class PlayerAI(BaseAI):
    def getMove(self, grid):
        algorithm = MiniMaxAlgorithm(grid)
        return algorithm.decision()