import sys
import nfldb
import numpy as np
from painfllib import AggregatedGame
from painfllib import StrategyLogisticRegression
from painfllib import StrategyNeuralNetwork



week = 1 if len(sys.argv) < 2 else sys.argv[1]

print "Week", week

s = None
if len(sys.argv) >= 3 and sys.argv[2] == "nn":
    print "Using Neural Network"
    s = StrategyNeuralNetwork()
else:
    print "Using Logistic Regression"
    s = StrategyLogisticRegression()


db = nfldb.connect()
q = nfldb.Query(db)

q.game(season_year=2017, season_type='Regular', week=week)

predictions = []
for g in q.as_games():

    # Make prediction
    p = s.predict(g)
    pp = s.predict_proba(g)[0]
    highest_proba = np.max(pp)

    predictions.append([g,highest_proba,pp,p])

predictions = sorted(predictions, key=lambda e: e[1], reverse=True)

for prediction in predictions:
    print prediction[0]
    if prediction[3] == 1:
        print "Bet on ", prediction[0].home_team, " with ", round(prediction[1]*100,2) , "% probability"
    else:
        print "Bet on ", prediction[0].away_team, " with ", round(prediction[1]*100,2) , "% probability"
    print prediction[2]

for prediction in predictions:
    p_team = prediction[0].home_team if prediction[3] == 1 else prediction[0].away_team
    print prediction[0].away_team, prediction[0].home_team, p_team, round(prediction[1]*100,2)
