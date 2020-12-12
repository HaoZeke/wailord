"""
Ensures wailord is present
"""
import sys


def main():
    try:
        import wailord
    except ImportError as error:
        # Output expected ImportErrors.
        print(error.__class__.__name__ + ": " + error.message)
        print("DO not use this template without wailord")
        sys.exit(1)
    except Exception as exception:
        # Output unexpected Exceptions.
        print(exception, False)
        print(exception.__class__.__name__ + ": " + exception.message)
        sys.exit(1)


if __name__ == "__main__":
    main()
