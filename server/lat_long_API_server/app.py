from concurrent import futures
import grpc
import lat_long_pb2
import lat_long_pb2_grpc
import requests
import os
from dotenv import load_dotenv
import redis

r = redis.Redis(host="localhost", port=6379, db=0)

load_dotenv()


class Lat_long(lat_long_pb2_grpc.LatLongServiceServicer):
    def GetLatLong(self, request, context):
        # Check if the response for this address is in the Redis cache
        cached_response = r.get(request.address)
        if cached_response is not None:
            print("\033[32mProcessed from Redis cache\033[0m")
            return lat_long_pb2.LatLon_res().FromString(cached_response)

        api_key = os.getenv("TOMTOM_API_KEY")
        url = f"https://api.tomtom.com/search/2/geocode/{request.address}.json?key={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            context.abort(grpc.StatusCode.UNAVAILABLE, "TomTom API is unavailable")
        data = response.json()
        if not data.get("results"):
            context.abort(
                grpc.StatusCode.NOT_FOUND, "No results found for the given address"
            )
        latitude = data["results"][0]["position"]["lat"]
        longitude = data["results"][0]["position"]["lon"]

        # Create the response
        res = lat_long_pb2.LatLon_res(latitude=latitude, longitude=longitude)

        # Store the response in the Redis cache and set an expiration time of 1 hour
        r.set(request.address, res.SerializeToString(), ex=3600)
        print("\033[33mProcessed from external API and stored in Redis cache\033[0m")

        return res


def serve():
    port = "50052"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lat_long_pb2_grpc.add_LatLongServiceServicer_to_server(Lat_long(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
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
