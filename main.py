import streamlit as st
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import openai
import re

# Set up OpenAI API credentials
API_KEY = "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"
openai.api_key = API_KEY


def generate_quiz(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text = completion.choices[0].message.content
    quest = re.compile(r'^\d+(?:\)|\.|\-)(.+\?$)')
    opt = re.compile(r'^[a-zA-Z](?:\)|\.|\-)(.+$)')
    ans = re.compile(r'(Correct )?Answer:\s(\()?([a-zA-Z])\)?(?:\.|\-)?(.+)?$')
    questions = []
    options = []
    sub = []
    answers = []
    for line in text.splitlines():
        if line == '':
            if sub:
                options.append(sub)
                sub = []
        else:
            if quest.match(line):
                line_mod = line.strip()
                questions.append(line_mod)
            if opt.match(line):
                line_mod = line.strip()
                if len(options) < len(questions):
                    options.append([line_mod])
                else:
                    options[-1].append(line_mod)
            if ans.match(line):
                line_mod = line.strip()
                answers.append(ans.findall(line_mod)[0][-1])
    if sub:
        options.append(sub)

    return questions, options, answers, text


def main():
    st.title("Quiz Generator")
    st.write("Please Record The audio as follows 'make me a quiz about (your topic) of (number) questions and for each "
             "question (number) answers'")
    if st.button('Start Recording'):
        st.write('Recording...')

        # Start recording audio
        fs = 44100  # Sample rate
        seconds = 10  # Duration of recording
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished

        st.write('Recording finished!')
        st.write('Generating quiz...')

        # Save the recording to a temporary file
        with sf.SoundFile("temp.wav", mode="w", samplerate=fs, channels=1) as file:
            file.write(recording)

        # Transcribe audio to text
        recognizer = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        st.write('Transcription: ' + text)
        text = text + ' and under each question give the right answer'

        # Generate the quiz based on the transcription
        questions, options, answers, message = generate_quiz(text)
        # Display the quiz
        st.write('Quiz:')
        num_questions = len(questions)
        selected_answers = []
        with st.form("quiz_form"):
            for i, question in enumerate(questions):
                st.write(f' {question}')
                option_selected = st.radio(f"Select the correct answer for question {i + 1}", options[i])
                selected_answers.append(option_selected)
                st.write('')

            submitted = st.form_submit_button("Submit")

            if submitted:
                # Compare user answers with correct answers
                num_correct = sum([selected == answer for selected, answer in zip(selected_answers, answers)])
                score = num_correct / num_questions

                st.write(f'Your score: {num_correct}/{num_questions} ({score:.2%})')

                # Reset the form to display the score
                st.form_submit_button("Reset")

        st.write(answers)
        st.write('Quiz generation complete.')


if __name__ == "__main__":
    main()
