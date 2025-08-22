import random

# --- Import all category datasets ---
from dataset.Travel.data import data as travel_data
from dataset.Shopping.data import data as shopping_data
from dataset.Transportation.data import data as transportation_data
from dataset.Education.data import data as education_data
from dataset.Entertainment.data import data as entertainment_data
from dataset.Taxes.data import data as taxes_data
from dataset.Pets.data import data as pets_data
from dataset.FoodDining.data import data as food_data
from dataset.Healthcare.data import data as healthcare_data
from dataset.Insurance.data import data as insurance_data
from dataset.Childcare.data import data as childcare_data
from dataset.Housing.data import data as housing_data
from dataset.PersonalCare.data import data as personalcare_data
from dataset.CharityDonations.data import data as charity_data
from dataset.FinancialObligations.data import data as financial_data
from dataset.Miscellaneous.data import data as misc_data


def generate_transaction(dataset, category, ambiguous_prob=0.7):
    """Generic generator for any category"""

    # Special case: Miscellaneous has only ambiguous data
    if category == "Miscellaneous":
        tpl = random.choice(dataset["ambiguous"]["description_templates"])
        name = random.choice(dataset["ambiguous"]["names"])
        amount = random.randint(*dataset["ambiguous"]["amount_range"])
        desc = tpl.format(name=name, amount=amount)
        return {"category": category, "description": desc, "amount": amount}

    # Normal categories
    if random.random() < ambiguous_prob:
        tpl = random.choice(dataset["ambiguous"]["description_templates"])
        merchant = random.choice(dataset["ambiguous"]["merchants"])
        amount = random.randint(*dataset["ambiguous"]["amount_range"])
        desc = tpl.format(merchant=merchant, amount=amount)
    else:
        item_key = random.choice(list(dataset["specific"]["items"].keys()))
        item = dataset["specific"]["items"][item_key]
        merchant = random.choice(item["merchants"])
        amount = random.randint(*item["amount_range"])
        tpl = random.choice(item["description_templates"])
        desc = tpl.format(item=item_key, merchant=merchant, amount=amount)

    return {"category": category, "description": desc, "amount": amount}


if __name__ == "__main__":
    # Example: generate 5 from each category
    categories = [
        ("Travel", travel_data),
        ("Shopping", shopping_data),
        ("Transportation", transportation_data),
        ("Education", education_data),
        ("Entertainment", entertainment_data),
        ("Taxes", taxes_data),
        ("Pets", pets_data),
        ("Food & Dining", food_data),
        ("Healthcare", healthcare_data),
        ("Insurance", insurance_data),
        ("Childcare", childcare_data),
        ("Housing", housing_data),
        ("Personal Care", personalcare_data),
        ("Charity & Donations", charity_data),
        ("Financial Obligations", financial_data),
        ("Miscellaneous", misc_data),
    ]

    for category, dataset in categories:
        print(f"\n--- {category} ---")
        for _ in range(5):
            print(generate_transaction(dataset, category))
