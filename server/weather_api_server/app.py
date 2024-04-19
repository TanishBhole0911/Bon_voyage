import grpc
from concurrent import futures
import weather_pb2 as pb2
import weather_pb2_grpc as pb2_grpc
import json
import requests
from dotenv import load_dotenv
import os
import redis

r = redis.Redis(host="localhost", port=6379, db=0)

load_dotenv()
# Import the generated gRPC classes

weatherCodeDay = {
    "0": "Unknown",
    "10000": "Clear, Sunny",
    "11000": "Mostly Clear",
    "11010": "Partly Cloudy",
    "11020": "Mostly Cloudy",
    "10010": "Cloudy",
    "11030": "Partly Cloudy and Mostly Clear",
    "21000": "Light Fog",
    "21010": "Mostly Clear and Light Fog",
    "21020": "Partly Cloudy and Light Fog",
    "21030": "Mostly Cloudy and Light Fog",
    "21060": "Mostly Clear and Fog",
    "21070": "Partly Cloudy and Fog",
    "21080": "Mostly Cloudy and Fog",
    "20000": "Fog",
    "42040": "Partly Cloudy and Drizzle",
    "42030": "Mostly Clear and Drizzle",
    "42050": "Mostly Cloudy and Drizzle",
    "40000": "Drizzle",
    "42000": "Light Rain",
    "42130": "Mostly Clear and Light Rain",
    "42140": "Partly Cloudy and Light Rain",
    "42150": "Mostly Cloudy and Light Rain",
    "42090": "Mostly Clear and Rain",
    "42080": "Partly Cloudy and Rain",
    "42100": "Mostly Cloudy and Rain",
    "40010": "Rain",
    "42110": "Mostly Clear and Heavy Rain",
    "42020": "Partly Cloudy and Heavy Rain",
    "42120": "Mostly Cloudy and Heavy Rain",
    "42010": "Heavy Rain",
    "51150": "Mostly Clear and Flurries",
    "51160": "Partly Cloudy and Flurries",
    "51170": "Mostly Cloudy and Flurries",
    "50010": "Flurries",
    "51000": "Light Snow",
    "51020": "Mostly Clear and Light Snow",
    "51030": "Partly Cloudy and Light Snow",
    "51040": "Mostly Cloudy and Light Snow",
    "51220": "Drizzle and Light Snow",
    "51050": "Mostly Clear and Snow",
    "51060": "Partly Cloudy and Snow",
    "51070": "Mostly Cloudy and Snow",
    "50000": "Snow",
    "51010": "Heavy Snow",
    "51190": "Mostly Clear and Heavy Snow",
    "51200": "Partly Cloudy and Heavy Snow",
    "51210": "Mostly Cloudy and Heavy Snow",
    "51100": "Drizzle and Snow",
    "51080": "Rain and Snow",
    "51140": "Snow and Freezing Rain",
    "51120": "Snow and Ice Pellets",
    "60000": "Freezing Drizzle",
    "60030": "Mostly Clear and Freezing drizzle",
    "60020": "Partly Cloudy and Freezing drizzle",
    "60040": "Mostly Cloudy and Freezing drizzle",
    "62040": "Drizzle and Freezing Drizzle",
    "62060": "Light Rain and Freezing Drizzle",
    "62050": "Mostly Clear and Light Freezing Rain",
    "62030": "Partly Cloudy and Light Freezing Rain",
    "62090": "Mostly Cloudy and Light Freezing Rain",
    "62000": "Light Freezing Rain",
    "62130": "Mostly Clear and Freezing Rain",
    "62140": "Partly Cloudy and Freezing Rain",
    "62150": "Mostly Cloudy and Freezing Rain",
    "60010": "Freezing Rain",
    "62120": "Drizzle and Freezing Rain",
    "62200": "Light Rain and Freezing Rain",
    "62220": "Rain and Freezing Rain",
    "62070": "Mostly Clear and Heavy Freezing Rain",
    "62020": "Partly Cloudy and Heavy Freezing Rain",
    "62080": "Mostly Cloudy and Heavy Freezing Rain",
    "62010": "Heavy Freezing Rain",
    "71100": "Mostly Clear and Light Ice Pellets",
    "71110": "Partly Cloudy and Light Ice Pellets",
    "71120": "Mostly Cloudy and Light Ice Pellets",
    "71020": "Light Ice Pellets",
    "71080": "Mostly Clear and Ice Pellets",
    "71070": "Partly Cloudy and Ice Pellets",
    "71090": "Mostly Cloudy and Ice Pellets",
    "70000": "Ice Pellets",
    "71050": "Drizzle and Ice Pellets",
    "71060": "Freezing Rain and Ice Pellets",
    "71150": "Light Rain and Ice Pellets",
    "71170": "Rain and Ice Pellets",
    "71030": "Freezing Rain and Heavy Ice Pellets",
    "71130": "Mostly Clear and Heavy Ice Pellets",
    "71140": "Partly Cloudy and Heavy Ice Pellets",
    "71160": "Mostly Cloudy and Heavy Ice Pellets",
    "71010": "Heavy Ice Pellets",
    "80010": "Mostly Clear and Thunderstorm",
    "80030": "Partly Cloudy and Thunderstorm",
    "80020": "Mostly Cloudy and Thunderstorm",
    "80000": "Thunderstorm",
}


