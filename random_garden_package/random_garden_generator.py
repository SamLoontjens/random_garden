import random
import time
import sys
import pkg_resources
import os

# Load all ascii art from one folder
def load_all_ascii_art(folder_name='flowers'):
    master_art_list = []
    folder_path = pkg_resources.resource_filename('random_garden_package', folder_name)

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                art_lines = file.readlines()
                art_lines = [line.rstrip('\n') for line in art_lines]
                master_art_list.append(art_lines)

    return master_art_list

# Generates a random garden
def random_garden(draw_height = 20, 
                  draw_width = 200, 
                  seed = None, 
                  load_time = 0, 
                  info=1, 
                  number_of_animals=1):
  # info 0: no info, 1: only seed, 2: basic info, 3: all info
  # flowers from https://www.asciiart.eu/plants/flowers
  # note if there is an \\ in the flower it has to be dubbled to \\\\
  # make sure all flowers are square, and the top row is used for width

  # load all flowers
  flowers = load_all_ascii_art(folder_name='flowers')
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

  # load all animals
  animals = load_all_ascii_art(folder_name='animals')
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

  # print draw dimentions
  print(f"\nThe selected draw height is:       {draw_height}") if info >= 2 else None
  print(f"The selected draw width is:        {draw_width}\n") if info >= 2 else None

  # select seed
  if seed is None:
        seed = round(time.time())
  random.seed(seed)
  print(f"Seed: {seed}") if info >= 1 else None

  # initialize parameters before loop
  animals_left = number_of_animals
  selected_art = []
  drawing = [''] * draw_height
  draw_width_left = draw_width

  # loop until no width left
  while draw_width_left > 0:

    # find eligible flowers
    eligible_flowers = [index for index, (flower_height, flower_width) in enumerate(zip(flower_heights, flower_widths)) if flower_height <= draw_height and flower_width <= draw_width_left]
    print(f"The eligible flowers are:        {eligible_flowers}") if info >= 3 else None

    # chance for animal
    if animals_left > 0 and random.random() < (animals_left / (animals_left + len(eligible_flowers))):
      eligible_animals = [index for index, (animal_height, animal_width) in enumerate(zip(animal_heights, animal_widths)) if animal_height <= draw_height and animal_width <= draw_width_left]
      print(f"The eligible animals are:        {eligible_animals}") if info >= 3 else None

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
        print("No animal was eligible")
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

    # add empty rows
    height_difference = draw_height - height
    for i in range(height_difference):
      drawing[i] = drawing[i] + width * " "

    # add rows
    for i in range(height):
      drawing[i+height_difference] = drawing[i+height_difference] + art[i]

    # subtract width
    draw_width_left = draw_width_left - width
    print(f"draw width left: {draw_width_left}\n") if info >= 3 else None

  # set sleep time
  sleep_time = load_time / draw_height
  print(f"each step waiting for: {sleep_time}") if info >= 2 else None
  print(f"Selected art: {selected_art}") if info >= 2 else None

  # print all rows
  for row in drawing:
    time.sleep(sleep_time)
    print(row)


