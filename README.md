# rtcqs-python

## Introduction

rtcqs-python, pronounced arteeseeks, is an attempt to port raboof's excellent [realtimeconfigquickscan](https://github.com/raboof/realtimeconfigquickscan) script to Python.

## Rationale

Why a port to Python?
- A Python version might be easier to maintain as Python seems to be more popular than Perl (i.e. there are 50 times more Python based repositories on Github than their Perl counterparts)
- I'm personally more proficient with Python than with Perl, this makes it it easier and faster for me to add or improve features
- A Python port allowed me to slap a more permissive license on the code
- Possibility to update or remove outdated features and add new features
- Python probably has better GUI bindings which might make it easier to add a nice GUI

## Features

Basically the same as the realtimeconfigquickscan:
- Root check
- Audio group check
- Background process scan
- CPU frequency check
- High resolution timers check
- 1000 Hz/No Hz check
- Preempt RT check
- rtprio check
- Swappiness check

## Usage

When writing this script I could rely on Python's built-in functionality so no extra modules are needed, just Python 3. To run the script first clone this repository.

```
git clone https://github.com/autostatic/rtcqs-python.git
```

Then cd into the newly created directory.

```
cd rtcqs-python
```

And run the script.

```
python3 ./rtcqs-python
```

Or add the executable bit and run the script directly.

```
cd rtcqs-python
chmod +x rtcqs-python
./rtcqs-python
```

## Future plans

- Make the project more modular so it gets easier to add new features
- Add a Qt GUI

## Contact

To contact me send me a mail or if it's a technical issue or question, use this project's issue tracker.

## Thanks

Many thanks of course to the original author of realtimeconfigquickscan, Arnout Engelen a.k.a. raboof.