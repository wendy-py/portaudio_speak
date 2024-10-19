import speech_recognition as sr
import tkinter as tk
import random

NUM_GUESSES = 3
PROMPT_LIMIT = 5
RED = "crimson"
GREEN = "darkgreen"
YELLOW = "lightyellow"
FONT_NAME = "Courier"

recognizer = sr.Recognizer()
microphone = sr.Microphone()
if random.randint(0, 99) % 2:
    WORDS = ["black", "white", "red", "fuchsia", "lime", "yellow", "blue", "aqua"]
else:
    WORDS = ["gray", "silver", "maroon", "purple", "green", "olive", "navy", "teal"]

def speech_from_mic():
    """Transcribe speech from `microphone`.
        Returns a dictionary with three keys:
        "success": a boolean indicating if API request is successful.
        "error":   `None` if no error, otherwise a string containing the error.
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer for ambient noise and record audio from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # initialise the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try to recognize the speech in the recording
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def game():
    # computer picks a word
    word = random.choice(WORDS)
    instructions = (
        "I'm thinking of one of these words:\n"
        "{words}\n"
        "You have {n} tries to guess which one.\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)
    print(instructions)

    for i in range(NUM_GUESSES):
        # get the guess from the user
        # if transcription returned, break out of the loop and continue
        # if no transcription and API request failed, break for error handling
        # if API request succeeded but no transcription was returned, re-prompt
        for j in range(PROMPT_LIMIT):
            print('Guess {}. Speak!'.format(i + 1))
            guess = speech_from_mic()
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there is an error, print error and the game
        if guess["error"]:
            prompt.config(text="ERROR: {}".format(guess["error"]))
            print("ERROR: {}".format(guess["error"]))
            break

        print("You said: {}".format(guess["transcription"]))

        guess_correct = guess["transcription"].lower() == word.lower()
        more_attempts = i < NUM_GUESSES - 1

        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no more_attempts left, the user loses the game
        if guess_correct:
            prompt.config(text="Correct! You win!", fg=GREEN)
            print("Correct! You win!")
            break
        elif more_attempts:
            text = ""
            for _ in range(NUM_GUESSES - 1 - i):
                text += "🕙"
            lives.config(text=text)
            print("Incorrect. Try again.\n")
        else:
            prompt.config(text="Sorry, you lose!\nI was thinking of '{}'.".format(word))
            print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
            break
    window.after(60000)
    window.quit()


window = tk.Tk()
window.title("Speak!")
window.config(padx=20, pady=20, bg=YELLOW)

canvas = tk.Canvas(width=200, height=200, bg=YELLOW, highlightthickness=0)
img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

choices = tk.Label(text=f'Speak among: {WORDS}', bg=YELLOW, fg=GREEN, font=(FONT_NAME, 14, "bold"))
choices.grid(row=1, column=1)
prompt = tk.Label(text='Speak!', bg=YELLOW, fg=GREEN, font=(FONT_NAME, 12))
prompt.grid(row=2, column=1)
lives = tk.Label(text="🕙🕙🕙", bg=YELLOW, fg=RED, font=(FONT_NAME, 35))
lives.grid(row=3, column=1)

window.after(1000, game)

window.mainloop()
