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
Zhang Zexin   320180940590  zhangzexin18@lzu.edu.cn """

"""
data4: group homework
get the data of time-to-fix 
collect the bug survival time in v4.9/v4.4/v4.14/v4.19
"""

__copyright__ = 'T1,Lanzhou University,2020'
__license__ = 'GPLV2 or later'
__version__ = 0.2
__author__ = ['Hanqiang Qiu','Yanfei Cao','Zheng Liu','Xiujie Song','Yuxuan Cao','Shan Gao','Zexin Zhang','Junwei Ding']
__email__ = ['479845114@qq.com','caoyf18@lzu.edu.cn','liuzheng2018@lzu.edu.cn','songxj2018@lzu.edu.cn','caoyx2018@lzu.edu.cn','shgao18@lzu.edu.cn','zhangzexin18@lzu.edu.cn','dingjw18@lzu.edu.cn']
__status__ = 'done'



import re
import unicodedata
from subprocess import Popen, PIPE
import csv


class Data:
    def __init__(self):
        self.commit = commit
        self.fixes = fixes

    def gitFixCommits(self, kernelRange, repo):
        """
        Getting commits and corresponding commits fixed.
        :return: lists of commits and corresponding commits fixed
        """
        nr_fixes = 0
        cmd = ["git", "log", "-P", "--no-merges", kernelRange]
        p = Popen(cmd, cwd=repo, stdout=PIPE)
        data, res = p.communicate()
        # we need to clean and normalize the data - note the errors ignore !
        data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))
        cmt_list = []
        fix_list = []
        for line in data.split("\n"):
            if (commit.match(line)):
                cur_commit = line
            if (fixes.match(line)):
                # we have a fixes tag
                nr_fixes += 1
                cmt_list.append(cur_commit[7:19])
                fix_list.append(line.strip()[7:30].split(' ')[0])
        return cmt_list, fix_list

    def git_time(self, lcmt, lfix, repo):
        """
        Getting timestamps of commits required
        :param lcmt: lists of commits fixing bugs
        :param lfix: lists of commits fixed
        :param repo: the repository where the Git command runs
        :return: lists of timestamps of commits and fixes
        """
        cmt_time = []
        fix_time = []
        c_f = dict(zip(lcmt, lfix))
        for cmt, fix in c_f.items():
            cmd_c = ['git', 'log', '-1', '--pretty=format:\"%ct\"', cmt]
            cmd_f = ['git', 'log', '-1', '--pretty=format:\"%ct\"', fix]
            p_c = Popen(cmd_c, cwd=repo, stdout=PIPE)
            p_f = Popen(cmd_f, cwd=repo, stdout=PIPE)

            data1, res = p_c.communicate()
            data2, res = p_f.communicate()
            data1 = unicodedata.normalize(u'NFKD', data1.decode(encoding="utf-8", errors="ignore"))
            data2 = unicodedata.normalize(u'NFKD', data2.decode(encoding="utf-8", errors="ignore"))
            if data2 != '':
                cmt_time.append(int(data1.strip('"')))
                fix_time.append(int(data2.strip('"')))
        return cmt_time, fix_time

    def get_diff(self, cmt_time, fix_time):
        """
        Getting time difference between commits and fixes
        :param cmt_time: list of timestamps of commits
        :param fix_time: list of timestamps of fixes
        :return: list of time differences
        """
        # get diff data
        sec_per_hour = 3600
        ldiff = [(cmt_time[i] - fix_time[i]) // sec_per_hour for i in range(len(cmt_time))]
        return ldiff

    def store_data(self ,ldiff):
        with open('v4_4.csv','w',encoding='utf-8') as f:
            writer = csv.writer(f)
            for i in ldiff:
                writer.writerow([i])


if __name__ == '__main__':
    commit = re.compile('^commit [0-9a-z]{40}$', re.IGNORECASE)
    fixes = re.compile('^\W+Fixes: [a-f0-9]{8,40} \(.*\)$', re.IGNORECASE)
    case = Data()
    l_ldiff = []
    avr_list = []

    lcmt, lfix = case.gitFixCommits("v4.4", 'D:\Github\Github_programs\linux-stable')
    cmt_time, fix_time = case.git_time(lcmt, lfix, 'D:\Github\Github_programs\linux-stable')
    ldiff = case.get_diff(cmt_time, fix_time)
    case.store_data(ldiff)
