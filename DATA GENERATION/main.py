from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import json


# --- Basic Setup ---
fake = Faker('en_IN')
fake.seed_instance(42)
random.seed(42)

TOTAL_RECORDS = 105,000
CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur",
    "Lucknow", "Surat", "Hyderabad", "Bhopal", "Indore", "Chandigarh", "Thiruvananthapuram",
    "Nagpur", "Patna", "Vadodara", "Visakhapatnam", "Kanpur", "Ludhiana", "Agra", "Varanasi",
    "Rajkot", "Ranchi", "Coimbatore", "Guwahati", "Kochi", "Mysuru", "Noida", "Gurgaon",
    "Faridabad", "Ghaziabad", "Jodhpur", "Amritsar", "Allahabad (Prayagraj)", "Aurangabad",
    "Madurai", "Jamshedpur", "Dehradun", "Shillong"
]

PAY_METHODS = ["UPI", "NetBanking", "Credit Card", "Debit Card", "Mobile Wallet", "Cash", "Cheque"]

CATEGORY_WEIGHTS = {
    "Shopping": 0.20, "Food & Dining": 0.18, "Transportation": 0.12, "Travel": 0.08,
    "Bills & Utilities": 0.09, "Entertainment": 0.08, "Healthcare": 0.05, "Housing": 0.05,
    "Personal Care": 0.04, "Insurance": 0.03, "Education": 0.03, "Financial Obligations": 0.03,
    "Miscellaneous": 0.02, "Taxes": 0.02, "Charity/Donations": 0.01, "Pets": 0.01, "Childcare": 0.01,
}


