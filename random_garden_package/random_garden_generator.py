import random
import time
import sys
import pkg_resources
import os

# For testing purposes
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
def random_garden(draw_height = 20, draw_width = 200, seed = random.randrange(9999), load_time = 0, info=1):
  # info 0: no info, 1: only seed, 2: basic info, 3: all info
  # flowers from https://www.asciiart.eu/plants/flowers
  # note if there is an \\ in the flower it has to be dubbled to \\\\
  # make sure all flowers are square, and the top row is used for width
  flowers = load_all_ascii_art(folder_name='flowers')

  total_flowers = len(flowers)
  print(f"The total number of flowers is:    {total_flowers}") if info >= 2 else None

  flower_heights = []
  flower_widths = []
  for flower in flowers:
    flower_height = len(flower)
    flower_width = len(flower[0])
    print(f"The flower height x width:       {flower_height} x {flower_width}") if info >= 3 else None

    flower_heights.append(flower_height)
    flower_widths.append(flower_width)

  print(f"\nThe selected draw height is:       {draw_height}") if info >= 2 else None

  print(f"The selected draw width is:        {draw_width}\n") if info >= 2 else None

  print(f"Seed: {seed}") if info >= 1 else None
  random.seed(seed)

  selected_flowers = []
  drawing = [''] * draw_height
  draw_width_left = draw_width
  while draw_width_left > 0:

    eligible_flowers = [index for index, (flower_height, flower_width) in enumerate(zip(flower_heights, flower_widths)) if flower_height <= draw_height and flower_width <= draw_width_left]
    print(f"The eligible flowers are:        {eligible_flowers}") if info >= 3 else None

    selected_flower = random.choice(eligible_flowers)
    print(f"The selected flower number:      {selected_flower}") if info >= 3 else None
    selected_flowers.append(selected_flower)

    flower = flowers[selected_flower]

    flower_height = flower_heights[selected_flower]
    flower_width = flower_widths[selected_flower]
    print(f"The flower height x width:       {flower_height} x {flower_width}") if info >= 3 else None

    height_difference = draw_height - flower_height

    for i in range(height_difference):
      drawing[i] = drawing[i] + flower_width * " "

    for i in range(flower_height):
      drawing[i+height_difference] = drawing[i+height_difference] + flower[i]

    draw_width_left = draw_width_left - flower_width
    print(f"draw width left: {draw_width_left}\\n") if info >= 3 else None

  sleep_time = load_time / draw_height
  print(f"each step waiting for: {sleep_time}") if info >= 2 else None
  print(f"Selected flowers: {selected_flowers}") if info >= 2 else None

  for row in drawing:
    time.sleep(sleep_time)
    print(row)


