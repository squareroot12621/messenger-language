import argparse
import random
import time

### MESSENGERMESSAGE CLASS ###

class MessengerMessage:
    """A message in Messenger."""

    def __init__(self, x, y, direction, content, grid, inFunc=True):
        """Return a MessengerMessage with the corresponding position,
        direction, and content, as well as the grid the message is in.
        """
        self.x = x
        self.y = y
        self.dir = direction
        self.content = content
        self.grid = grid
        self.inFunc = inFunc
        self.movedThisTick = False
        self.needsInput = False

    def __repr__(self):
        """Return a string representation of the MessengerMessage."""
        if self.inFunc:
            direction = 'inside a function'
        else:
            direction = f'going {self.dir}'
        return (f'<Message containing {self.content} at ({self.x}, {self.y}) '
                f'{direction}>')

    @property
    def type(self):
        """Return one of 'NULL', 'INT', or 'LIST', depending on the
        content attribute.
        """
        if self.content is None:
            return 'NULL'
        elif isinstance(self.content, int):
            return 'INT'
        elif isinstance(self.content, list):
            return 'LIST'
        else:
            raise TypeError(f'Message content is of an invalid type '
                            f'({repr(self.content)})')
        
    def clone(self):
        """Return a deep copy of the MessengerMessage."""
        messageClone = MessengerMessage(self.x, self.y, self.dir, self.content,
                                        self.grid, self.inFunc)
        messageClone.movedThisTick = self.movedThisTick
        messageClone.needsInput = self.needsInput
        return messageClone

    def tick(self):
        """Move the MessengerMessage and update the self.dir,
        self.content, self.inFunc, and self.movedThisTick attributes.
        """
        self.movedThisTick = not self.inFunc
        if not self.inFunc: # It can't move if it's stuck in a function
            # Move the message 1 unit
            if self.dir == 'up':
                self.y -= 1
            elif self.dir == 'down':
                self.y += 1
            elif self.dir == 'left':
                self.x -= 1
            elif self.dir == 'right':
                self.x += 1
            # Check if the message landed on a function
            characterAtPosition = self.grid[self.x, self.y]
            if characterAtPosition == ' ':
                self.inFunc = False
            elif characterAtPosition == '^':
                self.dir = 'up'
                self.inFunc = False
            elif characterAtPosition == '>':
                self.dir = 'right'
                self.inFunc = False
            elif characterAtPosition == 'v':
                self.dir = 'down'
                self.inFunc = False
            elif characterAtPosition == '<':
                self.dir = 'left'
                self.inFunc = False
            elif characterAtPosition == 'R':
                self.turn(random.choice([-1, 1]))
                self.inFunc = False
            elif characterAtPosition == 'W':
                if (self.type == 'LIST'
                    or (self.type == 'INT' and self.content > 0)):
                    self.turn(-1)
                elif (self.type == 'NULL'
                      or (self.type == 'INT' and self.content <= 0)):
                    self.turn(1)
                self.inFunc = False
            elif characterAtPosition == 'N':
                self.content = None
                self.inFunc = False
            elif characterAtPosition in '0123456789':
                self.content = int(characterAtPosition)
                self.inFunc = False
            elif characterAtPosition == 'L':
                self.content = [self.content]
                self.inFunc = False
            elif characterAtPosition == 'T':
                self.content = int(time.time() * 1000)
                self.inFunc = False
            elif characterAtPosition == 'I':
                self.needsInput = True
                self.inFunc = False
            else:
                self.inFunc = True

    def turn(self, rotations):
        """Change the direction of the MessengerMessage.
        Positive numbers indicate clockwise rotations, while
        negative numbers indicate counterclockwise rotations.
        """
        directionNumber = ['up', 'right', 'down', 'left'].index(self.dir)
        directionNumber = (directionNumber + rotations) % 4
        self.dir = ['up', 'right', 'down', 'left'][directionNumber]
        
    def release(self):
        """Set the inFunc attribute to False and return None."""
        self.inFunc = False

##### MESSENGERGRID CLASS ###
        
