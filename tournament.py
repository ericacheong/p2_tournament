#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# Date: 17 Jun 2015

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Cannot connect to database")

def dbquery(query, params=None):
    '''Query the PostgreSQL database. Returns result set if available 
    to the query.
    '''
    results = None
    conn, cur = connect()
    if params:
        try:
            cur.execute( query, params )
        except psycopg2.ProgrammingError as err:
            print err.pgerror
    else:
        try:
            cur.execute( query )
        except psycopg2.ProgrammingError as err:
            print err.pgerror

    try:
        results = cur.fetchall()
    except psycopg2.ProgrammingError:
        pass

    conn.commit()
    conn.close()
    if results:
        return results



def deleteMatches():
    """Remove all the match records from the database."""
    dbquery("DELETE FROM matches;")

def deletePlayers():
    """Remove all the player records from the database."""
    dbquery("DELETE FROM players;")


def countPlayers():
    """Returns the number of players currently registered."""
    result = dbquery("SELECT count(*) FROM players;")
    return result[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    dbquery("INSERT INTO players (name) VALUES (%s)", (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # conn = connect()
    # c = conn.cursor()
    # c.execute("select * from standings order by wins;")
    # result = c.fetchall()
    # conn.close()

    result = dbquery("SELECT * FROM standings ORDER BY wins;")

    # Change None value to 0
    f_result = []
    for (id, name, win, match) in result:
        if win == None:
            win = 0
        if match == None:
            match = 0
        i = id, name, win, match
        f_result.append(i)

    return f_result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    dbquery("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser))
 

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = dbquery("SELECT * FROM standings")

    #print standings
    pair = []
    swisspair = []
    #print standings
    for p in standings:
        (i, n, w, m) = p
        if len(pair) < 4:
            pair += i, n
        else:
            swisspair.append(pair)
            pair = i,n

    # check if the final pair is odd or even
    if len(pair) < 4:
        pair += 999, 'bye'
    swisspair.append(pair)
    return swisspair