import random
import os
import subprocess

def play_music_randomly(language):
    path = f"music/{language}_song"
    music_files = os.listdir(path)

    for i in range(len(music_files)):
        filename = random.choice(music_files)
        music_files.remove(filename)
        print(filename)
        # os.system(f"mpg123 -q music/{language}_song/{filename}")
        p = subprocess.call(['mpg123', '-q', f"music/{language}_song/{filename}"])
