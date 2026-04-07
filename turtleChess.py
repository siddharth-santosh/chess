import turtle as t
import time

# ================= SETTINGS =================

S=80
OX=-320
OY=-320

t.tracer(0)
t.hideturtle()
t.penup()

# ================= SYMBOLS =================

SYM={
"wp":"♙","wr":"♖","wn":"♘","wb":"♗","wq":"♕","wk":"♔",
"bp":"♟","br":"♜","bn":"♞","bb":"♝","bq":"♛","bk":"♚"
}

# ================= BOARD =================

board=[
["br","bn","bb","bq","bk","bb","bn","br"],
["bp"]*8,
["--"]*8,
["--"]*8,
["--"]*8,
["--"]*8,
["wp"]*8,
["wr","wn","wb","wq","wk","wb","wn","wr"]
]

turn="w"
selected=None
legal=[]
promotion=None
game_over=False

# ================= DRAW =================

def square():
    t.pendown()
    for _ in range(4):
        t.forward(S); t.left(90)
    t.penup()

def draw_board():
    for r in range(8):
        for c in range(8):
            t.goto(OX+c*S,OY+r*S)
            col="white" if (r+c)%2==0 else "green"
            t.color("black",col)
            t.begin_fill(); square(); t.end_fill()

def highlight(r,c,color):
    t.goto(OX+c*S,OY+r*S)
    t.color("black",color)
    t.begin_fill(); square(); t.end_fill()

def draw_pieces():
    for r in range(8):
        for c in range(8):
            p=board[r][c]
            if p!="--":
                t.goto(OX+c*S+40,OY+r*S+20)
                t.write(SYM[p],align="center",font=("Arial",32,"normal"))

def redraw():
    t.clear()
    draw_board()
    draw_pieces()
    t.update()

redraw()

# ================= HELPERS =================

def inside(r,c): return 0<=r<8 and 0<=c<8
def color(p): return p[0]
def enemy(a,b): return b!="--" and color(a)!=color(b)

# ================= RAW MOVES =================

def pawn(r,c):
    m=[]
    p=board[r][c]
    d=-1 if p[0]=="w" else 1
    start=6 if p[0]=="w" else 1
    if inside(r+d,c) and board[r+d][c]=="--":
        m.append((r+d,c))
        if r==start and board[r+2*d][c]=="--":
            m.append((r+2*d,c))
    for dc in [-1,1]:
        if inside(r+d,c+dc) and enemy(p,board[r+d][c+dc]):
            m.append((r+d,c+dc))
    return m

def line(r,c,dirs):
    m=[]
    p=board[r][c]
    for dr,dc in dirs:
        rr=r+dr; cc=c+dc
        while inside(rr,cc):
            if board[rr][cc]=="--":
                m.append((rr,cc))
            elif enemy(p,board[rr][cc]):
                m.append((rr,cc)); break
            else: break
            rr+=dr; cc+=dc
    return m

def knight(r,c):
    m=[]
    p=board[r][c]
    for dr,dc in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
        rr=r+dr; cc=c+dc
        if inside(rr,cc):
            if board[rr][cc]=="--" or enemy(p,board[rr][cc]):
                m.append((rr,cc))
    return m

def king_raw(r,c):
    m=[]
    p=board[r][c]
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            if dr==dc==0: continue
            rr=r+dr; cc=c+dc
            if inside(rr,cc):
                if board[rr][cc]=="--" or enemy(p,board[rr][cc]):
                    m.append((rr,cc))
    return m

def raw_moves(r,c):
    p=board[r][c]
    if p=="--": return []
    if p[1]=="p": return pawn(r,c)
    if p[1]=="r": return line(r,c,[(1,0),(-1,0),(0,1),(0,-1)])
    if p[1]=="b": return line(r,c,[(1,1),(1,-1),(-1,1),(-1,-1)])
    if p[1]=="q": return line(r,c,[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)])
    if p[1]=="n": return knight(r,c)
    if p[1]=="k": return king_raw(r,c)
    return []

# ================= CHECK DETECTION =================

def find_king(side):
    for r in range(8):
        for c in range(8):
            if board[r][c]==side+"k":
                return (r,c)

def square_attacked(r,c,by):
    for i in range(8):
        for j in range(8):
            p=board[i][j]
            if p!="--" and p[0]==by:
                if (r,c) in raw_moves(i,j):
                    return True
    return False

def in_check(side):
    kr,kc=find_king(side)
    opp="b" if side=="w" else "w"
    return square_attacked(kr,kc,opp)

# ================= LEGAL MOVES =================

def legal_moves(r,c):
    moves=[]
    p=board[r][c]
    for tr,tc in raw_moves(r,c):
        save=board[tr][tc]
        board[tr][tc]=p
        board[r][c]="--"
        if not in_check(p[0]):
            moves.append((tr,tc))
        board[r][c]=p
        board[tr][tc]=save
    return moves

# ================= CHECKMATE =================

def checkmate(side):
    if not in_check(side): return False
    for r in range(8):
        for c in range(8):
            if board[r][c]!="--" and board[r][c][0]==side:
                if legal_moves(r,c):
                    return False
    return True

# ================= ANIMATION =================

anim=t.Turtle()
anim.hideturtle()
anim.penup()

def animate(sr,sc,tr,tc,p):
    x1=OX+sc*S+40; y1=OY+sr*S+20
    x2=OX+tc*S+40; y2=OY+tr*S+20
    for i in range(12):
        x=x1+(x2-x1)*i/12
        y=y1+(y2-y1)*i/12
        anim.clear()
        anim.goto(x,y)
        anim.write(SYM[p],align="center",font=("Arial",32,"normal"))
        t.update()
        time.sleep(0.01)
    anim.clear()

# ================= PROMOTION =================

def draw_promo(side):
    for i,p in enumerate(["q","r","b","n"]):
        highlight(3,i+2,"orange")
        t.goto(OX+(i+2)*S+40,OY+3*S+20)
        t.write(SYM[side+p],align="center",
                font=("Arial",32,"normal"))

# ================= CLICK =================

def click(x,y):
    global selected,legal,turn,promotion,game_over

    if game_over: return

    c=int((x-OX)//S)
    r=int((y-OY)//S)
    if not inside(r,c): return

    # Promotion choice
    if promotion:
        pr,pc=promotion
        if r==3 and 2<=c<=5:
            board[pr][pc]=turn+["q","r","b","n"][c-2]
            promotion=None
            turn="b" if turn=="w" else "w"
            redraw()
        return

    # Select piece
    if selected is None:
        if board[r][c]!="--" and board[r][c][0]==turn:
            selected=(r,c)
            legal=legal_moves(r,c)
            t.clear()
            draw_board()
            for m in legal:
                highlight(m[0],m[1],"yellow")
            highlight(r,c,"orange")
            draw_pieces()
            t.update()
        return

    sr,sc=selected
    if (r,c) in legal:
        p=board[sr][sc]
        animate(sr,sc,r,c,p)
        board[r][c]=p
        board[sr][sc]="--"

        if p[1]=="p" and (r==0 or r==7):
            promotion=(r,c)
            redraw()
            draw_promo(turn)
            t.update()
            selected=None
            legal=[]
            return

        turn="b" if turn=="w" else "w"

        if checkmate(turn):
            redraw()
            t.goto(0,0)
            t.write("CHECKMATE!",align="center",
                    font=("Arial",36,"bold"))
            game_over=True
            return

    selected=None
    legal=[]
    redraw()

# ================= START =================

t.onscreenclick(click)
t.mainloop()