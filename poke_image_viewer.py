"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""
from site import makepath
from tkinter import *
from tkinter import ttk
import os
import requests
from PIL import Image, ImageTk
import ctypes

# Get the script and images directory
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')

# TODO: Create the images directory if it does not exist
if not os.path.exists(images_dir):
    os.makedirs(images_dir)
# Create the main window
root = Tk()
root.title("Pokemon Viewer")

# TODO: Set the icon
root.iconbitmap(os.path.join(script_dir, 'pokemon_icon.ico'))


# TODO: Create frames
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0)

def fetch_pokemon_names():
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
    pokemon_data = response.json()
    pokemon_names = [pokemon['name'].capitalize() for pokemon in pokemon_data['results']]
    return pokemon_names

def fetch_pokemon_artwork(pokemon_name):
    # Fetch Pokémon artwork from PokéAPI
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    pokemon_data = response.json()
    image_url = pokemon_data['sprites']['other']['official-artwork']['front_default']
    return image_url

def download_image(url, filename):
    # Download image from URL and save it
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

        def set_as_desktop_image():
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(makepath), 0) 

# TODO: Populate frames with widgets and define event handler functions
pokemon_names = fetch_pokemon_names()
selected_pokemon = StringVar()
combobox = ttk.Combobox(frame, textvariable=selected_pokemon, values=pokemon_names)
combobox.grid(row=0, column=0)


default_image = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, "default_image.png")))
image_label = ttk.Label(frame, image=default_image)
image_label.grid(row=1, column=0)

set_as_desktop_button = ttk.Button(frame, text="Set as Desktop Image", state="disabled")
set_as_desktop_button.grid(row=2, column=0)


def combobox_selected(event):
    selected_pokemon_name = selected_pokemon.get()
    if selected_pokemon_name:
        image_url = fetch_pokemon_artwork(selected_pokemon_name)
        image_filename = f"{selected_pokemon_name}.png"
        image_path = os.path.join(images_dir, image_filename)
        download_image(image_url, image_path)
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo
        # Enable the "Set as Desktop Image" button
        set_as_desktop_button.config(state="normal")

        combobox.bind("<<ComboboxSelected>>", combobox_selected)

def set_as_desktop_image():
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(makepath), 0)

set_as_desktop_button.config(command=set_as_desktop_image)
root.mainloop()