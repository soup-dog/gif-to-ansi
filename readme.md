# gif-to-ansi

A simple script for converting gifs into ANSI art that can be displayed in a terminal that supports ANSI escape sequences.

## Installation

### Prerequisites
[Python 3.9](https://www.python.org/downloads/release/python-390/)

[Pillow](https://github.com/python-pillow/Pillow) (tested with version 8.0.1)

```
pip install Pillow
```

### Usage

```
g2a.py [-h] [-w WIDTH] [-he HEIGHT] [-fr FRAME_RATE] [-so] [-sp]
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
```

## Examples
Some examples are located in [/examples](/examples). Display them in any ANSI terminal.

Bash: ```cat examples/example1.txt```

cmd: ```copy examples\example1.txt con```

![A gif demonstrating example usage](/example.gif)