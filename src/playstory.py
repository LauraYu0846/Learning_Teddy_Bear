import random
import os

def play_story_randomly(language):
    path = f"story/{language}_story"
    story_files = os.listdir(path)

    for i in range(len(story_files)):
        filename = random.choice(story_files)
        story_files.remove(filename)
        os.system(f"mpg123 -q story/{language}_story/{filename}")


