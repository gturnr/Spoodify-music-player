import sqlite3, getpass, os, time

global currentuser

conn = sqlite3.connect('spoodify.db')
c = conn.cursor()

print("Spoodify - Music Streaming service")

c.execute('CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, name text, artist text, genre text, album text, length real, year smallint)')
c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, fullname text, email text, username text, password text)')
# http://www.last.fm/api

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
    os.system('cls')

def menu():
    #give function to options 2,3
    print("Welcome " + currentuser)
    print("Please select the service you would like:")
    print("(1) View all songs available")
    print("(2) Search for a song")
    print("(3) Create/view/edit a playlist")
    print("(4) Logout")
    option = input()

    if option == "1":
        print("songs in our collection: ")
        c.execute('SELECT * FROM songs')
        songs = c.fetchall()
        print (songs)
        menu()
    elif option == "2":
        print("Search")
        menu()
    elif option == "3":
        print("Playlists")
        menu()
    elif option == "4":
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
        

def signup():
    global currentuser

    def getName():
        name = input("Please enter your full name: ")
        if " " not in name:
            print("Please enter your full name, including first and last name")
            getName()
        return name
    
    name = getName()

    def getEmail():
        chosenemail = str(input("Please enter your email: "))
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

    def getPassword():
        password = getpass.getpass("Please enter your chosen password, at leat 8 letters long and containing a symbol: ")
        validsymbols = ['!','"','£','$','%','^','&','*','(',')','_','=','+','[','{','}',']',';',':','@','#',',','<','>','.','?','/']

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
                return password
    
    password = getPassword()

    def validatePassword(password):
        passwordcheck = getpass.getpass("Please re-enter your password: ")
        if password != passwordcheck:
            print("Passwords do not match")
            getPassword()
            validatePassword()
            
    validatePassword(password)

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
