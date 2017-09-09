'''
-features to add:
    email validation
    form validation


'''
import sqlite3, getpass, os, time

logfile = open("log.txt", "a")

conn = sqlite3.connect('spoodify.db')
c = conn.cursor()

global currentuser

print("Spoodify - Music Streaming service")

c.execute('CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, name text, artist text, genre text, album text, length real, year smallint)')
c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, fullname text, email text, username text, password text)')
#c.execute('''CREATE TABLE IF NOT EXISTS playlists (name text, artist text, genre text, album text, length real, year smallint)''')
#c.execute("INSERT INTO songs VALUES ('Overjoyed','Bastille','Indie','Wild World',3.26, 2017)"
# http://www.last.fm/api

conn.commit()

def logout():
    confirmation = input("Please confirm you want to logout(Y/N):")
    if confirmation.upper() == "Y":
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
    os.system('cls')

def menu():
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
    else:
        menu()
        
def login():
    global currentuser
    username = input("Please enter your username: ")
    password = getpass.getpass("Please enter your password: ")
    #validate
    currentuser = username
    menu()

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
    
    passwordcheck = getpass.getpass("Please re-enter your password: ")
    if password != passwordcheck:
        print("Passwords do not match")
        getPassword()

    #save to db
    new_user = [name, email, username, password]
    c.execute('INSERT INTO users(fullname, email, username, password) VALUES(?,?,?,?)', (name, email, username, password))
    conn.commit()

    currentuser = username
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
logfile.close()
conn.close()
