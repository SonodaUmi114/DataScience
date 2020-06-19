# -*- coding: utf-8 -*-
"""
Created on 2020/6/11 16:26
@author: 12198
"""
import re
import csv
from subprocess import Popen, PIPE

author = re.compile('^Author: [A-Za-z]{1,} [A-Za-z]{1,} <.+>$')


def author(repo):
    developer = []
    cmd = ["git", "log", "-P"]
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()
    a = str(data).split("\\n")
    for line in a:
        if author.match(line):
            line = line.replace('<', ':').replace('>', '').split(':')[1].strip()
            if line not in developer and line is not None:
                developer.append(line)
                with open('author.csv', 'w+', encoding='utf-8', newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow([line])


author(repo='D:\git_warehouse\linux-stable')
