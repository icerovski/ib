# Selects relevant dataframes for calculations

REQUIRED_SECTIONS = [
    'Realized & Unrealized Performance Summary', 
    'Trade Summary by Symbol', 
    'Deposits & Withdrawals', 
    'Fees', 
    'Dividends', 
    'Withholding Tax', 
    'Interest', 
    'CYEP/Broker Fees', 
    'Payment In Lieu Of Dividends', 
    'Other Fees', 
    'Sales Tax Details', 
    'Broker Interest Paid',
    'Broker Interest Received', 
    'Bond Interest Paid', 
    'Bond Interest Received',
    'Financial Instrument Information'
    ]

PNL_SECTIONS = [
    'Realized & Unrealized Performance Summary', 
    'Dividends', 
    'Withholding Tax',  
    'Bond Interest Received',
    'Bond Interest Paid', 
    'Broker Interest Received', 
    'Broker Interest Paid',
    'Other Fees', 
    'Sales Tax Details', 
    ]

DO_NOT_REPEAT = [
    'Dividends'
]

RENAME_DICT = {
    "Realized Total": "Amount",  # Correcting typo
    "Sales Tax": "Amount"
}