#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 18:09:03 2020

@author: tomekgruszka
"""

import re


class FischerMesh:

    def __init__(self, atom, bond_max=4):
        self.atom = atom
        self.s_bonds = {
            "l": None,
            "r": None,
            "u": None,
            "d": None
        }
        self.p_bonds = {
            "l": None,
            "r": None,
            "u": None,
            "d": None
        }

        self.bond_max = bond_max
        self.bond_cur = 0

    def maxedOut(self):
        return self.bond_cur >= self.bond_max


    def hydrogenFill(self, visited = [None]):

        visited.append(self)

        if (not self.maxedOut()):
            for direction in ["u", "d", "r", "l"]:
                if (self.s_bonds[direction] == None):
                    self.sigmaBond(FischerMesh("H", 1), direction)

        for direction in ["u", "d", "r", "l"]:
            if (self.s_bonds[direction] not in visited):
                self.s_bonds[direction].hydrogenFill(visited)



    def sigmaBond(self, other, direction):
        op_dir = {
            "l": "r",
            "r": "l",
            "u": "d",
            "d": "u"
        }

        if (self.s_bonds[direction] != None):
            return False
        if (other.s_bonds[op_dir[direction]] != None):
            return False

        if (self.maxedOut()):
            return False
        if (other.maxedOut()):
            return False

        self.s_bonds[direction] = other
        other.s_bonds[op_dir[direction]] = self

        self.bond_cur +=1
        other.bond_cur +=1

        return self

    def piBond(self, direction):
        op_dir = {
            "l": "r",
            "r": "l",
            "u": "d",
            "d": "u"
        }
        if (self.s_bonds[direction] == None):
            return False

        other = self.s_bonds[direction]

        if (self.maxedOut()):
            return False
        if (other.maxedOut()):
            return False

        self.p_bonds[direction] = other
        other.p_bonds[op_dir[direction]] = self

        self.bond_cur +=1
        other.bond_cur +=1

        return self

    def copy(self):
        return FischerMesh(self.atom, self.bond_max)

    def __getitem__(self, key):
        return self.s_bonds[key]

    def __str__(self):
        return self.atom +": "+ self.s_bonds.__str__()

    def __repr__(self):
        return self.atom


class Sugar:

    def __init__(self, n, p, q):
        self.n = n
        self.p = p
        self.q = q
        return

    def getTuple(self):
        return (self.n, self.p, self.q)

    def copy(self):
        return Sugar(*self.getTuple())

    def enantiomer(self):
        n_ = self.n
        p_ = self.p
        if (p_ == 1):
            k = 2**(n_-2)-1
        else:
            k = 2**(n_-3)-1

        q_ = k - self.q

        return Sugar(n_, p_, q_)


    def makeMesh(self):
        if (not self.isValid()):
            return False

        # oh = FischerMesh("OH", 1)

        carbons = [FischerMesh("C") for i in range(self.n)]

        for i in range(self.n -1):
            carbons[i].sigmaBond(carbons[i+1], "d")

        ## make the carbonyl attachement

        carbons[self.p-1].sigmaBond(FischerMesh("O", 2), "r")
        carbons[self.p-1].piBond("r")

        ## decode the GBI
        if (self.p == 1):
            k = (self.n-2)
        else:
            k = (self.n-3)
        binary_str = bin(self.q).replace("0b", "").zfill(k)

        ## attach the alcohol groups to the non-maxed out carbons

        index = 0
        for i in range(self.n):
            if (not carbons[i].maxedOut()):
                if (i > 0 and i < self.n-1):
                    if(binary_str[index] == '1'):
                        carbons[i].sigmaBond(FischerMesh("OH", 1), "r")
                    else:
                        carbons[i].sigmaBond(FischerMesh("OH", 1), "l")
                    index += 1
                else:
                    carbons[i].sigmaBond(FischerMesh("OH", 1), "r")

        ## hydrogen fill

        carbons[0].hydrogenFill()

        return carbons


    def isValid(self):
        b1 = (self.n >= 3) and (self.p >0) and (self.p <0.5*self.n + 1) and (self.q>=0)
        if (self.p == 1):
            k = 2**(self.n-2)
        else:
            k = 2**(self.n-3)

        return b1 and self.q<k

    def __str__(self):
        return "%i, %i, %i" %(self.n, self.p, self.q)

    def __repr__(self):
        return self.getTuple().__str__()




def prettifyName(sugarname):
    sugar = interpretName(sugarname)

    name = interpretSugar(sugar)

    if not name:
        return False
    return name



def interpretSugar(sugar):
        n_reader ={
            3: "triose",
            4: "tetrose",
            5: "pentose",
            6: "hexose",
            7: "heptose",
            8: "octose"
        }


        try:
            name = n_reader[sugar.n]
            (p, q) = (sugar.p, sugar.q)

            rez = (p, q).__str__() + "-" + name

            if (sugar.isValid()):
                return rez.replace(" ","")
            print ("Invalid Sugar!")
            return False
        except:
            print ("Unknown sugar name!")
            return False

def interpretName(sugarname):
    n_generator ={
        "triose": 3,
        "tetrose": 4,
        "pentose":5,
        "hexose":6,
        "heptose":7,
        "octose":8,
    }
    sn = sugarname.replace(" ","")

    sn = sn.lower()

    (p, q) = (re.findall(r'\d+', sn))
    p = int(p)
    q = int(q)

    word = re.search(r'[a-z]+', sn).group(0).lower()

    n = n_generator[word]


    return Sugar(n, p, q)
