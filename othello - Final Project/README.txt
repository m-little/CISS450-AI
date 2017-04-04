AI - Adversarial Search
Y. Liow

This is used in my CISS450 AI class.
Most of the files are pyc files.
The only python source included is config.py and agent.py.
(This is to make sure that you implement some of the python source code on their own.)

To run it:
I assume you are using Python 2.7 with pygame installed.
The python program to run is RUNTHIS.py.

Take a look at config.py.
This will allow you to set some parameters for the game.

The python source file Agent.py contains some othello playing agents.
You should modify the class AIAgent.
You can create other classes if you like.
But you have to change config.py to pick a different Agent subclass.

The given AIAgent doesn't do much: picks a random (row, column).
The AIAgent class uses some of my classes/methods.
I have deliberately added code to slow down your AIAgent.
Therefore to speed up your AIAgent:
You should rewrite all the code in the AIAgent class.

EXERCISE:
The simplest thing you can do right away is to rewrite the AIAgent so that it picks a move that maximizes the number of white pieces in one move.

No copyright. At this point, I don't have time to worry about that.
-------------------------------------------------------------------------------
LOG:
04/03: Added agent options in config.py
04/02: Added config.py to handle some configuration.
04/02: First release to students.
