from __future__ import print_function
import os
from dotenv import load_dotenv

load_dotenv()

import os
import getpass
from dotenv import load_dotenv

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)

from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent

from prompt import *

prompt = hub.pull("hwchase17/structured-chat-agent")

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from typing import Optional, Type
import json

from places_agent import HotelAPI


def Places_agent(a: str):
    try:
        place = HotelAPI()
        return place.get_poi(a)
    except TypeError as e:
        return "Please provide a valid address."


places_tool = StructuredTool.from_function(
    func=Places_agent,
    name="Hotel API Tool",
    description="This tool allows you to query the Hotel API and get the results back. You can find hotels, and other places to stay near a given location. pass Address to get the hotels near that location.",
)

from food_agent import FoodAPI


def Food_agent(a: str):
    try:
        food = FoodAPI()
        return food.get_food(a)
    except TypeError as e:
        return "Please provide a valid address."


food_tool = StructuredTool.from_function(
    func=Food_agent,
    name="Food API Tool",
    description="This tool allows you to query the Food API and get the results back. You can find restaurants, and other places to eat near a given location. pass Address to get the restaurants near that location.",
)


from Weather_agent import WeatherForecast


def Weather_agent(a: str):
    try:
        forecast = WeatherForecast()  # Create an instance of the WeatherForecast class
        return forecast.get_forecast(a)  # Call the get_forecast method on the instance
    except Exception as e:
        return str(e)


weather_tool = StructuredTool.from_function(
    func=Weather_agent,
    name="Weather API Tool",
    description="This tool allows you to get the weather forecast for a given location. pass Address to get the weather forecast for that location.",
)


tools = [places_tool, weather_tool, food_tool]
master_llm = "You are a Travel agent, You are supposed to plan a travel itinerary for a client. You can use all the tools available to you to make the best itinerary for the client."

p_weather_tool = "Weather API Tool: This tool allows you to get the weather forecast for a given location.Just call the tool and pass Address to get the weather forecast for that location."

p_food_tool = "Place API Tool: This tool helps you find nearby places to eat. Just pass the location and you will get a list of places where you can eat."

p_hotel_tool = "Hotel API Tool: This tool helps you find nearby hotels. Just pass the location and you will get a list of hotels where you can stay."

# p_attraction_tool = "Attraction API Tool: This tool helps you find nearby attractions. Just pass the location and you will get a list of attractions where you can visit. You can call it multiple times but you have to change the location to get a different responses."

# p_navigation_tool = "Navigation API Tool: This tool helps you find the best route to reach a location. Just pass the source and destination location and you will get the best route to reach the destination."

p_hallucination_prompt = "always remember following points:-If a tool doesn't work, try changing how you call it or call another tool- always keep in mind the client's profile while planning the itinerary- always keep in mind the time "

p_order = "I would recommend you to start with the Weather API Tool to get the weather forecast for the location you are planning to visit.Then you can use the Place API Tool to find nearby places to eat. You should you use navigation API tool to find the best route to reach the location.You can use the Hotel API Tool to find nearby hotels and the Attraction API Tool to find nearby attractions."

p_example = "Example1:Input: Place - Indore; Food - Italian; Interests - Adventure, Religion; Health - None.Actions: 1) Hotel_api_tool - Find a place to stay near railway station.2) food_api_tool - find good place to eat nearby the places you want to stay.3) weather_api_tool - check how long the weather is clear. if weather is not clear then recommend moving to some other place.4) make a plan with all the information."

p = (
    master_llm
    + p_weather_tool
    + p_food_tool
    + p_hotel_tool
    + p_hallucination_prompt
    + p_order
    + p_example
)


from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferWindowMemory

conversational_memory = ConversationBufferWindowMemory(
    memory_key="chat_history", k=5, return_messages=True
)


