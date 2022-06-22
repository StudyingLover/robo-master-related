# -*- coding: utf-8 -*-
"""
Created on Sun May  1 11:25:42 2022

@author: Ni Jingzhe
"""


class ATK_solver:
    '''
    把和解24点的相关函数封装了一下。
    使用的话，实例化一个ATK_solver之后，直接调用generate_hit_order获取打击序列。
    打击序列中，0代表运算符，其他数字代表打击的数字在original_data中的下标。
    至于怎么处理成符合机器人视觉数据的格式，就交给你们使用者了。
    '''

    def __init__(self, OPT_, original_data_):
        '''


        Parameters
        ----------
        OPT_ : string
            the operator.            
        original_data_ : list
            4 number displayed on ATK.

        Returns
        -------
        None.

        '''

        self.original_data = original_data_
        self.opt = OPT_

    def add_solve(self):
        '''        
        Returns
        -------
        list
            directly return the hit order

        '''
        original_data = self.original_data
        arrange = []
        index = []
        for i in range(4):
            for j in range(4):
                for m in range(4):
                    for n in range(4):
                        # 通过索引位置不同，确定是不同的数字
                        if i != j and i != m and i != n and j != m and j != n and m != n:

                            arrange.append([original_data[i], original_data[j],
                                           original_data[m], original_data[n]])
                            index.append([i+1, j+1, m+1, n+1])

        # try
        for l in arrange:
            i = arrange.index(l)
            # first case: ab+c
            if l[0] * 10 + l[1] + l[2] == 24:
                hit_order = [index[i][0], index[i][1], 0, index[i][2]]
                return hit_order

            # second case: ab + cd:
            if l[0]*10+l[1] + (l[2]*10+l[3]) == 24:
                hit_order = [index[i][0], index[i]
                             [1], 0, index[i][2], index[i][3]]
                return hit_order

            # third case: ab + c + d
            if l[0]*10+l[1] + l[2] + l[3] == 24:
                hit_order = [index[i][0], index[i][1],
                             0, index[i][2], 0, index[i][3]]
                return hit_order

            #fourth case: a + b + c + d
            if l[0] + l[1] + l[2] + l[3] == 24:
                hit_order = [index[1][0], 0, index[i]
                             [1], 0, index[i][2], 0, index[i][3]]
                return hit_order

        return "No answer!"


    def mult_solve(self):
        '''        
        Returns
        -------
        list
            directly return the hit order

        '''
        original_data = self.original_data
        arrange = []
        index = []
        for i in range(4):
            for j in range(4):
                for m in range(4):
                    for n in range(4):
                        # 通过索引位置不同，确定是不同的数字
                        if i != j and i != m and i != n and j != m and j != n and m != n:

                            arrange.append([original_data[i], original_data[j],
                                           original_data[m], original_data[n]])
                            index.append([i+1, j+1, m+1, n+1])

        # try
        for l in arrange:
            i = arrange.index(l)
            # first case: ab * c
            if (l[0] * 10 + l[1]) * l[2] == 24:
                hit_order = [index[i][0], index[i][1], 0, index[i][2]]
                return hit_order

            # second case: a * b:
            if l[0]*l[1] == 24:
                hit_order = [index[i][0], 0, index[i][1]]
                return hit_order

            # third case: a * b * c * d
            if l[0] * l[1] * l[2] * l[3] == 24:
                hit_order = [index[i][0], 0, index[i][1],
                             0, index[i][2], 0, index[i][3]]
                return hit_order

            #fourth case: a * b * c
            if l[0] * l[1] * l[2] == 24:
                hit_order = [index[1][0], 0, index[i]
                             [1], 0, index[i][2]]
                return hit_order

        return "No answer!"
    

    def sub_solve(self):
        '''        
        Returns
        -------
        list
            directly return the hit order

        '''
        original_data = self.original_data
        arrange = []
        index = []
        for i in range(4):
            for j in range(4):
                for m in range(4):
                    for n in range(4):
                        # 通过索引位置不同，确定是不同的数字
                        if i != j and i != m and i != n and j != m and j != n and m != n:

                            arrange.append([original_data[i], original_data[j],
                                           original_data[m], original_data[n]])
                            index.append([i+1, j+1, m+1, n+1])

        # try
        for l in arrange:
            i = arrange.index(l)
            # first case: ab-c
            if l[0] * 10 + l[1] - l[2] == 24:
                hit_order = [index[i][0], index[i][1], 0, index[i][2]]
                return hit_order

            # second case: ab - cd:
            if l[0]*10+l[1] - (l[2]*10+l[3]) == 24:
                hit_order = [index[i][0], index[i]
                             [1], 0, index[i][2], index[i][3]]
                return hit_order

            # third case: ab - c - d
            if l[0]*10+l[1] - l[2] - l[3] == 24:
                hit_order = [index[i][0], index[i][1],
                             0, index[i][2], 0, index[i][3]]
                return hit_order

        return "No answer!"

    def get_index(self, arr, item, n_st):
        '''
        

        Parameters
        ----------
        arr : list
            an list
        item : list
            an item in the list
        n_st : TYPE
            the n_st times the item appeared

        Returns
        -------
        int
            the position of the n_st item in the list arr

        '''
        if n_st <= arr.count(item):
            all_index = [key for key, value in enumerate(arr) if value == item]
            return all_index[n_st-1]
        else:
            return None

    def div_solve(self):
        '''
        process div by enumerate.
        only the condition below are possible to be solved by div.
         2 4 1
         4 8 2
         7 2 3
         9 6 4、9 6 2 2
         1 2 0 5
         1 4 4 6
         1 6 8 7
         1 9 2 8
         2 1 6 9

        Returns
        -------
        Directly return the hit_order

        '''
        d = self.original_data

        if 2 in d and 4 in d and 1 in d:
            return [d.index(2)+1, d.index(4)+1, 0, d.index(1)+1]
        if 4 in d and 8 in d and 2 in d:
            return [d.index(4)+1, d.index(8)+1, 0, d.index(2)+1]
        if 7 in d and 2 in d and 3 in d:
            return [d.index(7)+1, d.index(2)+1, 0, d.index(3)+1]
        if 9 in d and 6 in d and 4 in d:
            return [d.index(9)+1, d.index(6)+1, 0, d.index(4)+1]
        if 1 in d and 2 in d and 0 in d and 5 in d:
            return [d.index(1)+1, d.index(2)+1, d.index(0)+1, 0, d.index(5)+1]
        if 1 in d and 6 in d and 8 in d and 7 in d:
            return [d.index(1)+1, d.index(6)+1, d.index(8)+1, 0, d.index(7)+1]
        if 1 in d and 9 in d and 2 in d and 8 in d:
            return [d.index(1)+1, d.index(9)+1, d.index(2)+1, 0, d.index(8)+1]
        if 2 in d and 1 in d and 6 in d and 9 in d:
            return [d.index(2)+1, d.index(1)+1, d.index(6)+1, 0, d.index(9)+1]
        if 9 in d and 6 in d and 2 in d and d.count(2) == 2:
            return [d.index(9)+1, d.index(6)+1, 0, self.get_index(d, 2, 1)+1, 0, self.get_index(d, 2, 2)+1]
        if 1 in d and 4 in d and 6 in d and d.count(4) == 2:
            return [d.index(1)+1, self.get_index(d, 4, 1)+1, self.get_index(d, 4, 2)+1, 0, d.index(6)+1]


    def generate_hit_order(self):
        '''


        Returns
        -------
        hit_order : list
            the order to hit the ATK.
            It should be empty if no solution was found
        '''
        if self.opt == "-":
            return self.sub_solve()
        elif self.opt == "+":
            return self.add_solve()
        elif self.opt == "/":
            return self.div_solve()
        elif self.opt == "*":
            return self.mult_solve()
