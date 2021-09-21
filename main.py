import curses
import re

stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
pieceValues = {
    "r": 5,
    "b": 3,
    "q": 9,
    "n": 3,
    "p": 1,
    "k": 999
}
moveList = []
material = {"w": 0, "b": 0}
# convert FEN to board
manhattan = {
    "n": 3,
    "k": 2,
    "p": 1
}

def getRank(n):
    return n>>3
print(getRank(63))


def getManhattan(sq1, sq2):
    file1 = sq1 & 7
    file2 = sq2 & 7
    rank1 = sq1 >> 3
    rank2 = sq2 >> 3
    rankDistance = abs(rank2 - rank1)
    fileDistance = abs(file2 - file1)
    return rankDistance + fileDistance


pieceCharacters = {"K": "\u2654",
                   "Q": "\u2655",
                   "R": "\u2656",
                   "B": "\u2657",
                   "N": "\u2658",
                   "P": "\u2659",
                   "k": "\u265A",
                   "q": "\u265B",
                   "r": "\u265C",
                   "b": "\u265D",
                   "n": "\u265E",
                   "p": "\u265F",
                   "E": " "
                   }
rayMoves = {
    "r": [8, -8, 1, -1],
    "b": [7, -7, 9, -9],
    "q": [7, -7, 9, -9, 8, -8, 1, -1]
}
oneMoves = {
    "k": [7, -7, 9, -9, 8, -8, 1, -1],
    "n": [17, 15, -17, -15, 10, 6, -6, -10]
}
check = False
legal = []


def generatePsuedoLegal(turn):
    psuedo_legal = []
    for start, piece in enumerate(board):
        if piece.isupper() and turn == "w":
            if piece in "RBQ":
                for move_direction in rayMoves[piece.lower()]:
                    index = start + move_direction
                    while 0 <= index <= 63:

                        if board[index] != "E":
                            if board[index].isupper():
                                break
                            else:
                                psuedo_legal.append((start, index))
                                break
                        psuedo_legal.append((start, index))
                        index += move_direction
            elif piece in "NK":
                for move_direction in oneMoves[piece.lower()]:
                    end = start + move_direction
                    if 63 >= start + move_direction >= 0 and getManhattan(start, end) <= manhattan[piece.lower()]:
                        if board[end] == "E":
                            psuedo_legal.append((start, end))
                        elif board[end].islower():
                            psuedo_legal.append((start, end))

            elif piece == "P":
                if board[start + 8] == "E" and getManhattan(start, start + 8) == 1:
                    psuedo_legal.append((start, start + 8))
                if board[start + 9] != "E" and board[start + 9].islower() and getManhattan(start, start + 9) == 2:
                    psuedo_legal.append((start, start + 9))
                if board[start + 7] != "E" and board[start + 7].islower() and getManhattan(start, start + 7) == 2:
                    psuedo_legal.append((start, start + 7))
                if 15 >= start >= 8 and getManhattan(start, start + 16) == 2 and board[start + 16] == "E":
                    psuedo_legal.append((start, start + 16))
        if piece.lower() and turn == "b":
            if piece in "rbq":
                for move_direction in rayMoves[piece.lower()]:
                    index = start + move_direction
                    while 0 <= index <= 63:

                        if board[index] != "E":
                            if board[index].islower():
                                break
                            else:
                                psuedo_legal.append((start, index))
                                break
                        psuedo_legal.append((start, index))
                        index += move_direction
            elif piece in "nk":
                for move_direction in oneMoves[piece.lower()]:
                    end = start + move_direction
                    if 63 >= end >= 0 and getManhattan(start, end) <= manhattan[piece.lower()]:
                        if board[end] == "E":
                            psuedo_legal.append((start, end))
                        elif board[end].isupper():
                            psuedo_legal.append((start, end))
            elif piece == "p":
                if board[start - 8] == "E" and getManhattan(start, start - 8) == 1:
                    psuedo_legal.append((start, start - 8))
                if board[start - 9] != "E" and board[start - 9].isupper() and getManhattan(start, start - 9) == 2:
                    psuedo_legal.append((start, start - 9))
                if board[start - 7] != "E" and board[start - 7].isupper() and getManhattan(start, start - 7) == 2:
                    psuedo_legal.append((start, start - 7))
                if 55 >= start >= 48 and getManhattan(start, start - 16) == 2 and board[start - 16] == "E":
                    psuedo_legal.append((start, start - 16))
    return psuedo_legal


def makeMove(move):
    if board[move[0]]== "p" and  getRank(move[1]) == 0:
        board[move[0]] = "E"
        board[move[1]]= "q"
    elif board[move[0]]== "P" and  getRank(move[1]) == 7:
        board[move[0]] = "E"
        board[move[1]]= "Q"
    else:
        board[move[1]] = board[move[0]]
        board[move[0]] = "E"


