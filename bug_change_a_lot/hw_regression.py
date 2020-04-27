from sklearn.linear_model import LinearRegression
import pandas as pd


def mul_regression():
    # 1. obtain the data
    fix = pd.read_csv('fixes.csv',
                      header=None, names=['added', 'removed', 'file modified'])
    # fix = fix[['added','removed']]
    fix.insert(3, 'bug_commit', 0)

    bug = pd.read_csv('bugs.csv',
                      header=None, names=['added', 'removed', 'file modified'])
    bug.insert(3, 'bug_commit', 1)
    fix_bug = pd.concat([bug, fix], ignore_index=True)

    factors = ['added', 'removed', 'file modified']
    x = fix_bug[factors]
    y = fix_bug['bug_commit']

    # 2. model training
    estimator = LinearRegression()
    model = estimator.fit(x, y)

    # 3. test
    rd_sample = pd.read_csv('random_commits.csv')
    rd_sample.columns = ['added', 'removed', 'file modified']
    pre_bug = estimator.predict(x)
    all_data = pd.concat([fix_bug, rd_sample])
    print(estimator.score(x, y))


def sin_regression():
    # 1. obtain the data
    fix = pd.read_csv('fixes.csv',
                      header=None, names=['added', 'removed', 'file modified'])
    # fix = fix[['added','removed']]
    fix.insert(3, 'bug_commit', 0)

    bug = pd.read_csv('bugs.csv',
                      header=None, names=['added', 'removed', 'file modified'])
    bug.insert(3, 'bug_commit', 1)
    fix_bug = pd.concat([bug, fix], ignore_index=True)
    fix_bug.insert(4, 'sum',
                   [fix_bug['added'].values[i]+fix_bug['removed'].values[i] for i in range(len(fix_bug))])

    x = fix_bug[['sum']]
    y = fix_bug['bug_commit']

    # 2. model training
    estimator = LinearRegression()
    model = estimator.fit(x, y)

    # 3. test
    print(estimator.score(x, y))


mul_regression()
sin_regression()
