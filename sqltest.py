import sqlite3, getpass, os, time

global currentuser

conn = sqlite3.connect('spoodify.db')
c = conn.cursor()

print("Spoodify - Music Streaming service")

c.execute('CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, name TEXT, artist TEXT, genre TEXT, album TEXT, length TEXT, year smallint)')
c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, fullname TEXT, email TEXT, username TEXT, password TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY, name TEXT, username TEXT, songs TEXT)')
conn.commit()

def logout():
    confirmation = input("Please confirm you want to logout(Y/N):")
    if confirmation.upper() == "Y":
        logfile = open("log.txt", "a")
        logfile.write(time.strftime("%d/%m/%Y") + " | " + time.strftime("%H:%M:%S") + " - user " + currentuser + "signed out \n")
        logfile.close()
        cls()
        print("Logged out")
        greeting()
    elif confirmation.upper() == "N":
        cls()
        print("returning to menu...")
        menu()
    else:
        cls()
        print("Please enter either Y or N")
        logout()
        
def cls():
    #add linux & Mac OS support
    #os.system('cls')
    #os.system('clear')
    print(" ")

def noResults():
    print(" ")
    print("Your search found no results! The search is case-sensitive.")
    choice = input("Would you like to 1) search again, or 2) go to the main menu? ")
    if choice == "1":
        searchSongs()
    elif choice == "2":
        menu()
    else:
        noResults()

def searchSongs():
    cls()
    choice = input("Do you want to 1) search for song title, 2) search for artist, or 3) search for album? ")
    if choice == "1":
        songName = input("Enter song name: ")
        c.execute("SELECT * FROM songs WHERE name=?", (songName,))
        results = c.fetchall()
        if len(results) == 0:
            noResults()
        else:
            for row in results:
                print(row[1] + " - " + row[4] + " | " + row[2] + " | " +str(row[6]))
            print(" ")

    elif choice == "2":
        artistName = input("Enter artist name: ")
        c.execute("SELECT * FROM songs WHERE artist=?", (artistName,))
        results = c.fetchall()
        if len(results) == 0:
            noResults()
        else:
            for row in results:
                print(row[1] + " - " + row[4] + " | " + row[2] + " | " +str(row[6]))
            print(" ")

    elif choice == "3":
        albumName = input("Enter album name: ")
        c.execute("SELECT * FROM songs WHERE album=?", (albumName,))
        results = c.fetchall()
        if len(results) == 0:
            noResults()
        else:
            for row in results:
                print(row[1] + " - " + row[4] + " | " + row[2] + " | " +str(row[6]))
            print(" ")
    else:
        print("Invalid")
        searchSongs()
    menu()

def playlists():
    choice = input("Do you wish to 1) create a new playlist, or 2) view all your playlists? ")
    if choice == "1":
        print("Create a playlist:")
        c.execute('SELECT * FROM songs ORDER BY id')
        songs = c.fetchall()
        for row in songs:
            print(row[0] + ") " + row[1] + " - " + row[4] + " | " + row[2] + " | " +str(row[6]))
        print(" ")
        print("Please a song number and press enter. When you have entered every song you wish to add type 'done' and hit enter")
        
        
    elif choice == "2":
        print("Your playlists:")
        c.execute("SELECT * FROM playlists WHERE username=?", (currentuser,))
        userPlaylistNames = []
        userPlaylistIDs = []
        for row in c.fetchall():
            userPlaylistNames.append(row[1])
            userPlaylistIDs.append(row[0])
            print(row[1])
        playlistChoice = input("Please enter the playlist name to view all songs: ")
        
    else:
        print("Please select an option...")
        playlists()
    menu()

def settings():
    print("Account options:")
    print("1) Change your password")
    print("2) Change your email")
    print("3) Return to main menu")
    choice = input()
    if choice == "1":
        usercheck = input("Please enter your current password: ")
        c.execute("SELECT password FROM users WHERE username=?", (currentuser,))
        currentPassword = c.fetchall()[0]
        if usercheck == currentPassword[0]:
            newpassword = getPassword()
            print("Savings changes...")
            c.execute('UPDATE users SET password = ? WHERE username = ?', (newpassword, currentuser))
            conn.commit()
            print("done")
        else:
            print("Incorrect password.")
            settings()
    elif choice == "2":
        newemail = getEmail()
        print("Savings changes...")
        c.execute('UPDATE users SET email = ? WHERE username = ?', (newemail, currentuser))
        conn.commit()
        print("done")
  
    elif choice == "3":
        cls()
        menu()
        
    else:
        print("Invalid input")
        settings()
    menu()