class MessengerGrid:
    """A 2D grid containing Messenger code."""

    def __init__(self, gridString):
        """Return a MessengerGrid formed from the code gridString."""
        # Raise an error if unknown characters are in code
        if (unknownCharSet := set(gridString)
            - set('<>^v SN0123456789LI+-*/W=GBERT\r\n')) != set():
            unknownCharList = sorted(list(unknownCharSet))
            characterPlural = 's' if len(unknownCharList) >= 2 else ''
            unknownCharStr = ', '.join([repr(i) for i in unknownCharList])
            raise SyntaxError(f'Unknown character{characterPlural} '
                              f'({unknownCharStr}) found in code')

        # Align the code into a grid format
        allLines = gridString.splitlines()
        if allLines == []: # Need at least 1 line
            allLines = ['']
        maxLineLength = max(map(len, allLines), default=1)
        self.code = [[char for char in line.ljust(maxLineLength)]
                     for line in allLines]

        # Get some information about the code grid
        self.width = maxLineLength
        self.height = len(allLines)
        self.originalCode = [[char for char in row] for row in self.code]
        
        # Check if the top-left corner is a redirector--
        # otherwise the message is stuck and throws an error
        if self[0, 0] in '<>^v':
            arrowsToWords = {'^': 'up',
                             '>': 'right',
                             'v': 'down',
                             '<': 'left'}
            self.messages = [MessengerMessage(0, 0, arrowsToWords[self[0, 0]],
                                              None, self, False)]
        else:
            raise ValueError(f'Top-left corner of code '
                             f'({repr(self.code[0][0])}) must be a redirector')

    def __repr__(self):
        """Return a string representation of the MessengerGrid."""
        grid = [[char for char in row] for row in self.code]
        for m in self.messages:
            grid[m.y][m.x] = '.'
        return '\n'.join([' '.join(row) for row in grid])

    def __getitem__(self, pos):
        """Return MessengerGrid.code[y][x], or ' ' if out of bounds."""
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.code[y][x]
        else:
            return ' '
    
    def tick(self):
        """Run 1 tick of Messenger code."""
        # Move all the messages
        for m in self.messages:
            m.tick()

        # Get input if necessary
        messagesNeedingInput = [m for m in self.messages if m.needsInput]
        if len(messagesNeedingInput) == 1: # Only one input
            previousContent = messagesNeedingInput[0].content
            if previousContent is None:
                raise TypeError("Can't input as type NULL")
            elif isinstance(previousContent, int):
                rawInput = input('Input an INT: ')
                try:
                    messagesNeedingInput[0].content = int(rawInput)
                    messagesNeedingInput[0].needsInput = False
                except ValueError:
                    raise ValueError(f'Invalid INT '
                                     f'({repr(rawInput)})') from None
            elif isinstance(previousContent, list):
                rawInput = input('Input a LIST: ').upper()
                if validList(rawInput):
                    messagesNeedingInput[0].content = rawInput
                    messagesNeedingInput[0].needsInput = False
                else:
                    raise ValueError(f'Invalid LIST ({repr(rawInput)})')
        elif len(messagesNeedingInput) > 1: # Too many inputs
            raise RuntimeError(f"{len(messagesNeedingInput)} inputs can't "
                               f'happen at the same time')

        # Print and delete messages that escaped from the program
        messagesToPrint = [m for m in self.messages
                           if m.x >= self.width or m.y >= self.height]
        if len(messagesToPrint) > 1:
            raise RuntimeError(f"{len(messagesToPrint)} messages can't be "
                               f'printed at the same time')
        messagesInBounds = []
        for m in self.messages:
            if m.x < 0 or m.y < 0: # Top or left edge
                pass
            elif m.x >= self.width: # Right edge
                print(str(m.content).replace('None', 'NULL'), end='')
            elif m.y >= self.height: # Bottom edge
                if m.type == 'INT':
                    print(chr(m.content), end='')
                elif m.type == 'LIST':
                    try:
                        print(''.join(map(chr, m.content)), end='')
                    except TypeError:
                        raise TypeError(f"Nested lists ({m.content}) can't be "
                                        f'converted to strings') from None
            else: # In bounds
                messagesInBounds.append(m)
        self.messages = messagesInBounds

        # Get rid of messages in the same position
        alreadySeen = {}
        for m in self.messages:
            if (m.x, m.y) in alreadySeen:
                if (functionAtPosition := self[m.x, m.y]) != ' ':
                    if (alreadySeen[(m.x, m.y)].movedThisTick
                        == m.movedThisTick):
                        # Two arguments to a function at the same time
                        raise RuntimeError("Two messages can't go into a "
                                           'function at the same time')
                    else: # One of +-*/=G is invoked
                        if m.movedThisTick:
                            firstArgument = alreadySeen[(m.x, m.y)]
                            secondArgument = m
                        else:
                            firstArgument = m
                            secondArgument = alreadySeen[(m.x, m.y)]
                        output = eval_bin_func(firstArgument,
                                               functionAtPosition,
                                               secondArgument)
                        secondArgument.content = output
                        secondArgument.release()
                        alreadySeen[(m.x, m.y)] = secondArgument
                else:
                    alreadySeen.pop((m.x, m.y))
            else:
                alreadySeen[(m.x, m.y)] = m
        self.messages = list(alreadySeen.values())
        
        # Run B, E, and S (splitters)
        updatedMessages = []
        for m in [message.clone() for message in self.messages]:
            if self[m.x, m.y] == 'S': # Split
                # Left clone
                updatedMessages.append(m.clone())
                updatedMessages[-1].turn(-1)
                updatedMessages[-1].release()
                # Right clone
                updatedMessages.append(m.clone())
                updatedMessages[-1].turn(1)
                updatedMessages[-1].release()
            elif self[m.x, m.y] == 'B': # Beginning
                if m.type == 'LIST':
                    # Left clone: (...)[0]
                    updatedMessages.append(m.clone())
                    updatedMessages[-1].turn(-1)
                    updatedMessages[-1].release()
                    if updatedMessages[-1].content == []:
                        newContent = None
                    else:
                        newContent = updatedMessages[-1].content[0]
                    updatedMessages[-1].content = newContent
                    # Right clone: (...)[1:]
                    updatedMessages.append(m.clone())
                    updatedMessages[-1].turn(1)
                    updatedMessages[-1].release()
                    newContent = updatedMessages[-1].content[1:]
                    updatedMessages[-1].content = newContent
                else:
                    raise TypeError(f"Can't calculate {m.type} B")
            elif self[m.x, m.y] == 'E': # End
                if m.type == 'LIST':
                    # Left clone: (...)[-1]
                    updatedMessages.append(m.clone())
                    updatedMessages[-1].turn(-1)
                    updatedMessages[-1].release()
                    if updatedMessages[-1].content == []:
                        newContent = None
                    else:
                        newContent = updatedMessages[-1].content[-1]
                    updatedMessages[-1].content = newContent
                    # Right clone: (...)[:-1]
                    updatedMessages.append(m.clone())
                    updatedMessages[-1].turn(1)
                    updatedMessages[-1].release()
                    newContent = updatedMessages[-1].content[:-1]
                    updatedMessages[-1].content = newContent
                else:
                    raise TypeError(f"Can't calculate {m.type} E")
            else:
                updatedMessages.append(m.clone())
        self.messages = updatedMessages

    def run(self, maxIterations):
        """Runs Messenger code until all messages either disappear or
        get trapped in functions."""
        tickNumber = 0
        if maxIterations == 0: # Don't check for tickNumber
            while not all([m.inFunc for m in self.messages]):
                self.tick()
                tickNumber += 1
        else:
            while not all([m.inFunc for m in self.messages]):
                self.tick()
                tickNumber += 1
                if tickNumber >= maxIterations:
                    raise RuntimeError(f'Ran for {tickNumber} iterations '
                                       f'without terminating')

    def reset(self):
        """Resets the Messenger code to before it was run."""
        self.code = [[char for char in row] for row in self.originalCode]
        arrowsToWords = {'^': 'up',
                         '>': 'right',
                         'v': 'down',
                         '<': 'left'}
        self.messages = [MessengerMessage(0, 0, arrowsToWords[self[0, 0]],
                                          None, self, False)]

