import re
import joblib
import pandas as pd

def extract(text):
    match = re.match(r'(\d+-?\d*)(\D+)', text)
    if match:
        return match.groups()
    return "0", "unknown"

def categorize_condition(condition):
    condition = condition.lower()  # Convert to lowercase for uniform comparison

    if 'excellent' in condition:
        return 'excellent'
    elif 'very good' in condition:
        return 'very good'
    elif 'like new' in condition or 'practically new' in condition:
        return 'like new'
    elif 'new with tags' in condition:
        return 'new with tags'
    elif 'new without tags' in condition:
        return 'new without tags'
    elif 'good' in condition:
        return 'good'
    elif 'play' in condition:
        return 'play'
    else:
        return 'unknown'  # Assign unknown for unknown/vague conditions or empty strings

def normalize_size(size_range):
    if '-' in size_range:  # For range values
        lower, upper = map(int, size_range.split('-'))
        return (lower + upper) / 2
    else:  # For single values
        return int(size_range)

def clean_size_letters(size_str):
    size_str = re.sub(r'\W+', '', str(size_str))  # Remove non-alphanumeric characters
    size_str = size_str.strip()  # Remove leading/trailing spaces
    # Map similar units/categories together
    if size_str in ['T', 'Toddler', 'T-', 'Tsmallfit']:  # Example mappings
        return 'Toddler'
    elif size_str in ['mos', 'months', 'mnos']:
        return 'Months'
    elif size_str in ['Youth', 'XYouth', 'X']:
        return 'Youth'
    elif 'Shoes' in size_str:
        if size_str in ["InfantShoes", "ShoesInfant"]:
            return "Shoes Infant"
        elif size_str in ["YouthShoes", "ShoesYouth"]:
            return "Shoes Youth"
        elif size_str in ["ToddlerShoes", "ShoesToddler"]:
            return "Shoes Toddler"
        else:
            return "Shoes"
    elif size_str in ['yrs', 'yr', 'Y']:
        return 'Year'
    elif size_str in ['nan', '']:
        return 'unknown'
    else:
        return size_str

def preprocess_input(vendor, type, condition, size=None, title=None):
    input_dict = {
        "Vendor": vendor,
        "Type": type,
        "Cleaned Condition": categorize_condition(condition),
        "NormalizedSize": 0,
        "CleanedSizeLetters":"unknown",
        "joggers":0,
        "jeans":0,
        "leggings":0
    }
    
    if size:
        try:
            number, letter = extract(size)
            input_dict["NormalizedSize"] = normalize_size(number)
            input_dict["CleanedSizeLetters"] = clean_size_letters(letter)
        except Exception as e:
            print(f"Error processing size: {e}")
    
    if title:
        try:
            if "joggers" in title.lower():
                input_dict["joggers"]= 1
            elif "jeans" in title.lower():
                input_dict["jeans"]= 1 
            elif "leggings" in title.lower():
                input_dict["leggings"] = 1
        except Exception as e:
            print(f"Error processing title: {e}")

    return input_dict


def make_prediction(input_dict):
    input_df = pd.DataFrame([input_dict])
    model = joblib.load("assets/optional_model.pkl")
    prediction = model.predict(input_df)
    return prediction[0]