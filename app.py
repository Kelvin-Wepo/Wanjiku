import pyttsx3
import speech_recognition as sr
import tkinter as tk
import datetime
import africastalking
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize africastalking
africastalking.initialize(
    username='Kwepo',
    api_key='f67c169248ae4bf36bdc9e798afed8428dcd3770bf78cf051d4faa752fd8a8a9',
)
sms = africastalking.SMS
message = "Thank you for booking an Appointment with us."
phone = "+254714805460"

# Initialize pyttsx3
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to make the assistant speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to wish the user based on the time of day
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning ")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon ")
    else:
        speak("Good Evening")

    assname = "Wanjiku"
    speak("I am your Assistant")
    speak(assname)
    speak("How can I help you")

# Function to take voice commands from the user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 0.5
        print("Listening...")
        audio = r.listen(source)
    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Unable to recognize your voice.")
        speak("Unable to recognize your voice.")
        return "None"
    return query

# Function to handle user commands
def handleCommand():
    query = takeCommand().lower()
    if 'hello' in query:
        speak('Hello, I am Wanjiku your booking assistant')
        speak('How may I help you?')
    elif 'book an appointment' in query:
        speak('Which service do you require?')
    elif 'passport' in query:
        speak('Okay..')
        speak('What is your name')
        uname = takeCommand()
        speak('Welcome to Huduma center services')
        speak(uname)
        speak('Time available is 8-12 and 2-5')
        speak('Which time is good for you?')
    elif 'good conduct' in query:
        speak('Okay..')
        speak('What is your name')
        uname = takeCommand()
        speak('Welcome to Huduma center services')
        speak(uname)
        speak('Time available is 8-12 and 2-5')
        speak('Which time is good for you?')
    elif 'Id' in query:
        speak('Okay..')
        speak('What is your name')
        uname = takeCommand()
        speak('Welcome to Huduma center services')
        speak(uname)
        speak('Time available is 8-12 and 2-5')
        speak('Which time is good for you?')
    elif 'driving licence' in query:
        speak('Okay..')
        speak('What is your name')
        uname = takeCommand()
        speak('Welcome to Huduma center services')
        speak(uname)
        speak('Time available is 8-12 and 2-5')
        speak('Which time is good for you?')
    elif '8 to 12' in query:
        speak('Your appointment has been booked for 8-12')
        response = sms.send('Your appointment has been booked for 8-12', [phone])
        print(response)
    elif '2 to 5' in query:
        speak('Your appointment has been booked for 2-5')
        response = sms.send('Your appointment has been booked for 2-5', [phone])
        print(response)
    elif 'thank you' in query:
        speak('You are welcome')
    elif 'search the web for' in query:
        search_query = query.replace('search the web for', '').strip()
        speak(f"Searching the web for {search_query}")
        search_internet(search_query)
    elif 'search ecitizen for' in query:
        search_query = query.replace('search ecitizen for', '').strip()
        speak(f"Searching eCitizen for {search_query}")
        search_ecitizen(search_query)
    elif 'login to ecitizen' in query:
        speak("Navigating to the eCitizen login page")
        navigate_to_ecitizen_login()
    elif 'signup to ecitizen' in query:
        speak("Navigating to the eCitizen signup page")
        navigate_to_ecitizen_signup()
    else:
        speak("I'm sorry, I didn't understand that command.")

# Function to search the web
def search_internet(query):
    # Initialize the WebDriver with WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    driver.get('https://www.google.com')

    # Find the search box, enter the query, and submit
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)  # Wait for results to load

    # Get search results
    results = driver.find_elements(By.CSS_SELECTOR, 'h3')
    
    # Debug print to check results
    for result in results:
        print(result.text)
    
    if results:
        speak(f"I found some results for {query}. Here are the top results:")
        # Iterate over results and speak each one
        for result in results[:3]:  # Limit to top 3 results
            speak(result.text)
    else:
        speak(f"Sorry, I couldn't find any results for {query}.")
    
    driver.quit()

# Function to search the eCitizen website
def search_ecitizen(query):
    # Initialize the WebDriver with WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    driver.get('https://www.ecitizen.go.ke/')

    # Find the search box, enter the query, and submit (Assuming eCitizen has a search box with name 'q')
    try:
        search_box = driver.find_element(By.NAME, 'q')  # Adjust the selector if the search box has a different name or identifier
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)  # Wait for results to load

        # Get search results
        results = driver.find_elements(By.CSS_SELECTOR, 'h3')  # Adjust the selector based on the actual results layout
        
        # Debug print to check results
        for result in results:
            print(result.text)
        
        if results:
            speak(f"I found some results for {query}. Here are the top results:")
            # Iterate over results and speak each one
            for result in results[:3]:  # Limit to top 3 results
                speak(result.text)
        else:
            speak(f"Sorry, I couldn't find any results for {query}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        #speak(f"Sorry, there was an error searching eCitizen for {query}.")
    
    driver.quit()

# Function to navigate to eCitizen login page
def navigate_to_ecitizen_login():
    # Initialize the WebDriver with WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    driver.get('https://www.ecitizen.go.ke/')

    # Find and click the login button
    try:
        login_button = driver.find_element(By.LINK_TEXT, 'Login')  # Adjust the selector based on the actual button text
        login_button.click()
        speak("You are now on the eCitizen login page.")
    except Exception as e:
        print(f"An error occurred: {e}")
        #speak("Sorry, I couldn't navigate to the eCitizen login page.")
    
    # Optionally, you can fill in the login details here if required

    driver.quit()

# Function to navigate to eCitizen signup page
def navigate_to_ecitizen_signup():
    # Initialize the WebDriver with WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    driver.get('https://www.ecitizen.go.ke/')

    # Find and click the signup button
    try:
        signup_button = driver.find_element(By.LINK_TEXT, 'Create an account')  # Adjust the selector based on the actual button text
        signup_button.click()
        speak("You are now on the eCitizen signup page.")
    except Exception as e:
        print(f"An error occurred: {e}")
        #speak("Sorry, I couldn't navigate to the eCitizen signup page.")
    
    # Optionally, you can fill in the signup details here if required

    driver.quit()

# Function to initialize the UI
def initUI():
    root = tk.Tk()
    root.title("Virtual Assistant")

    canvas = tk.Canvas(root, height=500, width=800)
    canvas.pack()

    frame = tk.Frame(root, bg='#003B4A', bd=5)
    frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

    button = tk.Button(frame, text="Speak", font=40, command=handleCommand)
    button.place(relx=0.7, relheight=1, relwidth=0.3)

    label = tk.Label(frame, text="Click 'Speak' and say your command", font=40)
    label.place(relx=0, relheight=1, relwidth=0.65)

    lower_frame = tk.Frame(root, bg='#003B4A', bd=10)
    lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

    text_box = tk.Text(lower_frame, font=40)
    text_box.place(relx=0, rely=0, relwidth=1, relheight=1)

    scrollbar = tk.Scrollbar(text_box)
    scrollbar.pack(side='right', fill='y')
    text_box.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_box.yview)

    root.mainloop()

if __name__ == '__main__':
    wishMe()
    initUI()