def Final(place, Food, Interests, Health, Days):
    agent_executor = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        memory=conversational_memory,
        max_iterations=10,
    )
    output = agent_executor.run(
        master_llm
        + "Place - "
        + place
        + "; Food - "
        + Food
        + "; Interests - "
        + Interests
        + "; Health - "
        + Health
        + ".Give me Atleast "
        + str(Days)
        + " days to plan the itinerary."
        + "You can use the following tools to plan the itinerary:"
        + f"Weather API Tool: This tool allows you to get the weather forecast for a given location.Just  pass {place} to get the weather forecast for that location."
        + f"Place API Tool: This tool helps you find nearby places to eat. Just pass {place} and you will get a list of places where you can eat."
        + f"Hotel API Tool: This tool helps you find nearby hotels. Just pass {place} and you will get a list of hotels where you can stay."
        + p_hallucination_prompt
        + p_order
        + """Example response:- 
Day 1:
* Arrive in Raipur and check into your hotel, Hotel Babylon International.
* Have lunch at Noorjahan, an Italian restaurant.
* Visit the Mahamaya Temple, one of the most famous temples in Raipur.
* Enjoy a traditional Raipuri dinner at Bajrang Bhog Bhandar.

Day 2:
* Visit the Raipur Zoo, home to a variety of animals from all over India.
* Have lunch at Golden Oak DKS, another Italian restaurant.
* Take a walk through the lush green gardens of the Budha Talab Park.
* Enjoy a romantic dinner at A Tristar Venture K Square, an Italian restaurant with a beautiful ambiance.

Day 3:
* Visit the Science Center, a great place to learn about science and technology.
* Have lunch at a local restaurant.
* Visit the Doodhadhari Temple, a famous temple dedicated to Lord Shiva.
* Enjoy a traditional Raipuri dinner at a local restaurant.

Day 4:
* Visit the Chhattisgarh State Museum, home to a collection of artifacts from the state's history.
* Have lunch at a local restaurant.
* Visit the Gandhi Udyan Park, a beautiful park with a variety of flowers and trees.
* Enjoy a farewell dinner at a local restaurant.

Day 5:
* Depart from Raipur.
output:"""
    )
    if output == "Agent stopped due to iteration limit or time limit.":
        return "Sorry Error: Agent stopped due to iteration limit or time limit."

    return output


from datetime import datetime
from bson.objectid import ObjectId
import pymongo


class MongoDBManager:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.client["BonVoyage"]
        self.collection = self.db["user-info"]

    def give(self, interest, food, health, email, in_date, chat_history, out_date):
        if isinstance(in_date, str):
            in_date = datetime.strptime(in_date, "%Y-%m-%d")
        if out_date and isinstance(out_date, str):
            out_date = datetime.strptime(out_date, "%Y-%m-%d")

        data = {
            "interest": interest,
            "food": food,
            "health": health,
            "email": email,
            "in_date": in_date,
            "chat_history": chat_history,
            "out_date": out_date,
        }

        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def get(self, document_id):
        document = self.collection.find_one({"_id": ObjectId(document_id)})
        return document if document else None

    def get_chat_histories_by_email(self, email):
        documents = self.collection.find({"email": email})
        chat_histories = [
            doc["chat_history"] for doc in documents if "chat_history" in doc
        ]
        return chat_histories


from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # React
    "http://localhost:8000",  # Angular
    "https://3c83-103-231-47-210.ngrok-free.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Task(BaseModel):
    Place: str
    Food: str
    Interests: str
    Health: str
    Days: int
    email: str
    in_date: str
    out_date: str


class GetTask(BaseModel):
    email: str


@app.post("/chat")
async def final_endpoint(task: Task):
    # Convert dates from "dd-mm-yyyy" to "yyyy-mm-dd"
    in_date = datetime.strptime(task.in_date, "%d-%m-%Y").strftime("%Y-%m-%d")
    out_date = datetime.strptime(task.out_date, "%d-%m-%Y").strftime("%Y-%m-%d")
    while True:
        out = Final(task.Place, task.Food, task.Interests, task.Health, task.Days)
        if "sorry" not in out and "Sorry" not in out:
            break
        if "sorry" in out and "Sorry" in out:
            if "Moving" in out and "moving" in out and "move" in out:
                break

    dbManager = MongoDBManager()
    dbManager.give(
        task.Interests,
        task.Food,
        task.Health,
        task.email,
        in_date,
        out,
        out_date,
    )
    return {"response": out}


@app.post("/get")
async def get_endpoint(task: GetTask):
    dbManager = MongoDBManager()
    return {"chat_histories": dbManager.get_chat_histories_by_email(task.email)}


# print(
#     Final(
#         "Place - raipur; Food - Italian; Interests - Adventure, Religion; Health - None."
#     )
# )
