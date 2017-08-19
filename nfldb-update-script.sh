psql -U nfldb nfldb -c "INSERT into team values('JAX','Jacksonville', 'Jaguars');"
nfldb-update
psql -U nfldb nfldb -c "UPDATE play SET pos_team = 'JAC' WHERE pos_team = 'JAX';"
psql -U nfldb nfldb -c "DELETE FROM team WHERE team_id = 'JAX';"
