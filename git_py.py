

import csv
from subprocess import Popen, PIPE, check_output

def gitFileDynamics(fileName, kernelRange, repo):
    # git log --stat --oneline --follow v4.4..v4.5 kernel/sched/core.c
    cmd = ["git", "-P", "log", "--stat", "--oneline", "--follow", kernelRange, fileName]
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()

    f = open('result.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)

    # print the git output as one blob
    #print(data.decode("utf-8"))
    # ...or print it split into lines
    li = []
    log = []
    i = 1
    for line in data.decode("utf-8").split("\n"):
        if i == 4:
            li.append(log)
            log = []
            i = 1
        if i == 1:
            ind = line.find(' ')
            log.append(line[0:ind])
            log.append(line[ind+1:])
            i += 1
            continue
        if i == 2:
            ind = line.find('|')
            log.append(line[0:ind])
            log.append(line[ind+1:])
            i += 1
            continue
        log.append(line)
        i += 1

    csv_writer.writerows(li)
    f.close()

def rearrange(filePath='result.csv'):
    li = []
    with open('result.csv', 'r') as fh:
        reader = csv.reader(fh)
        for row in reader:
            li.append(row)
    fh.close()
    fixed = []
    log = []
    num = 1
    for i in li:
        log.append(num)
        for j in i:
            log.append(j)
        fixed.append(log)
        log = []
        num += 1
    f = open('result.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerows(fixed)

gitFileDynamics("kernel/sched/core.c", "v4.4..v4.5", "E:/Python/linux-kernal/linux")

# with open('result.csv', 'r') as f:
#     reader = csv.reader(f)
#     print(type(reader))
#
#     for row in reader:
#         print(row)
rearrange()
