import joblib
from sklearn import datasets, svm

# load iris dataset
iris = datasets.load_iris()
X, y = iris.data, iris.target

# train model
clf = svm.LinearSVC()
clf.fit(X, y)

# save model
joblib.dump(clf, "iris_model.pickle")
