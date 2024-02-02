import os
import asyncio
import webbrowser

async def run_app():
    # Run the WebSocket server
    server_process = await asyncio.create_subprocess_exec(
        "python", "speech_to_text.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Wait for the server to start (you may need to adjust the waiting time)
    await asyncio.sleep(2)

    # Open the HTML file in a web browser
    webbrowser.open("file://" + os.path.abspath("speech_to_text.html"))

    # Wait for the user to close the web browser
    await asyncio.gather(server_process.wait())

if __name__ == "__main__":
    asyncio.run(run_app())
