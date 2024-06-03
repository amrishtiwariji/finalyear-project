import pickle
import joblib
import numpy
import pandas
import sklearn.ensemble as ek
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


dataset = pandas.read_csv('/Users/tamri/Documents/Malware-Detection-ML-Model-main/datasets/dataset_1.csv')

dataset.head()
dataset.describe()
dataset.groupby(dataset['legitimate']).size()

# data preprocessing
X = dataset.drop(['ID', 'md5', 'legitimate'], axis=1).values
y = dataset['legitimate'].values

# Features we need for DTs
extratrees = ek.ExtraTreesClassifier().fit(X, y)
model = SelectFromModel(extratrees, prefit=True)
X_new = model.transform(X)
nbfeatures = X_new.shape[1]

# print(nbfeatures)

X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.2)

features = []
index = numpy.argsort(extratrees.feature_importances_)[::-1][:nbfeatures]
for f in range(nbfeatures):
    #     print("%d. feature %s (%f)" % (f + 1, dataset.columns[2+index[f]], extratrees.feature_importances_[index[f]]))
    features.append(dataset.columns[2 + f])




# modelgive the best value
model = ek.RandomForestClassifier(n_estimators=33)
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print("Accuracy:", (score * 100), '%')

joblib.dump(model, "model/model.pkl")
open('model/features.pkl', 'wb').write(pickle.dumps(features))

# False Positives and Negatives
res = model.predict(X_new)
mt = confusion_matrix(y, res)
print("False positive rate : %f %%" % ((mt[0][1] / float(sum(mt[0]))) * 100))
print('False negative rate : %f %%' % (mt[1][0] / float(sum(mt[1])) * 100))
