from websockets.sync.client import ClientConnection, connect
import payloads
import asyncio
import heartbeat
import constants


def main():
    TOKEN = ""

    ws: ClientConnection = connect(constants.GATEWAY_URL)

    asyncio.run(heartbeat.start(ws))
    # identify_payload = payloads.IdentifyPayload(TOKEN, [])


if __name__ == "__main__":
    main()
