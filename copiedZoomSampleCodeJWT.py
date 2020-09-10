import http.client

conn = http.client.HTTPSConnection("api.zoom.us")

headers = {
    'authorization': "Bearer pP13W03hT7CLEKpVZqZBLw",
    'content-type': "application/json"
    }

conn.request("GET", "/v2/users/me", headers=headers)

res = conn.getresponse()
data = res.read()
decoded_data = data.decode("utf-8")
print(decoded_data)
