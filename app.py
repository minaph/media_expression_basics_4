
import asyncio
import websockets

device = None
web = None

# async def ping(websocket):
#     while True:
#         await websocket.send('{"message":"PING"}')
#         print('------ ping')
#         await asyncio.sleep(5)

async def echo(websocket):
    global device
    global web
    print(websocket.path)
    # async for message in websocket:
    #     await websocket.send(message)
    if websocket.path == '/device':
        device = websocket
        await device.send('Hello')

        
        while True:
            if web:
                try:
                    message = await device.recv()
                    await web.send(message)
                except websockets.exceptions.ConnectionClosed:
                    break
            else: 
                print("web not connected")
            # await asyncio.sleep(0.1)
        

    elif websocket.path == '/web':
        web = websocket
        # asyncio.create_task(ping(websocket))
        await web.send('Hello!')
        while True:
            try:
                message = await web.recv()
                # await device.send(message)
                # await asyncio.sleep(0.1)
            except websockets.exceptions.ConnectionClosed as e:
                break
    return

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())

