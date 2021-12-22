# rtcqs

## Introduction

rtcqs, pronounced arteeseeks, is an attempt to port raboof's excellent [realtimeconfigquickscan](https://github.com/raboof/realtimeconfigquickscan) script to Python.

## Rationale

Why a port to Python?
- A Python version might be easier to maintain as Python seems to be more popular than Perl (i.e. there are 50 times more Python based repositories on Github than their Perl counterparts)
- I'm personally more proficient with Python than with Perl, this makes it it easier and faster for me to add or improve features
- A Python port allowed me to slap a more permissive license on the code
- Python probably has better GUI bindings which might make it easier to add a nice GUI
- Seized the opportunity to remove obsolete features
- Incentive to improve the documentation in the linuxaudio.org wiki

## Features

Basically the same as realtimeconfigquickscan:
- Root check
- Audio group check
- Background process check
- CPU frequency check
- High resolution timers check
- System timer check
- Preempt RT check
- rtprio check
- Swappiness check
- max_user_watches check
- Filesystem check

Added features:
- Spectre/Meltdown mitigations check
- Basic IRQ check of sound cards and USB ports
- Qt GUI

## Usage

When writing this script I could rely on Python's built-in functionality so no extra modules are needed, just Python 3. To run the script first clone this repository.

```
git clone https://codeberg.org/rtcqs/rtcqs.git
```

Then cd into the newly created directory.

```
cd rtcqs
```

And run the script.

```
./rtcqs.py
```

## GUI

To run the GUI first install the PySimpleGUIQt module either in your home directory or a virtual environment.

### Home directory

Make sure `pip` is installed, on Ubuntu this would be the `python3-pip` package. Then install PySimpleGUIQt for your user.

```
pip install PySimpleGUIQt
```

### Virtual Environment

Make sure the virtual environment module is installed, on Ubuntu this would be `python3-venv`. Then create a virtual environment in the rtcqs directory and install PySimpleGUIQt in there.

```
python3 -m venv venv &&
. venv/bin/activate &&
pip install --upgrade pip setuptools PySimpleGUIQt
```

You can now run the GUI with `./rtcqs_gui.py`. Next time you'd like to run the GUI load the virtual environment again and spin up the GUI.

```
. venv/bin/activate
./rtcqs_gui.py
```

### Overview

When running the GUI it will imediately show the results of the checks. All checks have their own tab. Each tab title consists of a symbol that shows the check result and the name of the check. A ✔ means the check was successful while a ✘ means rtcqs encountered an issue. This way you can quickly spot which checks have issues.

Clicking 'Cancel' will close rtcqs. Clicking 'About' will bring up a popup window which displays the version and a short description.

<center><em>

![rtcqs_analysis](https://codeberg.org/attachments/8aaff793-d9b5-42f1-8c98-3d98ef31853d)<br>
rtcqs main window
<br>
<br>
![rtcqs_about](https://codeberg.org/attachments/832bbca7-24d2-4a36-8e04-3f6a03438243)<br>
rtcqs about window

</em></center>

## Future plans

- Make the project more modular so it gets easier to add new features

## Contact

To contact me send me a mail or if it's a technical issue or question, use this project's issue tracker.

## Thanks

Many thanks of course to the original author of realtimeconfigquickscan, Arnout Engelen a.k.a. raboof.