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
Using subprocess and re to get the commits and tags data of developers.
using the name of all developers in author.csv.

Process:
Get git log.
Get the data of number of sign-off tags, test tags, review tags, report tags, bugs, fixes and total commits of each developer.
Save the data into developer.csv.
"""

__copyright__ = 'T1,Lanzhou University,2020'
__license__ = 'GPLV2 or later'
__version__ = 0.1
__author__ = ['Hanqiang Qiu', 'Yanfei Cao', 'Zheng Liu', 'Xiujie Song', 'Yuxuan Cao', 'Shan Gao', 'Zexin Zhang',
              'Junwei Ding']
__email__ = ['479845114@qq.com', 'caoyf18@lzu.edu.cn', 'liuzheng2018@lzu.edu.cn', 'songxj2018@lzu.edu.cn',
             'caoyx2018@lzu.edu.cn', 'shgao18@lzu.edu.cn', 'zhangzexin18@lzu.edu.cn', 'dingjw18@lzu.edu.cn']
__status__ = 'done'

import re
import csv
import subprocess
from subprocess import Popen, PIPE


class Developer:
    def __init__(self):
        self.fix = re.compile('^\W+Fixes: [a-f0-9]{8,40} \(.*\)$', re.IGNORECASE)  # matching rule for fix_tag
        self.commit = re.compile('^[0-9a-z]{5,}')  # matching rule for bug_id
        self.repo = 'D:\git_warehouse\linux-stable'  # the storage path of linux-stable

        cmd = ["git", "log", "-P"]
        p = Popen(cmd, cwd=self.repo, stdout=PIPE)
        data, res = p.communicate()
        self.data = str(data).split("\\n")

        with open('developer.csv', 'w+', encoding='utf-8', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(
                ['author', 'commits', 'fixes', 'bugs', 'sign-off', 'test', 'review', 'report'])

        self.get_author()

    def get_author(self):
        """
        loop through the developer in author.csv
        :return: the commits and tags data for each developer in developer.csv
        """
        with open('author.csv') as f:
            csv_reader = csv.reader(f)
            for i, row in enumerate(csv_reader):
                author = row[0]
                try:
                    result = self.git(author)
                    # if the number of commits <= 10
                    if result == 0:
                        # print(i)
                        continue
                    else:
                        # print(i)
                        with open('developer.csv', 'a+', encoding='utf-8', newline='') as f:
                            csv_writer = csv.writer(f)
                            csv_writer.writerow(result)
                except:
                    continue

    def git(self, name):
        """
        obtaining the commits and tags data for developer
        :param name: the name of developer
        :return: the commits and tags data for developer
        """
        sign_off = re.compile('^\W+Signed-off-by: {} .+>$'.format(name))  # matching rule for signed-off by tag
        test = re.compile('^\W+Tested-by: {} .+>$'.format(name))  # matching rule for tested-by tag
        review = re.compile('^\W+Reviewed-by: {} .+>$'.format(name))  # matching rule for reviewed-by tag
        report = re.compile('^\W+Reported-by: {} .+>$'.format(name))  # matching rule for reported-by tag

        cmd = 'git log --author="{}" --oneline --shortstat'.format(name)
        p = subprocess.Popen(cmd, cwd=self.repo, stdout=subprocess.PIPE, shell=True)
        out = p.stdout.readlines()
        out = [i.decode('utf-8', "ignore").replace('\n', '').strip() for i in out]
        commit_id = []
        for i in out:
            commit_id.append(self.commit.findall(i))
        commit_id = [i for i in commit_id if i != []]  # all commits in a list
        commits = len(commit_id)  # the number of commits

        if commits >= 10:
            sign_off_number = 0  # the number of sign-off
            test_number = 0  # the number of test
            review_number = 0  # the number of review
            report_number = 0  # the number of report
            fixes = 0  # the number of fixes
            bugs = 0  # the number of bugs

            for line in self.data:
                if sign_off.match(line):
                    sign_off_number += 1
                elif test.match(line):
                    test_number += 1
                elif review.match(line):
                    review_number += 1
                elif report.match(line):
                    report_number += 1

            for i in commit_id:
                cmd1 = ["git", "show", "{}".format(i[0])]
                p = Popen(cmd1, cwd=self.repo, stdout=PIPE)
                data, res = p.communicate()
                for line in data.decode("utf-8", "ignore").split("\n"):
                    if self.fix.match(line):
                        fixes += 1
                        bug = line.split()[1]
                        if [bug] in commit_id:
                            bugs += 1
            # all the commit data
            result = [name, commits, fixes, bugs, sign_off_number, test_number, review_number, report_number]
            return result
        else:
            return 0


if __name__ == "__main__":
    developer = Developer()
