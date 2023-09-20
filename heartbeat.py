import payloads
import asyncio
import random


async def start(ws):

    # Send initial payload and get heartbeat interval
    payload = payloads.GenericEventPayload(ws.recv())
    heartbeat_interval = payload.response['d']['heartbeat_interval'] / 1000

    # Wait until first heartbeat
    sleep_time = random.uniform(0, 1) * heartbeat_interval
    await asyncio.sleep(sleep_time)

    # Heartbeat
    while True:
        try:
            heartbeat_payload = payloads.HeartbeatPayload()
            heartbeat_payload.send(ws)
        except TimeoutError as e:
            ws.close(1006)
            print(e)
        else:
            await asyncio.sleep(heartbeat_interval)
