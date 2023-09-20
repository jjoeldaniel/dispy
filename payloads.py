from opcodes import GatewayOpcode
from json import loads, dumps
import util
import platform
import constants
from gateway_intents import GatewayIntents
from websockets.sync.client import ClientConnection


class GenericEventPayload():
    def __init__(
        self,
        response: dict
    ):
        response = loads(response)
        self.opcode: GatewayOpcode = response['op']
        self.event_data: dict = response['d']
        self.sequence: int = response['s']
        self.event_name: str = str(response['t']).upper()
        self.response = {
            "op": self.opcode,
            "d": self.event_data,
            "s": self.sequence,
            "t": self.event_name
        }


class HeartbeatPayload():
    def __init__(self, last_sequence: dict = {}):
        self.opcode = GatewayOpcode.HEARTBEAT_SEND_RECEIVE.value
        self.d = last_sequence
        self.json = dumps({
            "op": self.opcode,
            "d": self.d
        })

    def send(self, ws: ClientConnection):

        # Create reply
        reply = HeartbeatPayload()

        # Send heartbeat
        ws.send(reply.json)

        print(util.load_filter(ws.recv(timeout=15)))


class IdentifyPayload(GenericEventPayload):

    # TODO: Make Intents class

    def __init__(self, TOKEN: str, INTENTS: list[GatewayIntents]):
        self.opcode: GatewayOpcode = GatewayOpcode.IDENTIFY_SEND.value

        INTENTS = sum([x.value for x in INTENTS])

        self.event_data = {
            "token": TOKEN,
            "intents": INTENTS,
            "properties": {
                "os": platform.system(),
                "browser": constants.LIBRARY,
                "device": constants.LIBRARY
            }
        }
        self.response = {
            "op": self.opcode,
            "d": self.event_data,
            "s": self.sequence,
            "t": self.event_name
        }
