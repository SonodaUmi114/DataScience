import re
import csv
import subprocess
from subprocess import Popen, PIPE


class Developer:
    def __init__(self):
        self.fix = re.compile('^\W+Fixes: [a-f0-9]{8,40} \(.*\)$', re.IGNORECASE)  # fix_tag
        self.commit = re.compile('^[0-9a-z]{5,}')  # bug_id
        self.repo = 'D:\git_warehouse\linux-stable'  # the address of linux-stable warehouse

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

        with open('author.csv') as f:
            csv_reader = csv.reader(f)
            for i, row in enumerate(csv_reader):
                author = row[0]
                try:
                    result = self.git(author)
                    if result == 0:
                        print(i)
                        continue
                    else:
                        print(i)
                        with open('developer.csv', 'a+', encoding='utf-8', newline='') as f:
                            csv_writer = csv.writer(f)
                            csv_writer.writerow(result)
                except:
                    continue

    def git(self, name):
        sign_off = re.compile('^\W+Signed-off-by: {} .+>$'.format(name))  # signed-off by tag
        test = re.compile('^\W+Tested-by: {} .+>$'.format(name))  # tested-by tag
        review = re.compile('^\W+Reviewed-by: {} .+>$'.format(name))  # reviewed-by tag
        report = re.compile('^\W+Reported-by: {} .+>$'.format(name))  # reported-by tag

        cmd = 'git log --author="{}" --oneline --shortstat'.format(name)
        p = subprocess.Popen(cmd, cwd=self.repo, stdout=subprocess.PIPE, shell=True)
        out = p.stdout.readlines()
        out = [i.decode('utf-8', "ignore").replace('\n', '').strip() for i in out]
        commit_id = []
        for i in out:
            commit_id.append(self.commit.findall(i))
        commit_id = [i for i in commit_id if i != []]
        commits = len(commit_id)

        if commits >= 10:
            sign_off_number = 0  # the number of sign-off
            test_number = 0  # the number of test
            review_number = 0  # the number of review
            report_number = 0  # the number of report
            fixes = 0
            bugs = 0

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

            result = [name, commits, fixes, bugs, sign_off_number, test_number, review_number, report_number]
            return result
        else:
            return 0


developer = Developer()
