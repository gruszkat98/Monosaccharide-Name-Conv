#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:10:15 2020

@author: tomekgruszka
"""


import sugars
import graphics as graph

def drawEnantiomer(sugarname=None, tradname = None, sugar = None):
    if not sugarname:
        sugarname = sugars.interpretSugar(sugar)

    if not sugar:
        sugar = sugars.interpretName(sugarname)

    sugar = sugar.enantiomer()

    drawSugar(sugar = sugar)

def drawSugar(sugarname=None, tradname = None, sugar = None):
    if not sugarname:
        sugarname = sugars.interpretSugar(sugar)

    if not sugar:
        sugar = sugars.interpretName(sugarname)

    mesh = sugar.makeMesh()

    if not mesh:
        print("The sugar is invalid!")
        return False

    if not tradname:
        title = sugars.prettifyName(sugarname)
    else:
        title = tradname


    h = 100 + (len(mesh) + 2) * 75

    win = graph.GraphWin(title, width = 500, height = h)

    text = graph.Text(graph.Point(250, 50), sugars.prettifyName(sugarname))
    text.setSize(30)
    text.draw(win)


    ## Actual drawing of the thing
    r = 20

    for i, c in enumerate(mesh):
        point = graph.Point(250, 100 + 75* (i + 1))
        carbon = graph.Text(point, c.atom )
        if (c != mesh[-1]):
            line = graph.Line(graph.Point(point.x, point.y + r), graph.Point(point.x, point.y + 75 - r))
            line.setWidth(2)
            line.draw(win)

        carbon.setSize(20)
        carbon.draw(win)

    length = len(mesh)
    for i in range(length):
        for direction in "udlr":
            if(mesh[i][direction] not in ([None] + mesh)):
                point = graph.Point(250, 100 + 75* (i + 1))

                if direction == "u":
                    point2 = graph.Point(point.x, point.y-75)
                    line = graph.Line(graph.Point(point.x, point.y-r), graph.Point(point.x, point.y-75+r))
                elif direction == "d":
                    point2 = graph.Point(point.x, point.y+75)
                    line = graph.Line(graph.Point(point.x, point.y+r), graph.Point(point.x, point.y+75-r))
                elif direction == "l":
                    point2 = graph.Point(point.x-75, point.y)
                    line = graph.Line(graph.Point(point.x-r, point.y), graph.Point(point.x-75+r, point.y))
                else:
                    point2 = graph.Point(point.x+75, point.y)
                    line = graph.Line(graph.Point(point.x+r, point.y), graph.Point(point.x+75-r, point.y))

                sub = graph.Text(point2, mesh[i][direction].atom)
                if direction == "l":
                    sub.setText(sub.getText()[::-1])

                sub.setSize(20)
                line.setWidth(2)

                sub.draw(win)

                if (mesh[i].p_bonds[direction] != None):
                    line2 = graph.Line(line.p1, line.p2)
                    line.setWidth(6)
                    line2.setWidth(2)
                    line2.setFill("white")
                    line.draw(win)
                    line2.draw(win)
                else:
                    line.draw(win)

    win.getMouse()
    win.close()
