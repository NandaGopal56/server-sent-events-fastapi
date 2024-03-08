from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, uvicorn
from asyncio import sleep

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def waypoints_generator():
    '''
    Note - Here \\n is intetionally added as to document the actual data instead of using i as new line.

    1. SSE messages are sent as a stream of text events, where each event is a separate piece of data. Each event consists of one or more lines. The minimum requirement for a line is to start with data: followed by the payload. Here's a simple example:
        data: This is a message\\n\\n

    2. SSE allows for optional fields in an event. Common fields include id, event, and retry. For example:
        id: 123
        event: customEvent
        data: Custom event message\\n\\n

    3.If the connection is closed, the client can attempt to reconnect. The server can include a retry field to suggest the time in milliseconds that the client should wait before attempting to reconnect.
        retry: 5000

    example.
    Below This format is necessary. Either event keyword or data keyword corresponding to that will be actual content
    
    ---------------------------------------

    yield f'event: ss\\ndata: food\\n\\n'

    data = {"eventNo": i, "message": "This is a message"}
    yield f"event: message\\ndata: {json.dumps(data)}\\n\\n"

    data = {"eventNo": i, "message": "This is a update"}
    yield f"event: update\\ndata: {json.dumps(data)}\\n\\n"

    '''
    waypoints = open('waypoints.json')
    waypoints = json.load(waypoints)
    for waypoint in waypoints[0: 10]:
        data = json.dumps(waypoint)
        yield f"event: locationUpdate\ndata: {data}\n\n"
        await sleep(1)



@app.get("/get-waypoints")
async def root():
    '''
    Set the Content-Type header to "text/event-stream" to indicate that the response should be interpreted as Server-Sent Events.
    '''
    return StreamingResponse(waypoints_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)