import requests
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
	respond = requests.get(api_url, headers={'X-Api-Key': 'UJZFFheG86lfY8Ol+/ds3A==5MGSoraTQj4jIVCG'})
	return (respond)

plane_dict = response().json()
print(plane_dict)
current_plane = plane_dict[0]
x = plane_dict[0]
print(x["manufacturer"])



"""if __name__ == "__main__":
	plane_dict = response().json()
	for i in range(len(plane_dict)):
		current_plane = plane_dict[i]
		print(f"{current_plane}")
		#print (f"{current_plane.get('manufacturer')}, {current_plane.get('model')}")


response = requests.get(api_url, headers={'X-Api-Key': 'UJZFFheG86lfY8Ol+/ds3A==5MGSoraTQj4jIVCG'})
if response.status_code == requests.codes.ok:
    print(response.text)else:
    print("Error:", response.status_code, response.text)
    
    
     plane_dict = response.json()
        current_plane = plane_dict[0]
        value_list = []
        print(current_plane.values())
        for x in current_plane.values():
            value_list.append = x
            
"""
