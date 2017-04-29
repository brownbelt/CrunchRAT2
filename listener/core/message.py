from colorama import Fore, Style


class Message(object):

    @staticmethod
    def display_error(message):
        """
        DESCRIPTION:
            This function displays an error message with bold red coloring
        """
        print(Style.BRIGHT + Fore.RED + message + Style.RESET_ALL)

    @staticmethod
    def display_status(message):
        """
        DESCRIPTION:
            This function displays a status message with bold green coloring
        """
        print(Style.BRIGHT + Fore.GREEN + message + Style.RESET_ALL)
