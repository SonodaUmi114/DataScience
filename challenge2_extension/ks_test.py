
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

def get_diff(filename):
    # get diff data
    df = pd.read_csv(filename, comment='#', header=0, sep=',', index_col='lv')
    a = list(df['hour'].values)
    diff=[a[0]] + [a[i + 1] - a[i] for i in range(len(a) - 1)]
    return diff

def ks_diff():
    v4_200 = [i for i in get_diff('4.4.csv') if i < 200]
    v9_200 = [i for i in get_diff('4.9.csv') if i < 200]
    v14_200 = [i for i in get_diff('4.14.csv') if i < 200]
    v19_200 = [i for i in get_diff('4.19.csv') if i < 200]

    st44_49,p44_49 = ks_2samp(v4_200,v9_200)
    st44_414,p44_414 = ks_2samp(v4_200,v14_200)
    st44_419,p44_419 = ks_2samp(v4_200,v19_200)
    st49_414,p49_414 = ks_2samp(v9_200,v14_200)
    st49_419,p49_419 = ks_2samp(v9_200,v19_200)
    st414_419,p414_419 = ks_2samp(v14_200,v19_200)

    st_list = [st44_49,st44_414,st44_419,st49_414,st49_419,st414_419]
    plist = [p44_49,p44_414,p44_419,p49_414,p49_419,p414_419]
    order = ['v4.4 & v4.9','v4.4 & v4.14','v4.4 & v4.19','v4.9 & v4.14','v4.9 & v4.19','v4.14 & v4.19']
    for i in range(len(plist)):
        print('p-value of comparision between', order[i],":",plist[i])

def get_num_in_range(filename,min,max):
    ldiff = get_diff(filename)
    tnum = len(ldiff)
    diff_in_range = [i for i in ldiff if i <= int(max) and i >= int(min)]
    range_num = len(diff_in_range)
    return tnum,range_num

def get_diff_percent():
    v44_num,v44_rnum = get_num_in_range('4.4.csv',50,150)
    v49_num,v49_rnum = get_num_in_range('4.9.csv',50,150)
    v414_num,v414_rnum = get_num_in_range('4.14.csv',50,150)
    v419_num,v419_rnum = get_num_in_range('4.19.csv',50,150)

    per_44 = v44_rnum/v44_num
    per_49 = v49_rnum/v49_num
    per_414 = v414_rnum/v414_num
    per_419 = v419_rnum/v419_num

    per_list = [per_44,per_49,per_414,per_419]
    ver_list = ['v4.4','v4.9','v4.14','v4.19']
    print('Ratio of diff data between 50-150:')
    for i in range(len(per_list)):
        print('{}:'.format(ver_list[i]), per_list[i])

ks_diff()
get_diff_percent()

