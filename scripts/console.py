from rich import print
from rich.status import Status
from os import system


class Console:
    @staticmethod
    def print(*objects):
        """
        Basic printing
        """
        for object in objects:
            print(object, end=" ")
        print("")
    
    @staticmethod
    def success(*objects):
        """
        Success. Bold and green.
        """
        for object in objects:
            print(f"[bold green]{object}[/bold green]", end=" ")
        print("")
    
    @staticmethod
    def warn(*objects):
        """
        Warning. Bold and yellow
        """
        for object in objects:
            print(f"[bold yellow]{object}[/bold yellow]", end=" ")
        print("")

    @staticmethod
    def error(*objects):
        """
        Error. Bold and red
        """
        for object in objects:
            print(f"[bold red]{object}[/bold red]", end=" ")
        print("")

    @staticmethod
    def clear():
        if "win" in __import__("sys").platform:
            system("cls")
        else:
            system("clear")


class Spinner:
    def __init__(self, status: str, done_text: str = "Done."):
        """
        A basic status spinner
        """
        self.done_text = done_text
        self.spinner = Status(
            status=status,
            spinner="dots"
        )
        self.spinner.start()

    def stop(self):
        """
        Stop the spinner, show the done_text and delete self
        """
        self.spinner.stop()
        print(self.done_text)
        del self


if __name__ == "__main__":
    Console.print("Basic")
    Console.success("Success")
    Console.warn("Warning")
    Console.error("Error")

    spinner = Spinner("Doing...", "Done")
    __import__("time").sleep(2)
    spinner.stop()

    Console.clear()
