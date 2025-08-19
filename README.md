# RASA-Powered Netflix Advisor Chatbot

Full Spanish Report: https://drive.google.com/file/d/1ipoCHMyh37e2znlnPLmWbLeWb0bfGJNU/view?usp=sharing

## 📜 Introduction

This project showcases the development of an intelligent conversational agent built with **RASA**, an open-source framework for creating AI-powered chatbots and voice assistants using Machine Learning and Natural Language Understanding (NLU).

The agent is deployed on **Telegram** and its primary function is to help users choose movies and series to watch on **Netflix**, offering personalized recommendations based on their preferences and mood.

---

## 🛠️ Technologies and Tools

* **Main Framework:** RASA Open Source
* **Programming Languages:** Python, Prolog
* **Messaging Platform:** Telegram API
* **Key Libraries:**
  * Pyswip (for Prolog integration)
  * Pandas & Scikit-learn (for the Decision Tree)
  * Beautiful Soup (for Web Scraping)

---

## 🤖 Agent Structure

The bot's architecture is built upon RASA's core components to manage dialogue, understand the user, and execute business logic.

### 1. Natural Language Understanding (NLU)

The bot's ability to understand the user is achieved through:

* **`Intents`**: Intentions were defined to capture the purpose of the user's message (e.g., greeting, saying goodbye, asking for a name, requesting a recommendation). The model is trained with multiple examples for each `intent`, allowing the NLU to generalize and recognize variations.

  ```yaml
  # Example of a goodbye intent
  - intent: goodbye
    examples: |
      - goodbye
      - bye
      - see you later
      - take care
  ```

* **`Entities`**: Key pieces of information extracted from messages, such as the user's **name**, their **mood**, or their preferred **movie genre**.

### 2. Dialogue Management

The conversation flow is controlled by a combination of rules and stories:

* **`Rules`**: Used to handle fixed and predictable conversation flows. For example, a simple rule states that if the user says goodbye (`intent: goodbye`), the bot should always respond with a farewell message.

* **`Stories`**: Define the more complex and dynamic conversational paths. Stories are sample dialogues that teach the bot how to react to different sequences of intents and events.

### 3. The `Domain`

This is the bot's "brain," where everything the agent knows is defined:

* All `intents`, `entities`, `slots`, and `actions`.
* **`Responses`**: Message templates that the bot can send to the user. Multiple options can be defined for a single response, and RASA will pick one at random to make the conversation more dynamic.

### 4. `Slots`

These act as the chatbot's memory. They are used to store relevant information throughout the conversation, such as the user's name or preferences. The values in slots can influence the course of the dialogue.

### 5. `Actions`

This is the most powerful part of the bot, allowing the execution of custom **Python** code. In this project, actions were used to:

* Interact with the **Prolog** knowledge base.
* Implement the **Decision Tree** model.
* Perform **Web Scraping** to get updated data.
* Generate complex and personalized responses.

---

## 🧠 Algorithms and Implemented Logic

### 1. Movie Recommendation System with Prolog

**Prolog**, a logic programming language ideal for knowledge representation and rules, was used for movie recommendations.

* **Knowledge Base:** A Prolog file was created with a series of facts that link movies to a specific **mood** and **genre**.

  ```prolog
  % Fact: movie(Mood, Genre, Title, Synopsis).
  movie(happy, comedy, 'Superbad', 'Two co-dependent high school seniors...').
  movie(sad, drama, 'Manchester by the Sea', 'A depressed uncle is asked...').
  ```

* **Inference Logic:** A predicate `get_recommended_movie/4` was defined. Given a mood and a genre, it searches the knowledge base and randomly returns a movie that matches the criteria.

* **Integration:** A Python `action` queries the Prolog engine, passing the `slots` (mood and genre), and processes the response to deliver it to the user.

### 2. Decision Tree for Series vs. Movies

A **Decision Tree** model was implemented to decide whether to recommend a series or a movie.

* **Data Collection:** The bot asks the user key questions to understand their preferences:
  1. Do you prefer a closed or an open ending?
  2. Do you like characters with deep evolution or more static ones?
  3. Do you prefer a slow, detailed pace or a fast, exciting one?

* **Preprocessing:** The categorical answers are converted into a numerical format using **One-Hot Encoding**.

* **Model Training:** A CSV file with sample data was used to train a classification model that predicts whether the user prefers a "Series" or a "Movie" based on their answers.

* **Execution:** A Python `action` collects the user's responses, processes them, and uses the trained model to make the final decision.

### 3. Web Scraping for Popular Series

To keep series recommendations up-to-date, an `action` that performs **Web Scraping** was implemented.

* The action connects to the official **Netflix Top 10** page.
* It extracts the real-time list of the 10 most popular series of the week.
* It formats the information and presents it to the user as a list of recommendations.

### 4. Handling Unrecognized Inputs

To manage situations where the bot doesn't understand the user, the `action_default_fallback` was customized. When the NLU cannot classify a message with a high enough confidence level, this action is triggered and kindly informs the user that it did not understand their request.
