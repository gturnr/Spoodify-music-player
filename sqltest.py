'''
-features to add:
    email validation
    form validation


'''
import sqlite3, getpass, os, time
conn = sqlite3.connect('spoodify.db')
c = conn.cursor()

global currentuser

print("Spoodify - Music Streaming service")
print("songs in our collection: ")

#c.execute('''CREATE TABLE songs (name text, artist text, genre text, album text, length real, year smallint)''')
#c.execute("INSERT INTO songs VALUES ('Overjoyed','Bastille','Indie','Wild World',3.26, 2017)")
#c.execute('DELETE FROM songs Where name=Overjoyed')
c.execute('SELECT name FROM songs')
songs = c.fetchall()
print (songs)

conn.commit()

conn.close()

def cls():
    os.system('cls')

def menu():
    print("Please select the service you would like:")
    print("(1) View all songs available")
    print("(2) Search for a song")
    print("(3) Create/view/edit a playlist")
    option = input()

    if option == "1":
        pass
    elif option == "2":
        pass
    elif option == "3":
        pass
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
    name = input("Please enter your full name: ")
    email = input("Please enter your email: ")
    username = input("Please enter your chosen username: ")
    ##sql lookup
    password = getpass.getpass("Please enter your password: ")
    passwordcheck = getpass.getpass("Please re-enter your password: ")
    if password != passwordcheck:
        cls()
        print("Passwords do not match")
        signup()

    new_user = [name, email, username, password]
    print(new_user)
    time.sleep(10)
    
    

loginchoice = str(input("Would you like to login (1) or sign up (2): "))

if loginchoice == "1":
    login()

elif loginchoice == "2":
    signup()
