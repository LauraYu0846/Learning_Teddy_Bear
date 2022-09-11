# Learning_Teddy_Bear

Setup the virtual environment at Raspberry pi

1)	Download the code from the Section 1.5 Project link: GitHub repository or direct download code into SD code from laptop


2)	By default, Raspbian uses version 3 by default. In a terminal windown, enter the following command to check is the python version you wanted:

COPY CODEpython --version

3)	Pip need to be installed, if you are using the full desktop version of Raspbian, then pip already installed, otherwise, you need to install it with the commands by yourself:

COPY CODEsudo apt-get update
sudo apt-get install python3-pip


4)	Thonny is already installed on Raspberry Pi OS and created a .env file in the src folder and includes the environment variables for all the needed services:

Speech_To_Text:
STT_KEY= ///
STT_URL= ///

Text_To_Speech:
TTS_KEY= ///
TTS_URL= ///

Language_Translator:
LT_KEY= ///
LT_URL= ///

Watson_Assistant:
ASSISTANT_KEY= /// 
ASSISTANT_URL= /// 
ASSISTANT_ID= ///

5)	Before Running the main.py, open the terminal to run these two commands to install the pyaudio and mpg123 which will be used on the project.

Sudo apt-get install python3-pyaudio
Sudo apt install mpg123

6)	Before running the main.py, the requirements need to be installed by running:

Pip install -r requirements.txt

7)	Change the working directory to the src folder and running run_forever.py.
