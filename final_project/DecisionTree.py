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
__author__ = ['Hanqiang Qiu','Yanfei Cao','Zheng Liu','Xiujie Song','Yuxuan Cao','Shan Gao','Zexin Zhang','Junwei Ding']
__email__ = ['479845114@qq.com','caoyf18@lzu.edu.cn','liuzheng2018@lzu.edu.cn','songxj2018@lzu.edu.cn','caoyx2018@lzu.edu.cn','shgao18@lzu.edu.cn','zhangzexin18@lzu.edu.cn','dingjw18@lzu.edu.cn']
__status__ = 'done'


from imblearn.over_sampling import SMOTE
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp
from sklearn.metrics import classification_report
import pydotplus
import graphviz


class Classifier:
    def __init__(self, dataset):
        # 1. obtaining data
        self.data = pd.read_csv(dataset)

    def data_processing(self, data):
        """
        cleansing and preprocessing data, and adding bug_rate and fixes_rate
        :param data: data in developer.csv
        :return: data preprocessed and data of bug rate
        """
        #  cleansing data
        data.dropna()
        data['bug_rate'] = [float(data['bugs'][i] / data['commits'][i]) for i in range(len(data))]
        data['fixes_rate'] = [data['fixes'][i] / data['commits'][i] for i in range(len(data))]
        data_1 = data[data['commits'] >= 50]
        br = data_1['bug_rate']
        return data_1, br

    def divide_set(self, data_1, br):
        """

        :param data_1: data preprocessed of developers
        :param br: data of rate of writing bugs
        """
        data_1.loc[br <= 0.02, 'quality'] = 'A'

        data_1.loc[br > 0.02, 'quality'] = 'B'
        # print(data_1['quality'].value_counts())

        #  select parameters needed for setting up model
        X = data_1[['sign-off', 'test', 'review', 'report', 'fixes_rate']]
        y = data_1['quality']

        #  split dataset into train set and test set
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(X, y)

    def enlarge(self):
        """
        using SMOTE to enlarge x_train and y_train to eliminate difference of numbers of them
        :return: enlarged data
        """
        # enlarge data set
        smo = SMOTE()
        self.x_train, self.y_train = smo.fit_sample(self.x_train, self.y_train)
        # print(self.x_train)
        # print(len(self.x_train))

    def trainning(self):
        """
        using decision tree to train and produce model1 of dntree
        :return: decision tree estimator and decision tree model1
        """
        #  training decision tree model
        dnestimator = DecisionTreeClassifier(criterion='gini')
        dnmodel1 = dnestimator.fit(self.x_train, self.y_train)
        return dnestimator, dnmodel1

    def model_value_1(self, dnmodel1):
        """
        printing the output of decision tree model1, such as the accuracy
        :param dnmodel1: decision tree model
        :return: accuracy of prediction with test dataset
        """
        #  evaluating decision tree model
        #  1. comparing true value and predicting value
        y_predict0 = dnmodel1.predict(self.x_test)
        # print('comparing true value and predicting value:\n', self.y_test == y_predict0)

        #  2. computing accuracy of prediction
        dnscore = dnmodel1.score(self.x_test, self.y_test)
        print('Accuracy of original model: ', dnscore)

    def grid_search(self, dnestimator):
        """
        using grid search to select the best value of parameters
        :param dnestimator: decision tree model
        :return: grid search estimator
        """
        #  grid search
        param_dict = {'max_depth': [4, 5, 6, 7, 8, 9, 10, 11, 12], 'min_samples_split': [2, 4, 6, 8],
                      'min_samples_leaf': [2, 4, 8, 10, 12]}
        gs_estimator = GridSearchCV(dnestimator, param_grid=param_dict, cv=10)
        wgmodel = gs_estimator.fit(self.x_train, self.y_train)

        # best_params_
        print('best parameters：\n', gs_estimator.best_params_)
        # 最佳结果：best_score_
        print('best score：\n', gs_estimator.best_score_)
        # 最佳估计器：best_estimator_
        print('best estimator：\n', gs_estimator.best_estimator_)
        return gs_estimator

    def model_improve(self, gs_estimator):
        """
        using best estimator to train a new model
        :param gs_estimator: grid search estimator
        :return: improved model, and prediction of improved model
        """
        #  using best estimator to train a new model
        imp_dn = gs_estimator.best_estimator_
        imp_model = imp_dn.fit(self.x_train, self.y_train)

        yimp_predict = imp_model.predict(self.x_test)
        #  computing accuracy of improved data
        imp_score = imp_model.score(self.x_test, self.y_test)
        print('Accuracy of improved model: ', imp_score)
        return imp_model, yimp_predict

    def model_value_2(self, imp_model, yimp_predict):
        """
        evaluating model by computing importance and AUC, and obtaining classification report.
        :param imp_model: improved decision tree model
        :param yimp_predict: prediction of improved model
        :return: false positive rate, true positive rate, and AUC of test set and train set
        """
        x_train = self.x_train
        y_train = self.y_train
        x_test = self.x_test
        y_test = self.y_test
        #  evaluating model
        #  1. importance
        importance = imp_model.feature_importances_
        print('feature importance: ',importance)
        #  show importance in picture
        Impt_Series = pd.Series(importance, index = x_train.columns)

        Impt_Series.sort_values(ascending = True).plot('barh')
        plt.show()

        #  2. classification report
        print('Classification Report:')
        print(classification_report(self.y_test, yimp_predict, target_names=['A', 'B']))

        #  3. calculating AUC
        #  translating A,B into 0,1 for calculating AUC
        y_test[y_test == 'A'] = 1
        y_test[y_test == 'B'] = 0
        yimp_predict[yimp_predict == 'A'] = 1
        yimp_predict[yimp_predict == 'B'] = 0
        yimp_predict = list(yimp_predict)
        y_test = list(y_test)
        test_fpr, test_tpr, threshold0 = roc_curve(y_test, yimp_predict)
        # calculating AUC of train set
        test_roc_auc = auc(test_fpr, test_tpr)

        #  calculating AUC of test set
        y_train_pre = imp_model.predict(x_train)
        y_train[y_train == 'A'] = 1
        y_train[y_train == 'B'] = 0
        y_train_pre[y_train_pre == 'A'] = 1
        y_train_pre[y_train_pre == 'B'] = 0
        y_train = list(y_train)
        y_train_pre = list(y_train_pre)
        train_fpr, train_tpr, threshold1 = roc_curve(y_train, y_train_pre)
        train_roc_auc = auc(train_fpr, train_tpr)
        return train_fpr, test_fpr, train_tpr, test_tpr, test_roc_auc, train_roc_auc

    def save(self):
        """
        saving data enlarged by SMOTE
        :return: file 'smo_data.csv'
        """
        smo_data = self.x_train
        smo_data['quality'] = self.y_train

        #  save data into csv file
        smo_data.to_csv('smo_data.csv')

    def plot(self, train_fpr, test_fpr, train_tpr, test_tpr, test_roc_auc, train_roc_auc):
        """
        getting ROC plot
        :param train_fpr: false positive rate of train set
        :param test_fpr: false positive rate of test set
        :param train_tpr: true positive rate of train set
        :param test_tpr: true positive rate of test set
        :param test_roc_auc: AUC value of test set
        :param train_roc_auc: AUC value of train set
        :return: showing plot of ROC
        """
        #  drawing area
        plt.stackplot(train_fpr, train_tpr, color='green', alpha=0.5, edgecolor='black')
        plt.stackplot(test_fpr, test_tpr, color='steelblue', alpha=0.5, edgecolor='black')

        #  adding marginal line
        plt.plot(test_fpr, test_tpr, color='black', lw=1)
        plt.plot(train_fpr, train_tpr, color='blue', lw=1)

        #  adding diagonal
        plt.plot([0, 1], [0, 1], color='red', linestyle='--')

        #  adding annotation
        plt.text(0.5, 0.3, 'test ROC curve (area = %0.2f)' % test_roc_auc)
        plt.text(0.5, 0.2, 'train ROC curve (area = %0.2f)' % train_roc_auc)

        #  adding labels of x-axis and y-axis
        plt.xlabel('1-Specificity')
        plt.ylabel('Sensitivity')

        # showing the plot
        plt.show()

    def decision_tree(self, imp_model):
        """
        getting pdf file of desicion_tree
        :param imp_model: improved decision tree model
        :return: pdf file of desicion_tree
        """
        
        dot_data = export_graphviz(imp_model, out_file=None,class_names=['A','B'])
        graph = graphviz.Source(dot_data)
        graph.render("dntree")
        print('Decision tree is produced successfully!')


if __name__ == "__main__":
    C = Classifier('developer.csv')
    # data pre-processing
    data_1, br = C.data_processing(C.data)
    C.divide_set(data_1, br)
    # Using SMOTE to enlarge train set
    C.enlarge()
    dnestimator, dnmodel1 = C.trainning()
    C.model_value_1(dnmodel1)
    gs_estimator = C.grid_search(dnmodel1)
    imp_model, yimp_predict = C.model_improve(gs_estimator)
    train_fpr, test_fpr, train_tpr, test_tpr, test_roc_auc, train_roc_auc = C.model_value_2(imp_model, yimp_predict)
    C.plot(train_fpr, test_fpr, train_tpr, test_tpr, test_roc_auc, train_roc_auc)
    C.decision_tree(imp_model)
