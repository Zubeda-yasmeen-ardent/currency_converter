from typing import Any, Dict, Optional
import requests

def get_currency_list() -> Optional[Dict[str, str]]:
    """Fetches the list of available currencies and their codes."""
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        response.raise_for_status()
        currencies = response.json()['rates']
        return currencies
    except requests.exceptions.RequestException as e:
        print(f"Error during HTTP request: {e}")
        return None

def get_exchange_rate(base_currency: str, target_currency: str) -> Optional[float]:
    """Fetches the exchange rate between the base currency and the target currency."""
    try:
        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base_currency}')
        response.raise_for_status()
        exchange_rates = response.json()['rates']
        return exchange_rates.get(target_currency, None)
    except requests.exceptions.RequestException as e:
        print(f"Error during HTTP request: {e}")
        return None
    except KeyError:
        print(f"Unexpected response format. Unable to retrieve exchange rates.")
        return None

def display_currency_list(currencies: Dict[str, str]) -> None:
    """Displays the list of available currencies and their codes."""
    print("Available currencies:")
    for currency, code in currencies.items():
        print(f"{code}: {currency}")

def convert_currency() -> None:
    """Main function to handle the currency conversion process."""
    print("Welcome to the Currency Converter App!\n")
    print("This app allows you to convert an amount from one currency to another.\n")
    currencies = get_currency_list()

    if currencies is None:
        print("\nUnable to retrieve the list of currencies. Exiting.")
        return

    display_currency_list(currencies)

    base_currency = input("\nEnter the code of the base currency: ").upper()
    target_currency = input("\nEnter the code of the target currency: ").upper()

    amount = input("\nEnter the amount: ")

    try:
        amount = float(amount)
    except ValueError:
        print("\nInvalid input. Please enter a numeric value.")
        return

    if base_currency not in currencies or target_currency not in currencies:
        print("\nInvalid currency code. Please enter a valid currency code.")
        return

    exchange_rate = get_exchange_rate(base_currency, target_currency)

    if exchange_rate is None:
        print(f"Unable to retrieve exchange rate for {base_currency} to {target_currency}.")
        return

    converted_amount = amount * exchange_rate
    print(f"\nConversion Summary:")
    print(f"\n{amount:} {base_currency} is equivalent to {converted_amount:} {target_currency} at an exchange rate of {exchange_rate:}\n")


convert_currency()
