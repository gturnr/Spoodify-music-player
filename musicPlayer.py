import pygame, spotipy, io, urllib.request, time
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.mp3 import MP3

global volume
volume = 0.5

def playSong(songID, c, conn):
        global volume
        c.execute("SELECT * FROM songs WHERE id=?", (songID,))
        songLookup = c.fetchall()[0]
        songName = songLookup[1]
        artistName = songLookup[2]
        
        currentHits = songLookup[7]
        c.execute('UPDATE songs SET hits = ? WHERE name = ?', (currentHits + 1, songName,))
        print(currentHits + 1)
        conn.commit()

        #initialize pygame and pygame music mixer
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        #fonts
        font = pygame.font.SysFont('Arial', 30)
        boldfont = pygame.font.SysFont('Arial', 50)

        #define colours
        white = (255,255,255)
        black = (0,0,0)
        red = (255,0,0)

        #define window size
        display_width = 600
        display_height = 800

        #define pygame window characteristics
        gameDisplay = pygame.display.set_mode((display_width,display_height))

        pygame.display.set_caption('Music Player')
        clock = pygame.time.Clock()

        volUpImg = pygame.image.load('images/volup.png')
        volUpImg = pygame.transform.scale(volUpImg, (100, 100))
        volDownImg = pygame.image.load('images/voldown.png')
        volDownImg = pygame.transform.scale(volDownImg, (100, 100))
        playPauseImg = pygame.image.load('images/playpause.png')
        playPauseImg = pygame.transform.scale(playPauseImg, (100, 100))
        fastforwardImg = pygame.image.load('images/fastforward.png')
        fastforwardImg = pygame.transform.scale(fastforwardImg, (100, 100))
        rewindImg = pygame.image.load('images/rewind.png')
        rewindImg = pygame.transform.scale(rewindImg, (100, 100))

        song = songName  + ', ' + artistName

        filename = "images/albums/" + song + '.jpg'
        songPath = 'music/' + songName + '.mp3'

        try:
                f = open(filename, 'r')
                f.close()
                albumImage = filename
        except:
                #initialize spotipy connection with Oauth
                client_credentials_manager = SpotifyClientCredentials(client_id='8b1f86a793164a1e87f6ddc455a48b98', client_secret='82f524e32888446980ff8115236f9471')
                sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

                #spotify get album url
                results = sp.search(q=(songName + " " + artistName), limit=1)
                albumUrl = results['tracks']['items'][0]['album']['images'][0]['url']

                image = urllib.request.urlopen(albumUrl).read()
                f = open(filename,'wb')
                f.write(image)
                f.close()

                albumImage = filename
                
        #images
        albumCover = pygame.image.load(albumImage)
        albumCover = pygame.transform.scale(albumCover, (600, 600))

        #load pygame mixer audio
        mutagenData = MP3(songPath)
        songLength = mutagenData.info.length
        songLengthMinutes = round(songLength / 60, 2)

        pygame.mixer.music.load(songPath)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()

        global paused, lastpaused
        paused = False
        lastpaused = time.time()

        def volUp():
                global volume
                volume = pygame.mixer.music.get_volume()
                if volume < 1:
                        volume += 0.01
                        pygame.mixer.music.set_volume(volume)

        def volDown():
                global volume
                volume = pygame.mixer.music.get_volume()
                if volume > 0:
                        volume -= 0.01
                        pygame.mixer.music.set_volume(volume)

        def playPause():
                global paused, lastpaused
                currenttime = time.time()
                timeSpace = currenttime - lastpaused
                if timeSpace > 0.5: 
                        if paused == False:
                                print("Paused")
                                pygame.mixer.music.pause()
                                paused = True
            
                        elif paused == True:
                                print("Unpaused")
                                pygame.mixer.music.unpause()
                                paused = False
                                
                lastpaused = time.time()


        def fastForward():
                global counter
                pygame.mixer.music.set_pos(1)
                counter += 1/0.02
                counter -= 2.9
                
        def rewind():
                global counter
                pygame.mixer.music.rewind()
                counter = 0

        def button(x,y,img, funcName):
                gameDisplay.blit(img, (x,y))
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

                if x+100 > mouse[0] > x and y+100 > mouse[1] > y:
                        if click[0] == 1:
                                funcName()
                                
        global counter  
        gameExit = False
        counter = 0

        #current = time.time()
        while not gameExit:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                gameExit = True

                songTitle = boldfont.render(songName, True, black)
                artistTitle = boldfont.render(artistName, True, black)

                #define gameDisplay layout
                gameDisplay.fill(black)
                pygame.draw.rect(gameDisplay, white, [000,600,600,200])
                gameDisplay.blit(albumCover, (0,0))
    
                gameDisplay.blit(songTitle, ((display_width /2) - (songTitle.get_width() / 2), display_height - 200))
                gameDisplay.blit(artistTitle, ((display_width /2) - (artistTitle.get_width() / 2), display_height - 150))

                if paused == False:
                        counter += 2.9

                if pygame.mixer.music.get_busy() == False:
                        gameExit = True

                volumeStr = font.render(str(int(pygame.mixer.music.get_volume()*100)) + "%", True, black)

                if paused == True:
                        playback = 'Paused at ' + str(int(counter*0.02)) + 's'
                elif paused == False:
                        playback = str(int(counter*0.02)) + " / " + str(int(songLength)) + " s"
    
                playbackState = font.render(playback, True, black)

                gameDisplay.blit(volumeStr, ((display_width /2) - (volumeStr.get_width() / 2), display_height - 40))
                gameDisplay.blit(playbackState, ((display_width /2) - (playbackState.get_width() / 2), display_height - 80))

                button(470, 610, fastforwardImg, fastForward)
                button(30, 610, rewindImg, rewind)
                button(500, 700, volUpImg, volUp)
                button(400, 700, volDownImg, volDown)
                button(30, 700, playPauseImg, playPause)
                
                #print(time.time() - current)
                #current = time.time()
                pygame.display.update()
                #print(clock)
                clock.tick(20)

        pygame.quit()