# Define your gRPC service by inheriting from the generated service class
class Weather_api(pb2_grpc.LatLongServiceServicer):
    def GetForcasteWeather(self, request, context):

        # Redis Cache Check
        cached_response = r.get(request.address)
        if cached_response is not None:
            print("\033[32mProcessed from Redis cache\033[0m")
            return pb2.Forcaste_Weather_res().FromString(cached_response)

        # Implement your logic here
        # Access request data using request.attribute_name
        # Return a response using pb2.YourResponse(attribute_name=value)
        base_url = "https://api.tomorrow.io/v4/timelines"
        params = {
            "location": request.address,
            "timesteps": "1d",
            "apikey": os.getenv("TOMORROW"),
            "fields": "temperature,precipitationProbability,weatherCodeDay",
        }

        try:
            response = requests.get(base_url, params=params)
            print(response)
            response.raise_for_status()  # Raise an exception if the request failed

        except requests.exceptions.RequestException as e:
            print(f"Request to Tomorrow.io API failed: {e}")
            return pb2.Forcaste_Weather_res()  # Return an empty response
        try:
            data = response.json()["data"]["timelines"]
        except (KeyError, TypeError) as e:
            print(f"Unexpected response format from Tomorrow.io API: {e}")
            return pb2.Forcaste_Weather_res()  # Return an empty response

        # replace the weather code with the actual weather
        for i in range(len(data[0]["intervals"])):
            data[0]["intervals"][i]["values"]["weatherCodeDay"] = weatherCodeDay[
                str(data[0]["intervals"][i]["values"]["weatherCodeDay"])
            ]
            print(data[0]["intervals"][i]["values"]["weatherCodeDay"])

        res = pb2.Forcaste_Weather_res(
            timestep=data[0]["timestep"],
            startTime=data[0]["startTime"],
            endTime=data[0]["endTime"],
            intervals=data[0]["intervals"],
        )
        resp = res
        # Store the response in the Redis cache with 1hr timeout
        r.set(request.address, res.SerializeToString(), ex=3600)
        print("\033[33mProcessed from external API and stored in Redis cache\033[0m")

        return resp


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_LatLongServiceServicer_to_server(Weather_api(), server)
    server.add_insecure_port("[::]:50053")
    server.start()
    print("Server started, listening on 50053")
    # Nuke Cache when server is stopped
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        # Purge the Redis cache when the server is done
        r.flushdb()
        print("\033[91mRedis cache purged\033[0m")


if __name__ == "__main__":
    serve()
