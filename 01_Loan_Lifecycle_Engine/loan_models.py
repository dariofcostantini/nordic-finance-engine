from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from dataclasses import dataclass
from typing import List
from datetime import date

class LoanType(Enum):
    ANNUITY = "Annuitetslån"       # French System: Constant total payment
    SERIAL = "Serielån"            # German System: Constant principal repayment
    BULLET = "Bullet"              # American System: Interest only, principal at the end

class PaymentFrequency(Enum):
    MONTHLY = 12
    QUARTERLY = 4
    SEMI_ANNUALLY = 2
    ANNUALLY = 1

@dataclass
class AmortizationRow:
    """
    Represents a single row in the loan amortization schedule.
    Data classes are great in Python for clean, strongly-typed data structures.
    """
    payment_number: int
    due_date: date
    payment_amount: Decimal     # Total amount paid by the client this period
    principal_paid: Decimal     # Amount that goes towards reducing the debt
    interest_paid: Decimal      # Amount that goes to the bank's profit
    remaining_balance: Decimal  # Debt left after this payment
