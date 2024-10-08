import speech_recognition as sr

def recognize_speech_from_mic():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the source for input
    with sr.Microphone() as source:
        # Adjust for ambient noise and record the audio
        recognizer.adjust_for_ambient_noise(source)
        print("Please speak into the microphone...")
        audio = recognizer.listen(source)

    try:
        if not audio:
            print("No audio detected")
            return
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError as e:
        print("Google Web Speech API could not understand the audio")
        print(e)
    except sr.RequestError as e:
        print("Could not request results from Google Web Speech API; {0}".format(e))

if __name__ == "__main__":
    recognize_speech_from_mic()