def printBoard(flip=False):
    stdscr.addstr(1, 10, "material:" + str(material["w"] - material["b"]))
    divboard = list(reversed([board[i:i + 8] for i in range(0, len(board), 8)]))
    for line in range(8):
        for char in range(8):
            if ((line + char) % 2 == 0):
                stdscr.addch(line, char + 1, pieceCharacters[divboard[line][char]], curses.color_pair(1))
            else:
                stdscr.addch(line, char + 1, pieceCharacters[divboard[line][char]], curses.color_pair(2))
    stdscr.addstr(8, 1, "abcdefgh")
    for line in range(8):
        stdscr.addch(line, 0, str(8 - line))


def ANToInt(AN):
    return "abcdefgh".index(AN[0]) + ((int(AN[1]) - 1) * 8)


def isInCheck(turn):
    check = False
    if turn == "w":
        kingIndex = board.index("K")
        psuedo_legal = generatePsuedoLegal("b")
        for move in psuedo_legal:
            if move[1] == kingIndex:
                check = True
    if turn == "b":
        kingIndex = board.index("k")
        psuedo_legal = generatePsuedoLegal("w")
        for move in psuedo_legal:
            if move[1] == kingIndex:
                check = True
    return check


stdscr.notimeout(1)
while True:
    board = [
    ]
    material = {"w":0,"b":0}

    stdscr.clear()
    stdscr.addstr(0, 0, "welcome to MCHESS v1.0")
    stdscr.addstr(1, 0, "(O)ver the board")
    stdscr.addstr(2, 0, "(C)ustom position")
    stdscr.refresh()
    choice = "000"
    while choice not in "ocOC":
        choice = chr(stdscr.getch())
    if choice.lower() == "o":
        FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
    elif choice.lower() == "c":
        pass
    turn = FEN.split(" ")[1]
    board = []
    check_board = board[:]
    FEN = "".join(reversed(FEN.split(" ")[0].split("/")))
    for char in FEN:
        if char in "12345678":
            board = board + ["E"] * int(char)
        else:
            board.append(char)
            if char.islower():
                material["b"] += pieceValues[char]
            if char.isupper():
                material["w"] += pieceValues[char.lower()]
        ###
        ###
    while True:
        stdscr.clear()
        psuedo_legal = generatePsuedoLegal(turn)
        legal = []
        board_cache = board[:]
        for possible in psuedo_legal:
            makeMove(possible)
            if not isInCheck(turn):
                legal.append(possible)
            board = board_cache[:]

        # stdscr.addstr(14,13, "%s legal moves" % len(legal))
        # try:
        #    stdscr.addstr(15,0,str(legal))
        # except curses.error:
        #    stdscr.addstr(14,0,"ER")
        #    pass
        stdscr.refresh()
        check_board = board[:]

        printBoard()
        stdscr.addstr(0, 9, "%s's turn" % {"w": "white", "b": "black"}[turn])
        if len(legal) == 0:
            if isInCheck(turn):
                stdscr.addstr(14, 2, "checkmate, %s is victorious" % {"w": "black", "b": "white"}[turn])
                stdscr.addstr(15, 2, "press any key to continue")
                stdscr.refresh()
                stdscr.getch()
                continue
            else:
                stdscr.addstr(14, 2, "draw by stalemate")
        if isInCheck(turn):
            stdscr.addstr(10, 0, "check!!")

        move = ""
        stdscr.addstr(11, 0, "your move in UCI:")
        while len(move) < 4:
            char = stdscr.getch()
            move = move + chr(char)
        if move == "0000":
            if turn == "w":
                turn = "b"
            else:
                turn = "w"
            continue

        if not re.match(r"([a-h][1-8][a-h][1-8])", move):
            continue
        ####debug tools#####
        if move == "skip":
            if turn == "w":
                turn = "b"
            else:
                turn = "w"
            continue
        start = str(move[0:2])
        target = str(move[2:4])
        chosenPiece = board[ANToInt(start)]
        stdscr.addstr(10, 0, "moving %s from %s (%d) to %s (%d)" % (
            chosenPiece, start, ANToInt(start), target, ANToInt(target)))
        move = (ANToInt(start), ANToInt(target))
        board_cache = board[:]

        if move in legal:
            stdscr.addstr(11, 0, "a legal move")
            if board[move[1]] != "E":
                material[("w", "b")[turn == "w"]] -= pieceValues[board[move[1]].lower()]
            makeMove(move)

        else:
            if move in psuedo_legal:
                stdscr.addstr(11, 0, "psuedo-legal!")
            else:
                stdscr.addstr(11, 0, "illegal!")
            stdscr.refresh()
            curses.napms(2000)
            continue
        if turn == "w":
            turn = "b"
        else:
            turn = "w"
