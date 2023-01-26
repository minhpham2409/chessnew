import util


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
        self.trans = {'w': "White",
                      'b': "Black"}

        self.getFunctionMove = {'p': self._getPawnMoves, 'R': self._getRookMoves,
                                'N': self._getKnightMoves, 'B': self._getBishopMoves,
                                'Q': self._getQueenMoves, 'K': self._getKingMoves}

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
        self.kingLocation = {'w': (7, 4), 'b': (0, 4)}

        # Format in ((x_pin,y_pin), (x_check,y_check), (dx,dy))
        self.pins = []
        # Format in ((x,y), (dx,dy)). Example ((4,4),(1,1))
        self.checks = []

    def makeMove(self, move):
        # Add capture piece
        if move.capturedPiece != '--':
            self.capturedPieces[move.capturedPiece] += 1

        self.board[move.sqEnd[0]][move.sqEnd[1]] = self.board[move.sqStart[0]][move.sqStart[1]]
        self.board[move.sqStart[0]][move.sqStart[1]] = '--'

        # If occurs pawn promotion
        if move.movePiece[1] == 'p' and move.sqEnd[0] in (0, 7):
            self.pawnPromotion(move)
            print(f"** Team {self.trans[self.turn]} has pawn promotion")

        # If King move
        if move.movePiece[1] == 'K':
            self.kingLocation[self.turn] = (move.sqEnd[0], move.sqEnd[1])

        self.turn = self.rival[self.turn]
        self.moveLog.append(move)

    def undoMove(self):
        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.sqStart[0]][move.sqStart[1]] = move.movePiece
            self.board[move.sqEnd[0]][move.sqEnd[1]] = move.capturedPiece
            self.turn = self.rival[self.turn]

    def getValidMoves(self):

        moves = []
        king_moves = self._getKingValidMoves()
        moves.extend(king_moves)
        self.pins, self.checks = self._getPinAndCheckPieces()
        num_checkers = len(self.checks)
        if num_checkers == 0:
            #   Get move of pin piece
            for pin in self.pins:
                type_pin = self.board[pin[0][0]][pin[0][1]][1]
                # Get square between check and king
                dx = (pin[1][0] - self.kingLocation[self.turn][0])
                dy = (pin[1][1] - self.kingLocation[self.turn][1])
                if dx == dy:
                    d = dx
                else:
                    d = dx + dy
                square = []
                for i in range(1, d + 1):
                    square.append((self.kingLocation[self.turn][0] + i * pin[2][0],
                                   self.kingLocation[self.turn][1] + i * pin[2][1]))
                moves_pin = self.getFunctionMove[type_pin](pin[0][0], pin[0][1])
                for move in moves_pin:
                    if move.sqEnd in square:
                        moves.append(move)

            #   Get move of another piece
            pin_tmp = [i[0] for i in self.pins]
            for i in range(8):
                for j in range(8):
                    # Check black or white
                    if self.turn == self.board[i][j][0]:
                        # Check type of piece
                        piece = self.board[i][j][1]
                        if (i, j) not in pin_tmp and piece != 'K':
                            moves.extend(self.getFunctionMove[piece](i, j))

        elif num_checkers == 1:
            # Get capture move
            capture_moves = []
            all_move = []
            for i in range(8):
                for j in range(8):
                    # Check black or white
                    if self.turn == self.board[i][j][0]:
                        # Check type of piece
                        piece = self.board[i][j][1]
                        if piece != 'K':
                            all_move.extend(self.getFunctionMove[piece](i, j, self.board))

            for move in all_move:
                if move.sqEnd == self.checks[0][0]:
                    capture_moves.append(move)

            # Get push move
            push_move = []
            type_check = self.board[self.checks[0][0][0]][self.checks[0][0][1]][1]
            if type_check == 'R' or type_check == 'B' or type_check == 'Q':

                # Get square between king and check
                square = []
                dx = (self.checks[0][0][0] - self.kingLocation[self.turn][0])
                dy = (self.checks[0][0][1] - self.kingLocation[self.turn][1])
                if dx == dy:
                    d = dx
                else:
                    d = dx + dy
                for i in range(1, d):
                    square.append((self.kingLocation[self.turn][0] + i * self.checks[0][1][0],
                                   self.kingLocation[self.turn][1] + i * self.checks[0][1][1]))
                for move in all_move:
                    if move.sqEnd in square:
                        push_move.append(move)

            print("push move:")
            util.move_print(push_move)
            print("Capture move:")
            util.move_print(capture_moves)
            print("King move: ")
            util.move_print(king_moves)

            moves.extend(push_move)
            moves.extend(capture_moves)
        else:
            moves = king_moves

        if not moves:
            print("Check mate")
        return moves

    def _getKingValidMoves(self):

        boardCopy = [row[:] for row in self.board]
        boardCopy[self.kingLocation[self.turn][0]][self.kingLocation[self.turn][1]] = '--'
        kingMoves = []

        # Lấy các nước đi của vua
        tmp = self._getKingMoves(self.kingLocation[self.turn][0], self.kingLocation[self.turn][1])

        # Lấy các ô có thể bị tấn công bởi đối thủ
        attack_square = self._getAttackSquare(boardCopy)

        # Kiểm tra nước đi của vua có hợp lệ hay không
        for move in tmp:
            if move.sqEnd not in attack_square:
                kingMoves.append(move)
        return kingMoves

    def _getAttackSquare(self, boardCopy):
        attackSquare = []
        self.turn = self.rival[self.turn]

        for i in range(8):
            for j in range(8):
                # Check black or white
                if self.turn == boardCopy[i][j][0]:
                    # Check type of piece
                    piece = self.board[i][j][1]
                    moves = self.getFunctionMove[piece](i, j, True)
                    for move in moves:
                        attackSquare.append(move.sqEnd)

        print("attack square pass")
        self.turn = self.rival[self.turn]
        return attackSquare

    def _getPinAndCheckPieces(self):

        checks = []
        pins = []
        sqStart = self.kingLocation[self.turn]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1))

        for i in range(len(directions)):
            direction = directions[i]
            j = 1
            possible_pin = ()
            while True:
                sqEnd = (sqStart[0] + j * direction[0], sqStart[1] + j * direction[1])
                if self._checkValidRowCol(sqEnd):
                    piece = self.board[sqEnd[0]][sqEnd[1]]
                    if piece[0] == self.turn:
                        if possible_pin:
                            break
                        else:
                            possible_pin = (sqEnd[0], sqEnd[1])
                    elif piece[0] == self.rival[self.turn]:
                        if (0 <= i <= 3 and piece[1] == "R") or (4 <= i <= 7 and piece[1] == "B") or (
                                j == 1 and piece[1] == "p" and (
                                (piece[0] == "w" and 6 <= i <= 7) or (piece[0] == "b" and 4 <= i <= 5))) or (
                                piece[1] == "Q"):
                            if possible_pin:
                                pins.append((possible_pin, sqEnd, direction))
                                break
                            else:
                                checks.append((sqEnd, direction))
                                break
                        else:
                            break
                    j += 1
                else:
                    break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2),
                        (2, -1), (2, 1), (-1, -2), (1, -2))

        for move in knight_moves:
            sqEnd = (sqStart[0] + move[0], sqStart[1] + move[1])
            if self._checkValidRowCol(sqEnd):
                end_piece = self.board[sqEnd[0]][sqEnd[1]]
                # enemy knight attacking a king
                if end_piece[0] == self.rival[self.turn] and end_piece[1] == "N":
                    checks.append((sqEnd, move))
        return pins, checks

    def _getPawnMoves(self, r, c, attackAble = False):
        moves = []
        if attackAble:
            des = (r + self.vP[self.turn][2][0], c + self.vP[self.turn][2][1])
            if self._checkValidRowCol(des):
                moves.append(Move((r, c), des, self.board))

            des = (r + self.vP[self.turn][3][0], c + self.vP[self.turn][3][1])
            if self._checkValidRowCol(des):
                moves.append(Move((r, c), des, self.board))
            return moves

        # Check special move
        if (self.turn == 'b' and r == 1) or (self.turn == 'w' and r == 6):
            des = (r + self.vP[self.turn][0][0], c)
            if self._checkValidRowCol(des) and self.board[des[0]][des[1]] == '--':
                moves.append(Move((r, c), des, self.board))

        des = (r + self.vP[self.turn][1][0], c)
        if self._checkValidRowCol(des) and self.board[des[0]][des[1]] == '--':
            moves.append(Move((r, c), des, self.board))

        # Check attack move

        des = (r + self.vP[self.turn][2][0], c + self.vP[self.turn][2][1])
        if self._checkValidRowCol(des) and self.board[des[0]][des[1]][0] == self.rival[self.turn]:
            moves.append(Move((r, c), des, self.board))

        des = (r + self.vP[self.turn][3][0], c + self.vP[self.turn][3][1])
        # Check des is a rival
        if self._checkValidRowCol(des) and self.board[des[0]][des[1]][0] == self.rival[self.turn]:
            moves.append(Move((r, c), des, self.board))

        # If occurs pawn en passant

        return moves

    def _getKnightMoves(self, r, c, attackAble=False):
        moves = []
        start = (r, c)
        # can attack
        for i in range(8):
            end = (r + self.vN[self.turn][i][0], c + self.vN[self.turn][i][1])
            if self._checkValidRowCol(end) and (attackAble or self._checkCollision(start, end)):
                moves.append(Move(start, end, self.board))
        return moves

    def _getRookMoves(self, r, c, attackAble=False):
        moves = []
        start = (r, c)
        for i in range(4):
            j = 1
            while True:
                end = (r + j * self.vR[i][0], c + j * self.vR[i][1])
                if self._checkValidRowCol(end):
                    typeCollision = self._checkCollision(start, end)
                    if typeCollision == 2:
                        moves.append(Move(start, end, self.board))
                        j += 1
                    elif typeCollision == 1 or (typeCollision == 0 and attackAble):
                        moves.append(Move(start, end, self.board))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def _getBishopMoves(self, r, c, attackAble=False):
        moves = []
        start = (r, c)
        for i in range(4):
            j = 1
            while True:
                end = (r + j * self.vB[i][0], c + j * self.vB[i][1])
                if self._checkValidRowCol(end):
                    typeCollision = self._checkCollision(start, end)
                    if typeCollision == 2:
                        moves.append(Move(start, end, self.board))
                        j += 1
                    elif typeCollision == 1 or (typeCollision == 0 and attackAble):
                        moves.append(Move(start, end, self.board))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def _getQueenMoves(self, r, c, attackAble=False):
        return self._getRookMoves(r, c, attackAble) + self._getBishopMoves(r, c, attackAble)

    def _getKingMoves(self, r, c, attackAble=False):
        moves = []
        start = (r, c)

        # Move as rook with step = 1
        for i in range(4):
            end = (r + self.vR[i][0], c + self.vR[i][1])
            if self._checkValidRowCol(end) and (attackAble or self._checkCollision(start, end)):
                moves.append(Move(start, end, self.board))

        # Move as bishop with step = 1
        for i in range(4):
            end = (r + self.vB[i][0], c + self.vB[i][1])
            if self._checkValidRowCol(end) and (attackAble or self._checkCollision(start, end)):
                moves.append(Move(start, end, self.board))

        return moves

    @staticmethod
    def _checkValidRowCol(p):
        if p[0] in range(8) and p[1] in range(8):
            return True
        return False

    def _checkCollision(self, start, end):
        # 0 represent collision with same team
        # 1 represent collision with enemy
        # 2 represent no collision
        if self.board[end[0]][end[1]][0] == '-':
            return 2
        if self.board[start[0]][start[1]][0] == self.board[end[0]][end[1]][0]:
            return 0
        return 1

    def pawnPromotion(self, move):
        self.board[move.sqEnd[0]][move.sqEnd[1]] = self.turn + 'Q'

    def getMoveNotation(self):
        s = ''
        move_turn = 0
        for move in self.moveLog:
            if move_turn % 2 == 0:
                s += f"\n{int(move_turn / 2 + 1)} "
            s += move.getNotation() + ' '
            move_turn += 1
        s = s.removeprefix('\n')
        return s


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
