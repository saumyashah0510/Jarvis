import speech_recognition as sr # shortcut for speech_recognition set to sr
import webbrowser #open web bprwser to search
import pyttsx3 #text to speech help
import music_library
import requests

from groq import Groq

recognizer = sr.Recognizer()
engine = pyttsx3.init() #initializes pyttsx3
news_API = "a8c4f635e8a84582b95485c6ae26b524"

# text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def ai_process(command):
    client = Groq(api_key="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")
    
    response = client.chat.completions.create(
    model="llama3-70b-8192",  # Or "mixtral-8x7b-32768"
    messages=[
        {
            "role": "system",
            "content": "You are Jarvis, a helpful AI assistant like Alexa. Be concise and response in 3-4 sentences max"
        },
        {
            "role": "user",
            "content": command
        }
    ],
    temperature=0.3  # Controls creativity (0-1)
    )
    return response.choices[0].message.content

def processCommand(c):
    c_lower = c.lower()  # Convert to lowercase once for efficiency
    
    # Check for exit command FIRST
    if "power off" in c_lower or "goodbye" in c_lower:
        speak("Goodbye boss. Shutting down.")
        return True  # Signal to exit the loop
    
    # Other commands
    elif "open google" in c_lower:
        webbrowser.open("https://google.com")
    elif "open youtube" in c_lower:
        webbrowser.open("https://youtube.com")   
    elif c_lower.startswith("play"):
        song = c_lower.replace("play", "", 1).strip()
        link = music_library.music.get(song)
        if link:
            speak(f"Playing {song}")    
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song} in the library.")
    elif "news" in c_lower:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_API}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            titles = [article['title'] for article in articles[:3]]  # Limit to 3 headlines
            speak("Here are the latest news headlines: " + ". ".join(titles))
        else:
            speak("Sorry, I couldn't fetch the news right now.")
    else:
        output = ai_process(c)
        speak(output)
    return False  # Default: continue running 
     
            
if __name__ == "__main__": 
    speak("Intializing Jarvis....")
    
    while True:
        # Listen for the wake word "Jarvis"
        r = sr.Recognizer()
        
    
        print("Recognizing....")
        try:
            # obtain audio from microphone
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
            word = r.recognize_google(audio)
            if (word.lower() == "jarvis"):
                speak("At your service, Sir.")
                #listen for command
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    
                    if processCommand(command):
                        break
                
        except Exception as e:
            print("Error; {0}".format(e))        
