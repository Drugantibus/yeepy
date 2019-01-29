# yeepy

##### A command line tool for controlling Yeelight RGB lightbulbs

## Usage:
`$ python yee.py [-h] [--reset] command argument`

`command` can be `power`, `bright`, `temp`, `color`, or `status`.

`argument` is dependent on `command`:
* `power`:
  - `on`
  - `off`
  - `toggle`
* `bright`:
  - a number 1-100
* `temp`:
  - a number 2500-6500
* `color`:
  - `red`
  - `green`
  - `blue`
  - a hex code in the form `'#ffffff'`
* `status` takes no argument

## Installation:
Install the only dependency:
`pip install yeelight`

Run

`$ git clone https://github.com/drugantibus/yeepy ~/yeepy`

and then add an alias to your `.bashrc` or `.zshrc`:

`alias yee="python ~/yeepy/yeel.py"`.

You can now turn your Yeelight on and off using
`$ yee power toggle`!

## TODO:
* Support natural values for `bright` and `temp`: (e.g. "full", "cold", etc.)
* Multi-bulb support
* Non-color bulb support
* Scene support
* GUI

This is very much a work-in-progress. Any and all contributions, issues included, are very appreciated.
