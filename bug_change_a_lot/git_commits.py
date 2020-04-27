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
