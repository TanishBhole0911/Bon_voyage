import requests
import grpc
import lat_long_pb2
import lat_long_pb2_grpc
import os
from concurrent import futures
import json


def call_api():
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = lat_long_pb2_grpc.LatLongServiceStub(channel)
        future = stub.GetLatLong.future(lat_long_pb2.LatLon_req(address="Indore"))
        response = future.result()
    # Manually extract the fields from the response
    response_dict = {
        "latitude": response.latitude,
        "longitude": response.longitude,
        # Add other fields as needed
    }
    json_response = json.dumps(response_dict)
    print(json_response)
    return json_response


if __name__ == "__main__":
    call_api()
