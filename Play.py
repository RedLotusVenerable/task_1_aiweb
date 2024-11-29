import random
import streamlit as st
from openai import OpenAI
import requests
import base64

# Page name and icon
st.set_page_config(page_title="Animal Guessing Game", page_icon=":paw_prints:")

st.title("🐾Welcome to the Animal Guessing Game!🐾")
st.header("CHRISTMAS EDITION 🎄")
# Introduction to the game
st.write("""
    Please guess the animal I am thinking about. The options are:\n
    Fly, Spider, Mouse, Rat, Bird, Rabbit, Monkey, Cat, Racoon, Fox, Pig, Panda, Dog, Wolf, Lion, Horse, Giraffe, Elephant, Whale🐾""")


def get_base64_from_url(url):
    response = requests.get(url)
    return base64.b64encode(response.content).decode()


# Function to fetch and encode image from URL
def get_base64_from_url(url):
    response = requests.get(url)
    return base64.b64encode(response.content).decode()


# Function to set background image with adjustable opacity
def set_background(url, opacity=1):
    bin_str = get_base64_from_url(url)
    page_bg_img = f'''
    <style>
    .stApp {{
      background-image: url("data:image/png;base64,{bin_str}");
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
      background-attachment: fixed;
    }}
    .stApp::before {{
      content: "";
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background-color: rgba(255, 255, 255, {1 - opacity});
      z-index: -1;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Apply the CSS styling to the Streamlit app
    st.markdown(page_bg_img, unsafe_allow_html=True)


# Set background image
set_background(
    'https://img.freepik.com/free-vector/christmas-vector-illustration-with-reindeer-forest-isolated-white-background_8130-1176.jpg')

# List of all possible Animals
animals = {
    "fly": {"Habitat": "Everywhere", "Size": "XS", "Food": "Omnivore", "Movement": "Flying", "Color": "Black",
            "Reproduction:": "Oviparous"},
    "spider": {"Habitat": "Everywhere", "Size": "XS", "Food": "Carnivore", "Movement": "Walking", "Color": "Black",
               "Reproduction:": "Oviparous"},
    "mouse": {"Habitat": "Everywhere", "Size": "XS", "Food": "Omnivore", "Movement": "Walking", "Color": "Grey",
              "Reproduction:": "Mammal"},
    "rat": {"Habitat": "Everywhere", "Size": "S", "Food": "Omnivore", "Movement": "Walking", "Color": "Grey",
            "Reproduction:": "Mammal"},
    "bird": {"Habitat": "Everywhere", "Size": "S", "Food": "Omnivore", "Movement": "Flying", "Color": "Colorful",
             "Reproduction:": "Oviparous"},
    "rabbit": {"Habitat": "Everywhere", "Size": "S", "Food": "Herbivore", "Movement": "Hopping", "Color": "Brown",
               "Reproduction:": "Mammal"},
    "monkey": {"Habitat": "Africa", "Size": "M", "Food": "Omnivore", "Movement": "Climbing", "Color": "Brown",
               "Reproduction:": "Mammal"},
    "cat": {"Habitat": "Everywhere", "Size": "M", "Food": "Carnivore", "Movement": "Walking", "Color": "Multi",
            "Reproduction:": "Mammal"},
    "racoon": {"Habitat": "America", "Size": "M", "Food": "Omnivore", "Movement": "Walking", "Color": "Grey",
               "Reproduction:": "Mammal"},
    "fox": {"Habitat": "Everywhere", "Size": "M", "Food": "Omnivore", "Movement": "Walking", "Color": "Red",
            "Reproduction:": "Mammal"},
    "pig": {"Habitat": "Everywhere", "Size": "L", "Food": "Omnivore", "Movement": "Walking", "Color": "Brown",
            "Reproduction:": "Mammal"},
    "panda": {"Habitat": "Asia", "Size": "L", "Food": "Herbivore", "Movement": "Climbing", "Color": "White",
              "Reproduction:": "Mammal"},
    "dog": {"Habitat": "Everywhere", "Size": "L", "Food": "Carnivore", "Movement": "Walking", "Color": "Multi",
            "Reproduction:": "Mammal"},
    "wolf": {"Habitat": "Europe", "Size": "L", "Food": "Carnivore", "Movement": "Walking", "Color": "Grey",
             "Reproduction:": "Mammal"},
    "lion": {"Habitat": "Africa", "Size": "L", "Food": "Carnivore", "Movement": "Walking", "Color": "Brown",
             "Reproduction:": "Mammal"},
    "horse": {"Habitat": "America", "Size": "L", "Food": "Herbivore", "Movement": "Walking", "Color": "Multi",
              "Reproduction:": "Mammal"},
    "giraffe": {"Habitat": "Africa", "Size": "XL", "Food": "Herbivore", "Movement": "Walking", "Color": "Brown",
                "Reproduction:": "Mammal"},
    "elephant": {"Habitat": "Africa", "Size": "XL", "Food": "Herbivore", "Movement": "Walking", "Color": "Grey",
                 "Reproduction:": "Mammal"},
    "whale": {"Habitat": "Ocean", "Size": "XL", "Food": "Carnivore", "Movement": "Swimming", "Color": "Grey",
              "Reproduction:": "Mammal"}
}


# Function to show animal picture
def show_animal(animal_name):
    try:
        image_path = f"images/{animal_name}.jpg"
        st.image(image_path, caption=animal_name, use_container_width=True)
    except:
        st.warning(f"Didn't find the image for '{animal_name}'")


def start_new_game():
    animal, animal_features = random.choice(list(animals.items()))
    st.session_state.animal = animal
    # st.session_state.animal_features = animal_features
    st.session_state.interaction_count = 0  # Reset interaction count
    st.session_state.wrong_guess_count = 0  # Reset wrong guess count
    st.session_state.non_related_count = 0  # Reset non related input count
    st.session_state.guess_count = 0  # Reset guess count
    st.session_state.game = False


# HERE THE ACTUAL GAME STARTS

# Initialize session state
if 'animal' not in st.session_state:
    animal, animal_features = random.choice(list(animals.items()))
    st.session_state.animal = animal
    st.session_state.animal_features = animal_features
    st.session_state.guess_count = 0
    st.session_state.wrong_guess_count = 0
    st.session_state.non_related_count = 0
    st.session_state.interaction_count = 0
    st.session_state.games_played = 0
    st.session_state.total_guesses = 0
    st.session_state.total_interactions = 0
    st.session_state.guesses_per_game = []
    st.session_state.game = False

if st.button("Next try") or st.session_state.game:
    animal, animal_features = random.choice(list(animals.items()))
    start_new_game()

    st.session_state.game = False

# Set up the OpenAI client with the API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set the model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history and counters
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Add game context to the chat history
if "system_message_added" not in st.session_state:
    animal = {"Fly", "Spider", "Mouse", "Rat", "Bird", "Rabbit", "Monkey", "Cat", "Racoon", "Fox", "Pig", "Panda",
              "Dog", "Wolf", "Lion", "Horse", "Giraffe", "Elephant", "Wale"}
    # Sst.write(st.session_state.animal)#####################AUSKOMMENTIEREN!!!!!!!!!!!!!!!!!!!!
    # Add game context and rules to the system
    st.session_state["system_message"] = (
        "You are an AI assistant for a guessing game about animals. "
        f"The possible animals are: {', '.join(animal)}. "
        f"The correct answer is {st.session_state.animal}. "
        "Rules:\n"
        "1. Never reveal the correct answer directly.\n"
        "2. You evaluate each guess to 'correct', 'wrong', 'game related questions' or 'not related' your response has to incorporate the respective keyword somehow.  .\n"
        "3. Respond with a cheerful congratulating message if the user guesses correctly.\n"
        "4. The respond lets the user know he was wrong in a funny way for incorrect guesses.\n"
        "5. Engage but remind of the purpose of the game for inputs not related to the game.\n"
        f"6. After 3 wrong guesses, provide a very small hint about the animal. Emojis of the {st.session_state.animal} are not allowed.\n"
        "7. After 3 consecutive inputs that are 'not related', remind the user to continue playing.\n"
        "8. Keep responses concise and engaging."
        "9. Game related questions are not 'not related' guesses."
        "10. Answer game related questions adequately."
        "11. If a guess was evaluated 'correct', use the word 'Correct' or the word 'Congratulations' or both in your response."
        "12. If a guess was evaluated 'not related', use the phrase 'not related to the game' in your response."
        "13. If a guess was evaluated 'wrong', use the word 'wrong' in your response."

    )
    # st.session_state.system_message_added = True  # Ensure this is only added once

# Accept user input
if prompt := st.chat_input("What is your guess?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    st.session_state.interaction_count += 1
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response from the assistant
    try:
        with st.chat_message("assistant"):
            # Combine system message with chat history
            messages = [{"role": "system", "content": st.session_state["system_message"]}] + st.session_state.messages
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=messages,  # Use the combined messages including the system message
                stream=True,
                temperature=0.7,
                top_p=0.8,
            )

            # Collect the streamed response
            response = ""

            for i, chunk in enumerate(stream):
                if hasattr(chunk.choices[0].delta, 'content'):
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        response += content

                else:
                    st.write("No content attribute in this chunk")

            st.write(f"{response}")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()

        ## Check the AI's classification
    if "correct" in response.lower() or "congratulations" in response.lower():
        show_animal(st.session_state.animal)
        st.toast('Hooray!', icon='🎉')
        st.toast(f'You only needed {st.session_state.interaction_count} interactions to guess correctly!')
        st.snow()
        st.session_state.guess_count += 1
        st.session_state.total_guesses += st.session_state.guess_count
        st.session_state.total_interactions += st.session_state.interaction_count
        st.session_state.guesses_per_game.append(st.session_state.guess_count)
        st.session_state.games_played += 1
        start_new_game()

    elif "wrong" in response.lower():
        st.session_state.guess_count += 1
        st.session_state.wrong_guess_count += 1

    elif "not related" in response.lower():
        st.session_state.non_related_count += 1
        if st.session_state.non_related_count >= 4:
            st.warning("Remember to keep guessing animals!")

        # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display counters (optional for debugging)
    st.sidebar.write(f"Number of interactions: {st.session_state.interaction_count}")
    st.sidebar.write(f"Wrong guesses: {st.session_state.wrong_guess_count}")
    st.sidebar.write(f"Not related guesses: {st.session_state.non_related_count}")