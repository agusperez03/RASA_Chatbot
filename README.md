Chatbot in Rasa

Installation
This repository is a chatbot developed in Rasa. It's about Netflix recomendations to see a serie or a movie (in Spanish).
If you dont have python 3.9.12, use a virtual enviroment as Anaconda, download and install it. Then you need Python, currently using version 3.9.12

Once you have both of them, get inside the terminal and create a virtual enviroment and excute, (without the ").

create --name "NameOfYourEnviroment" python="YourPythonVersion"
This command create the virtual enviroment, and everytime you want to get in the enviroment you must run the next command.

conda activate "NameOfYourEnviroment"
Once we are in the enviroment, we install the next dependencies, one at time.

conda install ujson
conda install tensorflow
pip install rasa
Now you are ready to pull the repository and in the terminal inside the virtual enviroment you can train it, and run it

Usage
Once you clone or pull the repository to your local, the you have to train it, so inside your terminal and inside the conda enviroment with rasa you run the next command

rasa train
when the train is finished, run the next commands for test it

rasa shell
After this command finish, in the terminal should appear a "type:" or something as this where you can insert your intention and talk to the chatbot.

Now you can talk with the bot in the command console! Try it!

Also the bot can be connected to Telegram.

To use it in Telegram, then you should do some modifications after the installation of rasa. Find where your virtual enviroment is installed, inside that directory go to
"PathOfYourEnvirment"/RASA/Lib/site-packages/rasa/core/channels/channel.py in windows and "PathOfYourEnvirment"/lib/python3.8/site-packages/rasa/core/channels in linux.
Then inside this python file search for the function "get_metadata()" and change the content to this

def get_metadata(self, request: Request) -> Optional[Dict[Text, Any]]:
       metadata = request.json
       return metadata

       
