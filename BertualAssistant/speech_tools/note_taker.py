"""note_taker.py - A simple note-taking application.

This module provides a simple note-taking application. It allows the user to
create notes by speaking into the microphone. When the user is done speaking,
the note is saved to a file."""

import asyncio
from concurrent.futures import ProcessPoolExecutor

import speech_recognition as sr


async def convert_speech_to_text(recognizer: sr.Recognizer,
                                 audio: sr.AudioData) -> str:
    text = recognizer.recognize_whisper(audio, language='english', model='base.en')
    if not text:
        print('No audio detected')
    elif text.lower().count('okay') > 1:
        print('clicky microphone')
    else:
        return text
    return ''


# define an asynchronous generator
async def take_note(recognizer: sr.Recognizer):
    """Take a note from the user and return it as a string."""

    # Create an audio source object
    with sr.Microphone() as source:
        while 1:
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print('Speak now...')
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=30)
            except sr.WaitTimeoutError:
                continue
            print('Processing...')
            yield audio


# define a simple coroutine
async def custom_coroutine():
    # Create a recognizer object
    recognizer = sr.Recognizer()

    # asynchronous for loop
    async for audio in take_note(recognizer):
        # report the result

        note = await convert_speech_to_text(recognizer, audio)
        if not note:
            continue
        elif 'stop listening' in note.lower():
            print('Stopping...')
            break
        print(note)


loop = asyncio.get_event_loop()
p = ProcessPoolExecutor(12)  # Create a ProcessPool with 2 processes
loop.run_until_complete(custom_coroutine())
