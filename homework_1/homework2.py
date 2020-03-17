# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# get the commit count per sublevel pointwise or cumulative (c)
# arguments is the tag as displayed by git tag and the number
# of sublevels to be counted. If count is out of range for a
# specific sublevel it will terminate the loop
#
# no proper header in this file
# no legal/copyright ...OMG !
#
# things to cleanup:
# restructure the code - use of functions
# error handling ...where is the try..except ?
# argument handling: you can do better right ?
# documentation: once you understand it - fix the docs !
# transform it into a class rather than just functions !


import re, sys, subprocess, shlex
from argparse import ArgumentParser
from matplotlib import pyplot as plt

class FoundException(BaseException):
    def __str__(self):
        pro = 'No more found!'
        return pro

class sl_hour_cnt:
    def __init__(self):
        try:
            self.rev = sys.argv[1]
            self.rev_range = sys.argv[2]
            self.cumulative = 0
            self.v44 = 1452466892
            self.sublevels = []
            self.release_hours = []
            self.commits = []
        except IndexError:
            print('2 or more arguments needed please!')
            sys.exit(0)

        parser = ArgumentParser(description='get the commit count per sublevel pointwise or cumulative (c)')
        parser.add_argument('revision1', help='first reversion')
        parser.add_argument('revision2', type=str, help='last reversion')
        parser.add_argument('-c','--cumulative',type=str, help='enable cumulative')
        args = parser.parse_args()
        if args.cumulative == 'c':
            self.cumulative = 1
        else:
            print("Dont know what you mean with {}" % format(args.cumulative))
            sys.exit(-1)

        # if len(sys.argv) == 4:
        #     if (sys.argv[3] == "c"):
        #         self.cumulative = 1
        #     else:
        #         print("Dont know what you mean with {}" % format(sys.argv[3]))
        #         sys.exit(-1)

        try:
            self.rev_range = int(args.revision2)
        except ValueError:
            print('Invalid input!')
            sys.exit(0)
        
        print("#sublevel commits %s stable fixes" % self.rev)
        print("lv hour bugs")  # tag for R data.frame
        self.get_list()
        self.get_picture()

    def get_commit_cnt(self, git_cmd):
        cnt = 0
        try:
            try:
                raw_counts = git_cmd.communicate(timeout=10)[0]
            except subprocess.TimeoutExpired:
                git_cmd.kill()
                raw_counts = git_cmd.communicate()[0]
                
            if len(raw_counts) == 0:
                raise FoundException
        except FoundException as e:
            print(e)
            sl_hour_cnt.get_picture(self)
            sys.exit(2)
        # if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_picture(self):
        plt.scatter(self.sublevels,self.commits)
        plt.title("development of fixes over sublevel")
        plt.ylabel("stable fix commits")
        plt.xlabel("kernel sublevel stable release")
        plt.savefig("sublevel_v4.4.png")
        plt.clf()
        plt.scatter(self.release_hours, self.commits)
        print(self.release_hours, self.commits)
        plt.title("development of fixes over days")
        plt.ylabel("stable fix commits")
        plt.xlabel("hours spent")
        plt.savefig("hours_v4.4.png")
        print('Success!')


    def get_tag_hours(self, git_cmd, base):
        SecPerHour = 3600
        try:
            try:
                seconds = git_cmd.communicate(timeout=10)[0]
            except subprocess.TimeoutExpired:
                git_cmd.kill()
                seconds = git_cmd.communicate()[0]
                
            if len(seconds) == 0:
                raise FoundException
        except FoundException as e:
            print(e)
            sys.exit(2)
        return (int(seconds)-base) // SecPerHour

# get dates of all commits - unsorted
#     def rev_and_range(self):
#         rev = sys.argv[1]
#         cumulative = 0
#         if len(sys.argv) == 4:
#             if (sys.argv[3] == "c"):
#                 cumulative = 1
#             else:
#                 print("Dont know what you mean with %s" % sys.argv[3])
#                 sys.exit(-1)
#         rev_range = int(sys.argv[2])
#
# setup and fill in the table

# base time of v4.1 and v4.4 as ref base
# fix this to extract the time of the base commit
# from git !
#
# hofrat@Debian:~/git/linux-stable$ git log -1 --pretty=format:"%ct" v4.4
# 1452466892
    def get_list(self):
        sublevels = self.sublevels
        release_hours = self.release_hours
        commits = self.commits
        v44 = 1452466892
        try:
            rev1 = self.rev
            # v = subprocess.Popen("git log -1 --pretty=format:\"%ct\" " + rev1, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            # v = int(v.communicate()[0])
            for sl in range(1, self.rev_range + 1):
                rev2 = self.rev + '.' + str(sl+1)
                gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
                gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
                gitcnt_list = shlex.split(gitcnt)
                gittag_list = shlex.split(gittag)
                git_rev_list = subprocess.Popen(gitcnt_list, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                commit_cnt = self.get_commit_cnt(git_rev_list)
                sublevels.append(sl)
                commits.append(commit_cnt)
                if self.cumulative == 0:
                    rev1 = rev2
                # if get back 0 then its an invalid revision number
                if commit_cnt:
                    git_tag_date = subprocess.Popen(gittag_list, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                    hours = self.get_tag_hours(git_tag_date, v44)
                    release_hours.append(hours)
                    print("%s %d %d" % (sl, hours, commit_cnt))

                else:
                    continue
        except ValueError:
            print('No such a revision!')
        return self.sublevels,self.release_hours,self.commits



if __name__ == '__main__':
    a = sl_hour_cnt()

