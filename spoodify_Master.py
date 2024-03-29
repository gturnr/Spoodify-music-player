###
### Guy Turner - 2017 Spotify player project MIT license
### GitHub - https://github.com/guyturner797/
###

#3.1.1.2 Sequence
import sqlite3, getpass, os, time, ast, hashlib, musicPlayer
global currentuser

###DEBUG MODE - AUTOSIGNIN
debug = True #3.1.1.5 Boolean

#opens connection to server
global c, conn   #3.1.1.14 global variables
conn = sqlite3.connect('spoodify.db') #3.1.1.6 Variable
c = conn.cursor() #3.1.1.6 Variable

print("Spoodify - Music Streaming service")

#creates all three sql tables required if not already made - songs, users and playlists
c.execute('CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, name TEXT, artist TEXT, genre TEXT, album TEXT, length TEXT, year smallint, hits INT)')
c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, fullname TEXT, email TEXT, username TEXT, password TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY, name TEXT, username TEXT, songs TEXT)')
#apply changes to db
conn.commit()

#  logout function
def logout(): #3.1.1.10 subroutines - function
    #  confirms if the user wishes to sign out
    confirmation = input("Please confirm you want to logout(Y/N):") #3.1.1.1 String
    if confirmation.upper() == "Y": #3.1.1.2 Selection, #3.1.1.4 Relational, equal to
        #  writes to the log file that the user has signed out
        logfile = open("log.txt", "a") #  3.1.1.13 local variable
        logfile.write(time.strftime("%d/%m/%Y") + " | " + time.strftime("%H:%M:%S") + " - user " + currentuser + "signed out \n")
        logfile.close()
        cls()
        print("Logged out")
        #returns user to greeting login page
        greeting()
    elif confirmation.upper() == "N":
        #returns user to signed in menu
        cls()
        print("returning to menu...")
        menu()
    #if the input is invalid it reruns the function
    else:
        cls()
        print("Please enter either Y or N")
        logout()


#when running the program in terminal the screen would clear (commented out temporarily)       
def cls():  #3.1.1.10 subroutines - function
    #add linux & Mac OS support
    #os.system('cls')
    #os.system('clear')
    print(" ")


#function run when a search is completed and no results are found
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


#search song function
def searchSongs():
    cls()
    choice = input("Do you want to 1) search for song title, 2) search for artist, or 3) search for album? ")
    if choice == "1":
        #returns all results from the songs table where the song variable is the same as the the user input
        songName = input("Enter song name: ")
        c.execute("SELECT * FROM songs WHERE name=?", (songName,))
        results = c.fetchall()
        #runs if the sqlite command returns no data
        if len(results) == 0:
            noResults()
        #prints out all found song entries
        else:
            for row in results:
                print(row[1] + " - " + row[4] + " | " + row[2] + " | " +str(row[6])) #3.1.1.7 concatenate strings, string operations
            print(" ")


    #returns all results from the songs table where the artist variable is the same as the the user input
    elif choice == "2":
        artistName = input("Enter artist name: ")
        c.execute("SELECT * FROM songs WHERE artist=?", (artistName,))
        results = c.fetchall()
        #runs if the sqlite command returns no data
        if len(results) == 0:
            noResults()
        #prints out all found song entries
        else:
            for row in results:
                print(row[1] + " - " + row[4] + " | " + row[2] + " | " +str(row[6]))
            print(" ")


    #returns all results from the songs table where the album variable is the same as the the user input
    elif choice == "3":
        albumName = input("Enter album name: ")
        c.execute("SELECT * FROM songs WHERE album=?", (albumName,))
        results = c.fetchall()
        #runs if the sqlite command returns no data
        if len(results) == 0:
            noResults()
        #prints out all found song entries
        else:
            for row in results:
                print(row[1] + " - " + row[4] + " | " + row[2] + " | " +str(row[6]))
            print(" ")
    else:
        print("Invalid")
        searchSongs()
    menu()


