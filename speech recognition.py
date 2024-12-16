import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import os

# Initialize recognizer and translator
r = sr.Recognizer()
translator = Translator()

# Function to expand common abbreviations
def expand_abbreviations(text):
    text = text.replace("r u", "are you")
    return text

# Function to choose the target language
def get_language_choice():
    print("Choose the target language:")
    print("1. French")
    print("2. Hindi")
    print("3. Spanish")
    print("4. German")
    print("5. Japanese")
    print("6. Korean")
    print("7. Marathi")
    print("8. Gujarati")
    print("9. Bengali")
    choice = input("Enter the number of your choice (1-9): ")
    
    if choice == '1':
        return 'fr', 'French'
    elif choice == '2':
        return 'hi', 'Hindi'
    elif choice == '3':
        return 'es', 'Spanish'
    elif choice == '4':
        return 'de', 'German'
    elif choice == '5':
        return 'ja', 'Japanese'
    elif choice == '6':
        return 'ko', 'Korean'
    elif choice == '7':
        return 'mr', 'Marathi'
    elif choice == '8':
        return 'gu', 'Gujarati'
    elif choice == '9':
        return 'bn', 'Bengali'
    else:
        print("Invalid choice, defaulting to French.")
        return 'fr', 'French'

# Get language choice
lang_code, lang_name = get_language_choice()
print(f"Translating to {lang_name} ({lang_code})")

while True:
    with sr.Microphone() as source:
        # Adjust for ambient noise to improve recognition for long speeches
        r.adjust_for_ambient_noise(source)
        print("Speak your paragraph now (or say 'exit' to quit):")
        
        # Listen for the entire paragraph until silence is detected
        audio = r.listen(source, phrase_time_limit=None)  # Remove time limit for continuous listening

        try:
            # Speech recognition using Google Speech Recognition
            speech_text = r.recognize_google(audio)
            print("You said:", speech_text)

            # Break the loop if "exit" is spoken
            if "exit" in speech_text.lower():
                break
        except sr.UnknownValueError:
            print("Could not understand")
            continue
        except sr.RequestError:
            print("Could not request result from Google Speech Recognition service.")
            continue

        # Expand abbreviations
        expanded_text = expand_abbreviations(speech_text)
        print("Expanded text:", expanded_text)

        # Translate the recognized speech to the chosen language
        translated_text = translator.translate(expanded_text, dest=lang_code).text
        print(f"Translated text ({lang_name}):", translated_text)

        # Use gTTS to convert the translated text to speech in the chosen language
        voice = gTTS(text=translated_text, lang=lang_code)
        voice.save("voice.mp3")
        playsound("voice.mp3")

        # Remove the temporary voice file
        os.remove("voice.mp3")
