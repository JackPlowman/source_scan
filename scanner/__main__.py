from application.app import generate_tech_report
from application.utils.custom_logging import set_up_custom_logging


def main() -> None:
    """Main function for the application."""
    set_up_custom_logging()
    generate_tech_report()


if __name__ == "__main__":
    main()
