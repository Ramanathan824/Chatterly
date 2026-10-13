import random
import string
greetings = [
    "Hello! How can I help you?",
    "Hi! Nice to meet you!",
    "Hey! What can I do for you?"
]

def chatbot(user_input):
    if user_input in ["hello", "hi", "hey", "hii"]:
        return random.choice(greetings)
    elif user_input in ["how are you", "how are you doing"]:
        return "I'm doing great! Thanks for asking."
    elif user_input in ["what is your name", "your name"]:
        return "I'm a simple Python chatbot."
    elif user_input in ["bye", "goodbye"]:
        return "Goodbye! Have a nice day!"
    elif user_input == "help":
        return "You can ask me about Python, Java, weather, jokes, news or say hello."
    elif user_input == "weather":
        return "I can provide you with weather updates. Please specify the location."
    elif user_input == "joke":
        return "Why don't scientists trust atoms? Because they make up everything!"    
    elif user_input in ["python", "what is python", "tell me about python", "explain python"]:
        return "Python is a high-level programming language. You can learn more about it at https://www.python.org/"
    elif user_input == "news":
        return "I can provide you with the latest news updates. Please specify the topic or region."
    elif user_input in ["java", "what is java", "tell me about java", "explain java"]:
        return "Java is a popular programming language. You can learn more about it at https://www.java.com/"
    elif user_input == "what is programming":
        return "Programming is the process of giving instructions to a computer."
    elif user_input == "what is coding":
        return "Coding means writing instructions for a computer using a programming language."
    elif user_input == "what is a variable":
        return "A variable is used to store a value in a program."
    elif user_input == "what is a loop":
        return "A loop is used to repeat a block of code multiple times."
    elif user_input == "what is a function":
        return "A function is a reusable block of code that performs a specific task."
    elif user_input == "what is html":
        return "HTML is used to create the structure of a web page."
    elif user_input == "what is css":
        return "CSS is used to style and design web pages."
    elif user_input == "what is javascript":
        return "JavaScript is used to make web pages interactive."
    elif user_input == "what is database":
        return "A database is used to store, organize and manage data."
    elif user_input == "what is sql":
        return "SQL is used to store, retrieve and manage data from databases."
    elif user_input == "what is django":
        return "Django is a Python web framework used to build web applications."
    elif user_input == "what is react":
        return "React is a JavaScript library used to build user interfaces."
    elif user_input == "what is api":
        return "API allows different software applications to communicate with each other."
    else:
        return "I'm still learning. I don't know the answer to that yet."

print("Welcome to the chatbot!")
conversation_history = []
while True:
    message = input("You: ").lower().strip().replace("?", "")
    message = message.translate(str.maketrans("", "", string.punctuation))
    if message == "exit":
        print("Chatbot: Goodbye!")
        break
    response = chatbot(message)

    conversation_history.append({
        "user": message,
        "bot": response
    })

    print("Chatbot:", response)