import pygame

# Variables
gameClose = False
dragging = False
dragged_index = None
off_x = 0
off_y = 0
board = 'board.png'
chess_positions = {
    "white_pawn": "pieces/white-pawn.png",
    "white_rook": "pieces/white-rook.png",
    "white_knight": "pieces/white-knight.png",
    "white_bishop": "pieces/white-bishop.png",
    "white_queen": "pieces/white-queen.png",
    "white_king": "pieces/white-king.png",
    "black_pawn": "pieces/black-pawn.png",
    "black_rook": "pieces/black-rook.png",
    "black_knight": "pieces/black-knight.png",
    "black_bishop": "pieces/black-bishop.png",
    "black_queen": "pieces/black-queen.png",
    "black_king": "pieces/black-king.png"
}
# 128x128 is size of pieces
loadRect = {}
squares = {}
loaded = {}

co = {}
# Initial Position of All Pieces
initial_positions = {
    "a1": "white_rook",
    "b1": "white_knight",
    "c1": "white_bishop",
    "d1": "white_queen",
    "e1": "white_king",
    "f1": "white_bishop",
    "g1": "white_knight",
    "h1": "white_rook",
    
    "a2": "white_pawn",
    "b2": "white_pawn",
    "c2": "white_pawn",
    "d2": "white_pawn",
    "e2": "white_pawn",
    "f2": "white_pawn",
    
    "h8": "black_rook",
    "h2": "white_pawn",

    "a8": "black_rook",
    "b8": "black_knight",
    "c8": "black_bishop",
    "d8": "black_queen",
    "e8": "black_king",
    "f8": "black_bishop",
    "g8": "black_knight",
    "g2": "white_pawn",
    
    "a7": "black_pawn",
    "b7": "black_pawn",
    "c7": "black_pawn",
    "d7": "black_pawn",
    "e7": "black_pawn",
    "f7": "black_pawn",
    "g7": "black_pawn",
    "h7": "black_pawn",
}

# Legel Moves
def legel(piece, cob, coa):
    # Extract current and target positions
    x1 = ord(cob[0]) - ord('a')
    y1 = int(cob[1])
    x2 = ord(coa[0]) - ord('a')
    y2 = int(coa[1])

    # White pawn logic
    if piece == "white_pawn":
        if x1 == x2:  # Moving straight
            if y2 == y1 + 1:  # Move forward one square
                return True
            elif y1 == 2 and y2 == 4:  # Initial double move
                return True
        return False  # If none of the conditions are met

    # Black pawn logic
    elif piece == "black_pawn":
        if x1 == x2:  # Moving straight
            if y1 > 5:  # Allow moving only if current rank is greater than 5
                if y2 == y1 - 1:  # Move forward one square
                    return True
                elif y1 == 7 and y2 == 5:  # Initial double move
                    return True
        return False  # If none of the conditions are met

    elif piece == "white_rook":
        if x1==x2 or y1 == y2:
            return True
    elif piece == "black_rook":
        if x1==x2 or y1 == y2:
            return True
    elif piece in ["black_bishop", "white_bishop"]:
        if abs(x1-x2) == abs(y1-y2):
            return True    
    elif piece in ["black_queen", "white_queen"]:
        if abs(x1-x2) == abs(y1-y2) or x1==x2 or y1==y2:
            return True
    elif piece in ["black_king", "white_king"]: 
        if abs(x2-x1) == 1 or abs(y2-y1) == 1:
            return True  
    elif piece in ["black_knight", "white_knight"]: 
        if (abs(x2-x1)==2 and abs(y2-y1) == 1) or (abs(y2-y1)==2 and abs(x2-x1) == 1):
            return True  
    return False  # If none of the conditions are met

def insert_before_index(original_dict, new_key, new_value, index):
    # Convert the dictionary items to a list
    items = list(original_dict.items())
    
    # Insert the new key-value pair at the specified index
    items.insert(index, (new_key, new_value))
    
    # Reconstruct the dictionary from the modified list
    original_dict.clear()
    original_dict.update(items)        

pygame.init()
game = pygame.display.set_mode((800,800))
pygame.display.set_caption("Chess Game by Dharmik")

