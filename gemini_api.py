import google.generativeai as genai
import re
import json
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# model = genai.GenerativeModel('gemini-1.5-pro')  # Or 'gemini-pro'
model = genai.GenerativeModel('gemini-2.0-flash')

def get_travel_info(user_input):
    """Uses Gemini AI to extract travel intent, origin, destination, and other travel details from user input."""

    prompt = f"""
      You are a travel assistant. Your job is to extract the travel intent, origin (from where), destination (to where), and departure date from a user's query.
      If the origin is not mentioned, return null.
      If the intent is not related to travel, return the intent and location in JSON format ONLY, like this:
      If either the intent, the origin, the destination, the departure_date, duration, budget, or num_people is not found, return null for that field.

      ```json
      {{
        "intent": "the extracted intent",
        "from": "the extracted origin",
        "to": "the extracted destination",
        "departure_date": "the extracted departure date",
        "duration": "the extracted duration",
        "budget": "the extracted budget",
        "num_people": "the extracted number of people"
      }}
      ```

      User Query: I want to plan a trip from Los Angeles to Paris for 5 days with a budget of $2000 for 2 people, leaving on March 15th.
      ```json
      {{
        "intent": "plan a trip",
        "from": "Los Angeles",
        "to": "Paris",
        "departure_date": "March 15th",
        "duration": "5 days",
        "budget": "$2000",
        "num_people": "2"
      }}
      ```

      User Query: Find a hotel in New York City for 3 nights with a budget of $1500 for 1 person, leaving on April 10th.
      ```json
      {{
        "intent": "Find a hotel",
        "from": null,
        "to": "New York City",
        "departure_date": "April 10th",
        "duration": "3 nights",
        "budget": "$1500",
        "num_people": "1"
      }}
      ```

      User Query: What is the weather like today?
      ```json
      {{
        "intent": null,
        "from": null,
        "to": null,
        "departure_date": null,
        "duration": null,
        "budget": null,
        "num_people": null
      }}
    ```

    User Query: {user_input}
    """

    response = model.generate_content(prompt)
    response_text = response.text
    # print(f"Raw Gemini Response: {response_text}")  # Debugging

    try:
        # Use regular expression to find the JSON string within the response
        match = re.search(r"\{.*?\}", response_text, re.DOTALL)
        if match:
            json_string = match.group(0).strip()
            data = json.loads(json_string)
            intent = data.get("intent")
            from_location = data.get("from")
            to_location = data.get("to")
            departure_date = data.get("departure_date")
            duration = data.get("duration")
            budget = data.get("budget")
            num_people = data.get("num_people")
            return {
                "intent": intent,
                "from": from_location,
                "to": to_location,
                "departure_date": departure_date,
                "duration": duration,
                "budget": budget,
                "num_people": num_people
            }
        else:
            print("Error: No JSON found in Gemini response.")
            return None

    except json.JSONDecodeError:
        print("Error: Could not decode JSON after extraction.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_travel_recommendations(intent, from_location, to_location, departure_date, duration, budget, num_people):
    """Uses Gemini AI to provide travel recommendations based on intent, origin, and destination."""

    prompt = f"""
      You are a travel assistant. Based on the given intent, origin (from where), destination (to where), duration, budget, and number of people, provide helpful travel recommendations in Markdown format.
      - Provide some common websites for booking flights as well as the like to the web.
      - List at least 2 of the cheapest flight options.
      - Provide at least 10 recommended attractions.
      - Provide at least 5 accommodations.
      - Provide at least 10 activities.
      - Provide at least 10 food recommendations.
      - Keep in mind the budget and number of people when suggesting accommodations and activities.
      - Use NTD as the currency

      Intent: {intent}
      From: {from_location}
      To: {to_location}
      Departure Date: {departure_date}
      Duration: {duration}
      Budget: {budget}
      Number of People: {num_people}

      Your response should look like this:

      # 🌍 Travel Guide: {to_location}

      ## 🌤️ Weather:
      - Weather details for {to_location}

      ## ✈️ Flights from {from_location} to {to_location}:
      - 
      - 

      ## 💳 Mobile Payment:
      - 
      - 

      ## 🚗 Local Transportations:
      - 
      - 

      ## 🏨 Accommodations:
      - 
      - 

      ## 🏰 Attractions:
      - 
      - 

      ## 🚀 Activities:
      - 
      - 

      ## 🍽️ Foods to Try:
      - 
      - 

      ## 💡 Tips for Planning:
      - 
      - 
    """

    response = model.generate_content(prompt)
    return response.text
