import json
from flask import Blueprint, request, jsonify

from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from src.wkspace.mlearn_works import get_minute_data

mlearn = Blueprint("mlearn", __name__, url_prefix="/api/v1/mlearn")

@mlearn.get("/binancedata")
# @jwt_required()
def get_binance_data():
    symbol = request.args.get('symbol', '', type=str)
    interval = request.args.get('interval', '', type=str)
    lookback = request.args.get('lookback', '', type=str)

    # get the data (pandas frame returned)
    df = get_minute_data(symbol, interval, lookback)   # 'BTCBUSD', '1m', '30'

    # convert to json then to dict
    out = df.to_json(orient='table')
    out = json.loads(out)

    return jsonify({
        'meta' : {
            'info': 'binance_data',
            'symbol': symbol,
            'interval': interval,
            'lookback': lookback,
        },
        'output': out['data']
    }), HTTP_200_OK