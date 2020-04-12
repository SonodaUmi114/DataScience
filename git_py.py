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
Moving the git command into python and calling it as a subprocess.
Collecting the output in python.
Reformatting it and write the whole record into a CSV file. 
"""

__copyright__ = 'T1,Lanzhou University,2020'
__license__ = 'GPLV2 or later'
__version__ = 0.2
__author__ = ['Hanqiang Qiu','Yanfei Cao','Zheng Liu','Xiujie Song','Yuxuan Cao','Shan Gao','Zexin Zhang','Junwei Ding']
__email__ = ['479845114@qq.com','caoyf18@lzu.edu.cn','liuzheng2018@lzu.edu.cn','songxj@lzu.edu.cn','caoyx2018@lzu.edu.cn','shgao18@lzu.edu.cn','zhangzexin18@lzu.edu.cn','dingjw18@lzu.edu.cn']
__status__ = 'done'

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
