
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
Use ks-testb to verify if diff hours of different versions are from the same distribution.
And get the proportion of diff hours in the range of 50-150. 
"""

__copyright__ = 'T1,Lanzhou University,2020'
__license__ = 'GPLV2 or later'
__version__ = 0.2
__author__ = ['Hanqiang Qiu','Yanfei Cao','Zheng Liu','Xiujie Song','Yuxuan Cao','Shan Gao','Zexin Zhang','Junwei Ding']
__email__ = ['479845114@qq.com','caoyf18@lzu.edu.cn','liuzheng2018@lzu.edu.cn','songxj@lzu.edu.cn','caoyx2018@lzu.edu.cn','shgao18@lzu.edu.cn','zhangzexin18@lzu.edu.cn','dingjw18@lzu.edu.cn']
__status__ = 'done'


import pandas as pd
from scipy.stats import ks_2samp


class Data:
    def __init__(self, filename):
        self.filename=filename

    def get_diff(self):
        # get diff data
        df = pd.read_csv(self.filename, comment='#', header=0, sep=',', index_col='lv')
        a = list(df['hour'].values)
        diff=[a[0]] + [a[i + 1] - a[i] for i in range(len(a) - 1)]
        return diff

    def get_num_in_range(self, min, max):
        ldiff = self.get_diff()
        # total number
        tnum = len(ldiff)
        diff_in_range = [i for i in ldiff if i <= int(max) and i >= int(min)]
        # number in the range [50,150]
        range_num = len(diff_in_range)
        return tnum,range_num

    def get_diff_percent(self):
        v_num,v_rnum = self.get_num_in_range(50,150)
        per = v_rnum/v_num
        return per


class Metric:

    def __init__(self, data1, data2):
        self.v_data1=data1
        self.v_data2=data2

    def ks_diff(self):
        """Using ks-test to compare distribution, return p-values."""
        v_200_1 = [i for i in self.v_data1.get_diff() if i < 200]
        v_200_2 = [i for i in self.v_data2.get_diff() if i < 200]

        st,p = ks_2samp(v_200_1,v_200_2)
        return p


if __name__ == '__main__':
    v44=Data('4.4.csv')
    v49=Data('4.9.csv')
    v414=Data('4.14.csv')
    v419=Data('4.19.csv')

    per_list = [v44.get_diff_percent(), v49.get_diff_percent(), v414.get_diff_percent(), v419.get_diff_percent()]
    ver_list = ['v4.4', 'v4.9', 'v4.14', 'v4.19']
    print('Ratio of diff data between 50-150:')
    for i in range(len(per_list)):
        print('{}:'.format(ver_list[i]), per_list[i])

    v44_49=Metric(v44, v49)
    v44_414=Metric(v44, v414)
    v44_419=Metric(v44, v419)
    v49_414=Metric(v49, v414)
    v49_419=Metric(v49, v419)
    v414_419=Metric(v414, v419)

    p44_49=v44_49.ks_diff()
    p44_414=v44_414.ks_diff()
    p44_419=v44_419.ks_diff()
    p49_414=v49_414.ks_diff()
    p49_419=v49_419.ks_diff()
    p414_419=v414_419.ks_diff()
    plist = [p44_49,p44_414,p44_419,p49_414,p49_419,p414_419]
    order = ['v4.4 & v4.9', 'v4.4 & v4.14', 'v4.4 & v4.19', 'v4.9 & v4.14', 'v4.9 & v4.19', 'v4.14 & v4.19']
    for i in range(len(plist)):
        print('p-value of comparision between', order[i], ":", plist[i])
