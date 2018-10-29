# yl.py
___
#### A command line tool for controlling Yeelight RGB lightbulbs

## Usage:
`$ python yl.py command argument`

`command` can be `power`, `bright`, `temp`, or `color`.

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