MERCHANT_POOLS = {
    "Shopping": [
        "Amazon", "Flipkart", "Myntra", "Big Bazaar", "Reliance Digital", "Croma", "Zara", "H&M",
        "Lifestyle", "Pantaloons", "Shoppers Stop", "Nykaa", "Ajio", "Snapdeal", "Tata Cliq",
        "Decathlon", "Pepperfry", "IKEA", "Home Centre", "FirstCry", "Meesho", "Max Fashion",
        "Westside", "FabIndia", "Reliance Trends"
    ],
    "Food & Dining": [
        "Zomato", "Swiggy", "McDonald's", "Domino's Pizza", "Starbucks", "Haldiram's", "Bikanervala",
        "KFC", "Subway", "Burger King", "Pizza Hut", "Barbeque Nation", "Mainland China",
        "Cafe Coffee Day", "Theobroma", "Chaayos", "Behrouz Biryani", "Faasos", "Box8", "FreshMenu"
    ],
    "Transportation": [
        "Ola", "Uber", "Meru Cabs", "Rapido", "Delhi Metro", "Mumbai Metro", "Hyderabad Metro",
        "Bangalore Metro", "Indian Railways", "IRCTC", "RedBus", "KSRTC", "VRL Travels",
        "Indigo Cabs", "BlaBlaCar", "SRS Travels", "TNSTC", "MSRTC", "Uber Auto", "Ola Electric"
    ],
    "Bills & Utilities": [
        "BSES", "Tata Power", "Airtel", "Jio", "Vodafone Idea", "Mahanagar Gas", "BSNL",
        "ACT Fibernet", "Hathway", "Reliance Energy", "DishTV", "Sun Direct", "Tata Sky",
        "Den Broadband", "You Broadband"
    ],
    "Travel": [
        "MakeMyTrip", "Goibibo", "Indigo Airlines", "Air India", "Vistara", "SpiceJet", "Akasa Air",
        "Cleartrip", "Yatra", "Expedia", "OYO Rooms", "Treebo Hotels", "FabHotels", "Airbnb",
        "Taj Hotels", "Marriott", "Hyatt", "ITC Hotels", "HolidayIQ", "Club Mahindra"
    ],
    "Entertainment": [
        "PVR Cinemas", "INOX", "BookMyShow", "Netflix", "Spotify", "Hotstar", "Sony LIV",
        "Amazon Prime Video", "Apple Music", "Gaana", "Wynk Music", "ALTBalaji", "Zee5",
        "Voot", "MX Player", "JioSaavn", "Sun NXT", "Hungama Music"
    ],
    "Healthcare": [
        "Apollo Pharmacy", "Fortis Hospital", "Dr. Lal PathLabs", "Practo", "1mg", "MedPlus",
        "NetMeds", "PharmEasy", "AIIMS", "Max Healthcare", "Narayana Health", "Manipal Hospitals",
        "Columbia Asia", "Cloudnine", "Medanta"
    ],
    "Housing": [
        "DLF", "Lodha Group", "Godrej Properties", "Sobha Ltd", "Prestige Group", "Brigade Group",
        "Puravankara", "Oberoi Realty", "Raheja Developers", "Embassy Group"
    ],
    "Personal Care": [
        "Nykaa", "Mamaearth", "Beardo", "The Man Company", "Sugar Cosmetics", "Lakme",
        "Forest Essentials", "WOW Skin Science", "Plum Goodness", "MCaffeine"
    ],
    "Insurance": [
        "LIC", "ICICI Lombard", "HDFC Ergo", "SBI Life Insurance", "Bajaj Allianz", "Max Bupa",
        "Religare Health Insurance", "New India Assurance", "Oriental Insurance", "Star Health"
    ],
    "Education": [
        "Byju's", "Unacademy", "Vedantu", "Toppr", "Simplilearn", "Coursera", "Udemy",
        "edX", "UpGrad", "Khan Academy"
    ],
    "Financial Obligations": [
        "HDFC Bank Loan", "SBI Loan", "ICICI Bank Loan", "Axis Bank Loan", "Bajaj Finserv EMI",
        "Home Credit India", "Paytm Postpaid", "CASHe", "MoneyTap", "KreditBee"
    ],
    "Miscellaneous": [
        "Amazon Pay", "Paytm Wallet", "PhonePe Wallet", "Google Pay Wallet", "Gift Cards",
        "Sodexo", "Qwikcilver", "Freecharge", "Mobikwik", "PayZapp"
    ],
    "Taxes": [
        "Income Tax Dept.", "GST Portal", "Municipal Corporation Tax", "Property Tax",
        "Professional Tax", "MCA Portal", "EPFO Contributions", "NPS", "Customs Duty", "RBI Penalties"
    ],
    "Charity/Donations": [
        "GiveIndia", "CRY", "Akshaya Patra", "Smile Foundation", "HelpAge India", "Oxfam India",
        "Goonj", "Teach for India"
    ],
    "Pets": [
        "Heads Up For Tails", "PetSutra", "Dogspot", "Pawfect", "Petsworld", "Supertails"
    ],
    "Childcare": [
        "FirstCry", "Mothercare", "Babyhug", "Mee Mee", "Chicco", "Johnson's Baby"
    ],
    "Generic": [
        "Reliance Retail", "Tata Group", "Paytm", "PhonePe", "Google Pay", "Amazon Pay",
        "Flipkart Pay Later", "Mobikwik", "Freecharge", "BHIM UPI"
    ]
}


SURNAMES = [
    "Agarwal", "Gupta", "Sharma", "Verma", "Singh", "Yadav", "Patel", "Shah",
    "Jain", "Mehta", "Bansal", "Goyal", "Kumar", "Choudhary", "Rastogi",
    "Reddy", "Naidu", "Pillai", "Menon", "Iyer", "Iyengar", "Shetty", "Pai",
    "Deshmukh", "Kulkarni", "Joshi", "Chopra", "Malhotra", "Kapoor", "Bhatia",
    "Arora", "Saxena", "Srivastava", "Mishra", "Pandey", "Tiwari", "Tripathi",
    "Banerjee", "Mukherjee", "Chatterjee", "Bose", "Dutta"
]

DEITIES_PREFIXES = [
    "Shri", "Sri", "Shree", "Jai", "Mahalaxmi", "Ganesh", "Balaji", "Krishna",
    "Sai", "Hanuman", "Durga", "Maa", "Lakshmi", "Saraswati", "Vishnu",
    "Shiv", "Ram", "Radha", "Om", "Mahadev", "Kali", "Parvati"
]

