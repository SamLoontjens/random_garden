import random
import time
import pkg_resources
import os

# define ascii art class
class AsciiArt:
    def __init__(self, name, category, weather, rarity, artist, editor, source, original_art, new_art):
        self.name = name
        self.category = category
        self.weather = weather
        self.rarity = rarity
        self.artist = artist
        self.editor = editor
        self.source = source
        self.original_art = original_art
        self.new_art = new_art

    @staticmethod
    def load_from_file(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        name = category = weather = rarity = artist = editor = source = None
        current_section = None
        original_art_lines = []
        new_art_lines = []
        is_new_art = False

        for line in lines:
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1].lower()
                if current_section == 'new':
                    is_new_art = True
            elif current_section == 'name':
                name = line
            elif current_section == 'category':
                category = line
            elif current_section == 'weather':
                weather = line.split(', ')
            elif current_section == 'rarity':
                rarity = int(line)
            elif current_section == 'artist':
                artist = line.split(', ')
            elif current_section == 'editor':
                editor = line
            elif current_section == 'retrieved from':
                source = line
            elif current_section == 'original' and not is_new_art:
                original_art_lines.append(line)
            elif current_section == 'new':
                new_art_lines.append(line)

        original_art = '\n'.join(original_art_lines)
        new_art = '\n'.join(new_art_lines)
        return AsciiArt(name, category, weather, rarity, artist, editor, source, original_art, new_art)

    def __str__(self):
        return self.new_art if self.new_art else self.original_art


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

  # function to split art into lines and get dimensions
  def split_art_and_get_dimensions(art_objects):
    split_art = []
    heights = []
    widths = []
    for art_obj in art_objects:
      art_lines = art_obj.new_art.split('\n') if art_obj.new_art else art_obj.original_art.split('\n')
      height = len(art_lines)
      width = len(art_lines[0]) if art_lines else 0
      split_art.append(art_lines)
      heights.append(height)
      widths.append(width)
      if info >= 3:
        print(f"Art height x width: {height} x {width}")
    return split_art, heights, widths

  # Function to filter art by weather
  def filter_art_by_weather(art_objects, selected_weather):
    return [art for art in art_objects if selected_weather in art.weather]

  # Load and filter art by weather
  all_flowers = load_ascii_art('art/flowers/')
  print(len(all_flowers))
  flowers = filter_art_by_weather(all_flowers, weather)

  all_animals = load_ascii_art('art/animals/')
  animals = filter_art_by_weather(all_animals, weather)

  all_buildings = load_ascii_art('art/buildings/')
  buildings = filter_art_by_weather(all_buildings, weather)

  # Split art into lines and get dimensions
  flowers_art, flower_heights, flower_widths = split_art_and_get_dimensions(flowers)
  animals_art, animal_heights, animal_widths = split_art_and_get_dimensions(animals)
  buildings_art, building_heights, building_widths = split_art_and_get_dimensions(buildings)

  # print draw dimentions
  print(f"\nThe selected draw height is:       {draw_height}") if info >= 2 else None
  print(f"The selected draw width is:        {draw_width}\n") if info >= 2 else None

  # select seed
  if seed is None:
        seed = round(time.time())
  random.seed(seed)
  print(f"Seed: {seed}") if info >= 1 else None

  # initialize parameters before loop
  animals_left = max_animals
  buildings_left = max_buildings
  selected_art = []
  drawing = [''] * draw_height
  draw_width_left = draw_width
  artists = set()
  editors = set()

  # drawing loop: loop until no width left
  while draw_width_left > 0:

    # find eligible flowers
    eligible_flowers = [index for index, (flower_height, flower_width) in enumerate(zip(flower_heights, flower_widths)) if flower_height <= draw_height and flower_width <= draw_width_left]
    print(f"The eligible flowers are:        {eligible_flowers}") if info >= 3 else None

    eligible_animals = [index for index, (animal_height, animal_width) in enumerate(zip(animal_heights, animal_widths)) if animal_height <= draw_height and animal_width <= draw_width_left]
    print(f"The eligible animals are:        {eligible_animals}") if info >= 3 else None

    eligible_buildings = [index for index, (building_height, building_width) in enumerate(zip(building_heights, building_widths)) if building_height <= draw_height and building_width <= draw_width_left]
    print(f"The eligible animals are:        {eligible_animals}") if info >= 3 else None

    chance_for_animal = (animals_left / (animals_left + len(eligible_flowers) + len(eligible_buildings)))

    chance_for_building = (buildings_left / (buildings_left + len(eligible_flowers) + len(eligible_animals)))

    # select category by chance
    if animals_left > 0 and eligible_animals and random.random() < chance_for_animal:
      selected_category = 'animal'
    elif buildings_left > 0 and eligible_buildings and random.random() < chance_for_building:
      selected_category = 'building'
    else:
      selected_category = 'flower'
    
    # load art
    if selected_category == 'animal':
      # choose a random eligible animal
      selected_animal = random.choice(eligible_animals)
      selected_art.append(f"a{selected_animal}")
      print(f"The selected animal number:      {selected_animal}") if info >= 3 else None
      # get the animal object
      art_obj = animals[selected_animal]
      # get the animal art
      art = animals_art[selected_animal]
      # get animal dimentions
      height = animal_heights[selected_animal]
      width = animal_widths[selected_animal]
      # subtract one from animals left
      animals_left -= 1

    elif selected_category == 'building':
      # choose a random eligible building
      selected_building = random.choice(eligible_buildings)
      selected_art.append(f"a{selected_building}")
      print(f"The selected building number:      {selected_building}") if info >= 3 else None
      # get the building object
      art_obj = buildings[selected_building]
      # get the building art
      art = buildings_art[selected_building]
      # get building dimentions
      height = building_heights[selected_building]
      width = building_widths[selected_building]
      # subtract one from buildings left
      buildings_left -= 1

    else:
      # choose a random eligible flower
      selected_flower = random.choice(eligible_flowers)
      print(f"The selected flower number:      {selected_flower}") if info >= 3 else None
      selected_art.append(selected_flower)
      # get the flower object
      art_obj = flowers[selected_flower]
      # get the flower art
      art = flowers_art[selected_flower]
      # get flower dimentions
      height = flower_heights[selected_flower]
      width = flower_widths[selected_flower]

    print(f"The art height x width:       {height} x {width}") if info >= 3 else None

    # add empty rows or weather
    height_difference = draw_height - height
    day_characters = [' ', '~']
    day_weights = [60, 1]
    night_characters = [' ', '.', '+']
    night_weights = [80, 2, 1]
    rain_characters = [' ', '|', '\'']
    rain_weights = [20, 2, 1]
    snow_characters = [' ', '-', '*']
    snow_weights = [20, 2, 1]
    for i in range(height_difference):
      if weather == 'day':
        weather_fill = ''.join(random.choices(day_characters, day_weights, k=width))
      elif weather == 'night':
        weather_fill = ''.join(random.choices(night_characters, night_weights, k=width))
      elif weather == 'rain':
        weather_fill = ''.join(random.choices(rain_characters, rain_weights, k=width))
      elif weather == 'snow':
        weather_fill = ''.join(random.choices(snow_characters, snow_weights, k=width))
      else:
        weather_fill = '' * width
      
      drawing[i] = drawing[i] + weather_fill

    # add rows
    for i in range(height):
      drawing[i+height_difference] = drawing[i+height_difference] + art[i]

    # subtract width
    draw_width_left = draw_width_left - width
    print(f"draw width left: {draw_width_left}\n") if info >= 3 else None

    # Add artist and editor to the respective sets
    artists.add(art_obj.artist)
    editors.add(art_obj.editor)

  # print selected art
  print(f"Selected art: {selected_art}") if info >= 2 else None

  # make one long drawing string
  drawing_string = ''
  for row in drawing:
    drawing_string = drawing_string + row + ' \n'

  # Convert sets to lists and sort (optional)
  unique_artists = sorted(list(artists))
  #unique_editors = sorted(list(editors))

  if contributors:
    # Append artists and editors to the drawing string
    drawing_string += '\n\nArtists:\n' + ', '.join(unique_artists)
    #drawing_string += '\n\nEditors:\n' + ', '.join(unique_editors)

  return drawing_string
