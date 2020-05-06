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
Get 50 randomly selected bugs, 50 fixes, and 50 random commits from Linux kernel. And save in csv file
"""

__copyright__ = 'T1,Lanzhou University,2020'
__license__ = 'GPLV2 or later'
__version__ = 0.2
__author__ = ['Hanqiang Qiu','Yanfei Cao','Zheng Liu','Xiujie Song','Yuxuan Cao','Shan Gao','Zexin Zhang','Junwei Ding']
__email__ = ['479845114@qq.com','caoyf18@lzu.edu.cn','liuzheng2018@lzu.edu.cn','songxj@lzu.edu.cn','caoyx2018@lzu.edu.cn','shgao18@lzu.edu.cn','zhangzexin18@lzu.edu.cn','dingjw18@lzu.edu.cn']
__status__ = 'done'

import re
import csv
import random
import numpy as np
import pandas as pd
from subprocess import Popen, PIPE, check_output


class Test():
    def __init__(self):
        self.repo = "D:\git_warehouse\linux-stable"
        self.random_list1 = random.sample(range(1, 37140), 50)
        self.random_list2 = random.sample(range(0, 548292), 50)

        for i in self.random_list1:
            self.read_csv1('fix_bug.csv', i)

        for j in self.random_list2:
            self.read_csv2('commit.csv', j)

    def read_csv1(self, path, index):
        reader = pd.read_csv(path, header=None, )
        row = np.array(reader.iloc[index])

        fix_id = row[0]
        self.get_data(fix_id, self.repo, 'fix.csv', 1)
        bug_id = row[1]
        self.get_data(bug_id, self.repo, 'bug.csv', 1)

    def read_csv2(self, path, index):
        reader = pd.read_csv(path, header=None, )
        row = np.array(reader.iloc[index])

        commit_id = row[1]
        self.get_data(commit_id, self.repo, 'random_commit.csv', 2)

    def get_data(self, x_id, repo, save_name, mode):
        try:
            cmd = ["git", "diff", "--numstat", "{}~..{}".format(x_id, x_id)]
            p = Popen(cmd, cwd=repo, stdout=PIPE)
            data = p.communicate()[0]
            result = data.decode('utf-8').split()
            result_list = np.array(result).reshape(int(len(result) / 3), 3)
        except:
            if mode == 1:
                instead = random.sample(range(1, 37140), 1)
                while instead in self.random_list1:
                    instead = random.sample(range(1, 37140), 1)
                self.read_csv1('fix_bug.csv', instead)
            elif mode == 2:
                instead = random.sample(range(1, 548292), 1)
                while instead in self.random_list2:
                    instead = random.sample(range(1, 548292), 1)
                self.read_csv2('commit.csv', instead)

        else:
            lines_added = 0
            lines_removed = 0
            files_modified = len(result_list)
            for i in range(files_modified):
                lines_added += int(result_list[i][0])
                lines_removed += int(result_list[i][1])
            with open(save_name, 'a', encoding='utf-8', newline='') as f:
                csv_writer = csv.writer(f, delimiter=',')
                csv_writer.writerow([lines_added, lines_removed, files_modified])


if __name__ == '__main__':
    a = Test()
