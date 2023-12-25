import random
import time
import pkg_resources
import os

# define ascii art class
class AsciiArt:
  def __init__(self, name, category, weather, rarity, artists, editors, source, original_art, new_art):
    self.name = name
    self.category = category
    self.weather = weather
    self.rarity = rarity
    self.artists = artists if artists else []
    self.editors = editors if editors else []
    self.source = source
    self.original_art = original_art
    self.new_art = new_art
    self.art_lines, self.height, self.width = self._split_art_and_get_dimensions()

  @staticmethod
  def load_from_file(file_path):
    with open(file_path, 'r') as file:
      lines = file.readlines()

    name = category = source = None
    weather = []
    artists = []
    editors = []
    rarity = 1

    original_art_lines = []
    new_art_lines = []
    is_new_art = False
    
    for line in lines:
      line = line.rstrip('\n')

      if line.startswith('[') and line.endswith(']'):
        current_section = line[1:-1].lower()
        is_new_art = current_section == 'new'
        continue

      if current_section == 'name':
        name = line.strip()
      elif current_section == 'category':
        category = line.strip()
      elif current_section == 'weather':
        weather = line.strip().split(', ') if line.strip() else []
      elif current_section == 'rarity':
        rarity = int(line.strip())
      elif current_section == 'artists':
        artists = [a.strip() for a in line.split(',')] if line.strip() else []
      elif current_section == 'editors':
        editors = [e.strip() for e in line.split(',')] if line.strip() else []
      elif current_section == 'retrieved from':
        source = line.strip()
      elif current_section == 'original' and not is_new_art:
        original_art_lines.append(line + '\n')
      elif is_new_art:
        new_art_lines.append(line + '\n')

    original_art = ''.join(original_art_lines)
    new_art = ''.join(new_art_lines)

    return AsciiArt(name, category, weather, rarity, artists, editors, source, original_art, new_art)

  def _split_art_and_get_dimensions(self):
    art_lines = self.new_art.split('\n') if self.new_art else self.original_art.split('\n')
    height = len(art_lines)
    width = len(art_lines[0]) if art_lines else 0
    return art_lines, height, width

  def __str__(self):
    return self.new_art if self.new_art else self.original_art

# Function to load all Ascii art from a folder
def load_ascii_art(folder_name='art/flowers/'):
  art_list = []
  folder_path = pkg_resources.resource_filename('random_garden_package', folder_name)

  if not os.path.exists(folder_path):
    return art_list

  for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
      file_path = os.path.join(folder_path, filename)
      art = AsciiArt.load_from_file(file_path)
      art_list.append(art)

    return art_list

# Generates a random garden
def random_garden(seed = None,
                  draw_height = 26, 
                  draw_width = 200,
                  weather = 'day',
                  max_animals=2,
                  max_buildings=1,
                  info=1,
                  contributors=True
                  ):
  # info 0: no info, 1: only seed, 2: basic info, 3: all info
  # weather 'day', 'night', 'rain', 'snow'
  # make sure all flowers are square, and the top row is used for width
  print('stifz')
  
  # print draw dimentions
  print(f"\nThe selected draw height is:       {draw_height}") if info >= 2 else None
  print(f"The selected draw width is:        {draw_width}\n") if info >= 2 else None

  # select seed
  if seed is None:
    seed = round(time.time())
  random.seed(seed)
  print(f"Seed: {seed}") if info >= 1 else None

  # Function to filter art by weather
  def filter_art_by_weather(art_objects, selected_weather):
    return [art for art in art_objects if not art.weather or selected_weather in art.weather]
  
  # Function to filter art by dimentions
  def select_eligible_objects(art_objects, max_height, max_width):
    return [obj for obj in art_objects if obj.height <= max_height and obj.width <= max_width]

  # Load and filter art by weather
  all_flowers = load_ascii_art('art/flowers/')
  print(len(all_flowers))
  flowers = filter_art_by_weather(all_flowers, weather)
  print(len(flowers))

  all_animals = load_ascii_art('art/animals/')
  animals = filter_art_by_weather(all_animals, weather)

  all_buildings = load_ascii_art('art/buildings/')
  buildings = filter_art_by_weather(all_buildings, weather)

  # initialize parameters before loop
  animals_left = max_animals
  buildings_left = max_buildings
  drawing = [''] * draw_height
  draw_width_left = draw_width
  used_art = set()
  used_artists = set()
  used_editors = set()
  # Define weather characters and weights
  weather_chars_weights = {
    'day': ([' ', '~'], [60, 1]),
    'night': ([' ', '.', '+'], [80, 2, 1]),
    'rain': ([' ', '|', '\''], [20, 2, 1]),
    'snow': ([' ', '-', '*'], [20, 2, 1]),
  }

  # drawing loop: loop until no width left
  while draw_width_left > 0:

    # Select eligible flowers, animals, and buildings
    eligible_flowers = select_eligible_objects(flowers, draw_height, draw_width_left)
    print(len(eligible_flowers))
    eligible_animals = select_eligible_objects(animals, draw_height, draw_width_left)
    eligible_buildings = select_eligible_objects(buildings, draw_height, draw_width_left)

    # Calculate chances for animal or buiding
    chance_for_animal = (animals_left / (animals_left + len(eligible_flowers) + len(eligible_buildings)))
    chance_for_building = (buildings_left / (buildings_left + len(eligible_flowers) + len(eligible_animals)))

    # select category by chance
    if animals_left > 0 and eligible_animals and random.random() < chance_for_animal:
      selected_category = 'animal'
    elif buildings_left > 0 and eligible_buildings and random.random() < chance_for_building:
      selected_category = 'building'
    else:
      selected_category = 'flower'
    
    # Load art
    if selected_category == 'animal':
      selected_obj = random.choice(eligible_animals)
      animals_left -= 1
    elif selected_category == 'building':
      selected_obj = random.choice(eligible_buildings)
      buildings_left -= 1
    else:  # 'flower'
      selected_obj = random.choice(eligible_flowers)

    # Add empty rows or weather
    height_difference = draw_height - selected_obj.height
    chars, weights = weather_chars_weights.get(weather, ([' '], [1]))
    for i in range(height_difference):
      weather_fill = ''.join(random.choices(chars, weights, k=selected_obj.width))
      drawing[i] += weather_fill

    # Append selected art to the drawing
    art = selected_obj.art_lines
    for i in range(selected_obj.height):
      drawing[i + height_difference] += art[i]

    # Subtract width
    draw_width_left -= selected_obj.width
    print(f"draw width left: {draw_width_left}\n") if info >= 3 else None

    # Add artists and editors to the respective sets
    used_art.update(selected_obj.name)
    used_artists.update(selected_obj.artists)
    used_editors.update(selected_obj.editors)

  # print selected art
  print(f"Selected art: {used_art}") if info >= 2 else None

  # make one long drawing string
  drawing_string = ''
  for row in drawing:
    drawing_string = drawing_string + row + ' \n'

  # Convert sets to lists and sort (optional)
  unique_artists = sorted(list(used_artists))
  unique_editors = sorted(list(used_editors))

  if contributors:
    # Append artists and editors to the drawing string
    drawing_string += '\n\nArtists:\n' + ', '.join(unique_artists)
    drawing_string += '\n\nEditors:\n' + ', '.join(unique_editors)

  return drawing_string
