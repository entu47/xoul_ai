import random
import time
import os
import signal
import argparse
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

if random.random() < 0.02:
    raise Exception("Failed to start the API with a 1% probability.")


def potentially_crash_api():
    if random.random() < 0.005:
        os.kill(os.getpid(), signal.SIGINT)
        raise SystemExit("API failed completely and is exiting.")


@app.get("/health")
async def health():
    potentially_crash_api()  
    return JSONResponse(content={"status": "ok"}, status_code=200)


@app.post("/v1/completions")
async def completions(request: Request):
    potentially_crash_api()
    
    sleep_time = random.triangular(1, 20, 5)
    time.sleep(sleep_time)
 
    return {"choices": [{"text": "EXAMPLE_RESPONSE"}], "_time": sleep_time}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the server")
    parser.add_argument("-p", "--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()

    uvicorn.run(app, host="127.0.0.1", port=args.port)
