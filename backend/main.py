from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio
import random
import time

app = FastAPI()

# CIRCUIT BREAKER CLASS

class CircuitBreaker:

    def __init__(self, failure_threshold=3, recovery_time=10):

        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time

        self.failure_count = 0
        self.last_failure_time = None

        self.state = "CLOSED"

    def can_request(self):

        if self.state == "OPEN":

            elapsed = time.time() - self.last_failure_time

            if elapsed > self.recovery_time:

                self.state = "HALF_OPEN"

                return True

            return False

        return True

    def success(self):

        self.failure_count = 0

        self.state = "CLOSED"

    def failure(self):

        self.failure_count += 1

        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:

            self.state = "OPEN"


breaker = CircuitBreaker()

# MIDDLEWARE HEADER

@app.middleware("http")
async def add_student_id_header(request, call_next):

    response = await call_next(request)

    response.headers["X-Student-ID"] = "23149"

    return response
# HOME ROUTE

@app.get("/")
async def home():

    return {
        "message": "StudySync Backend Running"
    }

# FAKE LLM API

async def fake_llm_call():

    # 70% chance of failure

    if random.random() < 0.7:

        await asyncio.sleep(3)

        raise Exception("LLM API failed")

    return "LLM Success Response"
# ASK ROUTE

@app.get("/ask")
async def ask_ai():

    if not breaker.can_request():

        return JSONResponse(
            status_code=503,
            content={
                "message": "Circuit OPEN - LLM unavailable"
            }
        )

    try:

        result = await fake_llm_call()

        breaker.success()

        return {
            "response": result
        }

    except Exception:

        breaker.failure()

        return JSONResponse(
            status_code=500,
            content={
                "message": "LLM Failure"
            }
        )