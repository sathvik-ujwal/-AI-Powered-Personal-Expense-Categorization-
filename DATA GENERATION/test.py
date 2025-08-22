import random
import pandas as pd
from datetime import datetime, timedelta

# -------------------------------
# Imports for all categories
# -------------------------------
from dataset.Travel.data import data as travel_data
from dataset.Shopping.data import data as shopping_data
from dataset.Transportation.data import data as transportation_data
from dataset.Education.data import data as education_data
from dataset.Entertainment.data import data as entertainment_data
from dataset.Taxes.data import data as taxes_data
from dataset.Pets.data import data as pets_data
from dataset.Housing.data import data as housing_data
from dataset.Childcare.data import data as childcare_data
from dataset.FoodDining.data import data as food_data
from dataset.BillsUtilities.data import data as bills_data
from dataset.Healthcare.data import data as healthcare_data
from dataset.PersonalCare.data import data as personalcare_data
from dataset.Insurance.data import data as insurance_data
from dataset.FinancialObligations.data import data as financial_data
from dataset.Miscellaneous.data import data as misc_data
from dataset.CharityDonations.data import data as charity_data

# -------------------------------
# Config
# -------------------------------
START = datetime(2022, 6, 1)
END = datetime(2025, 6, 1)
TOTAL_RECORDS = 100_000
USER_POOL = 10_000
CITIES = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata", "Pune",
          "Hyderabad", "Ahmedabad", "Jaipur", "Lucknow"]

CATEGORY_WEIGHTS = {
    "Shopping": 0.20, "Food & Dining": 0.18, "Transportation": 0.12, "Travel": 0.08,
    "Bills & Utilities": 0.09, "Entertainment": 0.08, "Healthcare": 0.05, "Housing": 0.05,
    "Personal Care": 0.04, "Insurance": 0.03, "Education": 0.03, "Financial Obligations": 0.03,
    "Miscellaneous": 0.02, "Taxes": 0.02, "Charity/Donations": 0.01, "Pets": 0.01, "Childcare": 0.01
}

