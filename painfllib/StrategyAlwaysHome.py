class StrategyAlwaysHome:
    # Always predict the home team wins
    def predict(self,game):
        return 1

    def predict_proba(self,game):
        return [0,1]
