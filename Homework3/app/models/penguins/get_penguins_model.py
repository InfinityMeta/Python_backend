import joblib
import pandas as pd
import seaborn as sns
from sklearn import svm

# load and transform penguin dataset
penguins = sns.load_dataset("penguins")
penguins.dropna(inplace=True)

# transform features
penguins["sex"] = penguins["sex"].map({"Male": 0, "Female": 1})
island_dummies = pd.get_dummies(penguins["island"], dtype=int)
penguins.drop(["island"], axis=1, inplace=True)
penguins = penguins.join(island_dummies)

# transform target
penguins["species"] = penguins["species"].map(
    {"Adelie": 0, "Chinstrap": 1, "Gentoo": 2}
)

X, y = penguins.drop(["species"], axis=1).values, penguins["species"].values


# train model
clf = svm.LinearSVC()
clf.fit(X, y)

# save model
joblib.dump(clf, "penguins_model.pickle")
