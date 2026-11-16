
def mask_imei(imei):
    """
    Removes dashes and spaces, then hides all but the last four digits.
    Returns an empty string for invalid IMEI inputs.
    """
    if not isinstance(imei, str):
        return ""

    imei = imei.replace('-', '').replace(' ', '')

    # An IMEI must contain exactly 15 ASCII digits.
    if len(imei) != 15 or not imei.isascii() or not imei.isdigit():
        return ""

    return '*' * (len(imei) - 4) + imei[-4:]


def parse_parts_order(text):
    """
    Parses 'screen x1; battery x2' into a dictionary.
    Invalid entries are skipped.
    """
    order = {}

    if not isinstance(text, str):
        return order

    for item in text.split(';'):
        item = item.strip()

        if not item:
            continue

        if 'x' not in item:
            continue

        part, separator, qty = item.partition('x')

        part = part.strip()
        qty = qty.strip()

        if not part or not qty:
            continue

        if not qty.isascii() or not qty.isdigit():
            continue

        quantity = int(qty)

        if quantity <= 0:
            continue

        order[part] = quantity

    return order


def parse_model(text):
    """
    Splits 'Brand Model name' into a (brand, model) tuple.
    Returns empty strings for invalid inputs.
    """
    if not isinstance(text, str):
        return "", ""

    parts = text.strip().split(maxsplit=1)

    if len(parts) != 2:
        return "", ""

    brand, model = parts

    if not brand or not model:
        return "", ""

    return brand.title(), model


def main():
    print("==== Running mask_imei ====")
    value = input("Enter an IMEI number (e.g. 35-209900-176148-1): ")
    print("Masked IMEI:", mask_imei(value))

    print("\n==== Running parse_parts_order ====")
    value = input(
        "Enter parts and quantities as PART xQTY separated by ; "
        "(e.g. screen x1; battery x2): "
    )
    print("Parts order:", parse_parts_order(value))

    print("\n==== Running parse_model ====")
    value = input("Enter the phone brand and model (e.g. Samsung Galaxy S23): ")
    print("Brand and model:", parse_model(value))


if __name__ == "__main__":
    main()
