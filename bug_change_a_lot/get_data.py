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
