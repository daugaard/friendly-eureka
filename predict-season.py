# Force floating point division
from __future__ import division

import nfldb
from painfllib import AggregatedGame
from painfllib import StrategyLogisticRegression
from painfllib import StrategyNeuralNetwork

db = nfldb.connect()
q = nfldb.Query(db)

s = StrategyNeuralNetwork()

def tally_predictions(predictions):
    total = 0
    correct = 0
    # predictions contains an array with [prediction, actual]
    for p in predictions:
        total += 1
        if p[0] == p[1]:
            correct += 1

    print "Correct predictions " + str(correct) + " of " + str(total) + " prediction rate: " + str(round((correct/total)*100,2)) + "%"

week = 0
all_predictions = []
weekly_predictions = []

for y in range(2016,2017):
    q = nfldb.Query(db)
    q.game(season_year=y, season_type='Regular').sort([('start_time', 'asc')])
    for g in q.as_games():
        # Check if new week started if so tally up predictions for that week
        if week != g.week:
            week = g.week
            if len(weekly_predictions) > 0:
                tally_predictions(weekly_predictions)
                weekly_predictions = []

            print "Predicting week " + str(week) + " of " + str(y)

        # Make prediction
        p = s.predict(g)

        all_predictions.append([p, AggregatedGame(g).winner()])
        weekly_predictions.append([p, AggregatedGame(g).winner()])
    print "Year " + str(y)
    tally_predictions(all_predictions)

print "Total score"
tally_predictions(all_predictions)
