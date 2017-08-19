import sys
import nfldb
from painfllib import AggregatedGame
from painfllib import FeatureVectorFactory

import csv

db = nfldb.connect()
q = nfldb.Query(db)

X = []
y = []

fvf = FeatureVectorFactory()

# For every year in our database
for year in range(2009,2017):
    print "Processing year " + str(year)
    q = nfldb.Query(db)
    q.game(season_year=year, season_type='Regular').sort([('start_time', 'asc')])
    # For every game in that year
    for g in q.as_games():
        # Generate the feature vector and corresponding correct prediction
        X.append( fvf.get_feature_vector_scheme5_for(g) )
        y.append( AggregatedGame(g).winner() )

        sys.stdout.write("\r" + str(len(X)))
        sys.stdout.flush()

with open('data/scheme5_X.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(X)

with open('data/scheme5_y.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(y)
