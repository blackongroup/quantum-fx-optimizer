import os
from oandapyV20 import API
from oandapyV20.endpoints.orders import OrderCreate

TOKEN = os.getenv("OANDA_TOKEN")
ACCOUNT = os.getenv("OANDA_ACCOUNT")
CLIENT = API(access_token=TOKEN)

def execute(allocations, prices):
    total = sum(prices.values())
    for pair, w in allocations.items():
        notional = total * w
        units = int(notional / prices[pair])
        order = {
            "order": {
                "instrument": pair,
                "units": str(units),
                "type": "MARKET",
                "positionFill": "REDUCE_ONLY"
            }
        }
        CLIENT.request(OrderCreate(ACCOUNT, data=order))
