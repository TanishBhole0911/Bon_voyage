from __future__ import print_function
import grpc
import os
import getpass
from dotenv import load_dotenv

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent


from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from typing import Optional, Type
import json

import weather_pb2
import weather_pb2_grpc


class WeatherForecast:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro", convert_system_message_to_human=True
        )
        self.prompt = hub.pull("hwchase17/structured-chat-agent")
        self.weather_api = StructuredTool.from_function(
            func=self.run_weather_api,
            name="Weather API Tool",
            description="This tool allows you to get the weather forecast for a given location. pass Address to get the weather forecast for that location.",
        )
        self.W_tools = [self.weather_api]
        self.W_agent = create_structured_chat_agent(self.llm, self.W_tools, self.prompt)
        self.W_agent_executor = AgentExecutor(
            agent=self.W_agent, tools=self.W_tools, verbose=True
        )

    def Weather_API(self, add: str):
        with grpc.insecure_channel("localhost:50053") as channel:
            stub = weather_pb2_grpc.LatLongServiceStub(channel)
            response = stub.GetForcasteWeather(
                weather_pb2.Forcaste_Weather_req(address=add)
            )
        return response

    def run_weather_api(self, a: str):
        try:
            return self.Weather_API(a)
        except Exception as e:
            return str(e)

    def get_forecast(self, address: str):
        x = self.W_agent_executor.invoke(
            {
                "input": f"give me weather forecast at Address:{{{address}}}. Use the Weather API Tool."
            }
        )
        return x["output"]


# print(WeatherForecast().get_forecast("New York"))
