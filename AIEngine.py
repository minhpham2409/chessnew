# Simplified Evaluation Function
import math

from GameState import GameState
from config import DEPTH

piece_score = {"K": 20000, "Q": 900, "R": 500, "B": 330, "N": 320, "p": 100}

pawn_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
               [50, 50, 50, 50, 50, 50, 50, 50],
               [10, 10, 20, 30, 30, 20, 10, 10],
               [5, 5, 10, 25, 25, 10, 5, 5],
               [0, 0, 0, 20, 20, 0, 0, 0],
               [5, 5, 10, 0, 0, 10, 5, 5],
               [5, 10, 10, 20, 20, 10, 10, 5],
               [0, 0, 0, 0, 0, 0, 0, 0]]

knight_scores = [[-50, -40, -30, -30, -30, -30, -40, -50],
                 [-40, -20, 0, 0, 0, 0, -20, -40],
                 [-30, 0, 10, 15, 15, 10, 0, -30],
                 [-30, 5, 15, 20, 20, 15, 5, -30],
                 [-30, 0, 15, 20, 20, 15, 0, -30],
                 [-30, 5, 10, 15, 15, 10, 5, -30],
                 [-40, -20, 0, 5, 5, 0, -20, -40],
                 [-50, -40, -30, -30, -30, -30, -40, -50]]

bishop_scores = [[-20, -10, -10, -10, -10, -10, -10, -20],
                 [-10, 0, 0, 0, 0, 0, 0, -10],
                 [-10, 0, 5, 10, 10, 5, 0, -10],
                 [-10, 5, 5, 10, 10, 5, 5, -10],
                 [-10, 0, 10, 10, 10, 10, 0, -10],
                 [-10, 10, 10, 10, 10, 10, 10, -10],
                 [-10, 5, 0, 0, 0, 0, 5, -10],
                 [-20, -10, -10, -10, -10, -10, -10, -20]]

rook_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
               [5, 10, 10, 10, 10, 10, 10, 5],
               [-5, 0, 0, 0, 0, 0, 0, -5],
               [-5, 0, 0, 0, 0, 0, 0, -5],
               [-5, 0, 0, 0, 0, 0, 0, -5],
               [-5, 0, 0, 0, 0, 0, 0, -5],
               [-5, 0, 0, 0, 0, 0, 0, -5],
               [0, 0, 0, 5, 5, 0, 0, 0]]

queen_scores = [[-20, -10, -10, -5, -5, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-5, 0, 5, 5, 5, 5, 0, -5],
                [0, 0, 5, 5, 5, 5, 0, -5],
                [-10, 5, 5, 5, 5, 5, 0, -10],
                [-10, 0, 5, 0, 0, 0, 0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]]

king_middle_score = [[-30, -40, -40, -50, -50, -40, -40, -30],
                     [-30, -40, -40, -50, -50, -40, -40, -30],
                     [-30, -40, -40, -50, -50, -40, -40, -30],
                     [-30, -40, -40, -50, -50, -40, -40, -30],
                     [-20, -30, -30, -40, -40, -30, -30, -20],
                     [-10, -20, -20, -20, -20, -20, -20, -10],
                     [20, 20, 0, 0, 0, 0, 20, 20],
                     [20, 30, 10, 0, 0, 10, 30, 20]]

king_end_score = [[-50, -40, -30, -20, -20, -30, -40, -50],
                  [-30, -20, -10, 0, 0, -10, -20, -30],
                  [-30, -10, 20, 30, 30, 20, -10, -30],
                  [-30, -10, 30, 40, 40, 30, -10, -30],
                  [-30, -10, 30, 40, 40, 30, -10, -30],
                  [-30, -10, 20, 30, 30, 20, -10, -30],
                  [-30, -30, 0, 0, 0, 0, -30, -30],
                  [-50, -30, -30, -30, -30, -30, -30, -50]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1],
                         "wK": king_middle_score,
                         'bK': king_middle_score[::-1]
                         }


class AIEngine:
    def __init__(self):
        self.bestMove = None
        self.nodeCount = 0
    # Heuristic 1
    @staticmethod
    def getMaterialScore(gs):
        white_score = 0
        black_score = 0
        for row in range(len(gs.board)):
            for col in range(len(gs.board[row])):
                piece = gs.board[row][col]
                if piece != "--":
                    if piece[0] == "w":
                        white_score += piece_score[piece[1]]
                    else:
                        black_score += piece_score[piece[1]]
        return black_score - white_score

    # Heuristic 2
    @staticmethod
    def getPiecePositionScore(gs):
        score = 0
        for row in range(len(gs.board)):
            for col in range(len(gs.board[row])):
                piece = gs.board[row][col]
                if piece != "--":
                    if piece[0] == "b":
                        score += piece_position_scores[piece][row][col]
                    else:
                        score -= piece_position_scores[piece][row][col]
        return score

    def MiniMax(self, gs: GameState, depth):
        self.__resetParameter()
        self.__MiniMax(gs, depth, True)

    def __resetParameter(self):
        self.bestMove = None
        self.nodeCount = 0

    def __MiniMax(self, gs: GameState, depth, maximizingPlayer):
        """Return a move """
        if depth == 0:
            self.nodeCount += 1
            return AIEngine.evaluation(gs)

        moves = gs.getValidMoves()
        if maximizingPlayer:
            maxEval = - math.inf
            for move in moves:
                gs.makeMove(move)
                self.nodeCount += 1
                eval_score = self.__MiniMax(gs, depth - 1, False)
                if eval_score > maxEval:
                    maxEval = eval_score
                    if depth == DEPTH:
                        self.bestMove = move
                gs.undoMove()
            return maxEval
        else:
            minEval = math.inf
            for move in moves:
                gs.makeMove(move)
                self.nodeCount += 1
                eval_score = self.__MiniMax(gs, depth - 1, True)
                if eval_score < minEval:
                    minEval = eval_score
                    if depth == DEPTH:
                        self.bestMove = move
                gs.undoMove()
            return minEval

    @staticmethod
    def evaluation(gs):
        score = AIEngine.getPiecePositionScore(gs) + AIEngine.getMaterialScore(gs)
        return score
