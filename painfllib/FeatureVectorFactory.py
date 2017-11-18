import nfldb
from AggregatedGame import AggregatedGame

db = nfldb.connect()

class FeatureVectorFactory:

    def get_last_game(self,game,team):
        last_game_home_team = []
        week = game.week
        year = game.season_year
        season_type = game.season_type

        while len(last_game_home_team) == 0 or AggregatedGame(last_game_home_team[0]).home_team_receiving() is None:
            if week == 1 and str(season_type) == "Regular":
                week = 4
                season_type = "Preseason"
            else:
                week -= 1
                if week <= 0: raise Exception("No more games in season")

            last_game_home_team = nfldb.Query(db).game(season_year=year,season_type=season_type,week=week,team=team).as_games()

        return last_game_home_team[0]


    # Feature vector for scheme 1 will give you a feature vector compromised of:
    # - Feature Vector from Home Teams last game
    # - Feature Vector from Away Teams last game
    def get_feature_vector_scheme1_for(self, game):
        last_game_home_team = self.get_last_game(game, game.home_team)
        last_game_away_team = self.get_last_game(game, game.away_team)

        feature_vector = [AggregatedGame(last_game_home_team).get_feature_vector_for(game.home_team), AggregatedGame(last_game_away_team).get_feature_vector_for(game.away_team)]

        # Flatten array and return
        return [item for subvector in feature_vector for item in subvector]

    # Feature vector for scheme 2 will give you a feature vector compromised of:
    # - Feature Vector from Home Teams 2 last games
    # - Feature Vector from Away Teams 2 last game
    def get_feature_vector_scheme2_for(self, game):
        last_game_home_team = self.get_last_game(game, game.home_team)
        second_last_game_home_team = self.get_last_game(last_game_home_team, game.home_team)
        last_game_away_team = self.get_last_game(game, game.away_team)
        second_last_game_away_team = self.get_last_game(last_game_away_team, game.away_team)

        feature_vector = [AggregatedGame(last_game_home_team).get_feature_vector_for(game.home_team), AggregatedGame(second_last_game_home_team).get_feature_vector_for(game.home_team), AggregatedGame(last_game_away_team).get_feature_vector_for(game.away_team), AggregatedGame(second_last_game_away_team).get_feature_vector_for(game.away_team)]

        # Flatten array and return
        return [item for subvector in feature_vector for item in subvector]


    # Feature vector for scheme 3 will give you a feature vector compromised of:
    # - Feature Vector from Home Teams 3 last games
    # - Feature Vector from Away Teams 3 last game
    def get_feature_vector_scheme3_for(self, game):

        feature_vector = []
        last_home_team_game = game
        for i in range(3):
            last_home_team_game = self.get_last_game(last_home_team_game, game.home_team)
            feature_vector.append(AggregatedGame(last_home_team_game).get_feature_vector_for(game.home_team))

        last_away_team_game = game
        for i in range(3):
            last_away_team_game = self.get_last_game(last_away_team_game, game.away_team)
            feature_vector.append(AggregatedGame(last_away_team_game).get_feature_vector_for(game.away_team))

        # Flatten array and return
        return [item for subvector in feature_vector for item in subvector]

    # Feature vector for scheme 4 will give you a feature vector compromised of:
    # - Feature Vector from Home Team last game
    # - Average performance from last 3 games before that or less if they didn't play 4 games yet this season (incl. preseason)
    # - Feature Vector from Away Team last game
    # - Average performance from last 3 games before that or less if they didn't play 4 games yet this season (incl. preseason)
    def get_feature_vector_scheme4_for(self, game):

        feature_vector = []
        last_home_team_game = self.get_last_game(game, game.home_team)
        feature_vector.append(AggregatedGame(last_home_team_game).get_feature_vector_for(game.home_team))

        summarized_features = [0,0,0,0,0,0,0,0]
        games = 0
        for i in range(3):
            try:
                last_home_team_game = self.get_last_game(last_home_team_game, game.home_team)
                fv = map(float,AggregatedGame(last_home_team_game).get_feature_vector_for_no_home_away(game.home_team))
                for n in range(8):
                    summarized_features[n] += fv[n]
                games += 1
            except:
                print "No more games in this season"

        for n in range(8):
            summarized_features[n] = round(summarized_features[n]/games,2)

        feature_vector.append(summarized_features)

        last_away_team_game = self.get_last_game(game, game.away_team)
        feature_vector.append(AggregatedGame(last_away_team_game).get_feature_vector_for(game.away_team))

        summarized_features = [0,0,0,0,0,0,0,0]
        games = 0
        for i in range(3):
            try:
                last_away_team_game = self.get_last_game(last_away_team_game, game.away_team)
                fv = map(float,AggregatedGame(last_away_team_game).get_feature_vector_for_no_home_away(game.away_team))
                for n in range(8):
                    summarized_features[n] += fv[n]
                games += 1
            except:
                print "No more games in this season"

        for n in range(8):
            summarized_features[n] = round(summarized_features[n]/games,2)

        feature_vector.append(summarized_features)

        # Flatten array and return
        return [item for subvector in feature_vector for item in subvector]

    # Feature vector for scheme 5 will give you a feature vector compromised of:
    # - Feature Vector from Home Team last game
    # - Average performance from last 4 games before that or less if they didn't play 4 games yet this season (incl. preseason)
    # - Feature Vector from Away Team last game
    # - Average performance from last 4 games before that or less if they didn't play 4 games yet this season (incl. preseason)
    def get_feature_vector_scheme5_for(self, game):

        feature_vector = []
        last_home_team_game = self.get_last_game(game, game.home_team)
        feature_vector.append(AggregatedGame(last_home_team_game).get_feature_vector_for(game.home_team))

        summarized_features = [0,0,0,0,0,0,0,0]
        games = 0
        for i in range(4):
            try:
                last_home_team_game = self.get_last_game(last_home_team_game, game.home_team)
                fv = map(float,AggregatedGame(last_home_team_game).get_feature_vector_for_no_home_away(game.home_team))
                for n in range(8):
                    summarized_features[n] += fv[n]
                games += 1
            except:
                print "No more games in this season"

        for n in range(8):
            summarized_features[n] = round(summarized_features[n]/games,2)

        feature_vector.append(summarized_features)

        last_away_team_game = self.get_last_game(game, game.away_team)
        feature_vector.append(AggregatedGame(last_away_team_game).get_feature_vector_for(game.away_team))

        summarized_features = [0,0,0,0,0,0,0,0]
        games = 0
        for i in range(4):
            try:
                last_away_team_game = self.get_last_game(last_away_team_game, game.away_team)
                fv = map(float,AggregatedGame(last_away_team_game).get_feature_vector_for_no_home_away(game.away_team))
                for n in range(8):
                    summarized_features[n] += fv[n]
                games += 1
            except:
                print "No more games in this season"

        for n in range(8):
            summarized_features[n] = round(summarized_features[n]/games,2)

        feature_vector.append(summarized_features)

        # Flatten array and return
        return [item for subvector in feature_vector for item in subvector]

    # Feature vector for scheme 5 will give you a feature vector compromised of:
    # - Feature Vector from Home Team last game
    # - Average performance from last 4 games before that or less if they didn't play 4 games yet this season (incl. preseason)
    # - Feature Vector from Away Team last game
    # - Average performance from last 4 games before that or less if they didn't play 4 games yet this season (incl. preseason)
    def get_feature_vector_scheme6_for(self, game):

        feature_vector = []
        last_home_team_game = self.get_last_game(game, game.home_team)
        feature_vector.append(AggregatedGame(last_home_team_game).get_feature_vector_ext_for(game.home_team))

        summarized_features = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        games = 0
        for i in range(4):
            try:
                last_home_team_game = self.get_last_game(last_home_team_game, game.home_team)
                fv = map(float,AggregatedGame(last_home_team_game).get_feature_vector_ext_for_no_home_away(game.home_team))
                for n in range(8):
                    summarized_features[n] += fv[n]
                games += 1
            except:
                print "No more games in this season"

        for n in range(8):
            summarized_features[n] = round(summarized_features[n]/games,2)

        feature_vector.append(summarized_features)

        last_away_team_game = self.get_last_game(game, game.away_team)
        feature_vector.append(AggregatedGame(last_away_team_game).get_feature_vector_ext_for(game.away_team))

        summarized_features = [0,0,0,0,0,0,0,0]
        games = 0
        for i in range(4):
            try:
                last_away_team_game = self.get_last_game(last_away_team_game, game.away_team)
                fv = map(float,AggregatedGame(last_away_team_game).get_feature_vector_ext_for_no_home_away(game.away_team))
                for n in range(8):
                    summarized_features[n] += fv[n]
                games += 1
            except:
                print "No more games in this season"

        for n in range(8):
            summarized_features[n] = round(summarized_features[n]/games,2)

        feature_vector.append(summarized_features)

        # Flatten array and return
        return [item for subvector in feature_vector for item in subvector]
