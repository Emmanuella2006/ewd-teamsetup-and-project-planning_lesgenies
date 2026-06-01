import json
import time
import xml.etree.ElementTree as ET

# step1: I started by parsing XML
def detect_type (body) :
    body_lower = body.lower()
    if "you have received" in body_lower :
        return "incoming_money"
    elif "payment" in body_lower and "airtime" in body_lower:
        return "airtime_purchase"
    elif "payment" in body_lower:
        return "payment"
    elif "withdrawn" in body_lower:
        return "cash withdrawal"
    elif "bank deposit" in body_lower:
        return "bank_deposit"
    elif "transferred to" in body_lower:
        return "transfer_sent"
    else:
        return "other"
def parse_xml(filepath):
    """Read the XML file and return a list of transaction dicts."""
    tree = ET.parse(filepath)
    root = tree.getroot()
    transactions = []
    for idx, sms in enumerate(root, start=1):
        record = {
            "id":            idx,
            "type":          detect_type(sms.attrib["body"]),
            "body":          sms.attrib["body"],
            "date":          sms.attrib["date"],
            "readable_date": sms.attrib["readable_date"],
            "address":       sms.attrib["address"]
        }
        transactions.append(record)
    return transactions

# step 2: I then implemented linear search logic

def linear_search(transactions, target_id):
    # I will be looping through every transaction one by one
    # and returning matching record, or none if not found

    for transaction in transactions:
        if transaction["id"] == target_id:
            return transaction
    return None
# step 3: For step 3 I implemented dictionary lookup logic

def build_lookup_dict(transactions):
    # I am going to convert list into a dictionary keyed by ID
    return {transaction["id"]: transaction for transaction in transactions}
def dict_lookup(lookup_dict, target_id):
    # going directly to the record using the ID as a key
    return lookup_dict.get(target_id, None)

# step 4: I tracked the time of running of the search methods to compare
# them and see which one performs better

def run_comparison(transactions, test_ids):
    # I will be searching for each ID in test_ids using both methods
    lookup_dict = build_lookup_dict(transactions)

    print (f"\n{'='*55}")
    print(f" DSA Search Comparison - {len(test_ids)} searches")
    print (f"{'='*55}")
    print(f" {'ID': <6} {'Linear (µs)':>14} {'Dict (µs)': >12} {'Found?':>8}")
    print (f"{'-'*55}")

    total_linear=0
    total_dict=0

    for target_id in test_ids:

        # Linear search timing
        t0 = time.perf_counter()
        result_linear = linear_search(transactions, target_id)
        t1 = time.perf_counter()
        linear_time = (t1 - t0) * 1e6  # convert to microseconds

        # Dictionary lookup timing
        t2=time.perf_counter()
        result_dict = dict_lookup(lookup_dict, target_id)
        t3=time.perf_counter()
        dict_time = (t3 - t2) * 1e6  # convert to microseconds

        total_linear += linear_time
        total_dict += dict_time
        found = "Yes" if result_linear else "No"
        print(f" {target_id:<6} {linear_time:>13.2f}µs {dict_time:>11.2f}µs {found:>8}")
    print(f"{'─'*55}")
    print(f" {'TOTAL':<6} {total_linear:>13.2f}µs {total_dict:>11.2f}µs")
    if total_dict > 0:
        speedup= total_linear / total_dict
        print(F"\n → Dictionary lookup was {speedup:.1f}x faster overall")
    print(f"{'=' * 55}")

# Now I am adding main to run everything
if __name__ == "__main__":
    # Loading transactions
    transactions = parse_xml("data/modified_sms_v2.xml")
    print(f"Loaded {len(transactions)} transactions.")
    # Save to JSON
    with open("data/transactions.json", "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2)
    print("Saved to data/transactions.json")

    # Preview first 3 records
    print("\nFirst 3 records: ")
    for t in transactions[:3]:
        print(f"[{t['id']}] {t['type']:<20}: {t['readable_date']}")
    n = len(transactions)
    test_ids= [i*(n//20) for i in range (1,21)]

    run_comparison(transactions, test_ids)
