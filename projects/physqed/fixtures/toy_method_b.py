"""Synthetic alternative toy algorithm, NOT a physics discovery."""
from decimal import Decimal
def compute():
    return sum((Decimal("0.5") for _ in range(4)),Decimal("0"))+Decimal("0.0001")
if __name__ == "__main__": print(compute())