CONCEPTS = [
    "National", "New", "Modern", "Swadeshi", "Royal", "Bharat", "Quality", "Unique",
    "Classic", "Heritage", "Golden", "Premium", "Super", "Mega", 
    "Fresh", "Supreme",  "Smart"
]

STORE_TYPES = [
    "Kirana Store", "General Store", "Sweets", "Medical Store", "Electronics",
    "Traders", "Enterprises", "Saree Centre", "Super Market", "Bazaar", "Mart",
    "Jewellers", "Stationery", "Cloth House", "Footwear", "Bakery",
    "Furniture", "Mobile Shop", "Provisions", "Toys", "Sports", "Book Depot",
    "Cosmetics", "Confectionery", "Steel Traders", "Glass House"
]


def generate_indian_store_name():
    """Generates a realistic-sounding Indian store name using various patterns."""
    pattern = random.choice([1, 2, 3, 4])
    if pattern == 1:
        return f"{random.choice(SURNAMES)} {random.choice(STORE_TYPES)}"
    elif pattern == 2:
        return f"{random.choice(DEITIES_PREFIXES)} {random.choice(SURNAMES)} {random.choice(STORE_TYPES)}"
    elif pattern == 3:
        return f"{random.choice(CONCEPTS)} {random.choice(STORE_TYPES)}"
   

NOISE_ELEMENTS = [
    lambda: f"TXN:{fake.random_number(digits=8)}",
    lambda: f"REF:{fake.lexify(text='????????').upper()}",
    lambda: f"UPI/{fake.random_int(1000,9999)}/", "via BillDesk", "via Razorpay",
]

AMBIGUOUS_PATTERNS = [
    "Payment to {}", "Charge from {}", "Fee for {}", "Subscription to {}", "Monthly payment",
    "Transfer to {}", "Purchase at {}", "Service fee from {}", "Unknown transaction", "Expense for {}",
    "Bill payment", "Online transaction", "Cash withdrawal", "Deposit to account", "Recurring payment"
]


DESC_PATTERNS = {
    "Shopping": [ "Amazon purchase of {} items: {}", "Flipkart order - {}", "Bought {} at Big Bazaar", "Purchase @ local mall: {}", "Grocery haul: {}", lambda: f"{fake.company()} shopping spree", "E-com order", "Retail therapy purchase"],
    "Food & Dining": [ "Dinner at {} with friends", "Ordered via Swiggy: {}", "Coffee @ {}", "Snack from {} bakery", "Zomato order - {}", "Lunch with colleagues", "Quick bite" ],
    "Transportation": [ "Taxi fare (Ola) for {}", "Ola ride to {}", "Uber to {}", "Metro token from {} station", "Bus ticket to {}", "Toll charge at {} toll plaza" ],
    "Travel": [ "Train ticket to {}", "Flight booking via {} Airlines", "Hotel stay at {} Hotel", "Holiday package: {} trip", "Taxi to airport for flight", lambda: f"Booked flight -> {fake.city()} ; luggage fee" ],
    "Bills & Utilities": [ "Electricity bill paid to {}", "Water bill - {} Municipal Corp", "Internet recharge for {}", "Mobile recharge - {}", "Airtel postpaid bill for {}", lambda: f"Paid {fake.company()} utility bill" ],
    "Entertainment": [ "Netflix subscription renewal", "Movie tickets at {}", "Spotify premium fee", "BookMyShow: {} event", "Gaming purchase on Steam", lambda: f"Concert ticket for {fake.word()} band" ],
    "Healthcare": [ "Doctor visit at {} Clinic", "Medicine from {} Pharmacy", "Dental checkup at {}", "Health package booking at {}", "Vaccine via {}" ],
    "Housing": [ "Rent payment to landlord {}", "Home loan EMI {} Bank", "Property tax for {} property", "Maintenance fee for apt {}", "HOA dues for {} community" ],
    "Personal Care": [ "Salon visit at {}", "Spa session at {}", "Gym membership renewal at {}", "Manicure at {}", "Haircut at {}" ],
    "Insurance": [ "Car insurance premium for {}", "Health insurance EMI with {}", "Life insurance payment - {}", "Home insurance renewal - {}", "Bike insurance fee for {}" ],
    "Education": [ "Tuition fee payment for {}", "Online course on {}", "Books from {} Bookstore", "School fee for grade {}", "Workshop fee at {}" ],
    "Financial Obligations": [ "Credit card bill payment - {}", "Loan EMI to {} Bank", "SIP investment in {}", "Mutual fund purchase via {}", "Stock purchase on {} platform" ],
    "Miscellaneous": [ "ATM wdl fee", "Bank service charge", "Late payment penalty", "Refund credited", "Cashback received" ],
    "Taxes": [ "Income tax payment FY{}", "GST settlement for {}", "TDS deduction by {}", "Property tax - {}", "Professional tax payment" ],
    "Charity/Donations": [ "Donation to {}", "Charity for {} relief", "Temple donation at {}", "NGO contribution to {}", "Crowdfund support for {}" ],
    "Pets": [ "Pet food from {}", "Vet consult at {}", "Dog grooming at {}", "Pet vaccine at {} clinic", "Aquarium supplies from {}" ],
    "Childcare": [ "Daycare fee paid to {}", "Baby products from {}", "School bus fee for {}", "Tuition class fee at {}", "Kids playzone entry at {}" ],
}
AMNT_RANGE = {
    "Shopping": (500, 20000), "Food & Dining": (50, 5000), "Transportation": (20, 3000), "Travel": (500, 50000), "Bills & Utilities": (100, 10000), "Entertainment": (100, 2000), "Healthcare": (200, 10000), "Housing": (5000, 50000), "Personal Care": (300, 5000), "Insurance": (500, 20000), "Education": (200, 50000), "Financial Obligations": (500, 20000), "Miscellaneous": (10, 500), "Taxes": (1000, 200000), "Charity/Donations": (50, 10000), "Pets": (100, 5000), "Childcare": (500, 20000),
}


