import os
import re

dir = 'music'
song_names_file = 'songNames.csv'
deviants_file = 'songNotFound.csv'

unused_words = ['audio', 'lyrics', '[FULL Audio]', 'MP3', '(lyrics)', '+', 'Audio', 'Lyrics', 'album', 'AUDIO', 'Album', 'mini', 'Mini']

def remove_chars_from_strings(text):
    pattern = r'[\[\]\(\)]'
    text = re.sub(pattern, '', text)
    for word in unused_words:
        if text.__contains__(word):
            text = text.replace(word, '')
    return text
        
def add_songs_to_csv():
    with open(song_names_file, 'w') as normal_names, open(deviants_file, 'w') as deviants:
        normal_names.write("Songs:" + '\n')
        deviants.write("Songs:" + '\n')
        for filename in os.listdir(dir):
            if remove_chars_from_strings(filename).endswith(".mp3") and filename.__contains__("-"):
                normal_names.write(remove_chars_from_strings(filename).replace('.mp3', '') + '\n')
            else:
                deviants.write(remove_chars_from_strings(filename).replace('.mp3', '') + '\n')
        normal_names.close()
        deviants.close()

add_songs_to_csv()