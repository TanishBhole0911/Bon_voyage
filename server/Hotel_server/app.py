from concurrent import futures
import grpc
import users_pb2
import users_pb2_grpc
import requests
import json
import redis

r = redis.Redis(host="localhost", port=6379, db=0)


class Users(users_pb2_grpc.UsersServicer):
    def GetUsers(self, request, context):
        return users_pb2.GetUsersResponse(
            users=[
                users_pb2.User(
                    id="1", name="John Doe", email="abc@gmail.com", password="123456"
                )
            ]
        )

    def RestaurantSearch(self, request, context):
        cached_response = r.get(f"{request.lat},{request.lon}")
        if cached_response is not None:
            print("Processed from Redis cache")
            return users_pb2.RestaurantSearchResponse(response=cached_response.decode())

        url = "https://api.tomtom.com/search/2/poiSearch/hotel.json"
        params = {
            "lat": request.lat,
            "lon": request.lon,
            "categorySet": request.categorySet,
            "view": request.view,
            "relatedPois": request.relatedPois,
            "key": request.key,
            "limit": request.limit,
        }
        headers = {"Accept": "*/*"}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            beautified_response = json.dumps(response.json(), indent=4)
            print("Logged: " + beautified_response)
            # Store the response in the Redis cache and set an expiration time of 1 hour
            r.set(f"{request.lat},{request.lon}", beautified_response, ex=3600)
            print("Processed from external API and stored in Redis cache")

            return users_pb2.RestaurantSearchResponse(response=beautified_response)

        else:
            print(response.text)
            context.abort(
                grpc.StatusCode.ABORTED,
                "Request to TomTom API failed with status code {}: {}".format(
                    response.status_code, response.text
                ),
            )


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServicer_to_server(Users(), server)
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
