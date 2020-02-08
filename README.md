# RandoGrid
Blender addon to create tunnels of random angled grid lines

![RandoGrid UI](https://imgur.com/1GNTImP.jpg)

### Installation

[Download the zip](https://github.com/mantissa-/RandoGrid/archive/master.zip) and install as an addon in Blender 2.80 or higher.
RandoGrid settings can be found in the side panel of the 3D viewport.

# Overview

**Number of lines:** Number of lines to generate in the grid block

**Line Steps (Length):** Number of angled steps each line gets in the block

**Start Offset:** Units to randomly offset the starting position of each line

**Width:** Random starting offset over the width for each line, also used as constraint when "Limit Width" is active

**Height:** Random starting offset over the height for each line, also used as constraint when "Limit Height" is active

**Limit Width:** Limit width of lines to starting width, ignored if step size is larger than width

**Limit Width:** Limit height of lines to starting width, ignored if step size is larger than height

**Length / Width / Height Step Growth:** Set the minimum and maximum step size in each direction

**Make Curve:** Convert the final result from mesh eges to a beveled curve
___

### Examples

![RandoGrid Example](https://imgur.com/nsQM3CA.jpg)
_Example of curve created with default settings_
