from FeatureVectorFactory import FeatureVectorFactory

from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

class StrategyNeuralNetwork:

    def __init__(self):
        self.clf = joblib.load('models/neural_network_scheme5_good.pkl')
        self.fvf = FeatureVectorFactory()

    # Always predict the home team wins
    def predict(self,game):
        feature_vector = self.fvf.get_feature_vector_scheme5_for(game)
        return int(self.clf.predict([feature_vector])[0])

    # Always predict the home team wins
    def predict_proba(self,game):
        feature_vector = self.fvf.get_feature_vector_scheme5_for(game)
        return self.clf.predict_proba([feature_vector])
