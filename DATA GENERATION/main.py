from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker('en_IN')
fake.seed_instance(42)
random.seed(42)

TOTAL_RECORDS = 100000
USER_POOL = 10000
CITIES = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata", "Pune", "Ahmedabad",
          "Jaipur", "Lucknow", "Surat", "Hyderabad", "Bhopal", "Indore", "Chandigarh", "Thiruvananthapuram"]
PAY_METHODS = ["UPI", "NetBanking", "Credit Card", "Debit Card", "Mobile Wallet", "Cash", "Cheque"]

CATEGORY_WEIGHTS = {
    "Shopping": 0.20,
    "Food & Dining": 0.18,
    "Transportation": 0.12,
    "Travel": 0.08,
    "Bills & Utilities": 0.09,
    "Entertainment": 0.08,
    "Healthcare": 0.05,
    "Housing": 0.05,
    "Personal Care": 0.04,
    "Insurance": 0.03,
    "Education": 0.03,
    "Financial Obligations": 0.03,
    "Miscellaneous": 0.02,
    "Taxes": 0.02,
    "Charity/Donations": 0.01,
    "Pets": 0.01,
    "Childcare": 0.01,
}

DESC_PATTERNS = {
    "Shopping": [
        "Amazon purchase of {} items: {}",
        "Flipkart order - {}",
        "Bought {} at Big Bazaar",
        "Purchase @ local mall: {}",
        "Grocery haul: {}",
        lambda: f"{fake.company()} shopping spree",
        "Bought {item} on {website}",
        "Shopping spree at {mall}",
        "Purchased {product} from {store}",
        "Online order: {item}",
        "Grocery shopping at {supermarket}",
        "Gift purchase for {occasion} at {shop}",
    ],
    "Food & Dining": [
        "Dinner at {} with friends",
        "Ordered via Swiggy: {}",
        "Coffee @ {}",
        "Snack from {} bakery",
        "Zomato order - {}",
        lambda: fake.sentence(nb_words=5),
        "Lunch with colleagues at {restaurant}",
        "Takeout from {fast_food}",
        "Coffee break at {cafe}",
        "Dinner party at {venue}",
        "Food delivery: {dish}",
        "Street food from {vendor}",
    ],
    "Transportation": [
        "Taxi fare (Ola) for {}",
        "Ola ride to {}",
        "Uber to {}",
        "Metro token from {} station",
        "Bus ticket to {}",
        "Toll charge at {} toll plaza",
        "Cab ride to {destination}",
        "Bus fare to {location}",
        "Train journey to {city}",
        "Flight to {destination} with {airline}",
        "Parking fee at {place}",
        "Auto-rickshaw ride to {location}",
    ],
    "Travel": [
        "Train ticket to {}",
        "Flight booking via {} Airlines",
        "Hotel stay at {} Hotel",
        "Holiday package: {} trip",
        "Taxi to airport for flight",
        lambda: f"Booked flight -> {fake.city()} ; luggage fee",
        "Hotel booking at {hotel}",
        "Vacation package to {destination}",
        "Car rental for trip",
        "Travel insurance purchase",
        "Tour guide fee in {city}",
        "Airport lounge access at {airport}",
    ],
    "Bills & Utilities": [
        "Electricity bill paid to {}",
        "Water bill - {} Municipal Corp",
        "Internet recharge for {}",
        "Mobile recharge - {}",
        "Airtel postpaid bill for {}",
        lambda: f"Paid {fake.company()} utility bill",
        "Gas bill payment",
        "Telephone bill for {month}",
        "Cable TV subscription",
        "Water bill for {address}",
        "Electricity bill for {period}",
    ],
    "Entertainment": [
        "Netflix subscription renewal",
        "Movie tickets at {}",
        "Spotify premium fee",
        "BookMyShow: {} event",
        "Gaming purchase on Steam",
        lambda: f"Concert ticket for {fake.word()} band",
        "Concert tickets for {artist}",
        "Movie night at {theater}",
        "Gaming subscription renewal",
        "Amusement park entry",
        "Sports event ticket",
    ],
    "Healthcare": [
        "Doctor visit at {} Clinic",
        "Medicine from {} Pharmacy",
        "Dental checkup at {}",
        "Health package booking at {}",
        "Vaccine via {}",
        lambda: fake.sentence(nb_words=6),
        "Pharmacy purchase: {medicine}",
        "Hospital visit for {reason}",
        "Dental cleaning at {clinic}",
        "Eye checkup at {optometrist}",
        "Health insurance premium",
    ],
    "Housing": [
        "Rent payment to landlord {}",
        "Home loan EMI {} Bank",
        "Property tax for {} property",
        "Maintenance fee for apt {}",
        "HOA dues for {} community",
        lambda: f"Paid {fake.company()} rent",
        "Mortgage payment for {property}",
        "Rent for apartment {number}",
        "Home maintenance fee",
        "Property management charge",
        "Utilities for house",
    ],
    "Personal Care": [
        "Salon visit at {}",
        "Spa session at {}",
        "Gym membership renewal at {}",
        "Manicure at {}",
        "Haircut at {}",
        lambda: fake.sentence(nb_words=4),
        "Hair salon appointment",
        "Spa day at {spa}",
        "Gym membership fee",
        "Beauty products purchase",
        "Massage therapy session",
    ],
    "Insurance": [
        "Car insurance premium for {}",
        "Health insurance EMI with {}",
        "Life insurance payment - {}",
        "Home insurance renewal - {}",
        "Bike insurance fee for {}",
        lambda: f"Paid insurance via {fake.company()}",
        "Auto insurance renewal",
        "Life insurance policy payment",
        "Homeowners insurance premium",
        "Travel insurance for trip",
        "Pet insurance fee",
    ],
    "Education": [
        "Tuition fee payment for {}",
        "Online course on {}",
        "Books from {} Bookstore",
        "School fee for grade {}",
        "Workshop fee at {}",
        lambda: fake.sentence(nb_words=5),
        "School tuition for {child}",
        "Online course enrollment",
        "Textbook purchase for {subject}",
        "Tutoring session fee",
        "Educational software subscription",
    ],
    "Financial Obligations": [
        "Credit card bill payment - {}",
        "Loan EMI to {} Bank",
        "SIP investment in {}",
        "Mutual fund purchase via {}",
        "Stock purchase on {} platform",
        lambda: f"Paid finance charges to {fake.company()}",
        "Credit card payment",
        "Loan installment for {loan_type}",
        "Investment in {fund}",
        "Retirement account contribution",
        "Tax preparation fee",
    ],
    "Miscellaneous": [
        "ATM wdl fee",
        "Bank service charge",
        "Late payment penalty",
        "Refund credited",
        "Cashback received",
        lambda: fake.word(),
        "Gift for {occasion}",
        "Donation to {cause}",
        "Lottery ticket purchase",
        "Vending machine snack",
        "Lost and found reward",
    ],
    "Taxes": [
        "Income tax payment FY{}",
        "GST settlement for {}",
        "TDS deduction by {}",
        "Property tax - {}",
        "Professional tax payment",
        lambda: f"Paid tax to {fake.company()}",
        "Income tax for FY{}",
        "Sales tax on purchase",
        "Property tax assessment",
        "Customs duty on import",
        "Excise tax payment",
    ],
    "Charity/Donations": [
        "Donation to {}",
        "Charity for {} relief",
        "Temple donation at {}",
        "NGO contribution to {}",
        "Crowdfund support for {}",
        lambda: f"Donated via {fake.company()}",
        "Contribution to {charity}",
        "Fundraiser for {cause}",
        "Sponsorship for {event}",
        "Alms to {recipient}",
        "Philanthropic gift",
    ],
    "Pets": [
        "Pet food from {}",
        "Vet consult at {}",
        "Dog grooming at {}",
        "Pet vaccine at {} clinic",
        "Aquarium supplies from {}",
        lambda: fake.sentence(nb_words=5),
        "Veterinary visit for {pet}",
        "Pet food purchase",
        "Grooming for {pet}",
        "Pet toy from {store}",
        "Pet sitting service",
    ],
    "Childcare": [
        "Daycare fee paid to {}",
        "Baby products from {}",
        "School bus fee for {}",
        "Tuition class fee at {}",
        "Kids playzone entry at {}",
        lambda: fake.sentence(nb_words=4),
        "Nursery fee for {child}",
        "Diaper purchase from {store}",
        "After-school program fee",
        "Kids' activity class",
        "Babysitting service payment",
    ],
}

