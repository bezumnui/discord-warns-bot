import sqlite3



def createTable(): #Создание таблицы
    con = sqlite3.connect("warns.db")
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS guild (player INT , reason TEXT, time INT)")
    con.commit()

def readWarns(player: int):
    createTable()
    con = sqlite3.connect("warns.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM guild WHERE player = {player}")
    return cur.fetchall()

def addWarn(player: int, reason: str, seconds: int):
    createTable()
    con = sqlite3.connect("warns.db")
    cur = con.cursor()
    cur.execute("INSERT INTO guild VALUES(?, ?, ?)", (player, reason, seconds))
    con.commit()
    return readWarns(player)

def delWarn(player: int, num: int):
    createTable()
    con = sqlite3.connect("warns.db")
    cur = con.cursor()
    reason = readWarns(player)[num - 1]
    cur.execute("DELETE FROM guild WHERE player = ? AND reason = '?'", (player, reason))
    con.commit()

def delWarnByReason(player: int, reason: int):
    createTable()
    con = sqlite3.connect("warns.db")
    cur = con.cursor()
    cur.execute("DELETE FROM guild WHERE player = ? AND reason = ?", (player, reason))
    con.commit()

def delWarns(player: int):
    createTable()
    con = sqlite3.connect("warns.db")
    cur = con.cursor()

    cur.execute("DELETE FROM guild WHERE player = ?", (player, ))
    con.commit()
