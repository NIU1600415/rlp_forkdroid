import requests
from typing import TypedDict, Literal


class MessageFromClient(TypedDict):
    type: Literal["CALIBRATE_TARGET", "CALIBRATE_DESTINATION"]
    data: None | int


class CalibrationData(TypedDict):
    upper: str
    lower: str


class MessageToClient(TypedDict):
    type: Literal["CALIB_DATA_TARGET", "CALIB_DATA_DESTINATION"]
    data: CalibrationData


class ClientMessaging:
    def __init__(self, endpoint="http://localhost:3006"):
        self.endpoint = endpoint
        self.available_messages: list[MessageFromClient] = []

    def update(self):
        try:
            resp = requests.get(f"{self.endpoint}/queue/outgoing")
            if resp.status_code == 200:
                self.available_messages.append(resp.json())
        except (ConnectionRefusedError, requests.exceptions.ConnectionError):
            print("Server offline.")

    def message_ready(self):
        return len(self.available_messages) > 0

    def read_message(self):
        """Returns first available message"""
        return self.available_messages.pop(0)

    def send(self, message: MessageToClient):
        r = requests.post(f"{self.endpoint}/queue/incoming",
                          json=message)
        print(
            f"STATEMACHINE sent message: {message}", r.request.body, r.status_code)
