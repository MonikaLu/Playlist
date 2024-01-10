
# Ta inn hele csv og lese gjennom
# Sortere i alfabetisk rekkefølge

import pandas as pd

data = pd.read_csv('songNames.csv', sep='|')
sorted_data = data.sort_values(by=['Songs:'], ascending=True)

sorted_data.to_csv('sortedSongNames.csv', index=False, sep='|')