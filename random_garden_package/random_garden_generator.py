import random
import time
import datetime
import pkg_resources
import os
from numpy.random import beta
import numpy as np

# define ascii art class
class AsciiArt:
  # biomes and their corresponding weathers
  biomes_and_weathers = {
    'ice': {'day', 'night', 'snow'},
    'tundra': {'day', 'night', 'snow'},
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
    'sky': {'day'},
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
        category = line.strip().split(', ') if line.strip() else []
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

  # Finds the position of the first non-interpunct character in the bottom line of the art
  def find_art_base_position(self):
    bottom_line = self.art_lines[-1]  # Get the bottom line of the art
    for i, char in enumerate(bottom_line):
        if char != '·':  # Check for the first non-interpunct character
            return i
    return None  # Return None if the base is not found

  def __str__(self):
    return self.new_art if self.new_art else self.original_art

# Function to filter art by weather
def filter_art_by_weather_and_biome(art_objects, selected_weather, selected_biome):
  return [art for art in art_objects if (not art.weather or selected_weather in art.weather) and (not art.biome or selected_biome in art.biome)]

def get_art_rarities(art_objects):
  rarities = []
  for obj in art_objects:
    # Assuming higher rarity value means less frequent appearance
    rarities.append(1.0 / obj.rarity if obj.rarity > 0 else 1.0)
  return rarities

def convert_grid_to_drawing_string(grid):
  drawing_lines = [''.join(row) for row in grid]
  return '\n'.join(drawing_lines)

def find_end_of_base_in_grid(grid):
  """Finds the position where the base of the grid ends+1 (i.e., the first interpunct)."""
  if not grid:
      return None

  bottom_row = grid[-1]  # Get the bottom row of the grid
  for i, char in enumerate(bottom_row):
      if char == '·':  # Check for a interpunct character
          return i  # Return the position of the non-interpunct character
  return len(bottom_row)  # Return the length of the row if only interpuncts are found

# Checks if art object can fit on the grid at a certain x,y position
def can_place_art_on_grid(grid, art_obj, x_position, y_position):
    """Checks if an art object can be placed on the grid at a given x position without overlapping non-interpunct characters."""
    
    # Check if the art object goes beyond the grid width
    if x_position + art_obj.width > len(grid[0]):
        return False

    # Check for overlapping non-interpunct characters
    for i, line in enumerate(art_obj.art_lines):
        grid_y = y_position + i  # Position on grid considering art height

        # Ignore if part of the art is above or below the grid
        if grid_y < 0 or grid_y >= len(grid):
            return False

        for j, char in enumerate(line):
            grid_x = x_position + j

            # Ignore if part of the art is beyond the grid width
            if grid_x < 0 or grid_x >= len(grid[0]):
                return False

            # Check for overlap, excluding interpuncts
            if char != '·' and grid[grid_y][grid_x] != '·':
                return False  # Overlap found, cannot place art here

    return True  # No overlap, art can be placed

# Function to filter art by dimentions
def select_eligible_flower_objects(grid, art_objects, x_position):
  eligible_objects = []
  for obj in art_objects:
    art_base_start = obj.find_art_base_position()  # Get the start of the base of the art object
    adjusted_x_position = x_position - art_base_start
    y_position = len(grid) - obj.height
    if can_place_art_on_grid(grid, obj, adjusted_x_position, y_position):
      eligible_objects.append(obj)
  return eligible_objects

# Function to filter ground art by dimentions around middle point
def select_eligible_ground_objects(grid, art_objects, x_position):
  eligible_objects = []
  for obj in art_objects:
    adjusted_x_position = x_position - round(0.5 * obj.width)
    y_position = len(grid) - obj.height
    if can_place_art_on_grid(grid, obj, adjusted_x_position, y_position):
      eligible_objects.append(obj)
  return eligible_objects

# Function that finds suitable potitions for an art object on the grid
def find_suitable_positions_for_art(grid, art_obj, min_y=None, max_y=None):

  suitable_positions = []
  for y in range(len(grid) - art_obj.height + 1):
    if (min_y is not None and y < min_y) or (max_y is not None and y + art_obj.height > max_y):
      continue  # Skip positions outside the specified vertical range
    for x in range(len(grid[y]) - art_obj.width + 1):
      if can_place_art_on_grid(grid, art_obj, x, y):
        suitable_positions.append((x, y))

  return suitable_positions

def place_art_in_grid(grid, art_obj, position_x, position_y):
  for i, line in enumerate(art_obj.art_lines):
    for j, char in enumerate(line):
      # skip if the character is an interpunkt
      if char == '·':
        continue
      if 0 <= position_x + j < len(grid[0]) and 0 <= position_y + i < len(grid):
        grid[position_y + i][position_x + j] = char

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

def create_grid(draw_width, draw_height):
  return [['·' for _ in range(draw_width)] for _ in range(draw_height)]

# Generates a random garden
def random_garden(seed = None,
                  draw_height = 36, 
                  draw_width = 200,
                  weather = None,
                  biome = None,
                  max_animals = 2,
                  max_buildings = 1,
                  max_airbornes = 4,
                  max_sky = 10,
                  duplication = True,
                  info = 1,
                  contributors = True
                  ):

  # select seed
  if seed is None:
    seed = round(time.time())
  random.seed(seed)
  print(f"Seed: {seed}") if info >= 1 else None

  # Create grid
  print(f"\nThe selected draw height is:       {draw_height}") if info >= 2 else None
  print(f"The selected draw width is:        {draw_width}\n") if info >= 2 else None
  grid = create_grid(draw_width, draw_height)

  # Get the available biomes and weathers dictionary
  biomes_and_weathers = AsciiArt.biomes_and_weathers

  # Select random biome if not provided
  if biome is None:
    biome = random.choice(list(biomes_and_weathers))
    print(f'Random chosen biome: {biome}') if info >= 2 else None

  # Select random weather if not provided
  if weather is None:
    weather = random.choice(list(biomes_and_weathers[biome]))
    print(f'Random chosen weather: {weather}') if info >= 2 else None

  # Check if draw height is enough for underwater otherwise change to ocean
  if biome == 'underwater' and draw_height < 22:
    biome = 'ocean'
    print(f"Adjusted biome to 'ocean' because draw_height was under 22.") if info >= 3 else None

  # Define weather characters and weights
  weather_chars_weights = {
    'day': ([' ', '~'], [60, 1]),
    'night': ([' ', '.', '+'], [80, 2, 1]),
    'rain': ([' ', '|', '\''], [20, 2, 1]),
    'snow': ([' ', '-', '*'], [20, 2, 1]),
  }

  # Check if the selected biome is available
  if biome not in biomes_and_weathers:
    raise ValueError(f"Invalid biome type: {biome}. Valid options are: {', '.join(biomes_and_weathers)}")

  # Adjust weather if it's not compatible with the selected biome
  if weather not in biomes_and_weathers[biome]:
    # Change to the first compatible weather
    weather = next(iter(biomes_and_weathers[biome]), 'day')  # Default to 'day' if no weathers are compatible
    print(f"Adjusted weather to '{weather}' for biome '{biome}'. Valid options are: {', '.join(biomes_and_weathers[biome])}") if info >= 3 else None

  # Load and filter art by weather
  all_flowers = load_ascii_art('art/flowers/')
  flowers = filter_art_by_weather_and_biome(all_flowers, weather, biome)

  all_animals = load_ascii_art('art/animals/')
  animals = filter_art_by_weather_and_biome(all_animals, weather, biome)

  all_buildings = load_ascii_art('art/buildings/')
  buildings = filter_art_by_weather_and_biome(all_buildings, weather, biome)

  all_airbornes = load_ascii_art('art/airbornes/')
  airbornes = filter_art_by_weather_and_biome(all_airbornes, weather, biome)

  all_sky = load_ascii_art('art/sky/')
  sky = filter_art_by_weather_and_biome(all_sky, weather, biome)

  # Start art lists
  used_art = list()
  used_artists = set()
  used_editors = set()
  
  # Calculate animal and building positions
  number_of_animals = random.randint(0, max_animals)
  print(number_of_animals) if info >= 2 else None
  number_of_buildings = random.randint(0, max_buildings)
  print(number_of_buildings) if info >= 2 else None
  animal_positions = beta(2,2,number_of_animals)
  print(animal_positions) if info >= 2 else None
  building_positions = beta(2,2,number_of_buildings)
  print(building_positions) if info >= 2 else None

  # Select and place building art
  for position in building_positions:
    x_position = round(draw_width * position)
    eligible_buildings = select_eligible_ground_objects(grid, buildings, x_position)
    if not eligible_buildings:
      continue
    building_rarities = get_art_rarities(eligible_buildings)
    selected_obj = random.choices(eligible_buildings, weights=building_rarities)[0]
    adjusted_x_position = x_position - round(0.5*selected_obj.width)
    y_position = draw_height - selected_obj.height  # Start from the bottom
    place_art_in_grid(grid, selected_obj, adjusted_x_position, y_position)
    # Add artists and editors to the respective sets
    used_art.append(selected_obj.name)
    used_artists.update(selected_obj.artists)
    used_editors.update(selected_obj.editors)
    if not duplication or 'unique' in selected_obj.category:
      buildings.remove(selected_obj)

  # Select and place animal art
  for position in animal_positions:
    x_position = round(draw_width * position)
    eligible_animals = select_eligible_ground_objects(grid, animals, x_position)
    if not eligible_animals:
      continue
    animal_rarities = get_art_rarities(eligible_animals)
    selected_obj = random.choices(eligible_animals, weights=animal_rarities)[0]
    adjusted_x_position = x_position - round(0.5*selected_obj.width)
    y_position = draw_height - selected_obj.height  # Start from the bottom
    place_art_in_grid(grid, selected_obj, adjusted_x_position, y_position)
    # Add artists and editors to the respective sets
    used_art.append(selected_obj.name)
    used_artists.update(selected_obj.artists)
    used_editors.update(selected_obj.editors)
    if not duplication or 'unique' in selected_obj.category:
      animals.remove(selected_obj)

  # Initialize parameters before loop
  current_x = 0
  load_grass = False
  # Select and place plant art
  while current_x < draw_width:
    # Select eligible flowers, animals, and buildings
    eligible_flowers = select_eligible_flower_objects(grid, flowers, current_x)
    # Get ground art rarities for selection
    flower_rarities = get_art_rarities(eligible_flowers)
    if eligible_flowers:  # 'flower'
      selected_obj = random.choices(eligible_flowers, weights=flower_rarities)[0]
      if not duplication or 'unique' in selected_obj.category:
        flowers.remove(selected_obj)
    else: # if nothing is available just pick grass
      if not load_grass: # just load grass once
        folder_name = 'art/flowers/'
        folder_path = pkg_resources.resource_filename('random_garden_package', folder_name)
        file_path = os.path.join(folder_path, 'grass1.txt')
        grass = AsciiArt.load_from_file(file_path)
        load_grass = True
      selected_obj = grass
    # Add artists and editors to the respective sets
    used_art.append(selected_obj.name)
    used_artists.update(selected_obj.artists)
    used_editors.update(selected_obj.editors)
    # Place ground art in the grid
    ground_start_x = current_x - selected_obj.find_art_base_position()
    ground_start_y = draw_height - selected_obj.height  # Start from the bottom
    place_art_in_grid(grid, selected_obj, ground_start_x, ground_start_y)
    # When the base of the drawing is full stop drawing the ground layer
    current_x = find_end_of_base_in_grid(grid)

  # Select and place sky art
  max_y_for_sky = draw_height // 3
  sky_left = random.randint(0, max_sky)
  while sky_left > 0 and sky:
    sky_rarities = get_art_rarities(sky)
    selected_obj = random.choices(sky, weights=sky_rarities)[0]
    suitable_positions = find_suitable_positions_for_art(grid, selected_obj, max_y=max_y_for_sky)
    if suitable_positions:
      selected_position = random.choice(suitable_positions)
      place_art_in_grid(grid, selected_obj, selected_position[0], selected_position[1])
      # Add artists and editors to the respective sets
      used_art.append(selected_obj.name)
      used_artists.update(selected_obj.artists)
      used_editors.update(selected_obj.editors)
      if not duplication or 'unique' in selected_obj.category:
        sky.remove(selected_obj)  # Remove the chosen art object to avoid duplication
    sky_left -= 1  # Decrement regardless of whether art was placed or not

  # Select and place airborne art
  min_y_for_airborne = draw_height // 3
  airborne_left = random.randint(0, max_airbornes)
  while airborne_left > 0 and airbornes:
    airborne_rarities = get_art_rarities(airbornes)
    selected_obj = random.choices(airbornes, weights=airborne_rarities)[0]
    suitable_positions = find_suitable_positions_for_art(grid, selected_obj, min_y=min_y_for_airborne)
    if suitable_positions:
      selected_position = random.choice(suitable_positions)
      place_art_in_grid(grid, selected_obj, selected_position[0], selected_position[1])
      # Add artists and editors to the respective sets
      used_art.append(selected_obj.name)
      used_artists.update(selected_obj.artists)
      used_editors.update(selected_obj.editors)
      if not duplication or 'unique' in selected_obj.category:
        airbornes.remove(selected_obj) # Remove the chosen art object to avoid duplication
    airborne_left -= 1  # Decrement regardless of whether art was placed or not

  # Change interpuncts with weather characters
  chars, weights = weather_chars_weights.get(weather, ([' '], [1]))
  for y in range(draw_height):
    for x in range(draw_width):
      if grid[y][x] == '·':
        grid[y][x] = random.choices(chars, weights)[0]

  # print selected art
  print(f"Selected art: {str(used_art)}") if info >= 2 else None

  drawing_string = convert_grid_to_drawing_string(grid)

  # Convert sets to lists and sort (optional)
  unique_artists = sorted(list(used_artists))
  unique_editors = sorted(list(used_editors))

  if contributors:
    # Append artists and editors to the drawing string
    drawing_string += '\n\nArtists:\n' + ', '.join(unique_artists)
    drawing_string += '\n\nEditors:\n' + ', '.join(unique_editors)

  return drawing_string
