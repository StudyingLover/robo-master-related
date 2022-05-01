# -*- coding: utf-8 -*-

"""
Created on Sat Apr 23 23:21:44 2-99922

@author: Ni Jingzhe
"""
data = []
index = [1, 2, 3, 4]
original_data = [0, 0, 0, 0]
OPT = ""
ans = [[-999, -999, -999], [-999, -999, -999],
       [-999, -999, -999], [-999, -999, -999]]


def bubble_sort(arr, index):
    '''


    Parameters
    ----------
    arr : list
        An list need to be sorted.
    index : list
        the index list will always follow the element in arr.

    Returns
    -------
    None.

    '''
    n = len(arr)

    # 遍历所有数组元素
    for i in range(n):

        # Last i elements are already in place
        for j in range(0, n-i-1):

            if arr[j] < arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                index[j], index[j+1] = index[j+1], index[j]


def check():
    '''


    Returns
    -------
    bool
        if there is a 24 in 'data' ,which represent we've got a solution, 
        the funcion will return True.

    '''
    for i in range(0, 4):
        if data[i] == 24:
            return True
    return False


def add_dfs(dep):
    '''


    Parameters
    ----------
    dep : int
        the depth of dfs,which should always 0 when you using this function.

    Returns
    -------
    None.

    '''
    if check() and dep >= 2:  # 递归的边界条件，有解且不是直接拼出24的情况（因为直接产生24的话，dep一定是1）
        return

    for i in range(0, 4):
        for j in range(0, 4):  # 枚举两个数
            if i != j and data[i] > 0 and data[j] > 0:  # 每次产生一个新数放回data中
                ans[dep][0] = index[i]  # 记录枚举的数字的索引
                ans[dep][1] = 0  # 格式为 【num1下标，0（代表运算符），num2下标】
                ans[dep][2] = index[j]
                x = data[i]
                y = data[j]
                data[i] = x+y  # 先是把枚举出的两个数相加，结果放回data，其中一个打成-1
                data[j] = -1
                add_dfs(dep+1)  # 进入下一层
                if check():  # 如果有解那么返回上一层
                    return
                data[i] = x  # 否则说明这一步的操作不可行，撤回这一步
                data[j] = y
                ans[dep][0] = -999
                ans[dep][1] = -999
                ans[dep][2] = -999

                # 第二种产生数的方式是拼接，必须保证是原数组中的数字拼接，而不是计算所得的结果参与拼接
                if data[i] in original_data and data[j] in original_data:
                    # 因为是24点，加法不可能出现三位加一位，所以只考虑两个数字拼接，且拼出来的数不可能大于等于24
                    data[i] = 10*y+x
                    if data[i] < 24:
                        ans[dep][1] = index[j]  # 记录下标，格式为【-999，num1下标，num2下标】
                        ans[dep][2] = index[i]
                        data[j] = -1
                        add_dfs(dep+1)
                        if check():
                            return
                        data[i] = x
                        data[j] = y
                        ans[dep][1] = -999
                        ans[dep][2] = -999
                    else:  # 拼接数大于24，撤回拼接操作
                        data[i] = x
                        data[j] = y

                    data[i] = 10*x+y  # 这里就是反过来拼接数字，同上
                    if data[i] < 24:
                        ans[dep][1] = index[i]
                        ans[dep][2] = index[j]
                        data[j] = -1
                        add_dfs(dep+1)
                        if check():
                            return
                        data[i] = x
                        data[j] = y
                        ans[dep][1] = -999
                        ans[dep][2] = -999
                    else:
                        data[i] = x
                        data[j] = y


def mult_dfs(dep):  # 乘法加法一样的，你们可以参考加法来理解乘法
    '''


    Parameters
    ----------
    dep : int
        the depth of dfs,which should always 0 when you using this function.

    Returns
    -------
    None.

    '''
    if check() and dep >= 2:
        return

    for i in range(0, 4):
        for j in range(0, 4):
            if i != j and data[i] > 0 and data[j] > 0:
                ans[dep][0] = index[i]
                ans[dep][1] = 0
                ans[dep][2] = index[j]
                x = data[i]
                y = data[j]
                data[i] = x*y
                data[j] = -1
                mult_dfs(dep+1)
                if check():
                    return
                data[i] = x
                data[j] = y
                ans[dep][0] = -999
                ans[dep][1] = -999
                ans[dep][2] = -999

                if data[i] in original_data and data[j] in original_data:
                    data[i] = 10*y+x
                    if data[i] <= 24 and dep == 0 or data[i] < 24 and dep >= 1:
                        ans[dep][1] = index[j]
                        ans[dep][2] = index[i]
                        data[j] = -1
                        mult_dfs(dep+1)
                        if check():
                            return
                        data[i] = x
                        data[j] = y
                        ans[dep][1] = -999
                        ans[dep][2] = -999
                    else:
                        data[i] = x
                        data[j] = y

                    data[i] = 10*x+y
                    if data[i] <= 24 and dep == 0 or data[i] < 24 and dep >= 1:
                        ans[dep][1] = index[i]
                        ans[dep][2] = index[j]
                        data[j] = -1
                        mult_dfs(dep+1)
                        if check():
                            return
                        data[i] = x
                        data[j] = y
                        ans[dep][1] = -999
                        ans[dep][2] = -999
                    else:
                        data[i] = x
                        data[j] = y


def solve(opt):
    '''
    Parameters
    ----------
    opt : String
        Tell the solve function which kind of operator is provided.

    Returns
    -------
    None.

    '''
    if opt == "*":
        mult_dfs(0)
    if opt == "+":
        add_dfs(0)


def generate_hit_order():
    '''


    Returns
    -------
    hit_order : list
        the order to hit the ATK.

    '''
    hit_order = []
    if ans[0][0] == -999:
        hit_order.append(ans[0][1])
        hit_order.append(ans[0][2])
    else:
        hit_order.append(ans[0][0])
        hit_order.append(ans[0][1])
        hit_order.append(ans[0][2])
    for i in range(1, 4):
        if ans[i][1] > -999 and ans[i][2] > -999:
            hit_order.append(ans[i][1])
            hit_order.append(ans[i][2])

    return hit_order


if __name__ == "__main__":
    OPT = input()
    original_data[0] = int(input())
    original_data[1] = int(input())
    original_data[2] = int(input())
    original_data[3] = int(input())

    for i in original_data:
        data.append(i)

    bubble_sort(data, index)  # 排序，带着索引一起排

    solve(OPT)

    if not check():
        print("no answer")
    else:
        print(generate_hit_order())
