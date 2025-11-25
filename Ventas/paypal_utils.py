# ventas/paypal_utils.py
from decimal import Decimal, ROUND_HALF_UP

def format_decimal_for_paypal(value):
    """
    Asegura que el string tenga 2 decimales y sea aceptable para PayPal.
    value: Decimal | float | int
    """
    d = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return format(d, "0.2f")