AMBIGUOUS_PATTERNS = [
    "Payment to {}",
    "Charge from {}",
    "Fee for {}",
    "Subscription to {}",
    "Monthly payment",
    "Transfer to {}",
    "Purchase at {}",
    "Service fee from {}",
    "Unknown transaction",
    lambda: fake.sentence(),
    "Expense for {}",
    "Bill payment",
    "Online transaction",
    "Cash withdrawal",
    "Deposit to account",
]

AMNT_RANGE = {
    "Shopping": (500, 20000),
    "Food & Dining": (50, 5000),
    "Transportation": (20, 3000),
    "Travel": (500, 50000),
    "Bills & Utilities": (100, 10000),
    "Entertainment": (100, 2000),
    "Healthcare": (200, 10000),
    "Housing": (5000, 50000),
    "Personal Care": (300, 5000),
    "Insurance": (500, 20000),
    "Education": (200, 50000),
    "Financial Obligations": (500, 20000),
    "Miscellaneous": (10, 500),
    "Taxes": (1000, 200000),
    "Charity/Donations": (50, 10000),
    "Pets": (100, 5000),
    "Childcare": (500, 20000),
}

counts = {cat: int(TOTAL_RECORDS * w) for cat, w in CATEGORY_WEIGHTS.items()}
diff = TOTAL_RECORDS - sum(counts.values())
for cat in list(counts)[:diff]:
    counts[cat] += 1

