import random
from dataset.Shopping.data import data as shopping_data

def generate_transaction(dataset, category="Shopping", ambiguous_prob=0.7):
    """Generate one synthetic transaction"""
    if category == "Miscellaneous":
        tpl = random.choice(dataset["ambiguous"]["description_templates"])
        name = random.choice(dataset["ambiguous"]["names"])
        amount = random.randint(*dataset["ambiguous"]["amount_range"])
        desc = tpl.format(name=name, amount=amount)
        merchant = name
    else:
        if random.random() < ambiguous_prob:
            tpl = random.choice(dataset["ambiguous"]["description_templates"])
            merchant = random.choice(dataset["ambiguous"]["merchants"])
            amount = random.randint(*dataset["ambiguous"]["amount_range"])
            desc = tpl.format(merchant=merchant)
        else:
            item_key = random.choice(list(dataset["specific"]["items"].keys()))
            item = dataset["specific"]["items"][item_key]
            merchant = random.choice(item["merchants"])
            amount = random.randint(*item["amount_range"])
            tpl = random.choice(item["description_templates"])
            desc = tpl.format(item=item_key, merchant=merchant)

    return {"category": category, "description": desc.strip(), "merchant": merchant, "amount": amount}


if __name__ == "__main__":
    tx = generate_transaction(shopping_data)
    print(tx)
