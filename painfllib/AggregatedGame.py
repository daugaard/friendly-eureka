import nfldb

db = nfldb.connect()

class AggregatedGame:
    def __init__(self, game):
        self.game = game

    def get_aggregated_attribute_for(self, attribute, team):
        agg_attr = 0
        with nfldb.Tx(db) as cursor:
            q = "SELECT sum(%(attr)s) FROM play_player WHERE gsis_id = '%(gsis_id)s' AND team = '%(team)s'" % {"attr": attribute, "gsis_id": self.game.gsis_id, "team": team}
            cursor.execute(q)
            for row in cursor.fetchall():
                agg_attr = row["sum"]

            # Special handling for some of the LA and LAC games where they are listed as UNK
            if agg_attr is None:
                q = "SELECT sum(%(attr)s) FROM play_player WHERE gsis_id = '%(gsis_id)s' AND team = '%(team)s'" % {"attr": attribute, "gsis_id": self.game.gsis_id, "team": "UNK"}
                cursor.execute(q)
                for row in cursor.fetchall():
                    agg_attr = row["sum"]

        return agg_attr

    def home_team(self):
        return self.game.home_team

    def home_team_receiving(self):
        return self.get_aggregated_attribute_for('receiving_yds', self.game.home_team)

    def home_team_rushing(self):
        return self.get_aggregated_attribute_for('rushing_yds', self.game.home_team)

    def home_team_defence_tackles(self):
        return self.get_aggregated_attribute_for('defense_tkl', self.game.home_team)

    def home_team_defence_forced_fumble(self):
        return self.get_aggregated_attribute_for('defense_ffum', self.game.home_team)

    def home_team_defence_sacks(self):
        return self.get_aggregated_attribute_for('defense_sk', self.game.home_team)

    def home_team_turnovers(self):
        return self.get_aggregated_attribute_for('defense_int', self.game.away_team) +  self.get_aggregated_attribute_for('defense_frec', self.game.away_team)

    def home_team_score(self):
        return self.game.home_score

    def away_team(self):
        return self.game.away_team

    def away_team_receiving(self):
        return self.get_aggregated_attribute_for('receiving_yds', self.game.away_team)

    def away_team_rushing(self):
        return self.get_aggregated_attribute_for('rushing_yds', self.game.away_team)

    def away_team_turnovers(self):
        return self.get_aggregated_attribute_for('defense_int', self.game.home_team) +  self.get_aggregated_attribute_for('defense_frec', self.game.home_team)

    def away_team_defence_tackles(self):
        return self.get_aggregated_attribute_for('defense_tkl', self.game.away_team)

    def away_team_defence_forced_fumble(self):
        return self.get_aggregated_attribute_for('defense_ffum', self.game.away_team)

    def away_team_defence_sacks(self):
        return self.get_aggregated_attribute_for('defense_sk', self.game.away_team)

    def away_team_score(self):
        return self.game.away_score

    def winner(self):
        # - home/away (1 = home or 0 = away)
        if self.game.home_score > self.game.away_score:
            return 1
        else:
            return 0

    def get_feature_vector_for(self, team):
        # Feature vector has format:
        # - home/away (1 = home or 0 = away)
        # - Team Score
        # - Team Receiving
        # - Team Rushing
        # - Team Turnovers
        # - Other Team Score
        # - Other Team Receiving
        # - Other Team Rushing
        # - Other Team Turnovers
        if team == self.game.home_team:
            return [1, self.home_team_score(), self.home_team_receiving(), self.home_team_rushing(), self.home_team_turnovers(), self.away_team_score(), self.away_team_receiving(), self.away_team_rushing(), self.away_team_turnovers()]
        elif team == self.game.away_team:
            return [0, self.away_team_score(), self.away_team_receiving(), self.away_team_rushing(), self.away_team_turnovers(), self.home_team_score(), self.home_team_receiving(), self.home_team_rushing(), self.home_team_turnovers()]
        else:
            raise Exception("Team is not playing in this game.")

    def get_feature_vector_ext_for(self, team):
        # Feature vector has format:
        # - home/away (1 = home or 0 = away)
        # - Team Score
        # - Team Receiving
        # - Team Rushing
        # - Team Turnovers
        # - Team Defence Tackles
        # - Team Defence forced fumbles
        # - Team Defence Sacks
        # - Other Team Score
        # - Other Team Receiving
        # - Other Team Rushing
        # - Other Team Turnovers
        # - Other Team Defence Tackles
        # - Other Team Defence forced fumbles
        # - Other Team Defence Sacks
        if team == self.game.home_team:
            return [1, self.home_team_score(), self.home_team_receiving(), self.home_team_rushing(), self.home_team_turnovers(), self.home_team_defence_tackles(),  self.home_team_defence_forced_fumble(),  self.home_team_defence_sacks(), self.away_team_score(), self.away_team_receiving(), self.away_team_rushing(), self.away_team_turnovers(), self.away_team_defence_tackles(),  self.away_team_defence_forced_fumble(),  self.away_team_defence_sacks()]
        elif team == self.game.away_team:
            return [0, self.away_team_score(), self.away_team_receiving(), self.away_team_rushing(), self.away_team_turnovers(), self.away_team_defence_tackles(),  self.away_team_defence_forced_fumble(),  self.away_team_defence_sacks(), self.home_team_score(), self.home_team_receiving(), self.home_team_rushing(), self.home_team_turnovers(),  self.home_team_defence_tackles(), self.home_team_defence_forced_fumble(),  self.home_team_defence_sacks()]
        else:
            raise Exception("Team is not playing in this game.")

    def get_feature_vector_for_no_home_away(self, team):
        # Feature vector has format:
        # - Team Score
        # - Team Receiving
        # - Team Rushing
        # - Team Turnovers
        # - Other Team Score
        # - Other Team Receiving
        # - Other Team Rushing
        # - Other Team Turnovers
        if team == self.game.home_team:
            return [self.home_team_score(), self.home_team_receiving(), self.home_team_rushing(), self.home_team_turnovers(), self.away_team_score(), self.away_team_receiving(), self.away_team_rushing(), self.away_team_turnovers()]
        elif team == self.game.away_team:
            return [self.away_team_score(), self.away_team_receiving(), self.away_team_rushing(), self.away_team_turnovers(), self.home_team_score(), self.home_team_receiving(), self.home_team_rushing(), self.home_team_turnovers()]
        else:
            raise Exception("Team is not playing in this game.")

    def get_feature_vector_ext_for_no_home_away(self, team):
        # Feature vector has format:
        # - home/away (1 = home or 0 = away)
        # - Team Score
        # - Team Receiving
        # - Team Rushing
        # - Team Turnovers
        # - Team Defence Tackles
        # - Team Defence forced fumbles
        # - Team Defence Sacks
        # - Other Team Score
        # - Other Team Receiving
        # - Other Team Rushing
        # - Other Team Turnovers
        # - Other Team Defence Tackles
        # - Other Team Defence forced fumbles
        # - Other Team Defence Sacks
        if team == self.game.home_team:
            return [self.home_team_score(), self.home_team_receiving(), self.home_team_rushing(), self.home_team_turnovers(), self.home_team_defence_tackles(),  self.home_team_defence_forced_fumble(),  self.home_team_defence_sacks(), self.away_team_score(), self.away_team_receiving(), self.away_team_rushing(), self.away_team_turnovers(), self.away_team_defence_tackles(),  self.away_team_defence_forced_fumble(),  self.away_team_defence_sacks()]
        elif team == self.game.away_team:
            return [self.away_team_score(), self.away_team_receiving(), self.away_team_rushing(), self.away_team_turnovers(), self.away_team_defence_tackles(),  self.away_team_defence_forced_fumble(),  self.away_team_defence_sacks(), self.home_team_score(), self.home_team_receiving(), self.home_team_rushing(), self.home_team_turnovers(),  self.home_team_defence_tackles(), self.home_team_defence_forced_fumble(),  self.home_team_defence_sacks()]
        else:
            raise Exception("Team is not playing in this game.")

# Old slow implementation of get_aggregated_attribute_for
#q = nfldb.Query(db)
#q.game(gsis_id=self.game.gsis_id).play(pos_team=team)
#agg_attr = 0
#for p in q.sort(attribute).as_aggregate():
#    agg_attr += getattr(p,attribute)
