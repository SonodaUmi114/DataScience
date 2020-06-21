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
Using classification decision tree to build a prediction model: 
using developers' number of Signed-off-by tags, Reviewed-by tags, Tested-by tags, Reported-by tags and fix rate(number of fix/ number of commits) to predict bug rates(number of bugs/ number of commits).
dividing bug rates into 2 classes: A(less than 0.02) and B(larger than 0.02)

Hypothesis:
If the developer has fixed more bugs, reported, signed off, reviewed and tested more codes before, 
he or she will has smaller bug rate.

Process:
Pre-process the data.
Built model.
Report the accuracy, precision, recall, RUC curve, AUC... to evaluate the model.
Use grid search to find best parameters and avoid over-fitting to improve model.
Draw the decision tree and report the importance of 5 features mentioned above.
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
from subprocess import Popen, PIPE

# matching rule for the name of developer
author = re.compile('^Author: [A-Za-z]{1,} [A-Za-z]{1,} <.+>$')


def author(repo):
    """
    obtaining the name of developers
    :param repo: the storage path of linux-stable
    :return: the name of developers in author.csv
    """
    developer = []
    cmd = ["git", "log", "-P"]
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()
    a = str(data).split("\\n")
    for line in a:
        if author.match(line):
            line = line.replace('<', ':').replace('>', '').split(':')[1].strip()
            # Prevent duplicates
            if line not in developer and line is not None:
                developer.append(line)
                with open('author.csv', 'w+', encoding='utf-8', newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow([line])


if __name__ == "__main__":
    author(repo='D:\git_warehouse\linux-stable')