CATEGORY_DATASETS = {
    "Travel": travel_data,
    "Shopping": shopping_data,
    "Transportation": transportation_data,
    "Education": education_data,
    "Entertainment": entertainment_data,
    "Taxes": taxes_data,
    "Pets": pets_data,
    "Housing": housing_data,
    "Childcare": childcare_data,
    "Food & Dining": food_data,
    "Bills & Utilities": bills_data,
    "Healthcare": healthcare_data,
    "Personal Care": personalcare_data,
    "Insurance": insurance_data,
    "Financial Obligations": financial_data,
    "Miscellaneous": misc_data,
    "Charity/Donations": charity_data
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

CATEGORY_STORE_MAP = {
    "Shopping": ["Kirana Store", "General Store", "Saree Centre", "Super Market", "Bazaar", "Mart", "Jewellers",
                 "Stationery", "Cloth House", "Footwear", "Cosmetics", "Confectionery", "Toys", "Sports", "Book Depot",
                 "Electronics", "Furniture", "Mobile Shop"],
    "Food & Dining": ["Bakery", "Sweets", "Super Market", "Confectionery", "Restaurant", "Cafe"],
    "Transportation": ["Traders", "Enterprises"],  # e.g., logistics, auto-parts traders
    "Travel": ["Enterprises", "Traders", "Glass House"],  # travel agencies, glass decor shops in hotels
    "Bills & Utilities": ["Enterprises", "Traders", "Electronics"],
    "Entertainment": ["Sports", "Book Depot", "Electronics", "Cafe"],
    "Healthcare": ["Medical Store", "Pharmacy", "Diagnostics"],
    "Housing": ["Furniture", "Steel Traders", "Glass House"],
    "Personal Care": ["Medical Store", "Cosmetics", "Super Market"],
    "Insurance": ["Enterprises", "Traders"],
    "Education": ["Book Depot", "Stationery"],
    "Financial Obligations": ["Enterprises", "Traders"],
    "Miscellaneous": STORE_TYPES,  # allow all
    "Taxes": ["Enterprises"],  
    "Charity/Donations": ["Trust", "Foundation"],
    "Pets": ["Super Market", "Medical Store", "General Store"],
    "Childcare": ["Toy Store", "Book Depot", "Super Market"]
}


def generate_merchant(category: str) -> str:
    """Generate merchant name based on category-specific store types."""
    # pick random pattern
    pattern = random.choice([1, 2, 3, 4])
    
    # store type for this category
    store_types = CATEGORY_STORE_MAP.get(category, STORE_TYPES)
    store_type = random.choice(store_types)

    # name generation patterns
    if pattern == 1:
        return f"{random.choice(SURNAMES)} {store_type}"
    elif pattern == 2:
        return f"{random.choice(DEITIES_PREFIXES)} {random.choice(SURNAMES)} {store_type}"
    elif pattern == 3:
        return f"{random.choice(CONCEPTS)} {store_type}"
    else:
        return f"{random.choice(DEITIES_PREFIXES)} {store_type}"


# -------------------------------
# Helper Functions
# -------------------------------
def random_date(start, end):
    """Random datetime between start and end"""
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def add_noise_to_text(text):
    """Introduce minor typos or spacing errors."""
    if random.random() < 0.1:
        text = text.replace(" ", "  ")  # double space
    if random.random() < 0.05:
        text = text.replace("a", "@", 1)
    return text



def generate_transaction(dataset, category, ambiguous_prob=0.6, random_prob=0.2):
    """Generate one synthetic transaction with noise."""
    
    # Miscellaneous category is handled differently
    if category == "Miscellaneous":
        tpl = random.choice(dataset["ambiguous"]["description_templates"])
        name = random.choice(dataset["ambiguous"]["names"])
        amount = random.randint(*dataset["ambiguous"]["amount_range"])
        desc = tpl.format(name=name, amount=amount)
        merchant = name
    else:
        rand_val = random.random()
        # --- ambiguous transaction ---
        if rand_val < ambiguous_prob:
            tpl = random.choice(dataset["ambiguous"]["description_templates"])
            merchant = random.choice(dataset["ambiguous"]["merchants"])
            # 10% chance to pick merchant from another category
            if random.random() < 0.1:
                merchant = generate_merchant(random.choice(list(CATEGORY_DATASETS.keys())))
            amount = int(random.randint(*dataset["ambiguous"]["amount_range"]) * random.uniform(0.8, 1.2))
            desc = tpl.format(merchant=merchant, amount=amount)
        
        # --- random merchant case ---
        elif rand_val < ambiguous_prob + random_prob:
            merchant = generate_merchant(category)
            amount = random.randint(100, 20000)
            tpl = random.choice(dataset["specific"].get("generic_templates", dataset["ambiguous"]["description_templates"]))
            desc = tpl.format(merchant=merchant, amount=amount)
        
        # --- dataset-specific item ---
        else:
            item_key = random.choice(list(dataset["specific"]["items"].keys()))
            item = dataset["specific"]["items"][item_key]
            merchant = random.choice(item["merchants"])
            # 10% chance to pick merchant from another category
            if random.random() < 0.1:
                merchant = generate_merchant(random.choice(list(CATEGORY_DATASETS.keys())))
            amount = int(random.randint(*item["amount_range"]) * random.uniform(0.8, 1.2))
            tpl = random.choice(item["description_templates"])
            
            # 5% chance: swap item template with another category
            if random.random() < 0.05:
                other_category = random.choice(list(CATEGORY_DATASETS.keys()))
                other_item_key = random.choice(list(CATEGORY_DATASETS[other_category]["specific"]["items"].keys()))
                tpl = random.choice(CATEGORY_DATASETS[other_category]["specific"]["items"][other_item_key]["description_templates"])
                item_key = other_item_key
            
            desc = tpl.format(item=item_key, merchant=merchant, amount=amount)
        
        # Add text noise
        desc = add_noise_to_text(desc)
        
        # 2% chance: duplicate entry (near duplicate)
       
    
    # Return transaction
    
    return desc.strip(), merchant, amount

# -------------------------------
# Data Generation Loop
# -------------------------------
records = []
tx_id = 1

for category, weight in CATEGORY_WEIGHTS.items():
    dataset = CATEGORY_DATASETS[category]
    n_records = int(TOTAL_RECORDS * weight)

    for _ in range(n_records):
        dt = random_date(START, END)
        desc, merchant, amount = generate_transaction(dataset, category)
        
        # Append main transaction
        records.append({
            "transaction_id": tx_id,
            "user_id": random.randint(1, USER_POOL),
            "date_time": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "city": random.choice(CITIES),
            "amount": amount,
            "merchant": merchant,
            "description": desc,
            "category": category
        })
        tx_id += 1
        

# -------------------------------
# Create DataFrame & Export
# -------------------------------
df = pd.DataFrame(records)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("transactions_final_complex_noisy.csv", index=False)

print("✅ Complex noisy dataset generated successfully!")
print("\n--- Sample of Generated Data ---")
print(df.head(30))