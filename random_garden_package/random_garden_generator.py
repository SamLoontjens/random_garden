import random
import time
import pkg_resources
import os

# Load all ascii art from one folder
def load_ascii_art(folder_name='flowers'):
    art_list = []
    folder_path = pkg_resources.resource_filename('random_garden_package', folder_name)

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                art_lines = file.readlines()
                art_lines = [line.rstrip('\n') for line in art_lines]
                art_list.append(art_lines)

    return art_list

# Generates a random garden
def random_garden(seed = None,
                  draw_height = 26, 
                  draw_width = 200,
                  weather = 'day',
                  max_animals=2,
                  max_buildings=1,
                  info=1
                  ):
  # info 0: no info, 1: only seed, 2: basic info, 3: all info
  # weather 'day', 'night', 'rain', 'snow'
  # flowers from https://www.asciiart.eu/plants/flowers
  # make sure all flowers are square, and the top row is used for width

  # load general flowers
  flowers = load_ascii_art(folder_name='art/general/flowers/')
  # load weather flowers
  flowers = flowers + load_ascii_art(folder_name=f'art/{weather}/flowers/')
  # check total flowers
  total_flowers = len(flowers)
  print(f"The total available flowers is:    {total_flowers}") if info >= 2 else None

  # get the flower dimentions
  flower_heights = []
  flower_widths = []
  for flower in flowers:
    flower_height = len(flower)
    flower_width = len(flower[0])
    print(f"The flower height x width:       {flower_height} x {flower_width}") if info >= 3 else None
    flower_heights.append(flower_height)
    flower_widths.append(flower_width)

  # load general animals
  animals = load_ascii_art(folder_name='art/general/animals')
  # load weather animals
  animals = animals + load_ascii_art(folder_name=f'art/{weather}/animals/')
  # check total animals
  total_animals = len(animals)
  print(f"The total available animals is:    {total_animals}") if info >= 2 else None

  # get the animal dimentions
  animal_heights = []
  animal_widths = []
  for animal in animals:
    animal_height = len(animal)
    animal_width = len(animal[0])
    print(f"The animal height x width:       {animal_height} x {animal_width}") if info >= 3 else None
    animal_heights.append(animal_height)
    animal_widths.append(animal_width)

  # Load general buildings
  buildings = load_ascii_art(folder_name='art/general/buildings/')
  # Load weather buildings
  buildings = buildings + load_ascii_art(folder_name=f'art/{weather}/buildings/')
  # Check total buildings
  total_buildings = len(buildings)
  print(f"The total available buildings is: {total_buildings}") if info >= 2 else None

  # get the buildings dimentions
  building_heights = []
  building_widths = []
  for building in buildings:
      building_height = len(building)
      building_width = len(building[0])
      print(f"The building height x width: {building_height} x {building_width}") if info >= 3 else None
      building_heights.append(building_height)
      building_widths.append(building_width)

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

  # drawing loop: loop until no width left
  while draw_width_left > 0:

    # find eligible flowers
    eligible_flowers = [index for index, (flower_height, flower_width) in enumerate(zip(flower_heights, flower_widths)) if flower_height <= draw_height and flower_width <= draw_width_left]
    print(f"The eligible flowers are:        {eligible_flowers}") if info >= 3 else None

    eligible_animals = [index for index, (animal_height, animal_width) in enumerate(zip(animal_heights, animal_widths)) if animal_height <= draw_height and animal_width <= draw_width_left]
    print(f"The eligible animals are:        {eligible_animals}") if info >= 3 else None

    eligible_buildings = [index for index, (building_height, building_width) in enumerate(zip(building_heights, building_widths)) if building_height <= draw_height and building_width <= draw_width_left]
    print(f"The eligible animals are:        {eligible_animals}") if info >= 3 else None

    # chance for animal
    if animals_left > 0 and random.random() < (animals_left / (animals_left + len(eligible_flowers) + len(eligible_buildings))):
      # select animal
      if(eligible_animals):
        selected_animal = random.choice(eligible_animals)
        print(f"The selected animal number:      {selected_animal}") if info >= 3 else None
        selected_art.append(f"a{selected_animal}")
        
        # get the animal art
        art = animals[selected_animal]

        # get animal dimentions
        height = animal_heights[selected_animal]
        width = animal_widths[selected_animal]
        
        # subtract one from animals left
        animals_left -= 1
      else:
        # no animals were eligible
        animals_left = 0
        print("No animal was eligible") if info >= 3 else None

        # go to start of loop
        continue
    elif buildings_left > 0 and random.random() < (buildings_left / (buildings_left + len(eligible_flowers) + len(eligible_animals))):
       # select building
      if(eligible_buildings):
        selected_building = random.choice(eligible_buildings)
        print(f"The selected building number:      {selected_building}") if info >= 3 else None
        selected_art.append(f"a{selected_building}")
        
        # get the building art
        art = buildings[selected_building]

        # get building dimentions
        height = building_heights[selected_building]
        width = building_widths[selected_building]
        
        # subtract one from buildings left
        buildings_left -= 1
      else:
        # no buildings were eligible
        buildings_left = 0
        print("No building was eligible") if info >= 3 else None

        # go to start of loop
        continue
    else:
      # select flower
      selected_flower = random.choice(eligible_flowers)
      print(f"The selected flower number:      {selected_flower}") if info >= 3 else None
      selected_art.append(selected_flower)

      # get the flower art
      art = flowers[selected_flower]

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

  # print selected art
  print(f"Selected art: {selected_art}") if info >= 2 else None

  # make one long drawing string
  drawing_string = ''
  for row in drawing:
    drawing_string = drawing_string + row + ' \n'

  return drawing_string
