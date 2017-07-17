# Introduction
This project is a simulator for co-axial transmission lines. It allows user to connect cables of different resistance and observe how a signal would look like traveling across it.

# Requirement
* homebrew
* pip
* [Python](https://www.python.org) (2.7.13)

# Deployment OSX
1. Download the [latest release](../../releases/latest).

2. Open terminal and run `brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer`.

3. Run `pip install kivy-garden`.

4. Run `garden install matplotlib`.

5. Navigate to downloaded folder (the one containing this README file), and run `pip install -r requirements.txt`.

6. Run `python src`

# Deployment Windows
1. Download the [latest release](../../releases/latest).

2. Delete `src/kivy` folder.

3. Install kivy for Windows by following instructions [here](https://kivy.org/docs/installation/installation-windows.html).

4. Run `pip install kivy-garden`.

5. Run `garden install matplotlib`.

6. Navigate to downloaded folder (the one containing this README file), and run `pip install -r requirements.txt`.

7. Run `python src`