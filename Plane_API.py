import requests
import os

x = 0
y = 10001
search_criteria = "MinMax range"

if search_criteria == "Manufacturer and model":
	api_url = 'https://api.api-ninjas.com/v1/aircraft?manufacturer={}&model={}&limit={}'.format(x,y,30)
elif search_criteria == "MinMax speed":
	api_url = 'https://api.api-ninjas.com/v1/aircraft?min_speed={}&max_speed={}&limit={}'.format(x,y,30)
elif search_criteria == "MinMax range":
	api_url = 'https://api.api-ninjas.com/v1/aircraft?min_range={}&max_range={}&limit={}'.format(x,y,30)
elif search_criteria == "MinMax length":
	api_url = 'https://api.api-ninjas.com/v1/aircraft?min_length={}&max_length={}&limit={}'.format(x,y,30)
elif search_criteria == "MinMax height":
	api_url = 'https://api.api-ninjas.com/v1/aircraft?min_height={}&max_height={}&limit={}'.format(x,y,30)
elif search_criteria == "MinMax Wingspan":
	api_url = 'https://api.api-ninjas.com/v1/aircraft?min_wingspan={}&max_wingspan={}&limit={}'.format(x,y,30)


# 'https://api.api-ninjas.com/v1/aircraft?manufacturer={}&model={}

def response():
	API_KEY = os.getenv("API_KEY")
	respond = requests.get(api_url, headers={'X-Api-Key': API_KEY})
	return (respond)

plane_dict = response().json()
print(plane_dict)
current_plane = plane_dict[0]
x = plane_dict[0]
print(x["manufacturer"])

