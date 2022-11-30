from gui_for_distorted_patterns import create_view_input
from visualise import generate_figures


def main():
    pattern_from_gui = create_view_input()

    generate_figures(pattern_from_gui, colors=["orange", "red"])


if __name__ == "__main__":
    SystemExit(main())
