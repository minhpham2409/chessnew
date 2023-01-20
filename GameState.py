import util
import itertools


class GameState:

    def __init__(self):
        # Direction of each piece
        self.vP = {'b': [(2, 0), (1, 0), (1, 1), (1, -1)],
                   'w': [(-2, 0), (-1, 0), (-1, 1), (-1, -1)]}
        self.vN = {'b': [(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)],
                   'w': [(-2, -1), (-1, -2), (-2, 1), (-1, 2), (2, 1), (2, -1), (1, 2), (1, -2)]}
        self.vR = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.vB = [(1, 1), (-1, -1), (-1, 1), (1, -1)]

        self.rival = {'b': 'w', 'w': 'b'}
        self.capturedPieces = {'wp': 0, 'wR': 0, 'wN': 0, 'wB': 0, 'wK': 0,
                               'wQ': 0, 'bp': 0, 'bR': 0, 'bN': 0, 'bB': 0, 'bK': 0, 'bQ': 0}

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.turn = 'w'
        self.moveLog = []

    def makeMove(self, move):
        # Add capture piece
        if move.capturedPiece != '--':
            self.capturedPieces[move.capturedPiece] += 1

        self.board[move.sqEnd[0]][move.sqEnd[1]] = self.board[move.sqStart[0]][move.sqStart[1]]
        self.board[move.sqStart[0]][move.sqStart[1]] = '--'
        self.turn = self.rival[self.turn]
        self.moveLog.append(move)

    def undoMove(self):
        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.sqStart[0]][move.sqStart[1]] = move.movePiece
            self.board[move.sqEnd[0]][move.sqEnd[1]] = move.capturedPiece
            self.turn = self.rival[self.turn]

    def getAllPossibleMoves(self):

        pawnMoves = []
        knightMoves = []
        rookMoves = []
        bishopMoves = []
        queenMoves = []
        kingMoves = []
        for i in range(8):
            for j in range(8):
                # Check black or white
                if self.turn == self.board[i][j][0]:
                    # Check type of piece
                    piece = self.board[i][j][1]
                    if piece == 'p':
                        pawnMoves.extend(self.getPawnMoves(i, j))
                    elif piece == 'N':
                        knightMoves.extend(self.getKnightMoves(i, j))
                    elif piece == 'R':
                        rookMoves.extend(self.getRookMoves(i, j))
                    elif piece == 'B':
                        bishopMoves.extend(self.getBishopMoves(i, j))
                    elif piece == 'Q':
                        queenMoves.extend(self.getQueenMoves(i, j))
                    else:
                        kingMoves.extend(self.getKingMoves(i,j))

        moves = list(itertools.chain(pawnMoves, knightMoves, rookMoves, bishopMoves, queenMoves,kingMoves))
        # print("----------------------Move Pawn-----------------")
        # util.move_print(pawnMoves)
        # print("----------------------Move Pawn-----------------")
        # print("----------------------Move Knight-----------------")
        # util.move_print(knightMoves)
        # print("----------------------Move Knight-----------------")
        # print("----------------------Move Rook-----------------")
        # util.move_print(rookMoves)
        # print("----------------------Move Rook-----------------")
        # print("----------------------Move Bishop-----------------")
        # util.move_print(bishopMoves)
        # print("----------------------Move Bishop-----------------")
        # print("----------------------Move Queen-----------------")
        # util.move_print(queenMoves)
        # print("----------------------Move Queen-----------------")
        # print("----------------------Move King-----------------")
        # util.move_print(kingMoves)
        # print("----------------------Move King-----------------")

        util.getNumberOfMoves(moves)
        return moves

    def getPawnMoves(self, r, c):
        moves = []

        # Check special move
        if (self.turn == 'b' and r == 1) or (self.turn == 'w' and r == 6):
            des = (r + self.vP[self.turn][0][0], c)
            if self.board[des[0]][des[1]] == '--':
                moves.append(Move((r, c), des, self.board))

        des = (r + self.vP[self.turn][1][0], c)
        if self.board[des[0]][des[1]] == '--':
            moves.append(Move((r, c), des, self.board))

        # Check attack move

        des = (r + self.vP[self.turn][2][0], c + self.vP[self.turn][2][1])
        if self._checkValidRowCol(des):
            # Check des is a rival
            if self.board[des[0]][des[1]][0] == self.rival[self.turn]:
                moves.append(Move((r, c), des, self.board))

        des = (r + self.vP[self.turn][3][0], c + self.vP[self.turn][3][1])
        # Check des is a rival
        if self._checkValidRowCol(des):
            # Check des is a rival
            if self.board[des[0]][des[1]][0] == self.rival[self.turn]:
                moves.append(Move((r, c), des, self.board))
        return moves

    def getKnightMoves(self, r, c):
        moves = []
        start = (r, c)
        # can attack
        for i in range(8):
            end = (r + self.vN[self.turn][i][0], c + self.vN[self.turn][i][1])
            if self._checkValidRowCol(end) and self._checkCollision(start, end):
                moves.append(Move(start, end, self.board))
        return moves

    def getRookMoves(self, r, c):
        moves = []
        start = (r, c)
        for i in range(4):
            j = 1
            while True:
                end = (r + j * self.vR[i][0], c + j * self.vR[i][1])
                if self._checkValidRowCol(end) and self._checkCollision(start, end):
                    moves.append(Move(start, end, self.board))
                    j += 1
                else:
                    break
        return moves

    def getBishopMoves(self, r, c):
        moves = []
        start = (r, c)
        for i in range(4):
            j = 1
            while True:
                end = (r + j * self.vB[i][0], c + j * self.vB[i][1])
                if self._checkValidRowCol(end) and self._checkCollision(start, end):
                    moves.append(Move(start, end, self.board))
                    j += 1
                else:
                    break
        return moves

    def getQueenMoves(self, r, c):
        return self.getRookMoves(r, c) + self.getBishopMoves(r, c)

    def getKingMoves(self, r, c):
        moves = []
        start = (r, c)

        # Move as rook with step = 1
        for i in range(4):
            end = (r + self.vR[i][0], c + self.vR[i][1])
            if self._checkValidRowCol(end) and self._checkCollision(start, end):
                moves.append(Move(start, end, self.board))

        # Move as bishop with step = 1
        for i in range(4):
            end = (r + self.vB[i][0], c + self.vB[i][1])
            if self._checkValidRowCol(end) and self._checkCollision(start, end):
                moves.append(Move(start, end, self.board))

        return moves

    @staticmethod
    def _checkValidRowCol(p):
        if p[0] in range(8) and p[1] in range(8):
            return True
        return False

    def _checkCollision(self, start, end):
        if self.board[start[0]][start[1]][0] == self.board[end[0]][end[1]][0]:
            return False
        return True


class Move:
    """
    Class represent a move in game.
    It contains:  starting point coordinates, ending point coordinates, piece move and piece is captured
    """
    _rankMap = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
    _fileMap = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    # (6,0) -> (4,0) ---> a2-a4 . We need mapping to (rank,file) to represent a move

    def __init__(self, sqStart, sqEnd, board):
        self.sqStart = sqStart
        self.sqEnd = sqEnd
        self.movePiece = board[sqStart[0]][sqStart[1]]
        self.capturedPiece = board[sqEnd[0]][sqEnd[1]]
        self.moveID = 1000 * self.sqStart[0] + 100 * self.sqStart[1] + 10 * self.sqEnd[0] + self.sqEnd[1]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getNotation(self):
        return f'{Move._fileMap[self.sqStart[1]]}{Move._rankMap[self.sqStart[0]]}-{Move._fileMap[self.sqEnd[1]]}{Move._rankMap[self.sqEnd[0]]} '

# if __name__ == '__main__':
#     board = GameState().board
#     move = Move((6, 0), (4, 0), board).getNotation()
#     print(move)
