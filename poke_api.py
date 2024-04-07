'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests
import os
POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_into() function
    # Use breakpoints to view returned dictionary
    poke_info = get_pokemon_info("Rockruff")
    return

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object,
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters
    pokemon = str(pokemon).strip().lower()

    # Check if Pokemon name is an empty string
    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return

    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')

    # TODO: Define function that gets a list of all Pokemon names from the PokeAPI
def get_pokemon_names():
    url = POKE_API_URL + "?limit=1000"
    resp_msg = requests.get(url)
    if resp_msg.status_code == requests.codes.ok:
        pokemon_data = resp_msg.json()
        pokemon_names = [pokemon['name'].capitalize() for pokemon in pokemon_data['results']]
        return pokemon_names
    else:
        print('Failed to fetch Pokemon names.')
        return []

    # TODO: Define function that downloads and saves Pokemon artwork
def download_pokemon_artwork(pokemon_name, directory):
    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_name.lower()}.png"
    if not os.path.exists(directory):
        os.makedirs(directory)

    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        filename = os.path.join(directory, f"{pokemon_name}.png")
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download artwork for {pokemon_name}.")

if __name__ == '__main__':
    main()