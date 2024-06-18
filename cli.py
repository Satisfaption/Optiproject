import click
from main import Application


@click.command()
def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
