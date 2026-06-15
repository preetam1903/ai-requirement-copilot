MODULE_CONTEXT = {

    "Customer Master": """
    Customer master data contains:
    - Customer Address
    - Postal Code
    - Payment Terms
    - Credit Management
    - Tax Classification
    - Billing Information

    Common business impacts:
    - Invoice Processing
    - Customer Communication
    - Sales Order Processing

    Typical testing:
    - Customer Create
    - Customer Update
    - Invoice Generation
    """,

    "Vendor Master": """
    Vendor master data contains:
    - Vendor Address
    - Bank Details
    - Payment Terms
    - Tax Information

    Common business impacts:
    - Procurement
    - Invoice Verification
    - Vendor Payments

    Typical testing:
    - Vendor Create
    - Vendor Update
    - Vendor Payment
    """,

    "Payment Terms": """
    Payment terms configuration controls:
    - Due Dates
    - Discount Calculation
    - Payment Scheduling

    Common business impacts:
    - Accounts Payable
    - Accounts Receivable
    - Cash Flow

    Typical testing:
    - Invoice Posting
    - Payment Run
    - Due Date Calculation
    """,

    "Tax Code": """
    Tax code configuration controls:
    - Tax Calculation
    - GST/VAT Processing
    - Reporting

    Common business impacts:
    - Billing
    - Procurement
    - Compliance

    Typical testing:
    - Invoice Posting
    - Tax Calculation
    - Tax Reporting
    """
}
