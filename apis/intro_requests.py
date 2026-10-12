# ============================================================
# HTTP Requests - GET with the requests Library
# ============================================================
# HTTP Status Codes:
#   200 OK              201 Created         204 No Content
#   400 Bad Request      401 Unauthorized    403 Forbidden
#   404 Not Found        500 Server Error    503 Unavailable
# ============================================================

import requests

base_url = "https://pokeapi.co/api/v2/"

# ------------------------------------------------------------
# Single GET Request with Status Code Handling
# ------------------------------------------------------------

# Define a Pokémon name (can be replaced with user input)
pokemon_name = "nonexistentpokemon"  # Example: a Pokémon that doesn't exist

# Construct the URL to fetch data
url = f"{base_url}pokemon/{pokemon_name}"

# Send GET request to the API
response = requests.get(url)

# Handle the response based on the status code
if response.status_code == 200:
    # Successful request
    data = response.json()
    print(f"Name: {data['name'].capitalize()}")
    print(f"Height: {data['height']} m")
    print(f"Weight: {data['weight']} hectograms")
    print("Types:")
    for type_info in data['types']:
        print(f"- {type_info['type']['name'].capitalize()}")
else:
    # Handle errors based on status code
    if response.status_code == 400:
        print("Bad Request: The request might have an issue with the endpoint or parameters.")
    elif response.status_code == 404:
        print(f"Not Found: The Pokémon '{pokemon_name}' does not exist.")
    elif response.status_code == 500:
        print("Server Error: Something went wrong on the server. Please try again later.")
    else:
        print(f"Error {response.status_code}: Please check your request and try again.")

# ------------------------------------------------------------
# Iterating Over Multiple Requests
# ------------------------------------------------------------

pokemon_names = ["pikachu", "bulbasaur", "charmander", "squirtle"]

# Iterate through a list of Pokémon names
for pokemon_name in pokemon_names:
    url = f"{base_url}pokemon/{pokemon_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Name: {data['name'].capitalize()}")
        print(f"Height: {data['height']} m")
        print(f"Weight: {data['weight']} hectograms")
        print("Types:")
        for type_info in data['types']:
            print(f"- {type_info['type']['name'].capitalize()}")
        print("-" * 40)
    else:
        print(f"Failed to fetch data for {pokemon_name}")


# ------------------------------------------------------------
# Fetching by ID with a Reusable Function
# ------------------------------------------------------------
def fetch_pokemon_info(pokemon_id):
    response = requests.get(f"{base_url}pokemon/{pokemon_id}")
    if response.status_code == 200:
        return response.json()  # Return the JSON data if successful
    else:
        return None


# Iterate through the first 20 Pokémon by ID
for i in range(1, 21):
    pokemon_info = fetch_pokemon_info(i)
    if pokemon_info:
        print(f"Pokémon #{i}: {pokemon_info['name'].capitalize()}")
        print(f"ID: {pokemon_info['id']}")
        print(f"Height: {pokemon_info['height']} m")
        print(f"Weight: {pokemon_info['weight']} hectograms")
        print(f"Types: {[t['type']['name'] for t in pokemon_info['types']]}")
        print("-----")

# ------------------------------------------------------------
# Filtering by Type - Nested JSON Traversal
# ------------------------------------------------------------
type_name = "fire"
url = f"{base_url}type/{type_name}"

response = requests.get(url)

# Check if the request for the Pokémon type was successful
if response.status_code == 200:
    data = response.json()
    print(f"{type_name.capitalize()} type Pokémon:")
    for pokemon in data['pokemon']:
        print(f"- {pokemon['pokemon']['name'].capitalize()}")
else:
    print(f"Failed to fetch data for {type_name} type Pokémon.")
