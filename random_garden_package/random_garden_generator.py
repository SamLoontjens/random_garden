import random
import time
import sys
import pkg_resources

# For testing purposes
def random_garden_test(file_name):
  file_path = pkg_resources.resource_filename('random_garden_package', f'flowers/{file_name}')
  with open(file_path, 'r') as file:
    art = file.read()
  print(art)

# Generates a random garden
def random_garden(draw_height = 20, draw_width = 200, seed = random.randrange(sys.maxsize), load_time = 20):
  # flowers from https://www.asciiart.eu/plants/flowers
  # note if there is an \\ in the flower it has to be dubbled to \\\\
  # make sure all flowers are square, and the top row is used for width
  flowers = [
  [#0 tiny patch of grass by SL
  "^"
  ],
  [#1 flower by MT
  "   _   ",
  " .\\ /. ",
  "< ~O~ >",
  " '/_\\' ",
  " \\ | / ",
  "  \\|/  ",
  "^^^^^^^"
  ],
  [#2 flower 1 from the Flower Garden by Joan G. Stark
  "  @@@@ ",
  " @@()@@",
  "  @@@@ ",
  "   /   ",
  "\\ |    ",
  "\\\\|//  ",
  "^^^^^^^^"
  ],
  [#3 flower 2 from the Flower Garden by Joan G. Stark
  "wWWWw ",
  "(___) ",
  "  Y   ",
  "\\ |/  ",
  "\\\\|///",
  "^^^^^^"
  ],
  [#4 flower 3 from the Flower Garden by Joan G. Stark
  "   _     ",
  " _(_)_   ",
  "(_)@(_)  ",
  "  (_)\\   ",
  "     `|/ ",
  "     \\|  ",
  "      | /",
  "   \\\\\\|//",
  "^^^^^^^^^"
  ],
  [#5 flower 4 from the Flower Garden by Joan G. Stark
  " vVVVv ",
  " (___) ",
  "   Y   ",
  "  \\|/  ",
  " \\ | / ",
  "\\\\\\|///",
  "^^^^^^^"
  ],
  [#6 flower 5 from the Flower Garden by Joan G. Stark
  "   _   ",
  " _(_)_ ",
  "(_)@(_)",
  " /(_)  ",
  "\\|/    ",
  "\\|///  ",
  "^^^^^^^"
  ],
  [#7 flower 6 from the Flower Garden by Joan G. Stark
  "  @@@@ ",
  " @@()@@",
  "  @@@@ ",
  "  \\|   ",
  "   |/  ",
  "\\\\\\|// ",
  "^^^^^^^"
  ],
  [#8 flower 7 from the Flower Garden by Joan G. Stark
  "wWWWw",
  "(___)",
  "  Y  ",
  " \\|/ ",
  "  |/ ",
  " \\|  ",
  "\\\\|//",
  "^^^^^"
  ],
  [#9 flower 8 from the Flower Garden by Joan G. Stark
  "   _    ",
  " _(_)_  ",
  "(_)@(_) ",
  "  (_)\\  ",
  "     |  ",
  "    \\|/ ",
  "  \\\\\\|//",
  "^^^^^^^^"
  ],
  [#10 by by Joan G. Stark
  "      wWWWw       ",
  "vVVVv (___) wWWWw ",
  "(___)  ~Y~  (___) ",
  " ~Y~   \\|    ~Y~  ",
  " \\|   \\ |/   \\| / ",
  "\\\\|// \\\\|// \\\\|///",
  "^^^^^^^^^^^^^^^^^^"
  ],
  [#11 by by Joan G. Stark
  "       wWWWw        ",
  "       (___)  vVVVv ",
  "vVVVv   ~Y~   (___) ",
  "(___)    |/    ~Y~  ",
  "\\~Y~/   \\|    \\ |/  ",
  "\\\\|//  \\\\|// \\\\\\|///",
  "^^^^^^^^^^^^^^^^^^^^"
  ],
  [#12 by ejm97
  "    __/) ",
  "   (__(=:",
  "|\\ |  \\) ",
  "\\ ||     ",
  " \\||     ",
  "  \\|     ",
  "   |     ",
  "^^^^^^^^^"
  ],
  [#13 Lilies by Joan G. Stark
  "   ,_('--,           ",
  "     (.--; ,--')_,   ",
  "         | ;--.)     ",
  "     .-. |.| .-.     ",
  "        \\|\\|/ .-.    ",
  "    .-.`\\|/|/`_      ",
  "       `\\|/|/` '     ",
  "`^`^^`^``^``^``^``^``"
  ],
  [#14 Clover patch by Joan G. Stark
  "     ,,,                      ,,,                  ",
  "    {{{}}    ,,,             {{{}}    ,,,          ",
  " ,,, ~Y~    {{{}},,,      ,,, ~Y~    {{{}},,,      ",
  "{{}}} |/,,,  ~Y~{{}}}    {{}}} |/,,,  ~Y~{{}}}     ",
  " ~Y~ \\|{{}}}/\\|/ ~Y~  ,,, ~Y~ \\|{{}}}/\\|/ ~Y~  ,,, ",
  " \\|/ \\|/~Y~  \\|,,,|/ {{}}}\\|/ \\|/~Y~  \\|,,,|/ {{}}}",
  " \\|/ \\|/\\|/  \\{{{}}/  ~Y~ \\|/ \\|/\\|/  \\{{{}}/  ~Y~ ",
  " \\|/\\\\|/\\|/ \\\\|~Y~//  \\|/ \\|/\\\\|/\\|/ \\\\|~Y~//  \\|/ ",
  " \\|//\\|/\\|/,\\\\|/|/|// \\|/ \\|//\\|/\\|/,\\\\|/|/|// \\|/ ",
  "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
  ],
  [#15 by Joan G. Stark
  "                       `::`                 ",
  "                        /                   ",
  "                       `    `;:`            ",
  "    _          .;:;          /              ",
  "  _(_)_        ::;       wWWWw  ,,,     _   ",
  " (_)@(_),,,  _ ';:;;'    (___) {{{}}  _(_)_ ",
  "  /(_) {{{}} >'. ||  _    ~Y~   ~Y~  (_)@(_)",
  "  |  {{}~Y~  `> \\||.'< (@)\\|{}} \\|/   /(_)  ",
  "(\\|/)~Y~\\|/    `>|/ <` \\Y/\\|~Y~ \\|/ (\\|/)   ",
  " \\|//\\|/\\|//    `||/`  \\|/\\|\\|/\\\\|//\\\\|//   ",
  "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
  ],
  [#16 Spring Garden by Joan G. Stark
  "      ,            __ \\/ __                                   ",
  "  /\\^/`\\          /o \\{}/ o\\   If I had a flower for each time",
  " | \\/   |         \\   ()   /     I thought of you, my garden  ",
  " | |    |          `> /\\ <`   ,,,     would be full...        ",
  " \\ \\    /  @@@@    (o/\\/\\o)  {{{}}                 _ _        ",
  "  '\\\\//'  @@()@@  _ )    (    ~Y~       @@@@     _{ ' }_      ",
  "    ||     @@@@ _(_)_   wWWWw .oOOo.   @@()@@   { `.!.` }     ",
  "    ||     ,/  (_)@(_)  (___) OO()OO    @@@@  _ ',_/Y\\_,'     ",
  "    ||  ,\\ | /)  (_)\\     Y   'OOOO',,,(\\|/ _(_)_ {_,_}       ",
  "|\\  ||  |\\\\|// vVVVv`|/@@@@    _ \\/{{}}}\\| (_)@(_)  |  ,,,    ",
  "| | ||  | |;,,,(___) |@@()@@ _(_)_| ~Y~ wWWWw(_)\\ (\\| {{{}}   ",
  "| | || / / {{}}} Y  \\| @@@@ (_)#(_) \\|  (___)   |  \\| /~Y~    ",
  " \\ \\||/ /\\\\|~Y~ \\|/  | \\ \\/  /(_) |/ |/   Y    \\|/  |//\\|/    ",
  "\\ `\\\\//`,.\\|/|//.|/\\\\|/\\\\|,\\|/ //\\|/\\|.\\\\\\| // \\|\\\\ |/,\\|/    ",
  "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
  ],
  [#17 Tulip by Joan G. Stark
  "      ,    ",
  "  /\\^/`\\   ",
  " | \\/   |  ",
  " | |    |  ",
  " \\ \\    /  ",
  "  '\\\\//'   ",
  "    ||     ",
  "    ||     ",
  "    ||     ",
  "    ||  ,  ",
  "|\\  ||  |\\ ",
  "| | ||  | |",
  "| | || / / ",
  " \\ \\||/ /  ",
  "  `\\\\//`   ",
  "^^^^^^^^^^^"
  ],
  [#18 by Susie Oviatt
  "              .                                                     ",
  "             .@.                                    .               ",
  "             @m@,.                                 .@               ",
  "            .@m%nm@,.                            .@m@               ",
  "           .@nvv%vnmm@,.                      .@mn%n@               ",
  "          .@mnvvv%vvnnmm@,.                .@mmnv%vn@,              ",
  "          @mmnnvvv%vvvvvnnmm@,.        .@mmnnvvv%vvnm@              ",
  "          @mmnnvvvvv%vvvvvvnnmm@, ;;;@mmnnvvvvv%vvvnm@,             ",
  "          `@mmnnvvvvvv%vvvvvnnmmm;;@mmnnvvvvvv%vvvvnmm@             ",
  "           `@mmmnnvvvvvv%vvvnnmmm;%mmnnvvvvvv%vvvvnnmm@             ",
  "             `@m%v%v%v%v%v;%;%;%;%;%;%;%%%vv%vvvvnnnmm@             ",
  "             .,mm@@@@@mm%;;@@m@m@@m@@m@mm;;%%vvvnnnmm@;@,.          ",
  "          .,@mmmmmmvv%%;;@@vmvvvvvvvvvmvm@@;;%%vvnnm@;%mmm@,        ",
  "       .,@mmnnvvvvv%%;;@@vvvvv%%%%%%%vvvvmm@@;;%%mm@;%%nnnnm@,      ",
  "    .,@mnnvv%v%v%v%%;;@mmvvvv%%;*;*;%%vvvvmmm@;;%m;%%v%v%v%vmm@,.   ",
  ",@mnnvv%v%v%v%v%v%v%;;@@vvvv%%;*;*;*;%%vvvvm@@;;m%%%v%v%v%v%v%vnnm@,",
  "`    `@mnnvv%v%v%v%%;;@mvvvvv%%;;*;;%%vvvmmmm@;;%m;%%v%v%v%vmm@'   '",
  "        `@mmnnvvvvv%%;;@@mvvvv%%%%%%%vvvvmm@@;;%%mm@;%%nnnnm@'      ",
  "           `@mmmmmmvv%%;;@@mvvvvvvvvvvmmm@@;;%%mmnmm@;%mmm@'        ",
  "              `mm@@@@@mm%;;@m@@m@m@m@@m@@;;%%vvvvvnmm@;@'           ",
  "             ,@m%v%v%v%v%v;%;%;%;%;%;%;%;%vv%vvvvvnnmm@             ",
  "           .@mmnnvvvvvvv%vvvvnnmm%mmnnvvvvvvv%vvvvnnmm@             ",
  "          .@mmnnvvvvvv%vvvvvvnnmm'`@mmnnvvvvvv%vvvnnmm@             ",
  "          @mmnnvvvvv%vvvvvvnnmm@':%::`@mmnnvvvv%vvvnm@'             ",
  "          @mmnnvvv%vvvvvnnmm@'`:::%%:::'`@mmnnvv%vvmm@              ",
  "          `@mnvvv%vvnnmm@'     `:;%%;:'     `@mvv%vm@'              ",
  "           `@mnv%vnnm@'          `;%;'         `@n%n@               ",
  "            `@m%mm@'              ;%;.           `@m@               ",
  "             @m@'                 `;%;             `@               ",
  "             `@'                   ;%;.             '               ",
  "   ,          `                    `;%;                             ",
  "   %,                               ;%;.                            ",
  "   `;%%%%%%%,                       `;%;                            ",
  "     `%%%%%%%%%,                     ;%;.                           ",
  "              ::,                    `;%;                           ",
  "              ::%,                    ;%;                           ",
  "              ::%%,                   ;%;                           ",
  "              ::;%%                  .;%;                           ",
  "              ::;;%%                 ;%;'                           ",
  "              `::;%%                .;%;                            ",
  "               ::;;%%               ;%;'                            ",
  "               `::;%%              .;%;                             ",
  "                ::;;%%             ;%;'                             ",
  "                `::;%%            .;%;                              ",
  "                 ::;;%%           ;%;'                              ",
  "                 `::;%%          .;%;                               ",
  "                  ::;;%%         ;%;'                               ",
  "                  `::;%%        .;%;                                ",
  "                   ::;%%,       ;%;'                                ",
  "                   `::;%%      .;%;                                 ",
  "                    ::;%%      ;%;'                                 ",
  "                    `::%%     .;%;                                  ",
  "                     ::%%     ;%;'                                  ",
  "                     `:;%    .;%;                                   ",
  "                      :;%   .;%;'                                   ",
  "                      :;%  .;%%;                                    ",
  "                      `:% .;%%;'                                    ",
  "                       `::%%;'                                      ",
  "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
  ],
  [#19
  "  _    _      ",
  " /=\\''/=\\^    ",
  "(=(0_0 |=)__  ",
  " \\_\\ _/_/   ) ",
  "   /_/   _  /\\",
  "  |/ |\\ || |  ",
  "     ~ ~  ~   ",
  "^^^^^^^^^^^^^^"
  ],
  [#20 Hummingbird by ejm
  "    __/)      __ ",
  "   (__( ---@./ww ",
  "|\\ |  \\)    (\\   ",
  '\\ ||         "\'  ',
  " \\||             ",
  "  \\|             ",
  "   |             ",
  "^^^^^^^^^^^^^^^^^"
  ]
  ]

  total_flowers = len(flowers)
  print(f"The total number of flowers is:    {total_flowers}")

  flower_heights = []
  flower_widths = []
  for flower in flowers:
    flower_height = len(flower)
    flower_width = len(flower[0])
    #print(f"The flower height x width:       {flower_height} x {flower_width}")

    flower_heights.append(flower_height)
    flower_widths.append(flower_width)

  #draw_height = 20
  print(f"\nThe selected draw height is:       {draw_height}")

  #draw_width = 200
  print(f"The selected draw width is:        {draw_width}\n")

  print(f"Seed: {seed}")
  random.seed(seed)

  selected_flowers = []
  drawing = [''] * draw_height
  draw_width_left = draw_width
  while draw_width_left > 0:

    eligible_flowers = [index for index, (flower_height, flower_width) in enumerate(zip(flower_heights, flower_widths)) if flower_height <= draw_height and flower_width <= draw_width_left]
    #print(f"The eligible flowers are:        {eligible_flowers}")

    selected_flower = random.choice(eligible_flowers)
    #print(f"The selected flower number:      {selected_flower}")
    selected_flowers.append(selected_flower)

    flower = flowers[selected_flower]

    flower_height = flower_heights[selected_flower]
    flower_width = flower_widths[selected_flower]
    #print(f"The flower height x width:       {flower_height} x {flower_width}")

    height_difference = draw_height - flower_height

    for i in range(height_difference):
      drawing[i] = drawing[i] + flower_width * " "

    for i in range(flower_height):
      drawing[i+height_difference] = drawing[i+height_difference] + flower[i]

    draw_width_left = draw_width_left - flower_width
    #print(f"draw width left: {draw_width_left}\\n")

  sleep_time = load_time / draw_height
  print(f"each step waiting for: {sleep_time}")
  print(f"Selected flowers: {selected_flowers}")
  for row in drawing:
    time.sleep(sleep_time)
    print(row)


