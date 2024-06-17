# FORKDROID

Automated forklift with machine vision.

## What is this?

This repository tracks the development of Forkdroid, a machine-vision powered robot which automates moving materials over short distances.
The Forkdroid prototype is a small-form robot actuated by SG90 servomotors with a Raspberry Pi Zero & Pi Camera.

#### Assembled prototype

#### Vision processing using OpenCV

## Repository structure

### Hardware

Fritzing files

See `schematics/`

### 3D Models

STL files

See `models/`

### Software

See `src/`

### Other files

Simulation scenes, diagrams

See `etc/`

### Todo

[TODO.md](https://github.com/NIU1600415/rlp_forkdroid/blob/main/TODO.md)

## Software

### Requirements

- Python 3
- Node >= 14
- Yarn

### Libraries

The minimum required Python libraries are `numpy, opencv & requests`.

For running the simulation, CoppeliaSim is required. See `requirements_sim.txt`.

For running on the Raspberry Pi, `requirements_phys.txt` must be satisfied. It includes Adafruit PCA9685 & picamera2, which should be included with Raspberry Pi OS.

The `server` & `ui` packages have their own npm requirements, and they use `Express` & `Vite`.

### Running

Find how to run either the simulation or the robot package in the [Software README](https://github.com/NIU1600415/rlp_forkdroid/blob/main/src/README.md)

## Hardware

The hardware used on the prototype robot is the following:

- Wifi enabled Raspberry Pi Zero
- Pi Camera rev. 2.1
- Adafruit PCA9685
- SG90 servomotor x5, 4 modified for continuous rotation (wheels)
- x4 2400mAh NiMh batteries, AA form-factor.
- LM2596 DC-DC buck converter (Pi power source)
- Toggle switch

## Modelling

See the [Models README](https://github.com/NIU1600415/rlp_forkdroid/blob/main/models/README.md) for more information.
The prototype modelling was fabricated using a combination of 3D printing and laser cutting.

## LICENSE

MIT

## References

- https://manual.coppeliarobotics.com/en/apiFunctions.htm

- https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

- https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
