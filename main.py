from datetime import date, datetime
from cachetools import Cache

from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel


# maxsize is the size of data the Cache can hold
cache_data = Cache(maxsize=50000)


class UssdRequest(BaseModel):
    sessionID: str
    userID: str
    newSession: bool
    msisdn: str
    userData: str | None = None
    network: str


class UssdResponse(BaseModel):
    sessionID: str | None = None
    userID: str | None = None
    continueSession: bool | None = None
    msisdn: str | None = None
    message: str | None = None


class UssdState(BaseModel):
    sessionID: str
    message: str
    newSession: bool
    msisdn: str
    userData: str | None = None
    network: str
    message: str
    level: int
    part: int


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/ussd")
async def handle_ussd(ussd_request: UssdRequest):
    response = UssdResponse(
        sessionID=ussd_request.sessionID,
        userID=ussd_request.userID,
        msisdn=ussd_request.msisdn,
    )

    if ussd_request.newSession:
        response.message = (
            "Welcome to Arkesel Voting Portal. Please vote for your favourite service from Arkesel"
            + "\n1. SMS"
            + "\n2. Voice"
            + "\n3. Email"
            + "\n4. USSD"
            + "\n5. Payments"
        )
        response.continueSession = True

        # Keep track of the USSD state of the user and their session

        current_state = UssdState(
            sessionID=ussd_request.sessionID,
            msisdn=ussd_request.msisdn,
            userData=ussd_request.userData,
            network=ussd_request.network,
            message=response.message,
            level=1,
            part=1,
            newSession=True,
        )

        user_response_tracker = cache_data.get(hash(ussd_request.sessionID), [])

        user_response_tracker.append(current_state)

        cache_data[hash(ussd_request.sessionID)] = user_response_tracker
    else:
        last_response = cache_data.get(hash(ussd_request.sessionID), [])[-1]

        if last_response.level == 1:
            user_data = ussd_request.userData

            if user_data == "1":
                response.message = (
                    "For SMS which of the features do you like best?"
                    + "\n1. From File"
                    + "\n2. Quick SMS"
                    + "\n\n #. Next Page"
                )
                response.continueSession = True

                # Keep track of the USSD state of the user and their session

                current_state = UssdState(
                    sessionID=ussd_request.sessionID,
                    msisdn=ussd_request.msisdn,
                    userData=ussd_request.userData,
                    network=ussd_request.network,
                    message=response.message,
                    level=2,
                    part=1,
                    newSession=ussd_request.newSession,
                )

                user_response_tracker = cache_data.get(hash(ussd_request.sessionID), [])

                user_response_tracker.append(current_state)

                cache_data[hash(ussd_request.sessionID)] = user_response_tracker
            elif (
                user_data == "2"
                or user_data == "3"
                or user_data == "4"
                or user_data == "5"
            ):
                response.message = "Thank you for voting!"
                response.continueSession = False
            else:
                response.message = "Bad choice!"
                response.continueSession = False
        elif last_response.level == 2:
            possible_choices = ["1", "2", "3", "4"]

            if last_response.part == 1 and ussd_request.userData == "#":
                response.message = (
                    "For SMS which of the features do you like best?"
                    + "\n3. Bulk SMS"
                    + "\n\n*. Go Back"
                    + "\n#. Next Page"
                )
                response.continueSession = True

                current_state = UssdState(
                    sessionID=ussd_request.sessionID,
                    msisdn=ussd_request.msisdn,
                    userData=ussd_request.userData,
                    network=ussd_request.network,
                    message=response.message,
                    level=2,
                    part=2,
                    newSession=ussd_request.newSession,
                )

                user_response_tracker = cache_data.get(hash(ussd_request.sessionID), [])

                user_response_tracker.append(current_state)

                cache_data[hash(ussd_request.sessionID)] = user_response_tracker
            elif last_response.part == 2 and ussd_request.userData == "#":
                response.message = (
                    "For SMS which of the features do you like best?"
                    + "\n4. SMS To Contacts"
                    + "\n\n*. Go Back"
                )
                response.continueSession = True

                current_state = UssdState(
                    sessionID=ussd_request.sessionID,
                    msisdn=ussd_request.msisdn,
                    userData=ussd_request.userData,
                    network=ussd_request.network,
                    message=response.message,
                    level=2,
                    part=3,
                    newSession=ussd_request.newSession,
                )

                user_response_tracker = cache_data.get(hash(ussd_request.sessionID), [])

                user_response_tracker.append(current_state)

                cache_data[hash(ussd_request.sessionID)] = user_response_tracker
            elif last_response.part == 3 and ussd_request.userData == "*":
                response.message = (
                    "For SMS which of the features do you like best?"
                    + "\n3. Bulk SMS"
                    + "\n\n*. Go Back"
                    + "\n#. Next Page"
                )
                response.continueSession = True

                current_state = UssdState(
                    sessionID=ussd_request.sessionID,
                    msisdn=ussd_request.msisdn,
                    userData=ussd_request.userData,
                    network=ussd_request.network,
                    message=response.message,
                    level=2,
                    part=2,
                    newSession=ussd_request.newSession,
                )

                user_response_tracker = cache_data.get(hash(ussd_request.sessionID), [])

                user_response_tracker.append(current_state)

                cache_data[hash(ussd_request.sessionID)] = user_response_tracker
            elif last_response.part == 2 and ussd_request.userData == "*":
                response.message = (
                    "For SMS which of the features do you like best?"
                    + "\n1. From File"
                    + "\n2. Quick SMS"
                    + "\n\n #. Next Page"
                )
                response.continueSession = True

                # Keep track of the USSD state of the user and their session

                current_state = UssdState(
                    sessionID=ussd_request.sessionID,
                    msisdn=ussd_request.msisdn,
                    userData=ussd_request.userData,
                    network=ussd_request.network,
                    message=response.message,
                    level=2,
                    part=1,
                    newSession=ussd_request.newSession,
                )

                user_response_tracker = cache_data.get(hash(ussd_request.sessionID), [])

                user_response_tracker.append(current_state)

                cache_data[hash(ussd_request.sessionID)] = user_response_tracker
            elif ussd_request.userData in possible_choices:
                response.message = "Thank you for voting!"
                response.continueSession = False
            else:
                response.message = "Bad choice!"
                response.continueSession = False

    return response
