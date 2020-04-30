# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Group1 members information:
Name, ID, E-mail
Cao Yanfei    320180939561  caoyf18@lzu.edu.cn
Cao Yuxuan    320180939571  caoyx2018@lzu.edu.cn
Ding Junwei   320180939671  dingjw18@lzu.edu.cn
Gao Shan      320180939740  shgao18@lzu.edu.cn
Liu Zheng     320180940101  liuzheng2018@lzu.edu.cn
Qiu Hanqiang  320180940181  479845114@qq.com
Song Xiujie   320180940211  songxj2018@lzu.edu.cn
Zhang Zexin   320180940590  zhangzexin18@lzu.edu.cn
"""

"""

"""

__copyright__ = 'T1,Lanzhou University,2020'
__license__ = 'GPLV2 or later'
__version__ = 0.2
__author__ = ['Hanqiang Qiu','Yanfei Cao','Zheng Liu','Xiujie Song','Yuxuan Cao','Shan Gao','Zexin Zhang','Junwei Ding']
__email__ = ['479845114@qq.com','caoyf18@lzu.edu.cn','liuzheng2018@lzu.edu.cn','songxj@lzu.edu.cn','caoyx2018@lzu.edu.cn','shgao18@lzu.edu.cn','zhangzexin18@lzu.edu.cn','dingjw18@lzu.edu.cn']
__status__ = 'done'

from sklearn.linear_model import LinearRegression
import pandas as pd


def mul_regression():
    # 1. obtain the data
    fix = pd.read_csv('fixes.csv',
                      header=None, names=['added', 'removed', 'file modified'])

    fix.insert(3, 'bug_commit', 0)

    bug = pd.read_csv('bugs.csv',
                      header=None, names=['added', 'removed', 'file modified'])
    bug.insert(3, 'bug_commit', 1)
    fix_bug = pd.concat([bug, fix], ignore_index=True)

    factors = ['added', 'removed', 'file modified']
    x = fix_bug[factors]
    y = fix_bug['bug_commit']

    # 2. model training
    estimator = LinearRegression()
    model = estimator.fit(x, y)

    # 3. test
    rd_sample = pd.read_csv('random_commits.csv')
    rd_sample.columns = ['added', 'removed', 'file modified']
    pre_bug = estimator.predict(x)
    all_data = pd.concat([fix_bug, rd_sample],sort=False)
    mul_r2 = estimator.score(x, y)
    print('r^2 of multiple linear regression is:\n {}'.format(mul_r2))


def sin_regression():
    # 1. obtain the data
    fix = pd.read_csv('fixes.csv',
                      header=None, names=['added', 'removed', 'file modified'])
    # fix = fix[['added','removed']]
    fix.insert(3, 'bug_commit', 0)

    bug = pd.read_csv('bugs.csv',
                      header=None, names=['added', 'removed', 'file modified'])
    bug.insert(3, 'bug_commit', 1)
    fix_bug = pd.concat([bug, fix], ignore_index=True)
    fix_bug.insert(4, 'sum',
                   [fix_bug['added'].values[i]+fix_bug['removed'].values[i] for i in range(len(fix_bug))])

    x = fix_bug[['sum']]
    y = fix_bug['bug_commit']

    # 2. model training
    estimator = LinearRegression()
    model = estimator.fit(x, y)

    # 3. test
    sin_r2 = estimator.score(x, y)
    print('r^2 of single linear regression is:\n {}'.format(sin_r2))


mul_regression()
sin_regression()
