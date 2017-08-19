from FeatureVectorFactory import FeatureVectorFactory

from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

class StrategyLogisticRegression:
    def __init__(self):
        self.clf = joblib.load('models/logistic_regression_scheme5_good.pkl')
        self.fvf = FeatureVectorFactory()

    # Always predict the home team wins
    def predict(self,game):
        feature_vector = self.fvf.get_feature_vector_scheme5_for(game)
        return self.clf.predict([feature_vector])

    # Always predict the home team wins
    def predict_proba(self,game):
        feature_vector = self.fvf.get_feature_vector_scheme5_for(game)
        return self.clf.predict_proba([feature_vector])
