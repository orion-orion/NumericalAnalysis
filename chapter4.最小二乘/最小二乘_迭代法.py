'''
Descripttion: 
Version: 1.0
Author: ZhangHongYu
Date: 2022-02-12 18:34:54
LastEditors: ZhangHongYu
LastEditTime: 2022-02-12 18:36:15
'''
import numpy as np
import torch
 
def mse_loss(y_pred, y):
    m = y.shape[0]
    return 1/m*torch.square(y-y_pred).sum()

def linear_f(X, w):
    return torch.matmul(X, w)

# 之前实现的梯度下降法，做了一些小修改
def gradient_descent(X, w, y, n_iter, eta, loss_func, f):
    # 初始化计算图参数，注意：这里是创建新对象，非参数引用
    w = torch.tensor(w, requires_grad=True)
    X = torch.tensor(X)
    y = torch.tensor(y)
    for i in range(1, n_iter+1):
        y_pred = f(X, w)
        loss_v = loss_func(y_pred, y)
        loss_v.backward() 
        with torch.no_grad(): 
            w.sub_(eta*w.grad)
        w.grad.zero_()  
    w_star = w.detach().numpy()
    return w_star 

# 本模型按照多分类架构设计
def linear_model(
    X, y, n_iter=200, eta=0.001, loss_func=mse_loss, optimizer=gradient_descent):
    # 初始化模型参数
    # 我们使w和b融合，X后面添加一维
    X = np.concatenate([np.ones([X.shape[0], 1]), X], axis=1)
    w = np.zeros((X.shape[1],), dtype=np.float64)
    # 调用梯度下降法对函数进行优化
    # 这里采用单次迭代对所有样本进行估计，后面我们会介绍小批量法减少时间复杂度
    w_star = optimizer(X, w, y, n_iter, eta, mse_loss, linear_f)
    return w_star

if __name__ == '__main__':
    X = np.array(
        [
            [-1],
            [0],
            [1],
            [2]
        ], dtype=np.float32
    )
    y = np.array([1, 0, 0, -2], dtype=np.float32)
    n_iter, eta = 200, 0.1
    w_star = linear_model(X, y, n_iter, eta, mse_loss, gradient_descent)
    print("最小二乘估计得到的参数:", w_star)