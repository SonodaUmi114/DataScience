"""
    correlation
    2020/6/8
"""


import numpy as np
import pandas as pd
import re
import unicodedata
from subprocess import Popen, PIPE
import matplotlib.pyplot as plt


class Data:
    def __init__(self):
        self.commit = commit
        self.fixes = fixes

    def gitFixCommits(self, kernelRange, repo):
        """
        Getting commits and corresponding commits fixed.
        :param kernelRange: range of kernal version's sublevels, such as 'v4.9..v4.9.216'
        :param repo: The repository where the Git command runs
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
        # print(len(cmt_time))

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

    def get_aver(self, ldiff):
        """
        Getting average of time differences between each adjacent sublevels.
        :param ldiff: list of time differences
        :return: mean of time differences
        """
        mean = np.mean(ldiff)
        return mean

    def pd_handling(self, vlist, mlist):
        """
        Using pandas to clean nan values in lists
        :param vlist: raw list of versions
        :param mlist: raw list of means
        :return: cleaned version list and mean list
        """
        ver = vlist
        mean = mlist
        d = {'version': ver, 'mean': mean}
        data = pd.DataFrame(d)
        data = data.dropna()
        vlist = data['version'].values.tolist()
        mlist = data['mean'].values.tolist()
        print(data)
        return vlist, mlist


class Plot:
    def __init__(self,vlist,mlist):
        self.vlist = vlist
        self.mlist = mlist



    def get_plot(self):
        """
        Plotting for average bug-survival time changed with sublevels.
        :param mlist: list of means of time differences
        :return: showing plot
        """
        plt.plot(self.vlist,self.mlist)
        plt.xlabel('sublevels')
        plt.ylabel('average bug-survival time')
        plt.title('bug-survival time changed over sublevels')
        plt.show()

    def correlation(self):
        """
        Calculate the correlation coefficient of data
        :param mlist:list of means of time differences
        :return:correlation coefficient of data
        """
        x=[int(i.split('.')[-1]) for i in self.vlist]
        y=self.mlist
        xy = np.array([x, y])
        np.cov(xy)
        corre = np.corrcoef(xy)
        print(corre)



if __name__ == '__main__':
    commit = re.compile('^commit [0-9a-z]{40}$', re.IGNORECASE)
    fixes = re.compile('^\W+Fixes: [a-f0-9]{8,40} \(.*\)$', re.IGNORECASE)
    case = Data()
    l_ldiff = []
    avr_list = []
    for i in range(1,216):
        lcmt, lfix = case.gitFixCommits("v4.9.{}..v4.9.{}".format(i,i+1), '/Volumes/云淡风轻/linux-stable')
        cmt_time, fix_time = case.git_time(lcmt, lfix, '/Volumes/云淡风轻/linux-stable')
        ldiff = case.get_diff(cmt_time, fix_time)
        mean = case.get_aver(ldiff)
        avr_list.append(mean)
    vlist_raw = ['v4.9.{}'.format(i) for i in range(1, len(avr_list) + 1)]
    vlist,mlist = case.pd_handling(vlist_raw,avr_list)
    p1 = Plot(vlist,mlist)
    p1.get_plot()
    p1.correlation()
