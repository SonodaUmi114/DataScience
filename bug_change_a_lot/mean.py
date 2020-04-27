"""
    calculating mean differences
    2020/4/20
"""

import csv
import pandas as pd


def mean(file):
    jir = pd.read_csv(file, header=None, names=['added', 'removed', 'file modified'])
    add_remove = jir['added']+jir['removed']
    sum = add_remove.sum()
    average = sum/50
    return average


print('random change:', mean('random_commits.csv'))
print('bug change:', mean('bugs.csv'))
print('fix change:', mean('fixes.csv'))
