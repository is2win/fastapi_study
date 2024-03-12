import requests
r = requests.get("http://127.0.0.1:8000/hotels/1",
                 params={'date_from': 'today', 'date_to': 'tom'})
print(r.text)
