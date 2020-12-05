"""gif to ansi art converter
A simple python script that converts a gif into ansi art that can be displayed in an ANSI terminal.
Display converted gif with `while [ true ]; do cat {}; done` in bash or `FOR /L %L IN (0,0,1) DO @(copy {} con)` in cmd.
Available on GitHub at https://github.com/soup-dog/gif-to-ansi

prerequisites:
  Pillow (working with 8.0.1)

usage: g2a.py [-h] [-w WIDTH] [-he HEIGHT] [-fr FRAME_RATE] [-so] [-sp]
              input_file output_file

positional arguments:
  input_file            path to input file
  output_file           path to output file

optional arguments:
  -h, --help            show this help message and exit
  -w WIDTH, --width WIDTH
                        width of output
  -he HEIGHT, --height HEIGHT
                        height of output
  -fr FRAME_RATE, --frame-rate FRAME_RATE
                        frame-rate of output
  -so, --show-output    show output
  -sp, --show-progress  display conversion progress
"""


from PIL import Image, ImageSequence
import argparse
import sys


ESC = "\u001b"
CSI = "["
SGR_END = "m"
CHA_END = "G"
CUP_END = "H"
ED_END = "J"
RESET_CURSOR = ESC + CSI + "1;1" + CUP_END
HIDE_CURSOR = ESC + CSI + "?25l"
RESET_DISPLAY = ESC + CSI + "0" + SGR_END + ESC + CSI + "2" + ED_END


def get_rgb_escape(r: float, g: float, b: float) -> str:
    return "\u001b[48;2;{};{};{}m".format(r, g, b) + "\u001b[38;2;{};{};{}m".format(r, g, b)


def brightness(r: float, g: float, b: float) -> float:
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def image_to_text(image: Image, palette=None) -> str:
    if palette is None:
        palette = {
            64: "█",
            128: "▓",
            192: "▒",
            256: "░",
        }

    text = ""

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            escape = get_rgb_escape(*image.getpixel((x, y)))
            character = next(palette[k] for k in palette.keys() if brightness(*image.getpixel((x, y))) < k)
            text += escape + character
        text += ESC + CSI + "0" + SGR_END + "\n"

    return text


if __name__ == '__main__':
    bar_length = 10
    info = "ANSI art gif made with gif-to-ansi (available on GitHub at https://github.com/soup-dog/gif-to-ansi)"

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="path to input file")
    parser.add_argument("output_file", type=str, help="path to output file")
    parser.add_argument("-w", "--width", type=int, help="width of output")
    parser.add_argument("-he", "--height", type=int, help="height of output")
    parser.add_argument("-fr", "--frame-rate", type=int, help="frame-rate of output", default=15)
    parser.add_argument("-so", "--show-output", action="store_true", help="show output", default=False)
    parser.add_argument("-sp", "--show-progress", action="store_true", help="display conversion progress", default=False)

    args = parser.parse_args()

    image = Image.open(args.input_file)

    frames = [frame.copy().convert("RGB") for frame in ImageSequence.Iterator(image)]

    frames = [frame.resize((frame.size[0] if args.width is None else args.width, frame.size[1] if args.height is None else args.height)) for frame in frames]

    text = HIDE_CURSOR + info + "\n"

    round_progress = 0

    for index, frame in enumerate(frames):
        image_text = image_to_text(frame)
        if args.show_output:
            print(RESET_CURSOR + image_text)

        text += RESET_CURSOR + image_text

        if args.show_progress:
            progress = index / len(frames)
            if round_progress != (round_progress := int(bar_length * progress + 0.5)):
                bar = "[{}{}]".format("█" * round_progress, " " * (bar_length - round_progress))
                sys.stdout.write(ESC + CSI + "1" + CHA_END + bar)
                sys.stdout.flush()

    text += RESET_DISPLAY

    if args.show_progress:
        print()

    with open(args.output_file, "wb") as f:
        f.write(bytes(text, "utf-8"))

    print("Done.")
    print("Converted {} to {}".format(args.input_file, args.output_file))
    print("Display in bash with `cat {}`".format(args.output_file))
    print("Loop in bash with `while [ true ]; do cat {}; done`".format(args.output_file))
    print("Display in cmd with `copy {} con`".format(args.output_file))
    print("Loop in cmd with `FOR /L %L IN (0,0,1) DO @(copy {} con)`".format(args.output_file))
