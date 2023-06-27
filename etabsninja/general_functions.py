
from colorama import Fore, Style

def FU(element: str, value: float, comparison_value: float) -> None:
    """
    Calculates the demand capacity ratio (DCR) and provides a verification message based on the comparison between
    the value and the comparison value.

    Parameters:
        element (str): The name or identifier of the element being analyzed.
        value (float): The actual value to be compared.
        comparison_value (float): The reference or target value for comparison.

    Returns:
        None
    """
    # Calculate the demand capacity ratio
    DCR = value / comparison_value

    # Compare the value to the comparison value
    if value < comparison_value:
        message = f"{element} is {value} < {comparison_value}. Verifies. {DCR * 100:.0f}% DCR"
        formatted_message = f"{Fore.GREEN}{message}{Style.RESET_ALL}"
    else:
        message = f"{element} is {value} >= {comparison_value}. Does not verify. {DCR * 100:.0f}% DCR"
        formatted_message = f"{Fore.RED}{message}{Style.RESET_ALL}"

    # Print the formatted result
    print(formatted_message)

def bold_terminal(text: str) -> None:
    """
    Prints the specified text in bold in the terminal.

    Parameters:
        text (str): The text to be printed in bold.

    Returns:
        None
    """
    print(Fore.WHITE + Style.BRIGHT + text + Style.RESET_ALL)

# # Example usage
# element = "Drift X"
# value = 0.006
# comparison_value = 0.005
# FU(element, value, comparison_value)