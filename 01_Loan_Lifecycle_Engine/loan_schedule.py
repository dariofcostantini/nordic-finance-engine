from decimal import Decimal, ROUND_HALF_UP
from typing import List
from datetime import date
from dateutil.relativedelta import relativedelta

from loan_models import AmortizationRow, PaymentFrequency
from loan_math import FinancialMath

class LoanScheduleGenerator:
    """
    Service responsible for generating the complete amortization schedule.
    It takes mathematical calculations and translates them into a time-based ledger.
    """

    @staticmethod
    def generate_annuity_schedule(
        principal: Decimal,
        annual_interest_rate: Decimal,
        start_date: date,
        years: int,
        frequency: PaymentFrequency = PaymentFrequency.MONTHLY
    ) -> List[AmortizationRow]:
        """
        Generates the schedule for a French System Loan (Annuitetslån).
        """
        schedule: List[AmortizationRow] = []
        
        # 1. Calculate fixed variables
        payments_per_year = frequency.value
        total_payments = years * payments_per_year
        periodic_rate = annual_interest_rate / Decimal(payments_per_year)
        
        # 2. Get the fixed payment amount from our Math module
        fixed_payment = FinancialMath.calculate_annuity_payment(
            principal=principal,
            annual_interest_rate=annual_interest_rate,
            payments_per_year=payments_per_year,
            years=years
        )
        
        current_balance = principal
        current_date = start_date

        for payment_num in range(1, total_payments + 1):
            # Calculate the next payment date (assuming simple monthly addition for now)
            months_to_add = 12 // payments_per_year
            current_date += relativedelta(months=months_to_add)

            # 3. Calculate Interest for the current period based on the REMAINING balance
            interest_paid = (current_balance * periodic_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # 4. Calculate Principal paid in this period
            principal_paid = fixed_payment - interest_paid
            
            # 5. Calculate new balance
            current_balance -= principal_paid
            
            # EDGE CASE: Final Payment Adjustment
            # Due to rounding over years, the final balance might not be exactly 0.00.
            # Banks adjust the very last payment so the balance drops to exactly zero.
            if payment_num == total_payments and current_balance != Decimal('0.00'):
                # We adjust the principal paid by whatever balance is left over
                principal_paid += current_balance
                # And recalculate the final payment amount just for this last month
                fixed_payment = principal_paid + interest_paid
                current_balance = Decimal('0.00')

            # Create the row and add it to our ledger
            row = AmortizationRow(
                payment_number=payment_num,
                due_date=current_date,
                payment_amount=fixed_payment,
                principal_paid=principal_paid,
                interest_paid=interest_paid,
                remaining_balance=current_balance
            )
            schedule.append(row)
            
        return schedule

    @staticmethod
    def generate_serial_schedule(
        principal: Decimal,
        annual_interest_rate: Decimal,
        start_date: date,
        years: int,
        frequency: PaymentFrequency = PaymentFrequency.MONTHLY
    ) -> List[AmortizationRow]:
        """
        Generates the schedule for a German System Loan (Serielån).
        In a Serielån, the principal paid each month is constant, 
        so the total payment decreases over time.
        """
        schedule: List[AmortizationRow] = []
        
        payments_per_year = frequency.value
        total_payments = years * payments_per_year
        periodic_rate = annual_interest_rate / Decimal(payments_per_year)
        
        # Get the constant principal repayment amount
        fixed_principal_payment = FinancialMath.calculate_constant_principal_repayment(
            principal=principal,
            payments_per_year=payments_per_year,
            years=years
        )
        
        current_balance = principal
        current_date = start_date

        for payment_num in range(1, total_payments + 1):
            months_to_add = 12 // payments_per_year
            current_date += relativedelta(months=months_to_add)

            # 1. Interest is still calculated on the remaining balance
            interest_paid = (current_balance * periodic_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # 2. The principal paid is ALWAYS the fixed amount we calculated...
            principal_paid = fixed_principal_payment
            
            # EDGE CASE: Final Payment Adjustment
            # Due to rounding, the final balance might not exactly match our fixed principal payment
            if payment_num == total_payments:
                principal_paid = current_balance

            # 3. The TOTAL payment to the bank this month is the sum of both
            total_payment = principal_paid + interest_paid
            
            # 4. Update balance
            current_balance -= principal_paid
            
            row = AmortizationRow(
                payment_number=payment_num,
                due_date=current_date,
                payment_amount=total_payment,
                principal_paid=principal_paid,
                interest_paid=interest_paid,
                remaining_balance=current_balance
            )
            schedule.append(row)
            
        return schedule
