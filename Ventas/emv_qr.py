from decimal import Decimal, ROUND_HALF_UP

def two_decimals_str(amount):
    d = Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return format(d, "0.2f")

# CRC16-CCITT (XModem) implementation for EMV QR
def crc16_ccitt(data: bytes) -> int:
    poly = 0x1021
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            if (crc & 0x8000):
                crc = ((crc << 1) & 0xFFFF) ^ poly
            else:
                crc = (crc << 1) & 0xFFFF
    return crc & 0xFFFF

def tlv(tag: str, value: str) -> str:
    return f"{tag}{len(value):02d}{value}"

def build_emv_payload(merchant_account: str, merchant_name: str, merchant_city: str, amount=None, currency="BOB"):
    """
    Construye un payload EMV QR (simplificado) con:
    - merchant_account: identificador del comercio (PAN, identificador PSP o CUIT)
    - merchant_name, merchant_city: descripción
    - amount: opcional (string/number). Si se pasa, se incluirá el campo 54 (amount).
    - currency: "BOB" o "USD" (luego lo mapeamos a código numérico si hace falta)
    NOTA: este es un payload simplificado que funciona con muchas apps locales.
    """
    payload = ""
    # Payload Format Indicator (00)
    payload += tlv("00", "01")
    # Point of initiation method (01) "12" means variable amount? "11" static; use "12" allows amount field present
    payload += tlv("01", "12")
    # Merchant Account Info (26) subfields: 00 = GUID/PSP, 01 = merchant_account
    mai = tlv("00", "BR.GOV.BCB.PIX") if merchant_account else ""
    mai += tlv("01", merchant_account)
    payload += tlv("26", mai)
    # Merchant category code (52) - generic 0000
    payload += tlv("52", "0000")
    # Transaction currency (53): BOB=068? (ISO 4217 numeric: BOB=068, USD=840)
    currency_map = {"BOB": "068", "USD": "840"}
    payload += tlv("53", currency_map.get(currency, "068"))
    # Transaction amount (54) optional
    if amount is not None:
        payload += tlv("54", two_decimals_str(amount))
    # Country code (58)
    payload += tlv("58", "BO")  # Bolivia
    # Merchant name (59)
    payload += tlv("59", merchant_name[:25])
    # Merchant city (60)
    payload += tlv("60", merchant_city[:15])
    # Additional data field template (62) - we can add ref number in subfield 05
    additional = tlv("05", merchant_account)  # usar mismo id como referencia
    payload += tlv("62", additional)

    # Append CRC placeholder (63) length 04
    payload_to_crc = payload + "6304"
    b = payload_to_crc.encode("utf-8")
    crc = crc16_ccitt(b)
    crc_hex = format(crc, "04X")
    payload_final = payload_to_crc + crc_hex
    return payload_final