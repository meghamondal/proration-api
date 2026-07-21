from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ProrationRequest(BaseModel):
    old_price: float
    new_price: float
    days_remaining: int
    days_in_actual_month: int
    spec: str


def calculate_charge(req: ProrationRequest):

    difference = req.new_price - req.old_price

    if req.spec == "v1":
        charge = difference * (req.days_remaining / 30)

    elif req.spec == "v2":
        charge = difference * (
            req.days_remaining / req.days_in_actual_month
        )

    else:
        return {"error": "Invalid spec"}

    return {"charge": round(charge, 2)}


@app.post("/")
def root(req: ProrationRequest):
    return calculate_charge(req)


@app.post("/proration")
def proration(req: ProrationRequest):
    return calculate_charge(req)


@app.post("/charge")
def charge(req: ProrationRequest):
    return calculate_charge(req)