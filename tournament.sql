-- Table definitions for the tournament project.
--
-- tournament.sql
-- Erica Cheong
-- Date: 17 Jun 2015

DROP DATABASE tournament;

-- create database
CREATE DATABASE tournament;

\c tournament;

-- player table
CREATE TABLE players ( id serial PRIMARY KEY,
					   name text
					   );

-- match table
CREATE TABLE matches ( id serial PRIMARY KEY,
					   winner integer REFERENCES players (id),
					   loser integer REFERENCES players (id)
					   );

-- view 1: number of matches each player has played
CREATE VIEW match_count AS
	SELECT players.id, count(*)
	FROM matches, players
	WHERE players.id IN (winner, loser) 
	GROUP BY players.id;

-- view 2: number of wins for each player
CREATE VIEW win_count AS
	SELECT winner, count(*)
	FROM matches LEFT JOIN players
	ON matches.winner = players.id
	GROUP BY winner;

-- view 3: player standings
CREATE VIEW standings AS
	SELECT players.id, players.name, coalesce(win_count.count,0) AS wins, match_count.count AS match
	FROM players 
	LEFT JOIN win_count ON players.id = win_count.winner
	LEFT JOIN match_count ON players.id = match_count.id
	ORDER BY wins DESC;
