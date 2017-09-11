import sqlite3
conn = sqlite3.connect('spoodify.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, name text, artist text, genre text, album text, length text, year smallint)')

def addSong():
    name = input("Enter song name: ")
    if name == "exit":
        conn.close()
    artist = input("Enter song artist: ")
    genre = input("Enter song genre: ")
    album = input("Enter song album: ")
    length = input("Enter song length: ")
    year = input("Enter song year: ")
    c.execute('INSERT INTO songs(name, artist, genre, album, length, year) VALUES(?,?,?,?,?,?)', (name, artist, genre, album, length, year))
    conn.commit()
    addSong()
    

addSong()
