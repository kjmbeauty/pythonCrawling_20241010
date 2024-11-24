import requests

server_url = "https://api.upbit.com"
#https://api.upbit.com/v1/ticker

params = {
    "markets": "KRW-BTC"  #비트코인 ticker
}

res = requests.get(server_url + "/v1/ticker", params=params)
print(res.json())
print("-----")



