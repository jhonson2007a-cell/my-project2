import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import sys

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set voice rate and volume (Optional configuration)
engine.setProperty('rate', 170)    # Speed of speech
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)


def speak(text):
    """Convert text to voice output and print it to the terminal."""
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()


def greet_user():
    """Greet the user based on the current time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning! I am JARVIS. How can I help you today?")
    elif 12 <= hour < 18:
        speak("Good Afternoon! I am JARVIS. How can I help you today?")
    else:
        speak("Good Evening! I am JARVIS. How can I help you today?")


def listen_command():
    """Listen for audio input from the microphone and return it as text."""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n[+] Listening...")
        # Adjust for ambient noise to improve accuracy
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try speaking again.")
            return "none"

    try:
        print("[+] Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {command}\n")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand what you said. Could you please repeat?")
        return "none"
    except sr.RequestError:
        speak("Network error. Please check your internet connection.")
        return "none"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "none"
        
    return command.lower()


def process_command(command):
    """Execute actions based on the recognized command."""
    if "open google" in command:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    elif "wikipedia" in command:
        speak("Searching Wikipedia...")
        # Remove the trigger word "wikipedia" from the query
        query = command.replace("wikipedia", "").strip()
        
        if query == "":
            speak("What would you like me to search on Wikipedia?")
            query = listen_command()
            
        if query != "none":
            try:
                # Fetch a 2-sentence summary from Wikipedia
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                speak(results)
            except wikipedia.DisambiguationError:
                speak("There were multiple matches. Please be more specific.")
            except wikipedia.PageError:
                speak("Sorry, I could not find any matching page on Wikipedia.")
            except Exception as e:
                speak("Failed to fetch information from Wikipedia.")

    elif any(exit_word in command for exit_word in ["exit", "stop", "quit", "bye"]):
        speak("Goodbye! Have a great day ahead.")
        sys.exit()

    else:
        speak("I am not sure how to handle that command yet. Try asking for time, Wikipedia, Google, or YouTube.")


def main():
    """Main loop to run the JARVIS assistant."""
    greet_user()
    while True:
        command = listen_command()
        if command != "none":
            process_command(command)


if __name__ == "__main__":
    main()
