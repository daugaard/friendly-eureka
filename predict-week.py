import nfldb
import numpy as np
from painfllib import AggregatedGame
from painfllib import StrategyLogisticRegression
from painfllib import StrategyNeuralNetwork

s = StrategyNeuralNetwork() #StrategyLogisticRegression()

db = nfldb.connect()
q = nfldb.Query(db)

q.game(season_year=2016, season_type='Regular', week=1)

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
