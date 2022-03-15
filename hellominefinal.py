from tkinter import *
from itertools import product
import random
import numpy as np
from tkinter import messagebox
import sys
sys.setrecursionlimit(100000000)

def check(i, j,block, neighbor,grid,lose, recur = False): #지뢰인지 아닌지를 check
    #질 경우 check 
    if lose(i, j) and not recur:
        for i in range(len(block)):
            for j in range(len(block[0])):
                           block[i][j].config(state = DISABLED, text = "X" if grid[i][j] else " ", bg = 'red' if grid[i][j] else 'green')
        messagebox.showinfo("Lose", "You Lose")
        return
    mine_count = len([1 for x,y in neighbor(i, j) if grid[x][y]]) # 주변의 있는 지뢰의 갯수 세기 

    if mine_count:
        block[i][j].config(state=DISABLED, text = str(mine_count), fg ="red")
        visited.append((i, j))
        return
        
    else:
        block[i][j].config(state=DISABLED, relief = FLAT)
        visited.append((i,j))
        relativeCoord = ((1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
        for crd in relativeCoord:
            if 0 <= i + crd[0] < len(grid) and 0 <= j + crd[1] < len(grid[0]) and (i + crd[0], j + crd[1]) not in visited:
                check(i + crd[0], j + crd[1], block, neighbor, grid, lose, recur = True)
                
def flag(i, j, block, mineCoord): # 깃발 설치 
    if block[i][j]['state'] != DISABLED: #활성화된 버튼이라면 깃발 설치 
        flagged.append((i,j))
        block[i][j].config(text = 'O', bg = 'blue', state = DISABLED)
    elif block[i][j]['state'] == DISABLED and block[i][j].cget('text') == 'O': #이미 깃발이 설치되어 있다면 
        flagged.remove((i,j))
        block[i][j].config(text = "", bg = 'white', state = NORMAL) #다시 보통 상태로 복귀

    if sorted(flagged) == sorted(mineCoord):
        for x in range(len(block)):
            for y in range(len(block)):
                block[x][y].config(state = DISABLED, relief = FLAT)

        messagebox.showinfo("Win", "You Win!")
def setup_level(size1, size2, mines):
    master.geometry('%dx%d' %(size1 * 20, size2 * 20))
    mineCoord = random.sample(sum([[(i,j) for j in range(size2)] for i in range(size1)], []), mines)
    grid = np.array([[0 for j in range(size2)] for i in range(size1)]) #block의 위치를 정할 grid
    neighbor = lambda i, j: [i for i in [(i+1,j), (i-1, j), (i, j+1), (i, j-1), (i+1, j+1), (i-1,j-1), (i+1,j-1), (i-1, j+1)] if 0 <= i[0] < len(grid) and 0 <= i[1] < len(grid[0])] #주변의 상대적 좌표
    lose = lambda i, j: bool(grid[i][j])
    for i, j in mineCoord: #정해진 사이즈만큼중에 10개의 지뢰를 생성 
        grid[i][j] = 1 #지뢰 생성, 지뢰는 [i][j] == 1일 때 지뢰
    block = [[Button(master, command=(lambda x_=i, y_=j: check(y_, x_, block, neighbor, grid, lose)), bg = 'white') for i in range(len(grid[0]))] for j in range(len(grid))] #버튼(block) 생성 이곳의 grid[0]과 grid를 바꾸면 해결의 실마리가 보일 것 
    for j in range(len(grid[0])):
        for i in range(len(grid)):
            block[i][j].bind('<Button-3>', (lambda event, i_=i, j_=j: flag(i_, j_, block, mineCoord))) # 우클릭 시 깃발 설치
        
    for i in range(len(block)):
        for j in range(len(block[i])):
            block[i][j].place(x = i*20, y = j*20, width = 20, height = 20) #블록의 크기 정하기 및 배치 

        
size1 = 9
size2 = 9
mines = 10
def easymode():
    size1 = 9
    size2 = 9
    mines = 10
    setup_level(size1, size2, mines)
    return
def normalmode():
    size1 = 16
    size2 = 16
    mines = 40
    setup_level(size1, size2, mines)
    return
def hardmode():
    size1 = 30
    size2 = 16
    mines = 99
    setup_level(size1, size2, mines)
    return
master = Tk()
master.title("Hello, Mine!")
master.geometry('%dx%d' %(size1 * 20, size2 * 20))

menubar = Menu(master)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label = "9 x 9", command = easymode)

filemenu.add_command(label = "16 x 16", command = normalmode)

filemenu.add_command(label = "16 x 30", command = hardmode)
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = master.destroy)
menubar.add_cascade(label = "File", menu = filemenu)

master.config(menu = menubar)


visited = []
flagged = []


master.mainloop()



 
