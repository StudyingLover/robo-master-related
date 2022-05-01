# -*- coding: utf-8 -*-

"""
Created on Sat Apr 23 23:21:44 2-99922

@author: Ni Jingzhe
"""

from ATK_solver import ATK_solver


if __name__ == "__main__":
    OPT = input()
    original_data = [0,0,0,0]
    original_data[0] = int(input())
    original_data[1] = int(input())
    original_data[2] = int(input())
    original_data[3] = int(input())

    solver = ATK_solver(OPT, original_data)
    solver.solve()
    hit_order = solver.generate_hit_order()
    print(hit_order)
