=====
rtcqs
=====

Introduction
------------

rtcqs is a Python utility to analyze your system and detect possible 
bottlenecks that could have a negative impact on the performance of your 
system when working with Linux audio. It is heavily inspired by raboof's 
excellent `realtimeconfigquickscan 
<https://github.com/raboof/realtimeconfigquickscan>`_
script in Python.

Features
--------

Basically the same as realtimeconfigquickscan:

- Root check
- Audio group check
- CPU frequency check
- High resolution timers check
- Preempt RT check
- rtprio check
- Swappiness check
- Filesystem check

Additional features:

- Spectre/Meltdown mitigations check
- Basic IRQ check of sound cards and USB ports
- Power management check
- Qt GUI
- tkinter GUI

Usage
-----

When writing this script I could rely on Python's built-in functionality so 
no extra modules are needed, just Python 3. To run the script first clone 
this repository.
::

 git clone https://codeberg.org/rtcqs/rtcqs.git

Then cd into the newly created directory.
::

  cd rtcqs

And run the script.
::

 ./src/rtcqs/rtcqs.py

GUI
---

rtcqs comes with two GUI's, a basic and light tkinter GUI and a polished and 
heavy Qt GUI. To run the GUI first install the PySimpleGUI (tkinter) or 
PySimpleGUIQt (Qt) module either in your home directory or in a virtual 
environment. Bear in mind that the Qt version will pull in a lot of 
dependencies and is in a beta state. Hence I do not recommend using the Qt 
version and installation of the Qt GUI is not covered in this manual.

Home directory
``````````````

Make sure ``pip`` is installed, on Ubuntu this would be the ``python3-pip`` 
package. For the tkinter GUI you will also need ``python3-tk``. Then install 
PySimpleGUI or PySimpleGUIQt for your user.

For the tkinter GUI you will need rtcqs and the PySimpleGUI module.
::

  pip install rtcqs PySimpleGUI

Virtual Environment
```````````````````

Make sure the virtual environment module is installed, on Ubuntu this would 
be ``python3-venv``. Then create a virtual environment in the rtcqs directory 
and install PySimpleGUI or PySimpleGUIQt in there.

For the tkinter GUI use the following commands.
::

  python3 -m venv venv &&
  . venv/bin/activate &&
  pip install --upgrade pip setuptools rtcqs PySimpleGUI

You can now run the GUI with ``rtcqs_gui``. Next time 
you'd like to run the GUI load the virtual environment again and spin up the 
GUI.
::

  . venv/bin/activate
  rtcqs_gui

Overview
````````

When running the GUI it will immediately show the results of the checks. All 
checks have their own tab. Each tab title consists of a symbol that shows the 
check result and the name of the check. A ✔ means the check was successful 
while a ✘ means rtcqs encountered an issue. This way you can quickly spot 
which checks have issues.

Clicking 'Cancel' will close rtcqs. Clicking 'About' will bring up a popup 
window which displays the version and a short description.

.. figure:: https://codeberg.org/attachments/5092d94a-2a06-4be1-b04e-ca61ae6ed732
   :align: center

   *rtcqs main window (tkinter version)*

.. figure:: https://codeberg.org/attachments/5345ce8a-773a-448a-9bac-a2fe5fd44b94
   :align: center

   *rtcqs main window (Qt version)*

.. figure:: https://codeberg.org/attachments/c0f72b82-470c-4f90-86d5-736226a146ed
   :align: center

   *rtcqs about window (tkinter version)*

.. figure:: https://codeberg.org/attachments/4dc26f40-76c9-4738-bfff-c57457f7f9bb
   :align: center

   *rtcqs about window (Qt version)*

Future plans
------------

- Extend filesystem check
- Disk scheduler check


Contact
-------

To contact me send me a mail or if it's a technical issue or question, use 
this project's issue tracker.

Thanks
------

Many thanks of course to the original author of realtimeconfigquickscan, 
Arnout Engelen a.k.a. raboof.