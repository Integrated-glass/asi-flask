from decimal import Decimal

def tuple_with_decimal_to_double(tp):
  return list(map(lambda x: float(x) if isinstance(x, Decimal) else x, tp or []))
