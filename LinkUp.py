# -*- coding: latin-1 -*-
import sys
import time
from itertools import combinations, permutations

class LinkNode:
    def __init__(self):
        self.L = self.R = self.U = self.D = self
        self.C = None      # le header de colonne
        self.size = 0      # nombre de 1 dans la colonne
        self.rid = -1
        self.cid = -1


class ManageLink:
    def __init__(self, N_cols):
        self.N = N_cols

        # racine
        self.root = LinkNode()

        # colonnes
        self.colHeader = []
        last = self.root
        for i in range(N_cols):
            col = LinkNode()
            col.cid = i
            col.C = col
            col.size = 0
            col.U = col.D = col
            # lier horizontalement
            col.L = last
            col.R = last.R
            last.R.L = col
            last.R = col
            last = col
            self.colHeader.append(col)

    def addNode(self, row, col):
        node = LinkNode()
        node.rid = row
        node.cid = col

        # --- colonne ---
        colHead = self.colHeader[col]
        node.C = colHead
        node.D = colHead
        node.U = colHead.U
        colHead.U.D = node
        colHead.U = node
        colHead.size += 1

        # --- ligne : lier avec les autres n�uds de la m�me ligne ---
        # cherche � ajouter � la fin de la ligne existante
        left = node  # si premier de la ligne, se lie � lui-m�me
        # pour construire une ligne compl�te, on devra lier horizontalement tous les n�uds de cette ligne
        # c'est � faire lors de l�insertion multiple par ligne

        node.L = node.R = node  # si seul pour l'instant

        return node

    def linkRowNodes(self, nodes):
        """Recevoir une liste de n�uds appartenant � la m�me ligne et les lier horizontalement."""
        n = len(nodes)
        for i in range(n):
            nodes[i].R = nodes[(i+1)%n]
            nodes[i].L = nodes[(i-1)%n]

    def cover(self, colHead):
        # retirer la colonne
        colHead.R.L = colHead.L
        colHead.L.R = colHead.R

        # supprimer les lignes qui contiennent 1 dans cette colonne
        i = colHead.D
        while i != colHead:
            j = i.R
            while j != i:
                j.D.U = j.U
                j.U.D = j.D
                j.C.size -= 1
                j = j.R
            i = i.D

    def uncover(self, colHead):
        # restaurer les lignes
        i = colHead.U
        while i != colHead:
            j = i.L
            while j != i:
                j.C.size += 1
                j.D.U = j
                j.U.D = j
                j = j.L
            i = i.U

        # restaurer la colonne
        colHead.R.L = colHead
        colHead.L.R = colHead

    def visualizeColumns(self):
        print("---- Visualize columns ----")
        c = self.root.R
        while c != self.root:
            nodes = []
            n = c.D
            while n != c:
                nodes.append(f"({n.rid},{n.cid})")
                n = n.D
            print(f"Col {c.cid}: ", " -> ".join(nodes))
            c = c.R
        print("---------------------------")

       

