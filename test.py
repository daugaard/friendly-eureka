import nfldb

from painfllib import AggregatedGame
from painfllib import FeatureVectorFactory

db = nfldb.connect()
q = nfldb.Query(db)

fvf = FeatureVectorFactory()

q.game(season_year=2017, week=1, season_type="Preseason")

for g in q.as_games():
    ag = AggregatedGame(g)
    print g
    print ag.get_feature_vector_for(g.home_team)
    print ag.get_feature_vector_for(g.away_team)
