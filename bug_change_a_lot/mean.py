"""
    calculating mean differences
    2020/4/20
"""

import csv
import pandas as pd


def mean(file):
    jir = pd.read_csv(file)
    add_remove = jir['lines_added']+jir['lines_removed']
    sum = add_remove.sum()
    average = sum/50
    return average


print('random change:', mean('random_commits.csv'))
print('bug change:', mean('bug.csv'))
print('fix change:', mean('fix.csv'))
