# Introduction
This project is a simulator for co-axial transmission lines. It allows user to connect cables of different resistance and observe how a signal would look like traveling across it.

# Requirement
* homebrew (on Mac)
* [Python](https://www.python.org) (2.7.13)
* pip
* kivy (install instruction for [Mac](https://kivy.org/docs/installation/installation-osx.html) | [Windows](https://kivy.org/docs/installation/installation-windows.html))

# Deployment OSX
1. Download the [latest release](../../releases/latest).

2. Navigate to downloaded folder (the one containing this README file), and run `pip install -r requirements.txt`.

3. Run `garden install matplotlib`.

4. Run `python src`

# Deployment Windows
1. Download the [latest release](../../releases/latest).

2. In the command prompt, navigate to your python installation folder (default is "C:\python27", so type in `cd C:\python27` and hit enter). Type `pip install -r ` (notice the trailing space) then drag the `requirements.txt` file from the downloaded folder into the command prompt and hit enter.

3. Type `Scripts\garden install matplotlib` and hit enter.

4. Type `python ` (notice the trailing space) the drag the `src` folder from the downloaded folder into the command prompt and hit enter.