#playlists function
def playlists():
    choice = input("Do you wish to 1) create a new playlist, 2) view all your playlists, 3) edit a playlist, or 4) return to menu? ")
    if choice == "1":
        #gets a user to create a  playlist
        print("Create a playlist:")
        def getPlaylistName():
            playlistname = input("Please enter a playlist name: ")
            #checks that the user didnt just hit enter or press space
            if playlistname == '':
                getPlaylistName()
            else:
                #gets all playlists names from the current user
                c.execute('SELECT name FROM playlists WHERE username =?', (currentuser,))
                currentplaylists = []
                #adds all current playlists from the user to a local list
                for row in c.fetchall():
                    currentplaylists.append(row[0])
                #checks if the chosen playlist name is already in the list
                if playlistname in currentplaylists:
                    print("A playlist with that name already exists.")
                    getPlaylistName()
                else:
                    return playlistname
            
        playlistname = getPlaylistName()
        print("Playlist successfully named " + str(playlistname))
        
        #gets all songs from the songs table
        c.execute('SELECT * FROM songs ORDER BY id')
        songs = c.fetchall()
        #prints out every song in the table, including the songs ID used for linking to the playlist table
        validIDs = []
        playlistSongs = []
        for row in songs:
            validIDs.append(row[0])
            print(str(row[0]) + ") " + row[1] + " - " + row[4] + " | " + row[2] + " | " +str(row[6]))
        print(" ")
        print("Please a song number and press enter. When you have entered every song you wish to add type 'done' and hit enter")


        def songSelector(): 
            song = input()
            if song == "done":
                pass
            else:
                #try - used in case the user enters a value that is not int
                try: #  3.1.1.9 exception handling
                    if int(song) in validIDs:
                        #checks if the song has already been added to the playlist
                        if song in playlistSongs:
                            print("you have already added this song to the playlist.")
                            songSelector()
                        #adds the song to the list and confirms the 'actual' song name to the user
                        else:
                            playlistSongs.append(song)
                            c.execute("SELECT name FROM songs WHERE id=?", (song,))
                            addedsong = c.fetchall()[0]
                            print("Added song - " + addedsong[0])
                            songSelector()
                    #error handling
                    else:
                        print("invalid entry. Please check the song number you entered and try again.")
                        songSelector()

                except:
                    print("invalid entry. Please check the song number you entered and try again.")
                    songSelector()
                
        songSelector()
        #checks if the list is empty (eg. the user added no songs)
        if not playlistSongs:
            print("No songs were selected. Please try again.")
            menu()

        else: 
            print("Here are the song numbers added to your playlist")
            print(playlistSongs)
            confirmation = input("Do you wish to save this playlist? (enter 'y' or 'n') ")
            if confirmation.upper() == "Y":
                #write to db
                c.execute('INSERT INTO playlists(name, username, songs) VALUES(?,?,?)', (playlistname, currentuser, str(playlistSongs)))
                conn.commit()
            else:
                print("Playlist not saved.")
                menu()
        
    elif choice == "2":
        print("Your playlists:")
        c.execute("SELECT * FROM playlists WHERE username=?", (currentuser,))
        userPlaylistNames = []
        for row in c.fetchall():
            userPlaylistNames.append(row[1])
            print(str(row[0]) + ") " + row[1])
            
        playlistChoice = input("Please enter the playlist name to view all songs: ")
        if playlistChoice in userPlaylistNames:
            c.execute("SELECT * FROM playlists WHERE name=? AND username=?", (playlistChoice, currentuser))
            playlistResult = c.fetchall()[0]
            print("")
            print("Playlist - " + playlistResult[1])
            #convert string output to list
            songs = playlistResult[3]
            songs = ast.literal_eval(songs)
            songs = [i.strip() for i in songs]
            print("")
            print("Songs:")
            print("")
            
            playlist = []

            for i in songs:
                c.execute("SELECT * FROM songs WHERE id=?", (i,))
                data = c.fetchall()[0]
                print(str(data[0]) + ") " + data[1] + " - " + data[4] + " | " + data[2] + " | " +str(data[6]))
                playlist.append(data[0])

            playPlaylist = input("Would you like to play all songs in the playlist? ")

            if playPlaylist.upper() == "YES":
                for songID in playlist:
                    musicPlayer.playSong(songID, c, conn) #  3.1.1.11 parameters of subroutines
                    
            menu()

        else:
            print("A playlist with that name could not be found on your account.")
            playlists()

    elif choice == "3":
        print("Edit a playlist:")
        c.execute("SELECT * FROM playlists WHERE username=?", (currentuser,))
        userPlaylistNames = []
        for row in c.fetchall():
            userPlaylistNames.append(row[1])
            print(str(row[0]) + ") " + row[1])
            
        playlistChoice = input("Please enter the name of the playlist you wish to edit: ")

        if playlistChoice in userPlaylistNames:
            c.execute("SELECT * FROM playlists WHERE name=? AND username=?", (playlistChoice, currentuser))
            playlistResult = c.fetchall()[0]
            #convert string output to list
            songs = playlistResult[3]
            songs = ast.literal_eval(songs)
            songs = [i.strip() for i in songs]
            print("")
            print("Songs:")

            playlist = []

            for i in songs:
                c.execute("SELECT * FROM songs WHERE id=?", (i,))
                data = c.fetchall()[0]
                print(str(data[0]) + ") " + data[1] + " - " + data[4] + " | " + data[2] + " | " +str(data[6]))
                playlist.append(data[0])

            print("")

        else:
            print("Please enter one of the above playlist names")
            playlists()


        def choiceSelection():
            choice = input("Would you like to 1) Remove a song, 2) Add a song, or 3) are you done? ")
            if choice == "1":
                songID = input("please enter the song number of the song you wish to remove: ")
                if songID in songs:
                    songs.remove(songID)
                    print(songs)

            elif choice == "2":
                c.execute('SELECT * FROM songs ORDER BY id')
                validSongs = c.fetchall()
                validIDs = []

                for row in validSongs:
                    validIDs.append(row[0])

                songToAdd = input("please enter the song number of the song you wish to add: ")
                try:
                    if int(songToAdd) in validIDs: #3.1.1.1 Int
                        if songToAdd not in songs:
                            c.execute("SELECT name FROM songs WHERE id=?", (int(songToAdd),))
                            songName = c.fetchall()[0]
                            print("Added song " + str(songName[0]))
                            songs.append(songToAdd)
                        else:
                            print("Song already in playlist")

                    else:
                        print("Please enter a valid song number.")

                except:
                    print("Please enter a valid song number")

            elif choice == "3":
                print(" ")
                print("New songs in playlist: ")
                if len(songs) == 0:
                    print("Cannot save a playlist with 0 songs. to delete a playlist please use the delete playlist option from the main menu.")
                    menu()
                else:
                    for i in songs:
                        c.execute("SELECT * FROM songs WHERE id=?", (i,))
                        data = c.fetchall()[0]
                        print(str(data[0]) + ") " + data[1] + " - " + data[4] + " | " + data[2] + " | " +str(data[6]))
                        playlist.append(data[0])

                    saveChoice = input("Would you like to update the playlist? ")
                    if saveChoice.upper() == "YES":
                        print("Saving to DB")
                        c.execute('UPDATE playlists SET songs = ? WHERE name = ?', (str(songs), playlistChoice))
                        conn.commit()
                        menu()

                    elif saveChoice.upper() == "NO":
                        print("Playlist edit cancelled. Returning to menu")
                        menu()

                    else:
                        print("please enter either yes or no.")

            choiceSelection()
        choiceSelection()

    elif choice == "4":
        pass
    
    else:
        print("Please select an option...")
        playlists()
	
