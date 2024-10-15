# import a player
import pyaudio
import speech_recognition as sr

CHUNK = 1024


def get_audio_from_microphone(source: object,
                              recognizer: sr.Recognizer) -> sr.AudioData:
    # Use the microphone as the source for input
    with sr.Microphone(chunk_size=CHUNK) as source:
        # Adjust for ambient noise and record the audio
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Please speak into the microphone...")
        audio = recognizer.listen(source)#, timeout=5, phrase_time_limit=15)
        print("Got it! Now to recognize it...")
    return audio


def recognize_speech_from_mic(recognizer: sr.Recognizer,
                              microphone: sr.Microphone) -> None:
    audio = get_audio_from_microphone(microphone, recognizer)

    if not audio:
        print("No audio detected")
        return
    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError as e:
        print("Google Web Speech API could not understand the audio")
        print(e)
    except sr.RequestError as e:
        print("Could not request results from Google Web Speech API; {0}".format(e))

def playback_audio(player: pyaudio.PyAudio,
                   audio: sr.AudioData) -> None:
    # Instantiate PyAudio and initialize PortAudio system resources (1)


    # Open stream (2)
    stream = player.open(format=audio.sample_width,
                    channels=2,
                    rate=audio.sample_rate,
                    output=True)
    # Play samples from the wave file (3)
    while len(data := audio.get_segment(CHUNK).frame_data):  # Requires Python 3.8+ for :=
        print(data)
    stream.write(data)

    # Close stream (4)
    stream.close()

    # Release PortAudio system resources (5)
    player.terminate()


if __name__ == "__main__":
    test_player = pyaudio.PyAudio()
    test_recognizer = sr.Recognizer()
    test_microphone = sr.Microphone()
    audio = get_audio_from_microphone(test_microphone, test_recognizer)
    #print(test_recognizer.recognize_whisper(audio))
    print(test_recognizer.recognize_google(audio))
    #playback_audio(test_player, audio)