def sudokuDLX(board):
    N_cols = 9*9*4  # 324 contraintes
    dlx = ManageLink(N_cols)
    row_map = {}  # row_id -> (r,c,val)

    row_id = 0
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                val_list = [board[r][c]]
            else:
                val_list = list(range(1,10))
            for val in val_list:
                nodes = []
                # Cellule
                nodes.append(dlx.addNode(row_id, r*9 + c))
                # Ligne
                nodes.append(dlx.addNode(row_id, 81 + r*9 + val - 1))
                # Colonne
                nodes.append(dlx.addNode(row_id, 162 + c*9 + val - 1))
                # Bloc
                blk = (r//3)*3 + (c//3)
                nodes.append(dlx.addNode(row_id, 243 + blk*9 + val - 1))
                # Lier horizontalement
                dlx.linkRowNodes(nodes)
                row_map[row_id] = (r,c,val)
                row_id += 1

    solution = []

    def search():
        if dlx.root.R == dlx.root:
            return True  # toutes les colonnes couvertes

        # choisir la colonne avec le moins de 1
        c = dlx.root.R
        min_size = c.size
        col = c
        while c != dlx.root:
            if c.size < min_size:
                min_size = c.size
                col = c
            c = c.R

        dlx.cover(col)
        r = col.D
        while r != col:
            solution.append(r.rid)
            j = r.R
            while j != r:
                dlx.cover(j.C)
                j = j.R
            if search():
                return True
            # backtrack
            solution.pop()
            j = r.L
            while j != r:
                dlx.uncover(j.C)
                j = j.L
            r = r.D
        dlx.uncover(col)
        return False

    search()

    # reconstruire la grille
    solved = [[0]*9 for _ in range(9)]
    for rid in solution:
        r,c,val = row_map[rid]
        solved[r][c] = val
    return solved



def sudokuDLX16(board):
    N_cols = 16*16*4  # 324 contraintes
    dlx = ManageLink(N_cols)
    row_map = {}  # row_id -> (r,c,val)

    row_id = 0
    for r in range(16):
        for c in range(16):
            if board[r][c] != 0:
                val_list = [board[r][c]]
            else:
                val_list = list(range(1,17))
            for val in val_list:
                nodes = []
                # Cellule
                nodes.append(dlx.addNode(row_id, r*16 + c))
                # Ligne
                nodes.append(dlx.addNode(row_id, 256 + r*16 + val - 1))
                # Colonne
                nodes.append(dlx.addNode(row_id, 512 + c*16 + val - 1))
                # Bloc
                blk = (r//4)*4 + (c//4)
                nodes.append(dlx.addNode(row_id, 768 + blk*16 + val - 1))
                # Lier horizontalement
                dlx.linkRowNodes(nodes)
                row_map[row_id] = (r,c,val)
                row_id += 1

    solution = []

    def search():
        if dlx.root.R == dlx.root:
            return True  # toutes les colonnes couvertes

        # choisir la colonne avec le moins de 1
        c = dlx.root.R
        min_size = c.size
        col = c
        while c != dlx.root:
            if c.size < min_size:
                min_size = c.size
                col = c
            c = c.R

        dlx.cover(col)
        r = col.D
        while r != col:
            solution.append(r.rid)
            j = r.R
            while j != r:
                dlx.cover(j.C)
                j = j.R
            if search():
                return True
            # backtrack
            solution.pop()
            j = r.L
            while j != r:
                dlx.uncover(j.C)
                j = j.L
            r = r.D
        dlx.uncover(col)
        return False

    search()

    symbols = "ABCDEFGHIJKLMNOP"

    # reconstruire la grille
    solved = [[0]*16 for _ in range(16)]
    for rid in solution:
        r,c,val = row_map[rid]
        solved[r][c] = symbols[val-1]
    return solved



board = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]



g = ['.LEK.G.....NO.C.',
        '..M.H.JOBDG.FENK',
        'J..C.BAN.EK....I',
        '.BG..K..C.J..DPM',
        '.HA.FL..K..M.P..',
        '...OA.....D.IK.G',
        '..KDJ.CBFAIG.MHL',
        '.M.....EPJNO.A..',
        'G...IA.DE.CJP...',
        'AK....GHNM..LIJ.',
        '..DJON..GL.BKH.F',
        '.N...J.K.F...GAB',
        'D..A..FJ..LIM.K.',
        'E.LFCDB.O.M.N.I.',
        '.JI....PD.....L.',
        '.....H.IJ....CBA']

symbols = "ABCDEFGHIJKLMNOP"
boardc = [[symbols.index(x)+1 if x != '.' else 0 for x in row] for row in g]

start = time.perf_counter()
sol = sudokuDLX16(boardc)
for row in sol:
    print(''.join(row))

end = time.perf_counter()
print("time:", end-start)



"""
    m = ManageLink(9)  # sudoku 9x9
    m.addNode(0, 0)
    m.addNode(0, 3)
    m.addNode(1, 3)
    m.addNode(2, 0)
    m.addNode(8, 8)

    m.visualizeColumns()

    col2 = m.colHeader[3]
    print(m.colHeader[3].C)
    print("\nCover column 3")
    m.cover(col2)
    m.visualizeColumns()

    print("\nUncover column 3")
    m.uncover(col2)
    m.visualizeColumns()
"""