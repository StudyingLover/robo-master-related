# -*- coding: utf-8 -*-
"""
Created on Sun May  1 11:25:42 2022

@author: Ni Jingzhe
"""


class ATK_solver:

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

        self.data = []
        self.index = [1, 2, 3, 4]
        self.original_data = original_data_
        self.opt = OPT_
        self.ans = [[-999, -999, -999], [-999, -999, -999],
                    [-999, -999, -999], [-999, -999, -999]]

        for i in self.original_data:
            self.data.append(i)

        self.bubble_sort()  # 排序，带着索引一起排

    def bubble_sort(self):
        '''


        Returns
        -------
        None.

        '''
        n = len(self.data)

        # 遍历所有数组元素
        for i in range(n):

            # Last i elements are already in place
            for j in range(0, n-i-1):

                if self.data[j] < self.data[j+1]:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]
                    self.index[j], self.index[j +
                                              1] = self.index[j+1], self.index[j]

    def check(self):
        '''


        Returns
        -------
        bool
            if there is a 24 in 'data' ,which represent we've got a solution,
            the funcion will return True.

        '''
        for i in range(0, 4):
            if self.data[i] == 24:
                return True
        return False

    def add_dfs(self, dep):
        '''


        Parameters
        ----------
        dep : int
            the depth of dfs,which should always 0 when you using this function.

        Returns
        -------
        None.

        '''
        if self.check() and dep >= 2:  # 递归的边界条件，有解且不是直接拼出24的情况（因为直接产生24的话，dep一定是1）
            return

        for i in range(0, 4):
            for j in range(0, 4):  # 枚举两个数
                if i != j and self.data[i] >= 0 and self.data[j] >= 0:  # 每次产生一个新数放回data中
                    self.ans[dep][0] = self.index[i]  # 记录枚举的数字的索引
                    self.ans[dep][1] = 0  # 格式为 【num1下标，0（代表运算符），num2下标】
                    self.ans[dep][2] = self.index[j]
                    x = self.data[i]
                    y = self.data[j]
                    self.data[i] = x+y  # 先是把枚举出的两个数相加，结果放回data，其中一个打成-1
                    self.data[j] = -1
                    self.add_dfs(dep+1)  # 进入下一层
                    if self.check():  # 如果有解那么返回上一层
                        return
                    self.data[i] = x  # 否则说明这一步的操作不可行，撤回这一步
                    self.data[j] = y
                    self.ans[dep][0] = -999
                    self.ans[dep][1] = -999
                    self.ans[dep][2] = -999

                    # 第二种产生数的方式是拼接，必须保证是原数组中的数字拼接，而不是计算所得的结果参与拼接
                    if self.data[i] in self.original_data and self.data[j] in self.original_data:
                        # 因为是24点，加法不可能出现三位加一位，所以只考虑两个数字拼接，且拼出来的数不可能大于等于24
                        self.data[i] = 10*y+x
                        if self.data[i] < 24:
                            # 记录下标，格式为【-999，num1下标，num2下标】
                            self.ans[dep][1] = self.index[j]
                            self.ans[dep][2] = self.index[i]
                            self.data[j] = -1
                            self.add_dfs(dep+1)
                            if self.check():
                                return
                            self.data[i] = x
                            self.data[j] = y
                            self.ans[dep][1] = -999
                            self.ans[dep][2] = -999
                        else:  # 拼接数大于24，撤回拼接操作
                            self.data[i] = x
                            self.data[j] = y

                        self.data[i] = 10*x+y  # 这里就是反过来拼接数字，同上
                        if self.data[i] < 24:
                            self.ans[dep][1] = self.index[i]
                            self.ans[dep][2] = self.index[j]
                            self.data[j] = -1
                            self.add_dfs(dep+1)
                            if self.check():
                                return
                            self.data[i] = x
                            self.data[j] = y
                            self.ans[dep][1] = -999
                            self.ans[dep][2] = -999
                        else:
                            self.data[i] = x
                            self.data[j] = y

    def mult_dfs(self, dep):  # 乘法加法一样的，你们可以参考加法来理解乘法
        '''


        Parameters
        ----------
        dep : int
            the depth of dfs,which should always 0 when you using this function.

        Returns
        -------
        None.

        '''
        if self.check() and dep >= 2:
            return

        for i in range(0, 4):
            for j in range(0, 4):
                if i != j and self.data[i] >= 0 and self.data[j] >= 0:
                    self.ans[dep][0] = self.index[i]
                    self.ans[dep][1] = 0
                    self.ans[dep][2] = self.index[j]
                    x = self.data[i]
                    y = self.data[j]
                    self.data[i] = x*y
                    self.data[j] = -1
                    self.mult_dfs(dep+1)
                    if self.check():
                        return
                    self.data[i] = x
                    self.data[j] = y
                    self.ans[dep][0] = -999
                    self.ans[dep][1] = -999
                    self.ans[dep][2] = -999

                    if self.data[i] in self.original_data and self.data[j] in self.original_data:
                        self.data[i] = 10*y+x
                        if self.data[i] <= 24 and dep == 0 or self.data[i] < 24 and dep >= 1:
                            self.ans[dep][1] = self.index[j]
                            self.ans[dep][2] = self.index[i]
                            self.data[j] = -1
                            self.mult_dfs(dep+1)
                            if self.check():
                                return
                            self.data[i] = x
                            self.data[j] = y
                            self.ans[dep][1] = -999
                            self.ans[dep][2] = -999
                        else:
                            self.data[i] = x
                            self.data[j] = y

                        self.data[i] = 10*x+y
                        if self.data[i] <= 24 and dep == 0 or self.data[i] < 24 and dep >= 1:
                            self.ans[dep][1] = self.index[i]
                            self.ans[dep][2] = self.index[j]
                            self.data[j] = -1
                            self.mult_dfs(dep+1)
                            if self.check():
                                return
                            self.data[i] = x
                            self.data[j] = y
                            self.ans[dep][1] = -999
                            self.ans[dep][2] = -999
                        else:
                            self.data[i] = x
                            self.data[j] = y

    def sub_dfs(self, dep):
        '''
        Parameters
        ----------
        dep : int
            the depth of dfs,which should always 0 when you using this function.

        Returns
        -------
        None.

        '''
        if self.check() and dep >= 2:
            return

        for i in range(0, 4):
            for j in range(0, 4):
                if i != j and self.data[i] > 0 and self.data[j] > 0:

                    x = self.data[i]
                    y = self.data[j]

                    if x in self.original_data and y in self.original_data:

                        self.data[j] = 10*y+x
                        if self.data[j] > 24 and dep == 0 or dep >= 1 and (self.data[j] == 24 and 48 in self.data or self.data[j] != 24):
                            self.ans[dep][1] = self.index[j]
                            self.ans[dep][2] = self.index[i]
                            self.data[i] = -1
                            self.sub_dfs(dep+1)
                            if self.check():
                                return
                            self.data[i] = x
                            self.data[j] = y
                            self.ans[dep][1] = -999
                            self.ans[dep][2] = -999
                        else:
                            self.data[i] = x
                            self.data[j] = y

                        self.data[i] = 10*x+y
                        if self.data[i] > 24 and dep == 0 or dep >= 1 and (self.data[i] == 24 and 48 in self.data or self.data[i] != 24):
                            self.ans[dep][1] = self.index[i]
                            self.ans[dep][2] = self.index[j]
                            self.data[j] = -1
                            self.sub_dfs(dep+1)
                            if self.check():
                                return
                            self.data[i] = x
                            self.data[j] = y
                            self.ans[dep][1] = -999
                            self.ans[dep][2] = -999
                        else:
                            self.data[i] = x
                            self.data[j] = y

                    if x > 24 or y > 24:
                        self.data[i] = abs(x - y)
                        self.data[j] = -1
                        if x - y < 0:
                            self.ans[dep][0] = self.index[j]
                            self.ans[dep][1] = 0
                            self.ans[dep][2] = self.index[i]
                        else:
                            self.ans[dep][0] = self.index[i]
                            self.ans[dep][1] = 0
                            self.ans[dep][2] = self.index[j]
                        self.sub_dfs(dep+1)
                        if self.check():
                            return
                        self.data[i] = x
                        self.data[j] = y
                        self.ans[dep][0] = -999
                        self.ans[dep][1] = -999
                        self.ans[dep][2] = -999

    def solve(self):
        '''
        Parameters
        ----------
        opt : String
            Tell the solve function which kind of operator is provided.

        Returns
        -------
        None.

        '''
        if self.opt == "*":
            self.mult_dfs(0)
        if self.opt == "+":
            self.add_dfs(0)
        if self.opt == "-":
            self.sub_dfs(0)

    def generate_hit_order(self):
        '''


        Returns
        -------
        hit_order : list
            the order to hit the ATK.
            It should be empty if no solution was found
        '''
        self.solve()

        if not self.check():
            return []

        hit_order = []
        if self.ans[0][0] == -999 and self.ans[1][0] == -999:
            if self.original_data[self.ans[0][1]-1]*10+self.original_data[self.ans[0][2]-1] > self.original_data[self.ans[1][1]-1]*10+self.original_data[self.ans[1][2]-1]:
                hit_order = [self.ans[0][1], self.ans[0][2],
                             0,
                             self.ans[1][1], self.ans[1][2]]
            else:
                hit_order = [self.ans[1][1], self.ans[1][2],
                             0,
                             self.ans[0][1], self.ans[0][2]]
        else:
            if self.ans[0][0] == -999:
                hit_order.append(self.ans[0][1])
                hit_order.append(self.ans[0][2])
            else:
                hit_order.append(self.ans[0][0])
                hit_order.append(self.ans[0][1])
                hit_order.append(self.ans[0][2])
            for i in range(1, 4):
                if self.ans[i][1] > -999 and self.ans[i][2] > -999:
                    hit_order.append(self.ans[i][1])
                    hit_order.append(self.ans[i][2])

        return hit_order
