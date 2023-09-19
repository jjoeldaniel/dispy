from websockets.sync.client import connect
import random
import payloads
import constants
import asyncio


async def heartbeat():

    # NOTE: We should probably move this function

    with connect(constants.GATEWAY_URL) as ws:

        # Send initial payload and get heartbeat interval
        payload = payloads.GenericEventPayload(ws.recv())
        heartbeat_interval = payload.response['d']['heartbeat_interval'] / 1000

        # Wait until first heartbeat
        sleep_time = random.uniform(0, 1) * heartbeat_interval
        await asyncio.sleep(sleep_time)

        # Heartbeat
        while True:
            try:
                payloads.heartbeat(ws, heartbeat_interval)
            except TimeoutError as e:
                ws.close(1006)
                print(e)
            else:
                await asyncio.sleep(heartbeat_interval)


def main():
    asyncio.run(heartbeat())


if __name__ == "__main__":
    main()