### OTHER FUNCTIONS ###

def validList(inputString):
    """Return True if inputString is a valid list in Messenger,
    and False otherwise.
    """
    if (not rawInput.startswith('[') or not rawInput.endswith(']')
        or rawInput.count('[') != rawInput.count(']')):
        # Doesn't have balanced or surrounding brackets
        return False
    else:
        listElements = rawInput[1:-1]
        if listElements == ['']: # Empty list
            return True
        for element in listElements: # Check each element
            if element == '': # Missing element
                return False
            if element == 'NULL': # NULL
                continue
            elif (element[0] in '-0123456789'
                  and set(element[1:]) <= set('0123456789')): # INT
                continue
            elif validList(element): # LIST
                continue
        return True
    
def eval_bin_func(message1, operator, message2):
    """Return the output content from applying operator on message1 and
    message2.
    """
    if operator == '+': # Add
        if message1.type == 'NULL' or message2.type == 'NULL':
            return None
        elif message1.type == message2.type == 'INT':
            return message1.content + message2.content
        elif message1.type == message2.type == 'LIST':
            return message1.content + message2.content
        elif message1.type == 'INT' and message2.type == 'LIST':
            return [message1.content] + message2.content
        elif message1.type == 'LIST' and message2.type == 'INT':
            return message1.content + [message2.content]
    elif operator == '-': # Subtract
        if message1.type == 'NULL' or message2.type == 'NULL':
            return None
        if message1.type == message2.type == 'INT':
            return message1.content - message2.content
        else:
            raise TypeError(f"Can't calculate"
                            f'{message1.type} - {message2.type}')
    elif operator == '*': # Multiply
        if message1.type == 'NULL' or message2.type == 'NULL':
            return None
        if message1.type == message2.type == 'INT':
            return message1.content * message2.content
        else:
            raise TypeError(f"Can't calculate"
                            f'{message1.type} * {message2.type}')
    elif operator == '/': # Divide
        if message1.type == 'NULL' or message2.type == 'NULL':
            return None
        if message1.type == message2.type == 'INT':
            try:
                return message1.content // message2.content
            except ZeroDivisionError:
                return None
        else:
            raise TypeError(f"Can't calculate"
                            f'{message1.type} / {message2.type}')
    elif operator == '=': # Equals
        return int(message1.content == message2.content)
    elif operator == 'G': # Greater than
        if ((message2.type == 'LIST' and message2.type in ['NULL', 'INT'])
            or (message1.type == 'INT' and message2.type == 'NULL')):
            return 1
        elif (message1.type == 'NULL'
              or (message1.type == 'INT' and message2.type == 'LIST')):
            return 0
        elif message1.type == message2.type == 'INT':
            return int(message1.content > message2.content)
        elif message1.type == message2.type == 'LIST':
            return int(message1.content > message2.content)
    else:
        raise RuntimeError(f"{operator} doesn't take 2 arguments")