def random_datetime(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def generate_description(pattern):
    if callable(pattern):
        return pattern()
    elif "{}" in pattern:
        num_placeholders = pattern.count("{}")
        args = [fake.word() for _ in range(num_placeholders)]
        return pattern.format(*args)
    else:
        return pattern

def inject_noise(text):
    if random.random() < 0.1:
        pos = random.randint(0, len(text)-1)
        if random.random() < 0.5:
            text = text[:pos] + text[pos+1:]
        else:
            text = text[:pos] + text[pos] + text[pos:]
    if random.random() < 0.05:
        text = text.replace(" ", random.choice([" ", "  ", "  pls ", " thx "]), 1)
    return text

START = datetime(2024,6,1)
END = datetime(2025,6,1)

records = []
tx_id = 1
for category, num in counts.items():
    for _ in range(num):
        if random.random() < 0.2:
            pattern = random.choice(AMBIGUOUS_PATTERNS)
        else:
            pattern = random.choice(DESC_PATTERNS.get(category, [lambda: fake.sentence()]))
        desc = generate_description(pattern)
        desc = inject_noise(desc)

        
        dt = random_datetime(START, END)
        low, high = AMNT_RANGE.get(category, (100,10000))
        amount = round(random.uniform(low, high), 2)
        merchant = fake.company() if random.random()<0.7 else fake.word().title()
        records.append({
            "transaction_id": tx_id,
            "user_id": random.randint(1, USER_POOL),
            "date_time": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "city": random.choice(CITIES),
            "amount": amount,
            "payment_method": random.choice(PAY_METHODS),
            "merchant": merchant,
            "description": desc,
            "category": category
        })
        tx_id += 1

df = pd.DataFrame(records)
df.to_csv('complex_transactions_faker1.csv', index=False)