def settings():
    print("Account options:")
    print("1) Change your password")
    print("2) Change your email")
    print("3) Return to main menu")
    choice = input()
    if choice == "1":
        usercheck = getpass.getpass("Please enter your current password: ")
        usercheck = "M4Zd" + usercheck + "2k9"
        h = hashlib.md5(usercheck.encode())
        usercheck =h.hexdigest()
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
        c.execute('SELECT * FROM songs ORDER BY id')
        songs = c.fetchall()
        songIDs = []
        for row in songs:
            print(str(row[0]) + ") " + row[1] + " - " + row[4] + " | " + row[2] + " | " +str(row[6]) + " | Hits: " + str(row[7]))
            songIDs.append(row[0])
        print(" ")
        choice = input("Would you like to play a song? ")
        if choice.upper() == 'YES':
            songNumber  = input("Please enter a song number to play: ")
            try:
                if int(songNumber) in songIDs:
                    musicPlayer.playSong(songNumber, c, conn)
                else:
                    print("Invalid song number")
            except:
                pass
        else:
            pass
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
    password = "M4Zd" + password + "2k9"
    h = hashlib.md5(password.encode())
    passwordHash =h.hexdigest()
    c.execute('SELECT username FROM users')
    currentusers = []
    for row in c.fetchall():
        currentusers.append(row[0])

    if username in currentusers:
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        searchResult = c.fetchall()
        validatePswd = searchResult[0]
        if passwordHash == validatePswd[0]:
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

    if len(password) < 8: #3.1.1.4 Relational, less than
        print("Your chosen password is too short")
        getPassword()
    else:
        i = 0
        valid = False
        while i < len(validsymbols):
            if validsymbols[i] in password:
                valid = True
            i += 1 #3.1.1.3 Arithmetic
        if valid == False:
            print(" Password does not contain a Symbol")
            getPassword()
        else:
            j = 0
            containsNumber = False
            while j< len(validnumbers): #3.1.1.2 Iteration
                if validnumbers[j] in password:
                    containsNumber = True
                j += 1 #3.1.1.3 Arithmetic
            if containsNumber == False:
                print(" Password does not contain a Number")
                getPassword()
            else:
                passwordcheck = getpass.getpass("Please re-enter your password: ")
                if password != passwordcheck:
                    print("Passwords do not match")
                    getPassword()
                else:
                    password = "M4Zd" + password + "2k9"
                    h = hashlib.md5(password.encode())
                    passwordHash =h.hexdigest()
                    return passwordHash


