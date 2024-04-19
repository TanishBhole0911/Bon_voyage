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
from langchain.tools import StructuredTool
from typing import Optional, Type
import json

import lat_long_pb2
import lat_long_pb2_grpc
import users_pb2
import users_pb2_grpc
from concurrent import futures


class FoodAPI:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro", convert_system_message_to_human=True
        )
        self.prompt = hub.pull("hwchase17/structured-chat-agent")
        self.places_api = StructuredTool.from_function(
            func=self.run_places_api,
            name="restaurant API Tool",
            description="This tool allows you to query the Places API and get the results back. You can find restaurants and other places to eat near a given location. pass Address to get the restaurants near that location.",
        )
        self.P_tools = [self.places_api]
        self.agent = create_structured_chat_agent(self.llm, self.P_tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.P_tools, verbose=True
        )

    def POI_API(self, lat=24.43791667, lon=77.15891667):
        # if task is None:
        #     # Handle case when task is not provided
        #     lat = 24.43791667  # default value if not provided
        #     lon = 77.15891667  # default value if not provided
        # else:
        #     task_dict = json.loads(task)
        #     input_dict = task_dict.get("input", {})
        #     lat = input_dict.get("latitude", 24.43791667)  # default value if not provided
        #     lon = input_dict.get("longitude", 77.15891667)  # default value if not provided

        # print("Will try to greet world ...")
        with grpc.insecure_channel("localhost:50054") as channel:
            stub = users_pb2_grpc.UsersStub(channel)
            response = stub.RestaurantSearch(
                users_pb2.RestaurantSearchRequest(
                    lat=lat,
                    lon=lon,
                    categorySet=7315,
                    view="IN",
                    relatedPois="off",
                    key=str(os.getenv("TOMTOM_API_KEY")),
                    limit=4,
                )
            )
        return response.response

    def Lat_Long_API(self, add: str):
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = lat_long_pb2_grpc.LatLongServiceStub(channel)
            future = stub.GetLatLong.future(
                lat_long_pb2.LatLon_req(
                    address=add,
                )
            )
            response = future.result()
        response_dict = {
            "latitude": response.latitude,
            "longitude": response.longitude,
        }
        json_response = json.dumps(response_dict)
        print(json_response)
        return json_response

    # Places API Tool--------------------------------------------------
    def run_places_api(self, a: str):
        try:
            json_dump_lat_long = self.Lat_Long_API(a)
        except Exception as e:
            return str(e)
        lat_long_dict = json.loads(json_dump_lat_long)
        try:
            api_response = self.POI_API(
                lat_long_dict["latitude"], lat_long_dict["longitude"]
            )
            api_response_dict = json.loads(api_response)  # convert string to dictionary
            return self.extract_place_info(api_response_dict)
        except Exception as e:
            return str(e)

    def extract_place_info(self, api_response):
        places_info = []
        for result in api_response["results"]:
            place_info = {
                "name": result["poi"]["name"],
                "latitude": result["position"]["lat"],
                "longitude": result["position"]["lon"],
            }
            places_info.append(place_info)
        return places_info

    def get_food(self, address: str):
        x = self.agent_executor.invoke(
            {
                "input": f"""give me restaurants at Address: {{{address}}}. Use the restaurant API Tool. Return the name, latitude, and longitude of the restaurants."""
            }
        )
        return x["output"]


# print(FoodAPI().get_food("Railway Station Hyderabad, India"))
