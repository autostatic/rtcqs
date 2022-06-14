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
script.

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
- tkinter GUI
- Qt GUI (beta)

Installation
------------
GUI
```
If you want to use the GUI you will have to install the ``python3-tk`` 
package or similar for your distro.

Home directory
``````````````

Make sure ``pip`` is installed, on Ubuntu this would be the ``python3-pip`` 
package. With ``pip`` installed you can install rtcqs with the following 
command.
::

  pip install --upgrade rtcqs

You can now run rtcqs by simply running ``rtcqs`` in a terminal. The GUI can 
be run with with ``rtcqs_gui``.

Virtual Environment
```````````````````

Make sure the virtual environment module is installed, on Ubuntu this would 
be ``python3-venv``. Then create a virtual environment in a directory of 
choice and install rtcqs in there.
::

  mkdir -p ~/path/to/rtcqs
  cd ~/path/to/rtcqs
  python3 -m venv venv &&
  . venv/bin/activate &&
  pip install --upgrade rtcqs

You can now run rtcqs by simply running ``rtcqs`` in a terminal. The GUI can 
be run with with ``rtcqs_gui``. Next time you'd like to run the script or the 
GUI load the virtual environment again and run either ``rtcqs`` or 
``rtcqs_gui``.
::

  . venv/bin/activate
  rtcqs
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

.. figure:: https://codeberg.org/attachments/c0f72b82-470c-4f90-86d5-736226a146ed
   :align: center

   *rtcqs about window (tkinter version)*

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