-- Table definitions for the tournament project.
--
-- tournament.sql
-- Erica Cheong
-- Date: 17 Jun 2015


-- create database
create DATABASE tournament;

\c tournament;

-- player table
create TABLE players ( id serial primary key,
					   name text
					   );

-- match table
create TABLE matches ( p1 integer references players,
					   p2 integer references players,
					   winner integer references players
					   );

-- view 1: number of matches each player has played
create view match_count as 
	select p1, count(*) 
	from matches
	group by p1;

-- view 2: number of wins for each player
create view win_count as
	select winner, count(*)
	from matches
	group by p1;



-- view 3: player standings
create view standings as
	select players.id, players.name, win_count.count as wins, match_count.count as match
	from players 
	left join win_count on players.id = win_count.winner
	left join match_count on players.id = match_count.p1



