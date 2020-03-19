# !/usr/bin/env python3
# -*- coding: utf-8 -*-
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
Zhang Zexing  320180940590  zhangzexin18@lzu.edu.cn
"""

"""
Basic function of file: print the number of commits and the time in the Linux kernel of v4.4 of 203 sublevels (from v4.4.1 to v4.4.203) , and visualize the result by scatter plot.
Parameter: v4.4(the Linux kernel), 203(sublevel) .
Output: sublevel, hour, bug and their simple scatter plot.
"""

__copyright__ = 'T1,Lanzhou University,2020'
__license__ = 'GPLV2 or later'
__version__ = 0.2
__author__ = ['Hanqiang Qiu','Yanfei Cao','Zheng Liu','Xiujie Song','Yuxuan Cao','Shan Gao','Zexin Zhang','Junwei Ding']
__email__ = ['liuzheng2018@lzu.edu.cn','479845114@qq.com','songxj@lzu.edu.cn','shgao18@lzu.edu.cn','dingjw18@lzu.edu.cn','caoyf18@lzu.edu.cn','caoyx2018@lzu.edu.cn']
__status__ = 'done'

import re, sys, shlex, datetime
from argparse import ArgumentParser
from matplotlib import pyplot as plt
from subprocess import Popen, TimeoutExpired, PIPE, DEVNULL

class FoundException(BaseException):
    def __str__(self):
        """
        write an exception

        :return: a string for tips
        :rtype: str
        """
        pro = 'No more found!'
        return pro


class sl_hour_cnt:
    def __init__(self):
        parser = ArgumentParser(description='get the commit count per sublevel pointwise or cumulative (c)')
        parser.add_argument('revision1', help='first reversion, like v4.4')
        parser.add_argument('rev_range', type=str, help='last reversion, like 203')
        parser.add_argument('-c', '--cumulative', type=str, help='enable cumulative')
        args = parser.parse_args()
        # try:
        self.rev = args.revision1
        self.cumulative = 0
        self.sublevels = []
        self.release_hours = []
        self.commits = []

        if args.cumulative == 'c':
            self.cumulative = 1
        elif args.cumulative:
            # print("Dont know what you mean with {}" % format(args.cumulative))
            err = "Dont know what you mean with {}".format(args.cumulative)
            print(err)
            self.log_err(err)
            # {value}".format(value=value)
            sys.exit(-1)

        # if len(sys.argv) == 4:
        #     if (sys.argv[3] == "c"):
        #         self.cumulative = 1
        #     else:
        #         print("Dont know what you mean with {}" % format(sys.argv[3]))
        #         sys.exit(-1)

        try:
            self.rev_range = int(args.rev_range)
        except ValueError:
            err = 'Invalid range!'
            print(err)
            self.log_err(err)
            sys.exit(-1)

        print("#sublevel commits %s stable fixes" % self.rev)
        tplt = "{:<9}\t{:<9}\t{:<9}"
        print(tplt.format('lv', 'hour', 'bugs'))  # tag for R data.frame
        self.get_list()
        self.get_picture()

    def get_commit_cnt(self, git_cmd) -> int:
        """
        Get the number of stable fix commits

        :param git_cmd: subprocess.Popen object
        :return: The number of the commits time
        :rtype: int
        >>> a.get_commit_cnt(Popen(['git', 'rev-list', '--pretty=format:%ai', 'v4.4...v4.4.2'], stdout=PIPE, stderr=DEVNULL))
        189
        """
        # cnt = 0
        try:
            try:
                raw_counts = git_cmd.communicate(timeout=10)[0]
            except TimeoutExpired:
                git_cmd.kill()
                raw_counts = git_cmd.communicate()[0]

            if len(raw_counts) == 0:
                raise FoundException
        except FoundException as e:
            print(e)
            sl_hour_cnt.get_picture(self)

            sys.exit(-1)
        # if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_picture(self):
        """
        visualize the result by scatter plot

        :return: The scatter plot of the results
        """
        plt.scatter(self.sublevels, self.commits)
        plt.title("development of fixes over sublevel")
        plt.ylabel("stable fix commits")
        plt.xlabel("kernel sublevel stable release")
        plt.savefig("sublevel_%s.png" % self.rev)
        print("Successfully saved picture as sublevel_%s.png" % self.rev)
        plt.clf()
        plt.scatter(self.release_hours, self.commits)
        # print(self.release_hours, self.commits)
        plt.title("development of fixes over days")
        plt.ylabel("stable fix commits")
        plt.xlabel("hours spent")
        plt.savefig("hours_%s.png" % self.rev)
        print("Successfully saved picture as hours_%s.png" % self.rev)

    def get_tag_hours(self, git_cmd, base: int) -> int:
        """
        Get the hour spent during the development of fixes

        :param git_cmd: subprocess.Popen object
        :param base: 1452466892
        :return: the hour spent
        :rtype: int
        >>> a.get_tag_hours(Popen(['git', 'log', '-1', '--pretty=format:%ct', 'v4.4.2'], stdout=PIPE, stderr=DEVNULL),1452466892)
        909
        """
        SecPerHour = 3600
        try:
            try:
                seconds = git_cmd.communicate(timeout=10)[0]
            except TimeoutExpired:
                git_cmd.kill()
                seconds = git_cmd.communicate()[0]

            if len(seconds) == 0:
                raise FoundException
        except FoundException as e:
            print(e)
            sl_hour_cnt.log_err(e)
            sys.exit(-1)
        return (int(seconds) - base) // SecPerHour


    def get_list(self):
        """
        Get the list of sublevel, hours spent and stable fix commits

        :return: a string of the list of sublevel, hours, and bugs
        :rtype: str
        """
        sublevels = self.sublevels
        release_hours = self.release_hours
        commits = self.commits
        try:
            rev1 = self.rev
            v = Popen("git log -1 --pretty=format:\"%ct\" " + rev1, stdout=PIPE,
                                 stderr=DEVNULL, shell=True)
            v = int(v.communicate()[0])  # The timestamp for the initial version, like v44 = 1452466892.
            for sl in range(1, self.rev_range + 1):
                rev2 = self.rev + '.' + str(sl + 1)
                gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
                gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
                gitcnt_list = shlex.split(gitcnt)
                gittag_list = shlex.split(gittag)
                git_rev_list = Popen(gitcnt_list, stdout=PIPE, stderr=DEVNULL)
                commit_cnt = self.get_commit_cnt(git_rev_list)
                sublevels.append(sl)
                commits.append(commit_cnt)
                if self.cumulative == 0:
                    rev1 = rev2
                # if get back 0 then its an invalid revision number
                if commit_cnt:
                    git_tag_date = Popen(gittag_list, stdout=PIPE, stderr=DEVNULL)
                    hours = self.get_tag_hours(git_tag_date, v)
                    release_hours.append(hours)
                    tplt = "{:<9}\t{:<9}\t{:<9}"
                    print(tplt.format(sl, hours, commit_cnt))

                else:
                    continue
        except ValueError:
            err = 'Invalid revision!'
            print(err)
            sl_hour_cnt.log_err(self, err)

    def log_err(self, err):
        """
        record the error to a log

        :param err: 'Invalid revision!'
        :return: a log of the error
        """
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        log = 'log.txt'  # define the name of file
        with open(log, 'a', encoding="utf-8") as f:
            f.write(current_time + '   ' + err + '\n')


if __name__ == '__main__':
    a = sl_hour_cnt()
    import doctest
    doctest.testmod()
