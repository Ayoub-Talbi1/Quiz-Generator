# Quiz-Generator
Quiz Generator with Streamlit
# Quiz Generator

This is a simple application that generates quizzes based on audio recordings. It uses the OpenAI GPT-3.5 language model to transcribe the audio, generate quiz questions, and evaluate the user's answers.

## Features

- Record audio to provide the topic and number of questions for the quiz.
- Transcribe the audio using the Google Speech-to-Text API.
- Utilize the OpenAI GPT-3.5 model to generate quiz questions and options.
- Allow users to select answers for each question.
- Compute the score based on the user's answers and display the results.

## Technologies Used

- Python
- Streamlit: A Python framework for building interactive web applications.
- Sounddevice and Soundfile: Python libraries for recording and working with audio.
- SpeechRecognition: A library for performing speech recognition using various APIs.
- OpenAI GPT-3.5: A state-of-the-art language model for natural language processing tasks.

## Setup and Usage

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/quiz-generator.git
2. Install the required dependencies:
   - pip install -r requirements.txt
3. Set up your OpenAI API credentials:
   Sign up for an account at OpenAI (https://openai.com/).
   Obtain an API key.
   Replace API_KEY variable in the code with your API key.
4. Run the application:
   - streamlit run main.py
5. Click on the "Start Recording" button to begin the audio recording.
6. Speak the topic and number of questions for the quiz.
