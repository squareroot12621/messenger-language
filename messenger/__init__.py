"""Messenger is a 2D esoteric programming language.
For more information, see the README.md at
https://github.com/squareroot12621/messenger-language/blob/main/README.md."""

from messenger.interpreter import *

if __name__ == '__main__': # Run directly
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=30)
    parser = argparse.ArgumentParser(
        prog='Messenger Interpreter v1.0.2',
        description='Runs Messenger, a 2D programming language designed to be '
                    'as annoying as possible.',
        formatter_class=formatter
    )
    parser.add_argument('code',
                        help='The Messenger code to be run.',
                        type=str)
    parser.add_argument('-c', '--check',
                        help='show grid and flags before running code',
                        action='store_true')
    parser.add_argument('-i', '--iterations',
                        help='runs for ITER iterations; 0 = runs forever '
                             '(DEFAULT: 50000)',
                        metavar='ITER',
                        type=int,
                        default=50000)
    arguments = parser.parse_args()
    
    grid = MessengerGrid(arguments.code)
    if arguments.check:
        print(f'\nGrid:\n{grid}\n')
        print(f'Arguments:\n'
              f'-i, --iterations: {arguments.iterations}'
              f'\n')
        gridChecked = input('Type "no" (without quotes) to cancel execution.\n'
                            'Type anything else to continue.\n')
        if gridChecked.upper() != 'NO':
            grid.run(arguments.iterations)
    else:
        grid.run(arguments.iterations)
