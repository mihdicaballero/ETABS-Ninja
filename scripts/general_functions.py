
from colorama import Fore, Style

def FU(element, value, comparison_value):
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

# # Example usage
# element = "Drift X"
# value = 0.006
# comparison_value = 0.005
# FU(element, value, comparison_value)