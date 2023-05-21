# DeepLearningProject
Team Members:

Chaitra Bengaluru Vishweshwaraiah
Krishna Pranathi Mokshagundam

## Usage


Put the text you want to transcribe in input.txt, and run

python main.py --transcribe --play

You need to have both an OpenAI API key and an ElevenLabs API key. You will also need to create voices with labels used in the code such that they can be matched with the characters.

export OPENAI_API_KEY="your_openai_api_key_here"

export ELEVENLABS_API_KEY="your_elevenlabs_api_key_here"

The labels used in this project are {'sex': 'male/female', 'age': 'young/old', 'accent': 'british/american/irish/scottish/indian'}, but you can change these as you like.


You can set the narrator voice in main.py to any voice you like by giving it the voice_id.

## Options


The following options are available when running main.py:

--transcribe: Transcribes the input text and saves it to transcript.txt.
--play: Reads the transcribed text line by line using TTS.
--introduce: Provides a brief introduction of the characters using TTS.
