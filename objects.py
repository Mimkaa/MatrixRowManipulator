import pygame as pg
import sys
from settings import *
from os import path
import re
import copy

vec = pg.Vector2
class Cell:
    def __init__(self, num, pos, size, game):
        self.num = num
        self.pos = vec(pos.x,pos.y)
        self.size = size
        self.game = game
    def draw(self, surface):
        pg.draw.rect(surface, WHITE, (self.pos.x,self.pos.y, self.size, self.size))
        self.game.draw_text("{:.{}f}".format(self.num, 1) ,self.game.font,self.size//3, BLACK, self.pos.x+self.size/2, self.pos.y+self.size/2, "center")
        pg.draw.rect(surface, BLACK, (self.pos.x,self.pos.y, self.size, self.size),1)

class Matrix:
    def __init__(self, mat, size, x, y, game):
        self.mat = copy.deepcopy(mat)
        self.cells = []
        self.cellSize = size
        self.pos = vec(x,y)
        self.game = game
        self.operations = []
        self.matOr = mat
        self.backUps = []
        self.backUps.append(copy.deepcopy(mat))
        self.backupIndex = 0
        self.currentMat = [[0 for _ in range(len(self.mat[0]))] for _ in range(len(self.mat[0]))]
        self.fininshed = True
        self.fillCells()

    def fillCells(self):
        for p,r in enumerate(self.mat):
            for k,n in enumerate(r):

                posVec = self.pos + vec(self.cellSize* k, self.cellSize*p)
                self.cells.append(Cell(n, posVec, self.cellSize, self.game))


    def saveMat(self):
        cc = [[0 for i in range(len(self.mat))]for j in range(len(self.mat))]
        for i in range(len(self.mat)):
            for j in range(len(self.mat[0])):
                cc[i][j] = self.mat[i][j]
        self.backUps+=[copy.deepcopy(cc)]


    def updateCells(self):

        for p,r in enumerate(self.mat[0]):
            for k,n in enumerate(self.mat[0]):
                self.cells[p * len(self.mat[0]) + k].num = self.mat[p][k]


    def execute(self, string):

        self.operations.append(string)
        pattern = r'(\+|\-|\*|\/)'

        # Use re.split to split the line based on the pattern
        parts = re.split(pattern, string)


        # solve negative multiplication
        for n,e in enumerate(parts):
            if(e=="-" and parts[n+1].isnumeric()):
                parts[n+1] = e+ parts[n+1]
                parts.pop(n)
        parts = [i for i in parts if  i!='']


        keys = []


        for n,p in enumerate(parts):
            if 'r' in p :
                keys.append(p)

        dic = {value: {"mul":[], "div":[], "operation":"", "mem":"", "save":[]} for value in keys}

        # multiplication and division
        for n,p in enumerate(parts):
            if p == "*":

                if 'r' in parts[n-1]:
                    dic[parts[n-1]]["mul"].append(parts[n+1])
                    parts.pop(n+1)
                    parts.pop(n)

            if p == "/":
                if 'r' in parts[n-1]:
                    dic[parts[n-1]]["div"].append( parts[n+1])
                    parts.pop(n+1)
                    parts.pop(n)

        # row subtraction addition
        for n,p in enumerate(parts):
            if p =="+" or p == "-":
                dic[parts[n-1]]["operation"] = p
                dic[parts[n-1]]["mem"] = parts[n+1]

        # perform the mult div
        if len(dic) == 1:
            for key in dic:
                row_num = int(key[1:])
                if dic[key]["mul"]:
                    for i in range(len(self.mat[row_num])):
                        self.mat[row_num][i]*=float(dic[key]["mul"][0])
                if dic[key]["div"]:
                    for i in range(len(self.mat[row_num])):
                        self.mat[row_num][i]/=float(dic[key]["div"][0])

        else:
            #create saves
            for key in dic:

                row_num = int(key[1:])

                save = [i for i in self.mat[row_num]]
                if dic[key]["mul"]:
                    for i in range(len(self.mat[row_num])):
                        save[i]*=float(dic[key]["mul"][0])
                        dic[key]["save"] = copy.deepcopy(save)
                if dic[key]["div"]:
                    for i in range(len(self.mat[row_num])):
                        save[i]/=float(dic[key]["div"][0])
                        dic[key]["save"] = copy.deepcopy(save)

            for key in dic:
                row_num = int(key[1:])

                if dic[key]["operation"]!="":
                    nextt = int(dic[key]["mem"][1:])
                    nextKey = dic[key]["mem"]

                    if(dic[nextKey]["save"]):
                        for n,i in enumerate(self.mat[nextt]):
                            if (dic[key]["operation"]=="+"):
                                self.mat[row_num][n]+=dic[nextKey]["save"][n]
                            if (dic[key]["operation"]=="-"):
                                self.mat[row_num][n]-=dic[nextKey]["save"][n]

                    else:
                        for n,i in enumerate(self.mat[nextt]):
                            if (dic[key]["operation"]=="+"):
                                self.mat[row_num][n]+=copy.deepcopy(self.mat[nextt][n])
                            if (dic[key]["operation"]=="-"):
                                self.mat[row_num][n]-=copy.deepcopy(self.mat[nextt][n])





        print(self.backUps)
        print(self.operations)


    def draw(self,surface):
        for c in self.cells:
            c.draw(surface)

class Input:
    def __init__(self, pos, width, height, game):
        self.pos = pos
        self.width = width
        self.height = height
        self.game = game
        self.text = ""



    def getString(self):
        return self.text

    def draw(self, surf):
        pg.draw.rect(surf,WHITE,(self.pos.x,self.pos.y,self.width,self.height))
        self.game.draw_text(self.text,self.game.font,self.height, BLACK, self.pos.x+self.width/2, self.pos.y+self.height/2, "center")
        pg.draw.rect(surf,BLACK,(self.pos.x,self.pos.y,self.width,self.height),1)
