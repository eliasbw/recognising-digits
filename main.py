from view import create_view_input
from visualise import visualise


def main():
    pattern_from_gui = create_view_input()

    visualise(pattern_from_gui, colors=["orange", "red"])


if __name__ == '__main__':
    SystemExit(main())
