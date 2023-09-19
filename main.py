from websockets.sync.client import connect
import time
import random
import payloads
import constants


def heartbeat():
    with connect(constants.GATEWAY_URL) as ws:

        # Send initial payload and get heartbeat interval
        payload = payloads.GenericEventPayload(ws.recv())
        heartbeat_interval = payload.response['d']['heartbeat_interval'] / 1000

        # Wait until first heartbeat
        jitter = random.uniform(0, 1)
        sleep_time = jitter * (heartbeat_interval)
        time.sleep(jitter * sleep_time)

        while 1:
            payloads.heartbeat(ws, heartbeat_interval)
            time.sleep(heartbeat_interval)

        return ws


def main():
    heartbeat()


if __name__ == "__main__":
    main()
