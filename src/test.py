import json
#
# with open('questions.json') as questionbank:
#     q = json.load(questionbank)
#     print(q)

x = {
  "easy":
    {
      "age": "How old are you?",
      "day": "How are you",
      "weather": "How was today's weather"
    },
  "medium": {
      "location": "Where are you?",
      "color": "What is your favorite color",
      "flower": "What is your favorite flower",
      "food": "What is your favorite food",
      "sport": "What is your favorite sport",
      "hobby": "What is your hobby",
      "season": "What is your favorite season",
      "hat": "What do you wear on your head"
    },
  "hard":
    {
      "thing": "What was the favorite thing you did today",
      "subject": "What subjects did you do at school?",
      "homework": "What homework do you have to do today?",
      "homework2": "Have you completed your homework?",
      "fork": "What do you do with a fork"
    }
}


# with open('questions.json', "w") as outfile:
#   json.dump(x, outfile, indent=1)
# print(x)

# print(x["easy"])

import random
def random_question(difficulty):
  with open('questions.json') as questionbank:
      q = json.load(questionbank)
  return random.choice(list(q[difficulty].values()))


print(random_question("easy"))


def speaker(text):
    text_to_audio(text)
    play_audio_file()