counts = {cat: int(TOTAL_RECORDS * w) for cat, w in CATEGORY_WEIGHTS.items()}
diff = TOTAL_RECORDS - sum(counts.values())
for cat in list(counts)[:diff]:
    counts[cat] += 1

def random_datetime(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def generate_description(pattern, merchant):
    if callable(pattern): return pattern()
    elif "{}" in pattern: return pattern.format(*[fake.word() for _ in range(pattern.count("{}"))])
    else: return pattern

START = datetime(2024, 6, 1)
END = datetime(2025, 6, 1)
records = []
tx_id = 1

for category, num in counts.items():
    for _ in range(num):
       
        if random.random() < 0.7 and category in MERCHANT_POOLS:
            merchant = random.choice(MERCHANT_POOLS[category])
        elif random.random() < 0.9:
             merchant = random.choice(MERCHANT_POOLS["Generic"])
        else:
          
            merchant = generate_indian_store_name()

       
        if random.random() < 0.15:
            pattern = random.choice(AMBIGUOUS_PATTERNS)
            desc = pattern.format(merchant if "{}" in pattern else "")
        else:
            pattern = random.choice(DESC_PATTERNS.get(category, [lambda: fake.sentence()]))
            desc = generate_description(pattern, merchant)
      

        #if random.random() < 0.30:
        #    noise = random.choice(NOISE_ELEMENTS)
        #    desc = f"{desc} {noise() if callable(noise) else noise}"

        dt = random_datetime(START, END)
        low, high = AMNT_RANGE.get(category, (100, 10000))
        amount = round(random.uniform(low, high), 2)
        
        records.append({
            "transaction_id": tx_id,
            "user_id": random.randint(1, USER_POOL),
            "date_time": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "city": random.choice(CITIES),
            "amount": amount,
            "payment_method": random.choice(PAY_METHODS),
            "merchant": merchant,
            "description": desc.strip(),
            "category": category
        })
        tx_id += 1

df = pd.DataFrame(records)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv('transactions_final_complex.csv', index=False)

print("Complex dataset generated successfully!")
print("\n--- Sample of Generated Data ---")
print(df.head(30))