#gets user email, and valdiates it by ensuring it contains an '@', a '.' and that the email is not already assigned to a user
def getEmail():
        chosenemail = str(input("Please enter your chosen email: "))
        if '@' not in chosenemail or '.' not in chosenemail:
            print("Invalid email")
            getEmail()
        else:
            #gets all current emails in the users table, and checks if the new email is already stored in the table
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

    #gets username and validates it is unique against the db
    def getUsername():
        chosenusername = input("Please enter your chosen username: ")
        #gets all current usernames
        c.execute('SELECT username FROM users')
        currentusers = []
        #adds all current users to a local list
        for row in c.fetchall():
            currentusers.append(row[0])
        #checks if the chosen username is already in the list
        if chosenusername in currentusers:
            print("Username is taken")
            getUsername()    
        return chosenusername
    
    username = getUsername()
    password = getPassword()
    #creates a list containing the new users inputted data
    new_user = [name, email, username, password]
    #writes the user to the table
    c.execute('INSERT INTO users(fullname, email, username, password) VALUES(?,?,?,?)', (name, email, username, password))
    conn.commit()
    #assigns the new users username to the global current user variable
    currentuser = username
    #writes to the log file that a new user has been created
    logfile = open("log.txt", "a")
    logfile.write(time.strftime(time.strftime("%d/%m/%Y") + " | " + "%H:%M:%S") + " - user " + currentuser + "registered successfully \n")
    logfile.close()
    #takes the new user to the logged in menu
    menu()


#function ran on startup, sign in/sign up input
def greeting(): 
    loginchoice = str(input("Would you like to login (1) or sign up (2): "))
    if loginchoice == "1":
        login()
    elif loginchoice == "2":
        signup()
    else:
        cls()
        greeting()
if debug == True:
    currentuser = 'GuyTurner797'
    menu()
else:
    greeting()
#closes connection to db
conn.close()
