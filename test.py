import nfldb

from painfllib import AggregatedGame
from painfllib import FeatureVectorFactory

db = nfldb.connect()
q = nfldb.Query(db)


with nfldb.Tx(db) as cursor:
    cursor.execute("SELECT sum(%(attr)s) FROM play_player WHERE gsis_id = '%(gsis_id)s' AND team = '%(team)s'" % {"attr": "rushing_yds", "gsis_id": "2009081351", "team": "PHI"})
    for row in cursor.fetchall():
        print row["sum"]


q.game(season_year=2016, season_type='Regular', team='NYJ')
fvf = FeatureVectorFactory()
for g in q.as_games():

    ag = AggregatedGame(g)
    print ag.home_team_receiving(), ag.home_team_rushing(), ag.home_team_turnovers(), ag.away_team_receiving(), ag.away_team_rushing()

    at = []
    for attr in ["receiving_yds","rushing_yds","defense_int","defense_frec"]:
        with nfldb.Tx(db) as cursor:
            cursor.execute("SELECT sum(%(attr)s) FROM play_player WHERE gsis_id = '%(gsis_id)s' AND team = '%(team)s'" % {"attr": attr, "gsis_id": g.gsis_id, "team": g.home_team})
            for row in cursor.fetchall():
                at.append(row["sum"])


    print at
