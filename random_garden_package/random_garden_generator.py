import random
import time
import datetime
import pkg_resources
import os

# define ascii art class
class AsciiArt:
  # biomes and their corresponding weathers
  biomes_and_weathers = {
    'ice': {'day', 'night', 'snow'},
    'tundra': {'day', 'night', 'rain', 'snow'},
    'taiga': {'day', 'night', 'rain', 'snow'},
    'temperate': {'day', 'night', 'rain', 'snow'},
    'grassland': {'day', 'night', 'rain', 'snow'},
    'desert': {'day', 'night'}, 
    'steppe': {'day', 'night', 'rain'},
    'savanna': {'day', 'night', 'rain'},
    'tropical': {'day', 'night', 'rain',},
    'swamp': {'day', 'night', 'rain'},
    'mangrove': {'day', 'night', 'rain'},
    'lake': {'day', 'night', 'rain', 'snow'},
    'ocean': {'day', 'night', 'rain', 'snow'},
    'underwater': {'day', 'night', 'rain', 'snow'},
    'space': {'night'},
    'fantasy': {'day', 'night', 'rain', 'snow'},
    }

  def __init__(self, name, category, weather, biome, rarity, dates, artists, editors, source, original_art, new_art):
    self.name = name
    self.category = category
    self.weather = weather
    self.biome = biome
    self.rarity = rarity
    self.dates = dates
    self.artists = artists if artists else []
    self.editors = editors if editors else []
    self.source = source
    self.original_art = original_art
    self.new_art = new_art
    self.art_lines, self.height, self.width = self._split_art_and_get_dimensions()
    self.validate_attributes()

  @staticmethod
  def load_from_file(file_path):
    with open(file_path, 'r') as file:
      lines = file.readlines()

    name = category = source = None
    weather = []
    biome = []
    artists = []
    editors = []
    rarity = 1
    dates = []

    original_art_lines = []
    new_art_lines = []
    is_new_art = False
    
    for line in lines:
      line = line.rstrip('\n')

      if line.startswith('[') and line.endswith(']'):
        current_section = line.strip().lower()[1:-1]
        is_new_art = current_section == 'new'
        continue

      if current_section == 'name':
        name = line.strip()
      elif current_section == 'category':
        category = line.strip()
      elif current_section == 'weather':
        weather = line.strip().split(', ') if line.strip() else []
      elif current_section == 'biome':
        biome = line.strip().split(', ') if line.strip() else []
      elif current_section == 'rarity':
        rarity = int(line.strip())
      elif current_section == 'dates':
        dates = [d.strip() for d in line.split(',')] if line.strip() else []
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

    return AsciiArt(name, category, weather, biome, rarity, dates, artists, editors, source, original_art, new_art)

  def _split_art_and_get_dimensions(self):
    # Split new art into lines or if there is no new art split original art into lines
    art_lines = self.new_art.split('\n') if self.new_art else self.original_art.split('\n')
    
    # Return empty values if there's no art
    if not art_lines:
      raise ValueError(f"No art found in art object: {self.name}")
    
    # Remove the last line because it is empty
    deleted_line = art_lines.pop()
    assert deleted_line == '', f'deleted line should be empty for art object: {self.name}'

    # Get height and width of art
    height = len(art_lines)
    width = len(art_lines[0]) if art_lines else 0

    # Check if all lines have the same width
    for line in art_lines:
      if len(line) != width:
        raise ValueError(f"Inconsistent line width in art object: {self.name}")

    return art_lines, height, width

  def validate_attributes(self):
    # Ensure all listed biomes are valid
    for b in self.biome:
      if b not in self.biomes_and_weathers:
        raise ValueError(f"Invalid biome '{b}' in art '{self.name}'. Valid biomes: {', '.join(self.biomes_and_weathers.keys())}")

    # Check if each weather condition is valid in at least one of the biomes
    for w in self.weather:
      if not any(w in self.biomes_and_weathers[b] for b in self.biome):
        valid_biomes_for_weather = [b for b in self.biome if w in self.biomes_and_weathers[b]]
        raise ValueError(f"Weather '{w}' is not typical for the biomes '{', '.join(self.biome)}' in art '{self.name}'. Valid biomes for this weather: {', '.join(valid_biomes_for_weather)}")

  def __str__(self):
    return self.new_art if self.new_art else self.original_art

# Function to load all Ascii art from a folder
def load_ascii_art(folder_name='art/flowers/'):
  art_list = []
  folder_path = pkg_resources.resource_filename('random_garden_package', folder_name)
  today = datetime.datetime.now().strftime("%m:%d")  # Current date in mm:dd format

  if not os.path.exists(folder_path):
    return art_list

  for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
      file_path = os.path.join(folder_path, filename)
      art = AsciiArt.load_from_file(file_path)
      # Check if today matches on of the dates or if there's no date specified
      if not art.dates or today in art.dates:
        art_list.append(art)

  return art_list

def concatenate_art_by_height():
  all_art = load_ascii_art('art/flowers/') + load_ascii_art('art/animals/') + load_ascii_art('art/buildings/')

  # Sort the art by height
  sorted_art = sorted(all_art, key=lambda art: art.height)

  # Find the maximum height among all art
  max_height = max(art.height for art in sorted_art) if sorted_art else 0

  # Concatenate art side by side with alignment at bottom
  concatenated_art_lines = [''] * max_height
  for art in sorted_art:
    space_above = max_height - art.height  # Calculate space needed above the art
    for i in range(max_height):
      if i < space_above:
        # Add spaces for lines above the current art
        art_line = ' ' * art.width
      else:
        # Add the actual art line
        art_line = art.art_lines[i - space_above]
      concatenated_art_lines[i] += art_line + ' '  # Add a space as a separator

  return '\n'.join(concatenated_art_lines)

