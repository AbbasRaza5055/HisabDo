"""
Sample transaction data for the Smart Expense Categorization POC.

These descriptions are written the way HisabDo's actual users would type
them: short, informal, often mixing Roman Urdu and English - not clean
textbook English. This matters because it's a realistic test of whether
our categorization approach can handle the app's real user base.

Categories chosen reflect what a small shopkeeper/wholesaler/freelancer
in Pakistan would actually track (per Day 8's persona research):
- Inventory Purchase
- Utility Bill
- Customer Sale
- Supplier Payment
- Rent
- Salary/Wages
"""

TRAINING_DATA = [
    # Inventory Purchase
    ("kirana samaan wholesale market se khareeda", "Inventory Purchase"),
    ("bought rice and sugar from wholesaler", "Inventory Purchase"),
    ("stock liya dukaan ke liye", "Inventory Purchase"),
    ("purchased cooking oil cartons for shop", "Inventory Purchase"),
    ("naya maal mandi se aaya", "Inventory Purchase"),
    ("flour and pulses bought in bulk", "Inventory Purchase"),
    ("dukaan ke liye chawal aur daal khareedi", "Inventory Purchase"),
    ("restocked shelves with packaged snacks", "Inventory Purchase"),

    # Utility Bill
    ("bijli ka bill jama karaya", "Utility Bill"),
    ("paid electricity bill this month", "Utility Bill"),
    ("gas bill payment kiya", "Utility Bill"),
    ("water bill paid at bank", "Utility Bill"),
    ("internet aur phone ka bill diya", "Utility Bill"),
    ("paid the monthly wifi connection bill", "Utility Bill"),
    ("meter reading ke mutabiq bijli bill", "Utility Bill"),

    # Customer Sale
    ("Ahmed ko cheezein becheen udhar par", "Customer Sale"),
    ("sold groceries to regular customer", "Customer Sale"),
    ("customer ne cash mein saman liya", "Customer Sale"),
    ("Fatima ne udhar par kapra liya", "Customer Sale"),
    ("daily sale to walk-in customers", "Customer Sale"),
    ("bikri hui aaj dukaan mein", "Customer Sale"),
    ("sold items to Bilal on credit", "Customer Sale"),
    ("customer payment received for last month udhar", "Customer Sale"),

    # Supplier Payment
    ("supplier ko payment ki maal ke liye", "Supplier Payment"),
    ("paid the distributor for last delivery", "Supplier Payment"),
    ("wholesaler ka pichla udhar clear kiya", "Supplier Payment"),
    ("payment cleared to vendor for stock", "Supplier Payment"),
    ("supplier invoice ka payment kiya", "Supplier Payment"),
    ("cleared outstanding balance with distributor", "Supplier Payment"),

    # Rent
    ("dukaan ka kiraya diya is mahine", "Rent"),
    ("paid monthly shop rent", "Rent"),
    ("rent payment to landlord", "Rent"),
    ("makan malik ko kiraya jama karaya", "Rent"),

    # Salary/Wages
    ("karigar ko tankhwa di", "Salary/Wages"),
    ("paid worker's monthly salary", "Salary/Wages"),
    ("staff ki tankhwa is hafte", "Salary/Wages"),
    ("wages paid to shop helper", "Salary/Wages"),
    ("mazdoor ko din ki mazdoori di", "Salary/Wages"),
]

# A separate, held-out test set - descriptions the model has NOT seen during
# "training" (fitting the TF-IDF vectorizer). This is how we honestly check
# whether the approach generalizes, rather than just memorizing.
TEST_DATA = [
    ("chai patti aur cheeni khareedi dukaan ke liye", "Inventory Purchase"),
    ("electricity ka bill is mahine bhara", "Utility Bill"),
    ("Zainab ne udhaar par grocery li", "Customer Sale"),
    ("distributor ko baqaya payment diya", "Supplier Payment"),
    ("shop ka monthly kiraya ada kiya", "Rent"),
    ("helper ko is hafte ki mazdoori di", "Salary/Wages"),
    ("bought new stock of cold drinks", "Inventory Purchase"),
    ("customer bought items on credit today", "Customer Sale"),
]

CATEGORIES = [
    "Inventory Purchase",
    "Utility Bill",
    "Customer Sale",
    "Supplier Payment",
    "Rent",
    "Salary/Wages",
]
