from values import input_initial_values
from base import Grabber


def main():
    '''Main function.'''
    initial_values = input_initial_values()

    Grabber(initial_values).start()


if __name__ == "__main__":
    main()