def menu():
    print(" ")
    print(currentuser + " - Please select the service you would like:")
    print("(1) View all songs available")
    print("(2) Search for a song")
    print("(3) Create/view/edit a playlist")
    print("(4) Account settings")
    print("(5) Logout")
    option = input()

    if option == "1":
        cls()
        print("songs in our collection: ")
        c.execute('SELECT * FROM songs ORDER BY artist')
        songs = c.fetchall()
        for row in songs:
            print(row[1] + " - " + row[4] + " | " + row[2] + " | " +str(row[6]))
        print(" ")
        menu()
    elif option == "2":
        searchSongs()
    elif option == "3":
        playlists()
    elif option == "4":
        settings()
    elif option == "5":
        logout()
    elif option == "exit":
        pass 
    else:
        menu()
        
def login():
    global currentuser
    username = input("Please enter your username: ")
    password = getpass.getpass("Please enter your password: ")
    c.execute('SELECT username FROM users')
    currentusers = []
    for row in c.fetchall():
        currentusers.append(row[0])

    if username in currentusers:
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        searchResult = c.fetchall()
        validatePswd = searchResult[0]
        if password == validatePswd[0]:
            currentuser = username
            logfile = open("log.txt", "a")
            logfile.write(time.strftime("%d/%m/%Y") + " | " + time.strftime("%H:%M:%S") + " - user " + currentuser + "signed in \n")
            logfile.close()
            menu()
        else:
            print("Invalid password")
            greeting()
    else:
        print("Invalid login, please try again or signup")
        greeting()
        

def getPassword():
    password = getpass.getpass("Please enter your chosen password, must contain a number, symbol and 8 characters: ")
    validsymbols = ['!','"','$','%','^','&','*','(',')','_','=','+','[','{','}',']',';',':','@','#',',','<','>','.','?','/']
    validnumbers = ['0','1','2','3','4','5','6','7','8','9']

    if len(password) < 8:
        print("Your chosen password is too short")
        getPassword()
    else:
        i = 0
        valid = False
        while i < len(validsymbols):
            if validsymbols[i] in password:
                valid = True
            i += 1
        if valid == False:
            print(" Password does not contain a Symbol")
            getPassword()
        else:
            j = 0
            containsNumber = False
            while j< len(validnumbers):
                if validnumbers[j] in password:
                    containsNumber = True
                j += 1
            if containsNumber == False:
                print(" Password does not contain a Number")
                getPassword()
            else:
                passwordcheck = getpass.getpass("Please re-enter your password: ")
                if password != passwordcheck:
                    print("Passwords do not match")
                    getPassword()
                else:
                    return password

def getEmail():
        chosenemail = str(input("Please enter your chosen email: "))
        if '@' not in chosenemail or '.' not in chosenemail:
            print("Invalid email")
            getEmail()

        else:
            c.execute('SELECT email FROM users')
            currentemails = []
            for row in c.fetchall():
                currentemails.append(row[0])

            if chosenemail in currentemails:
                print("An account with this email already exists")
                getEmail()
                    
            return chosenemail

def signup():
    global currentuser

    def getName():
        name = input("Please enter your full name: ")
        if " " not in name:
            print("Please enter your full name, including first and last name")
            getName()
        return name
    name = getName()
    
    email = getEmail()

    def getUsername():
        chosenusername = input("Please enter your chosen username: ")
        c.execute('SELECT username FROM users')
        currentusers = []
        for row in c.fetchall():
            currentusers.append(row[0])
        if chosenusername in currentusers:
            print("Username is taken")
            getUsername()    
        return chosenusername
    username = getUsername()
    ###
    password = getPassword()
    print(password)
    new_user = [name, email, username, password]
    c.execute('INSERT INTO users(fullname, email, username, password) VALUES(?,?,?,?)', (name, email, username, password))
    conn.commit()
    currentuser = username
    logfile = open("log.txt", "a")
    logfile.write(time.strftime(time.strftime("%d/%m/%Y") + " | " + "%H:%M:%S") + " - user " + currentuser + "registered successfully \n")
    logfile.close()
    menu()
    
def greeting(): 
    loginchoice = str(input("Would you like to login (1) or sign up (2): "))
    if loginchoice == "1":
        login()
    elif loginchoice == "2":
        signup()
    else:
        cls()
        greeting()

greeting()
conn.close()
