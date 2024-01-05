import os

dir = 'music'
song_names_file = 'songNames.csv'

with open(song_names_file, 'w') as file:
    file.write('Songs:' + '\n')
    for filename in os.listdir(dir):
        if filename.endswith(".mp3"):
            file.write(filename.replace('.mp3', '') + '\n')

with open("songNotFound.csv", 'w') as file:
    file.write('Songs:' + '\n')
    file.close()