# Generates a random garden
def random_garden(seed = None,
                  draw_height = 26, 
                  draw_width = 200,
                  weather = 'day',
                  biome = 'temperate',
                  max_animals=2,
                  max_buildings=1,
                  info=1,
                  contributors=True
                  ):
  # info 0: no info, 1: only seed, 2: basic info, 3+: all info
  # weather 'day', 'night', 'rain', 'snow'

  # print draw dimentions
  print(f"\nThe selected draw height is:       {draw_height}") if info >= 2 else None
  print(f"The selected draw width is:        {draw_width}\n") if info >= 2 else None

  # Check if draw height is enough for underwater otherwise change to ocean
  if biome == 'underwater' and draw_height < 22:
    biome = 'ocean'
    print(f"Adjusted biome to 'ocean' because draw_height was under 22.") if info >= 3 else None

  # select seed
  if seed is None:
    seed = round(time.time())
  random.seed(seed)
  print(f"Seed: {seed}") if info >= 1 else None

  # Define weather characters and weights
  weather_chars_weights = {
    'day': ([' ', '~'], [60, 1]),
    'night': ([' ', '.', '+'], [80, 2, 1]),
    'rain': ([' ', '|', '\''], [20, 2, 1]),
    'snow': ([' ', '-', '*'], [20, 2, 1]),
  }
  # Check if the provided weather is valid
  if weather not in weather_chars_weights:
    raise ValueError(f"Invalid weather type: {weather}. Valid options are: {', '.join(weather_chars_weights.keys())}")

  # Get the available biomes and weathers dictionary
  biomes_and_weathers = AsciiArt.biomes_and_weathers

  # Check if the selected biome is available
  if biome not in biomes_and_weathers:
    raise ValueError(f"Invalid biome type: {biome}. Valid options are: {', '.join(biomes_and_weathers)}")
  
  # Adjust weather if it's not compatible with the selected biome
  if weather not in biomes_and_weathers[biome]:
    # Change to the first compatible weather
    weather = next(iter(biomes_and_weathers[biome]), 'day')  # Default to 'day' if no weathers are compatible
    print(f"Adjusted weather to '{weather}' for biome '{biome}'.") if info >= 3 else None

  # Function to filter art by weather
  def filter_art_by_weather_and_biome(art_objects, selected_weather, selected_biome):
    return [art for art in art_objects if (not art.weather or selected_weather in art.weather) and (not art.biome or selected_biome in art.biome)]
  
  # Function to filter art by dimentions
  def select_eligible_objects(art_objects, max_height, max_width):
    eligible_objects = []
    rarities = []
    for obj in art_objects:
      if obj.height <= max_height and obj.width <= max_width:
        eligible_objects.append(obj)
        # Assuming higher rarity value means less frequent appearance
        rarities.append(1.0 / obj.rarity if obj.rarity > 0 else 1.0)
    return eligible_objects, rarities

  # Load and filter art by weather
  all_flowers = load_ascii_art('art/flowers/')
  flowers = filter_art_by_weather_and_biome(all_flowers, weather, biome)

  all_animals = load_ascii_art('art/animals/')
  animals = filter_art_by_weather_and_biome(all_animals, weather, biome)

  all_buildings = load_ascii_art('art/buildings/')
  buildings = filter_art_by_weather_and_biome(all_buildings, weather, biome)

  # initialize parameters before loop
  animals_left = max_animals
  buildings_left = max_buildings
  drawing = [''] * draw_height
  draw_width_left = draw_width
  used_art = list()
  used_artists = set()
  used_editors = set()

  # drawing loop: loop until no width left
  while draw_width_left > 0:

    # Select eligible flowers, animals, and buildings
    eligible_flowers, flower_rarities = select_eligible_objects(flowers, draw_height, draw_width_left)
    eligible_animals, animal_rarities = select_eligible_objects(animals, draw_height, draw_width_left)
    eligible_buildings, building_rarities = select_eligible_objects(buildings, draw_height, draw_width_left)

    # Calculate chances for animal or buiding
    chance_for_animal = (animals_left / (animals_left + len(eligible_flowers) + len(eligible_buildings)))
    chance_for_building = (buildings_left / (buildings_left + len(eligible_flowers) + len(eligible_animals)))

    # Pick random art weighted by rarity
    if animals_left > 0 and eligible_animals and random.random() < chance_for_animal:
      selected_obj = random.choices(eligible_animals, weights=animal_rarities)[0]
      animals_left -= 1
    elif buildings_left > 0 and eligible_buildings and random.random() < chance_for_building:
      selected_obj = random.choices(eligible_buildings, weights=building_rarities)[0]
      buildings_left -= 1
    else:  # 'flower'
      selected_obj = random.choices(eligible_flowers, weights=flower_rarities)[0]

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
    used_art.append(selected_obj.name)
    used_artists.update(selected_obj.artists)
    used_editors.update(selected_obj.editors)

  # print selected art
  print(f"Selected art: {str(used_art)}") if info >= 2 else None

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
