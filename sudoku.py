from typing import List
import random
from collections import defaultdict
from collections import Counter
from collections import deque
import heapq
import math
from itertools import product
from functools import lru_cache
import sys

from collections import deque


from functools import lru_cache

sys.setrecursionlimit(10**6)

import copy
class Node:
    def __init__(self, idx = 0):
        self.idx = idx
        self.liste = []

class Sudoku:
    def __init__(self, board):
        self.row = []
        self.col = []
        self.case = [[] for i in range(9)]
        self.free = []
        self.boardo = copy.deepcopy(board)
        self.boardf = [['' for i in range(9)] for j in range(9)]

        for i in range(9):
            l = []
            for j in range(9):
                if board[i][j] != 0:
                    l.append((board[i][j], j, i))
                else:
                    self.free.append(i*9+j)
            self.row.append(l)

        for i in range(9):
            l = []
            for j in range(9):
                if board[j][i] != 0:
                    l.append((board[j][i], i, j))
            self.col.append(l)

        for i in range(9):
            for j in range(9):
                ind = (i//3) * 3 + (j//3)
                #print(ind)
                if board[i][j] != 0:
                    self.case[ind].append((board[i][j], j, i))

    def isValidSudoku(self, board):
        # lignes et colonnes
        for i in range(9):
            row = set()
            col = set()
            for j in range(9):
                # vérifier ligne
                if board[i][j] != 0:
                    if board[i][j] in row:
                        return False
                    row.add(board[i][j])
                # vérifier colonne
                if board[j][i] != 0:
                    if board[j][i] in col:
                        return False
                    col.add(board[j][i])
        
        # sous-grilles 3x3
        for block_i in range(3):
            for block_j in range(3):
                block = set()
                for i in range(3):
                    for j in range(3):
                        num = board[block_i*3 + i][block_j*3 + j]
                        if num != 0:
                            if num in block:
                                return False
                            block.add(num)
        return True

    def ValidRCC(self, row, col, case):


        for r in row:
            nums = [num for (num, _, _) in r]
            if len(nums) != len(set(nums)):
                print("row", nums)
                return False

        # Vérifie doublons dans chaque colonne
        for c in col:
            nums = [num for (num, _, _) in c]
            if len(nums) != len(set(nums)):
                print("col", nums)
                return False

        # Vérifie doublons dans chaque case 3x3
        for sc in case:
            nums = [num for (num, _, _) in sc]
            if len(nums) != len(set(nums)):
                print("case", nums)
                return False

        return True

    def Valid(self, row, col, case):

        setone = set(range(1, 10))
        setf = set()
        for r in row:
            nums = [num for (num, _, _) in r]
            if len(nums) != len(set(nums)):
                print("row", nums)
                return False

        # Vérifie doublons dans chaque colonne
        for c in col:
            nums = [num for (num, _, _) in c]
            if len(nums) != len(set(nums)):
                print("col", nums)
                return False

        # Vérifie doublons dans chaque case 3x3
        for sc in case:
            nums = [num for (num, _, _) in sc]
            if len(nums) != len(set(nums)):
                print("case", nums)
                return False

        for r in row:
            for n, x, y in r:
                setf.add(n)

       
        #sf =  ({num for (num, cx, cy) in row}|{num for (num, cx, cy) in col}|{num for (num, cx, cy) in case})
        return setf == setone

    
    def resolve(self):

        row = copy.deepcopy(self.row)
        col = copy.deepcopy(self.col)
        case =copy.deepcopy(self.case)
        free = copy.deepcopy(self.free)
        print(len(free))
        self.STOP = False
        
        self.COUNTER = 0

        #@lru_cache(None)
        def dfs(ind):#rw, cl, cse, 
                        
            if len(free) == 0:
                board = [[0 for i in range(9)] for j in range(9)]
                for r in row:
                    #print('r', r)
                    for v, x, y in r:
                        board[y][x] = v

                for b in board:
                    print(b)
                print('------')
                        
                if self.Valid(row,col,case):
                    
                    self.STOP = True

                    for i in range(9):
                        for j in range(9):
                            self.boardf[i][j] = str(board[i][j])
                            
                    for r in self.boardf:
                        print(r)

                    print('-----------------------------------------------------------------')
                return


            #row = copy.deepcopy(rw)
            #col = copy.deepcopy(cl)
            #case =copy.deepcopy(cse)
            #free = copy.deepcopy(fee)


            #for f in free:
            if self.STOP: return
            
            f = free.pop(0)
            cx = f % 9
            cy = f // 9

            indcase = (cy // 3) * 3 + (cx // 3)

            sr = row[cy]
            sc = col[cx]
            scase = case[indcase]

            setone = set(range(1,10))

            sminus = setone - ({num for (num, cx, cy) in sr}|{num for (num, cx, cy) in sc}|{num for (num, cx, cy) in scase})
            #print(sminus)
            for num in sminus:
                row[cy].append((num, cx, cy))
                col[cx].append((num, cx, cy))
                case[indcase].append((num, cx, cy))
          
                dfs(ind+1)
                self.COUNTER +=1

                row[cy].pop()
                col[cx].pop()
                case[indcase].pop()
                
            free.insert(0, f)

        dfs(0) #row, col, case, free)

        print("COUNTER=", self.COUNTER)


    def resolveBit(self):

        row = copy.deepcopy(self.row)
        col = copy.deepcopy(self.col)
        case =copy.deepcopy(self.case)
        free = copy.deepcopy(self.free)
        print(len(free))
        self.STOP = False
        board = copy.deepcopy(self.boardo)

        rowbit = [0] * 9
        colbit = [0] * 9
        boxbit = [0] * 9
        vide = []

        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    bit = 1 << board[i][j]

                    rowbit[i] |= bit
                    colbit[j] |= bit
                    boxbit[(i // 3) * 3 + (j // 3)] |= bit
                else:
                    vide.append((j, i))

        #@lru_cache(None)
        def dfs(ind):#rw, cl, cse, 

            if ind == len(vide):
                return self.isValidSudoku(board)

            i, j = vide[ind]
            boxind = (i // 3) * 3 + (j // 3)
            used = rowbit[i] | colbit[j] | boxbit[boxind]

            for num in range(9):

                bit = 1 << num

                if not (used & bit):

                    board[i][j] = num + 1
                    rowbit[i] |= bit
                    colbit[j] |= bit
                    boxbit[(i // 3) * 3 + (j // 3)] |= bit

                    if dfs(ind+1):
                        return True

                    board[i][j] = 0
                    rowbit[i] ^= bit
                    colbit[j] ^= bit
                    boxbit[(i // 3) * 3 + (j // 3)] ^= bit

            return False

        dfs(0)


        for i in range(9):
            for j in range(9):
                self.boardf[i][j] = str(board[i][j])

        for r in self.boardf:
            print(r)
            

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        
        board = [[int(x) if x.isdigit() else 0 for x in l]for l in board]

        #print(board)
            
        sudoku = Sudoku(board)
        sudoku.resolve()

#board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
board = [[".",".",".",".",".",".",".",".","."],[".","9",".",".","1",".",".","3","."],[".",".","6",".","2",".","7",".","."],[".",".",".","3",".","4",".",".","."],["2","1",".",".",".",".",".","9","8"],[".",".",".",".",".",".",".",".","."],[".",".","2","5",".","6","4",".","."],[".","8",".",".",".",".",".","1","."],[".",".",".",".",".",".",".",".","."]]

s = Solution()
print(s.solveSudoku(board))