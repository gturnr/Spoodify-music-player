import pygame, spotipy, io
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.request import urlopen
from mutagen.mp3 import MP3

#read song to play
f = open('songLoader.txt', 'r')
song = f.read().rstrip()
f.close()
print(song)
songName, artistName = song.split(', ')

#initialize spotipy connection with Oauth
client_credentials_manager = SpotifyClientCredentials(client_id='8b1f86a793164a1e87f6ddc455a48b98', client_secret='82f524e32888446980ff8115236f9471')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#spotify get album url
results = sp.search(q=(songName + " " + artistName), limit=1)
albumUrl = results['tracks']['items'][0]['album']['images'][0]['url']
image_str = urlopen(albumUrl).read()
# create a file object (stream)
albumImage = io.BytesIO(image_str)

#initialize pygame and pygame music mixer
pygame.init()
pygame.mixer.init()

#define colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

#define window size
display_width = 600
display_height = 700

#define pygame window characteristics
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Music Player')
clock = pygame.time.Clock()

#images
albumCover = pygame.image.load(albumImage)
albumCover = pygame.transform.scale(albumCover, (600, 600))
volUp = pygame.image.load('images/volup.png')
volUp = pygame.transform.scale(volUp, (100, 100))
volDown = pygame.image.load('images/voldown.png')
volDown = pygame.transform.scale(volDown, (100, 100))
playPause = pygame.image.load('images/playpause.png')
playPause = pygame.transform.scale(playPause, (100, 100))

#load pygame mixer audio
songPath = 'music/' + songName + '.mp3'
mutagenData = MP3(songPath)
print('length - ' + str(round(mutagenData.info.length / 60, 2)))

pygame.mixer.music.load(songPath)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

#define gameDisplay layout
gameDisplay.fill(black)
pygame.draw.rect(gameDisplay, white, [0,600,600,100])
gameDisplay.blit(albumCover, (0,0))
gameDisplay.blit(volUp, (500,600))
gameDisplay.blit(volDown, (400,600))
gameDisplay.blit(playPause, (0,600))
pygame.display.update()

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

        #if button push then .....
    #pygame.display.update()

    clock.tick(20)


pygame.quit()
quit()
