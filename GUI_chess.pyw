import sys, pygame
from random import choice
from math import floor,ceil
pygame.init()
FEN = "6Q1/6p1/p1R3kp/5b1q/P2p4/3P4/1P1B1PPb/5R1K b"
turn = FEN.split(" ")[1]
board = []
check_board = board[:]
FEN = "".join(reversed(FEN.split(" ")[0].split("/")))
for char in FEN:
    if char in "12345678":
        board = board + ["E"] * int(char)
    else:
        board.append(char)

SRC_DIR = "src"
print(len(board))



pieceSize = 100
choices = []
size = width, height = pieceSize*8+200, pieceSize*8
screen = pygame.display.set_mode(size)
pieceImages = {"K": pygame.image.load("%s/wk.png" % SRC_DIR),
                   "Q":  pygame.image.load("%s/wq.png" % SRC_DIR),
                   "R":  pygame.image.load("%s/wr.png" % SRC_DIR),
                   "B":  pygame.image.load("%s/wb.png" % SRC_DIR),
                   "N":  pygame.image.load("%s/wn.png" % SRC_DIR),
                   "P":  pygame.image.load("%s/wp.png" % SRC_DIR),
                   "k":  pygame.image.load("%s/k.png" % SRC_DIR),
                   "q":  pygame.image.load("%s/q.png" % SRC_DIR),
                   "r":  pygame.image.load("%s/r.png" % SRC_DIR),
                   "b":  pygame.image.load("%s/b.png" % SRC_DIR),
                   "n":  pygame.image.load("%s/n.png" % SRC_DIR),
                   "p":  pygame.image.load("%s/p.png" % SRC_DIR),
                    "dark":pygame.image.load("%s/dark.png" % SRC_DIR),
                "light":pygame.image.load("%s/light.png" % SRC_DIR),
               "selected":pygame.image.load("%s/selected.png" % SRC_DIR),
               "dot":pygame.image.load("%s/dot.png"%SRC_DIR),
               "check":pygame.image.load("%s/check.png"%SRC_DIR)
                   }

for key in pieceImages.keys():
    pieceImages[key] = pygame.transform.scale(pieceImages[key].convert_alpha(),(pieceSize,pieceSize))
imageRect = pieceImages["K"].get_rect()



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
    "p": 1,
    "b":2,
    "q":2,
    "r":1,
}

def getFile(n):
    return n&7

def getRank(n):
    return n>>3
def getSquare(file,rank):
    return
def getManhattan(sq1, sq2):
    file1 = sq1 & 7
    file2 = sq2 & 7
    rank1 = sq1 >> 3
    rank2 = sq2 >> 3
    rankDistance = abs(rank2 - rank1)
    fileDistance = abs(file2 - file1)
    return rankDistance + fileDistance



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
                        if getManhattan(index,index-move_direction)>manhattan[piece.lower()]:
                            break
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
                if 15 >= start >= 8 and getManhattan(start, start + 16) == 2 and board[start + 16] == "E" and board[start +8] == "E":
                    psuedo_legal.append((start, start + 16))
        if piece.lower() and turn == "b":
            if piece in "rbq":
                for move_direction in rayMoves[piece.lower()]:
                    index = start + move_direction

                    while 0 <= index <= 63:
                        if getManhattan(index,index-move_direction)>manhattan[piece.lower()]:
                            break
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
                if 55 >= start >= 48 and getManhattan(start, start - 16) == 2 and board[start - 16] == "E" and board[start - 8] == "E":
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

##### secret devcodes
imSoRandom = False
cheatCodeBuffer = ["*"]*6
def draw():

    divboard = list(reversed([board[i:i + 8] for i in range(0, len(board), 8)]))
    c = 56
    for line in range(8):
        for char in range(8):
            location = [char*pieceSize,line*pieceSize]
            if(line+char) %2 ==0:
                screen.blit(pieceImages["dark"],location)
            else:
                screen.blit(pieceImages["light"],location)
            if ([char,7-line] == [getFile(selected),getRank(selected)]):
                screen.blit(pieceImages["selected"],location)
            if check == "w" and divboard[line][char] == "K":
                screen.blit(pieceImages["check"],location)
                print("drawn w check")
            if check == "b" and divboard[line][char] == "k":
                screen.blit(pieceImages["check"],location)
                print("drawn b check")
            if divboard[line][char] !="E":
                screen.blit(pieceImages[divboard[line][char]],location)
            if c in choices:
                screen.blit(pieceImages["dot"],[location[0],location[1]])

            c+=1
        c-=16

    pygame.display.flip()



noRefresh = False;
selected = 999
dev = ""
click_mode = "empty"
check = "none"
while 1:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYUP:
            cheatCodeBuffer.append(event.unicode)
            cheatCodeBuffer.pop(0)
            print(cheatCodeBuffer)
            if cheatCodeBuffer == ["r","a","d","s","a","f"]:
                imSoRandom = True

                dev = turn
                print("initiated random")
        if event.type == pygame.MOUSEBUTTONUP:
            print("\n ~~~~~~~~~~~~")
            pos =  pygame.mouse.get_pos()
            clicked = [floor(pos[0]/pieceSize),floor((height-pos[1])/pieceSize)]
            clicked = clicked[0] + ((clicked[1]) * 8)
            if click_mode == "empty":
                print("click mode is empty")
                if board[clicked] !="E":
                    print("clicked on a piece",board[clicked])
                    if (board[clicked].isupper(),board[clicked].islower())[turn == "w"]:
                        print("piece is yours",)
                        selected = clicked
                        choices = [move[1] for move in legal if move[0] == selected]
                        click_mode = "choose"
            if click_mode =="choose":
                print("click mode is choose")
                choices = [move[1] for move in legal if move[0] == selected]
                if clicked in choices:
                    print(choices)
                    print("make move")
                    makeMove((selected,clicked))
                    selected = 999
                    choices = []
                    click_mode = "empty"
                    noRefresh = False;
                else:
                    if board[clicked] !="E":
                        print("clicked on another piece",board[clicked])
                        if (board[clicked].isupper(),board[clicked].islower())[turn == "w"]:
                            print("piece is yours")
                            selected = clicked
                            choices = [move[1] for move in legal if move[0] == selected]






    if noRefresh:
        continue
    psuedo_legal = generatePsuedoLegal(turn)
    legal = []
    board_cache = board[:]
    check = ""
    for possible in psuedo_legal:
        makeMove(possible)
        if not isInCheck(turn):
            legal.append(possible)
        board = board_cache[:]
    if isInCheck(turn):
        check = turn
        print("check")
        if len(legal )==0:
            print("checkmate")


    if turn == "w":
        turn = "b"
    else:
        turn = "w"


    noRefresh = True


