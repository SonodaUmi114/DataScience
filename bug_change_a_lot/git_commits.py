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

import re
import csv
from subprocess import Popen, PIPE

commit = re.compile('^commit [0-9a-z]{40}$', re.IGNORECASE)
fixes = re.compile('^\W+Fixes: [a-f0-9]{8,40} \(.*\)$', re.IGNORECASE)


def git_fix_commits(range, repo):
    cmd = ["git", "log", "-P", range]
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()

    for line in data.decode("utf-8").split("\n"):
        if commit.match(line):
            cur_commit = line
        if fixes.match(line):
            a = line.strip().split(" ")
            b = [cur_commit.replace('commit', ' ').lstrip(), a[1], ' '.join(a[2:])]
            # fix_commit,bug_commit,explanation
            with open('fix_bug.csv', 'a', encoding='utf-8', newline='') as f:
                csv_writer = csv.writer(f, delimiter=',')
                csv_writer.writerow(b)

            # print(b)
    print('success git_fix_commits')


def git_commits(range, repo):
    cmd = ["git", "log", "-P", range]
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()

    a = str(data).split("\\n")
    for line in a:
        if commit.match(line):
            cur_commit = line
            b = cur_commit.strip().split()
            with open('commit.csv', 'a', encoding='utf-8', newline='') as f:
                csv_writer = csv.writer(f, delimiter=',')
                csv_writer.writerow(b)
    print('success git_commits')


git_fix_commits("v4.3..HEAD", "D:\git_warehouse\linux-stable")
git_commits("v4.3", "D:\git_warehouse\linux-stable")
