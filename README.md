# Messenger
A 2D esolang with the goal of being as annoying as possible.

## Table of Contents
* [How To Run Messenger](#how-to-run-messenger)
* [How Messenger Works](#how-messenger-works)

## How To Run Messenger
This Messenger interpreter runs via the command line. Type <code>py \_\_init\_\_.py <i>&lt;code&gt;</i></code> to run *\<code\>*. You may need to surround the code in quotes to work.

>[!WARNING]
>The interpreter throws an error if you call it without any arguments. I may change this in the future.

In addition, you can add on some flags:
* `-c` or `--check` lets you check that the code you typed in was correct. If you don't like the code, type `No` (case-insensitive) in the prompt.
* `-h` or `--help` gives you a list of all of the arguments and options.
* `-i` or `--iterations` lets you change the number of iterations the code runs for before giving up. The default is 50,000, but this may not be enough for long-running `while` loops.

## How Messenger Works
Messenger has an extensive documentation [here](https://esolangs.org/wiki/Messenger), but here is a brief summary.

Messenger is based around sending actual messages to functions in 2D space and redirecting them into the right places.

A message can contain either a NULL, an INT, or a LIST. The equivalent types in Python are pretty much the same.

To run a code, a message is placed in the top-left corner, and travels in the direction corresponding to the redirector under it.

Now, on the 2D grid, any character that isn't a space is a function. Functions take 1 or 2 messages as arguments, and output 1 or 2 new messages.

If a function takes 2 messages as input, the order of when the messages enter the function determines the argument order.

If a message reaches the edge of the grid, three things can happen:
* **The message leaves the top or left edge:** It just disappears.
* **The message leaves the right edge:** The content the message is carrying gets printed verbatim.
* **The message leaves the bottom edge:** The content is treated as a series of Unicode codepoints and printed as the corresponding Unicode characters.

There are also tons of ways that things can go wrong in Messenger, which all result in an error:
* two messages colliding and annihilating each other,
* a message with invalid Unicode codepoints being printed,
* a function getting two messages at the same time,
* a function getting messages with invalid types,
* unknown characters in the code area,
* the code running too long,

etc.
