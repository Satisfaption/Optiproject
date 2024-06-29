import click
from main import Application
from update import prompt_update


@click.command()
def main():
    # Check for updates before initializing the main GUI
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
