import asyncio
import websockets
import speech_recognition as sr
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

#python -m uvicorn main:app --reload

app = FastAPI()
html_file_path = "speech_to_text.html"
text = ""
init_flag = False
with open(html_file_path, "r") as html_file:
    html = html_file.read()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# html_file_path = "speech_to_text.html"
# # text = ""
# # init_flag = False
# with open(html_file_path, "r") as html_file:
#     html = html_file.read()

async def speech_to_text(websocket: WebSocket):
    init_rec = sr.Recognizer()

    # LOOPING BIAR KONEKSINYA GA BERENTI
    # while True:
    with sr.Microphone() as source:
        init_rec.pause_threshold = 0.7
        audio_data = init_rec.adjust_for_ambient_noise(source)
        print("katakan sesuatu..")

        try:
            text = recog(init_rec, source)
            print(text)

            # Send the recognized text to the connected WebSocket client
            await websocket.send_text(text)

        except sr.UnknownValueError:
            print("Speech Recognition did not understand the voice")
        except sr.WaitTimeoutError:
            print("Listening timed out. No speech detected.")

        #if close dipencet, maka berhenti di backendnya juga

def recog(init_rec, source):
    audio_data = init_rec.listen(source, timeout=3, phrase_time_limit=None)
    print("....")
    return init_rec.recognize_google(audio_data, language="id-ID")

# FastAPI WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # await manager.connect(websocket)
    await websocket.accept()    
    while True:
        await speech_to_text(websocket)

    #gimana caranya selesaiin di backend bejir

@app.get("/")
async def get():
    return HTMLResponse(html)

# Start the WebSocket server
# start_server = websockets.serve(speech_to_text, "localhost", 8000)
# async def echo_server(stop):
#     async with websockets.serve(speech_to_text, "localhost", 8000):
#         await stop


if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(echo_server(stop))
    # asyncio.get_event_loop().run_forever()
    uvicorn.run(app, host="localhost", port=8000)
    # asyncio.get_event_loop().run_until_complete(echo_server(stop))
# Run FastAPI
# if __name__ == "__main__":

