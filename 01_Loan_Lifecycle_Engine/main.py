from decimal import Decimal
from datetime import date
from loan_models import PaymentFrequency
from loan_schedule import LoanScheduleGenerator

def main():
    print("="*60)
    print("🏦 NORDIC LOAN ENGINE (CLI)")
    print("="*60)
    
    try:
        # 1. Input variables (Simulating a frontend form)
        principal_input = input("1. Enter Loan Amount (Principal) [e.g. 1000000]: ")
        principal = Decimal(principal_input.replace(",", ""))
        
        rate_input = input("2. Enter Annual Interest Rate (%) [e.g. 4.5]: ")
        # Convert user's 4.5% to backend's 0.045
        annual_rate = Decimal(rate_input) / Decimal('100')
        
        years_input = input("3. Enter Loan Term in Years [e.g. 20]: ")
        years = int(years_input)
        
        currency = input("4. Enter Currency [e.g. NOK, DKK, EUR]: ").upper()
        
        print("\n5. Select Amortization System:")
        print("   [1] French System (Annuitetslån) - Constant total payment")
        print("   [2] German System (Serielån) - Constant principal payment")
        system_type = input("   Choice [1 or 2]: ")
        
    except Exception as e:
        print("\n❌ Error: Invalid input. Please enter numbers only.")
        return

    if system_type == "1":
        print("\n⏳ Generating Annuitetslån (French System) Schedule...\n")
        schedule = LoanScheduleGenerator.generate_annuity_schedule(
            principal=principal,
            annual_interest_rate=annual_rate,
            start_date=date.today(),
            years=years,
            frequency=PaymentFrequency.MONTHLY
        )
    elif system_type == "2":
        print("\n⏳ Generating Serielån (German System) Schedule...\n")
        schedule = LoanScheduleGenerator.generate_serial_schedule(
            principal=principal,
            annual_interest_rate=annual_rate,
            start_date=date.today(),
            years=years,
            frequency=PaymentFrequency.MONTHLY
        )
    else:
        print("\n❌ Error: Invalid system choice.")
        return

    # 3. Print the Ledger
    print(f"{'#':<4} | {'Date':<10} | {'Payment ('+currency+')':<15} | {'Principal':<15} | {'Interest':<15} | {'Balance':<15}")
    print("-" * 85)
    
    total_interest = Decimal('0')
    
    for row in schedule:
        total_interest += row.interest_paid
        
        # To avoid flooding the console with 240 lines, we print the first 12 and the last 12
        if row.payment_number <= 12 or row.payment_number > (years * 12) - 12:
            print(f"{row.payment_number:<4} | {row.due_date.strftime('%Y-%m-%d'):<10} | "
                  f"{row.payment_amount:<15.2f} | {row.principal_paid:<15.2f} | "
                  f"{row.interest_paid:<15.2f} | {row.remaining_balance:<15.2f}")
        elif row.payment_number == 13:
            print(f"{'... ':<4} | {'...':<10} | {'...':<15} | {'...':<15} | {'...':<15} | {'...':<15}")

    print("-" * 85)
    print(f"💰 SUMMARY:")
    print(f"  - Total Principal Borrowed: {principal:,.2f} {currency}")
    print(f"  - Total Interest Paid:      {total_interest:,.2f} {currency}")
    print(f"  - Total Amount Paid to Bank: {(principal + total_interest):,.2f} {currency}")
    print("="*60)

if __name__ == "__main__":
    main()