clock = pygame.time.Clock()
# load and Transform Images
boardImg = pygame.image.load(board)
for i,j  in chess_positions.items():
    xs = pygame.image.load(j)
    loaded[i] = pygame.transform.scale(xs, (100,100))
boardImg = pygame.transform.scale(boardImg, (800,800))

# Assigning Coordinates
letters = ["a","b","c","d","e","f","g","h"]
letter = {"a":5,"b":3,"c":2,"d":0,"e":-2,"f":-3,"g":-5,"h":-6}

no = [1,2,3,4,5,6,7,8]
nos = [3,1,2,0,-2,-5,-8,-9]
nos = nos[::-1]
for x in range(8):
    for y in range(-1, -9, -1):
        co[letters[x]+str(no[y])] = (100*(x)+letter[letters[x]], (100*(abs(y)-1))+nos[y])
# print(co)
for x in range(8):
    for y in range(8):  
        rect = pygame.Rect(x*100,y*100, 100, 100)
        squares[(x,y)] = rect
for posi, piece in initial_positions.items():
    rect = loaded[piece].get_rect(topleft=co[posi])
    loadRect[posi] = rect
while not gameClose:
    for event in pygame.event.get():
        # Bliting The Image
        game.blit(boardImg, (0,0))
        # Setup Board
        for posi, piece in initial_positions.items():
            game.blit(loaded[piece], loadRect[posi])
        # cob = 0
        pygame.display.update()
        # Events
        if event.type == pygame.QUIT:
            gameClose = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, l in enumerate(loadRect.values()):
                if l.collidepoint(event.pos):
                    cob = list(initial_positions.keys())[i]
                    piecec = list(initial_positions.values())[i]
                    dragging = True
                    dragged_index = i
                    off_x = l.x
                    off_y = l.y
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            new_x = (event.pos[0]//100)
            new_y = (event.pos[1]//100)
            finalloc = letters[new_x]+str(no[7-new_y])
            if dragging and dragged_index is not None:
                dragging = False
                dragged_index = None    
                try:
                    if legel(piecec, cob, finalloc):
                        loadRect[cob].topleft = (new_x*100, new_y*100)
                        xas = loadRect[cob]
                        if legel(piecec, cob, finalloc) and finalloc not in initial_positions:
                            if finalloc not in loadRect:
                                insert_before_index(loadRect, finalloc, xas, dragged_index)
                                del loadRect[cob]
                                
                                if cob in initial_positions:
                                    print(f"{cob}, {piecec}, {finalloc}")
                                    insert_before_index(initial_positions, finalloc, piecec, dragged_index)  # Add it to the new position
                                    del initial_positions[cob]  # Remove the piece from the current position
                                    print(initial_positions)
                                else:
                                    print("False")
                                    list(loadRect.values())[dragged_index].x  = off_x
                                    list(loadRect.values())[dragged_index].y  =off_y
                        break
                except:
                    try:
                        if legel(piecec, cob, finalloc):
                            loadRect[cob].topleft = (new_x*100, new_y*100)
                            xas = loadRect[cob]
                            if legel(piecec, cob, finalloc) and finalloc not in initial_positions:
                                if finalloc not in loadRect:
                                    insert_before_index(loadRect, finalloc, xas, dragged_index)
                                    del loadRect[cob]
                                    
                                    if cob in initial_positions:
                                        print(f"{cob}, {piecec}, {finalloc}")
                                        insert_before_index(initial_positions, finalloc, piecec, dragged_index)  # Add it to the new position
                                        del initial_positions[cob]  # Remove the piece from the current position
                                        print(initial_positions)
                                    else:
                                        list(loadRect.values())[dragged_index].x  = squares[cob][0]
                                        list(loadRect.values())[dragged_index].y  = squares[cob][1]
                    except:
                        print("Error")
            
        # elif event.type == pygame.MOUSEMOTION:
        #     if dragging:
        #         list(loadRect.values())[dragged_index].x  = (event.pos[0]//100)*100
        #         list(loadRect.values())[dragged_index].y  = (event.pos[1]//100)*100
                
    clock.tick(60)
    pygame.display.update()
                
pygame.quit()
quit()