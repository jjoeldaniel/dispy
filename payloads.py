from opcodes import GatewayOpcode
from json import loads, dumps
import util
from websockets.sync.client import ClientConnection


def heartbeat(ws: ClientConnection, interval: int, last_sequence={}):

    # HACK: Can we improve this?

    # Create reply
    reply = dumps({
        "op": GatewayOpcode.HEARTBEAT_SEND_RECEIVE.value,
        "d": last_sequence
    })

    # Send heartbeat
    ws.send(reply)
    print(util.load_filter(ws.recv()))


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
