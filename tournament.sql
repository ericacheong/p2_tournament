-- Table definitions for the tournament project.
--
-- tournament.sql
-- Erica Cheong
-- Date: 17 Jun 2015

drop database tournament;

-- create database
create DATABASE tournament;

\c tournament;

-- player table
create TABLE players ( id serial primary key,
					   name text
					   );

-- match table
create TABLE matches ( id serial primary key,
					   p1 integer references players,
					   p2 integer references players,
					   winner integer references players
					   );

-- view 1: number of matches each player has playedß
create view match_count as
	select players.id, count(*)
	from matches, players
	where players.id in (p1, p2) 
	group by players.id;

-- view 2: number of wins for each player
create view win_count as
	select winner, count(*)
	from matches left join players
	on matches.winner = players.id
	group by winner;

-- view 3: player standings
create view standings as
	select players.id, players.name, coalesce(win_count.count,0) as wins, match_count.count as match
	from players 
	left join win_count on players.id = win_count.winner
	left join match_count on players.id = match_count.id
	order by wins desc;




