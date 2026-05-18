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

