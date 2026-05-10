from decimal import Decimal, ROUND_HALF_UP

class FinancialMath:
    """
    Core mathematical engine for all financial calculations.
    Separating math from models is a standard practice in Domain-Driven Design (DDD).
    """

    @staticmethod
    def calculate_annuity_payment(
        principal: Decimal, 
        annual_interest_rate: Decimal, 
        payments_per_year: int, 
        years: int
    ) -> Decimal:
        """
        Calculates the fixed periodic payment for a French System Loan (Annuitetslån).
        
        Formula: PMT = P * (r * (1 + r)^n) / ((1 + r)^n - 1)
        Where:
        - P = Principal (Amount borrowed)
        - r = Periodic interest rate (annual_rate / payments_per_year)
        - n = Total number of payments (years * payments_per_year)
        """
        # Edge Case: If the interest rate is 0%, we just divide the principal by total payments
        if annual_interest_rate == Decimal('0'):
            total_payments = Decimal(years * payments_per_year)
            pmt = principal / total_payments
            return pmt.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # 1. Calculate the periodic rate (r) and total periods (n)
        r = annual_interest_rate / Decimal(payments_per_year)
        n = years * payments_per_year
        
        # 2. Mathematical compounding: (1 + r)^n
        compounded = (Decimal('1') + r) ** n
        
        # 3. Calculate PMT
        pmt = principal * (r * compounded) / (compounded - Decimal('1'))
        
        # 4. Bank standard rounding: round up to exactly 2 decimal places (øre / cents)
        return pmt.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @staticmethod
    def calculate_constant_principal_repayment(
        principal: Decimal, 
        payments_per_year: int, 
        years: int
    ) -> Decimal:
        """
        Calculates the fixed principal repayment for a German System Loan (Serielån).
        In this system, you amortize the exact same amount of principal every period.
        
        Formula: Principal Payment = Principal / Total Payments
        """
        total_payments = Decimal(years * payments_per_year)
        principal_payment = principal / total_payments
        
        return principal_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
