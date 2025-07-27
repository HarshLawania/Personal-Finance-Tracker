from datetime import datetime 

DATE_FORMAT = "%d-%m-%Y"

def get_date(prompt = "Enter date (dd-mm-yyyy) or leave blank for today: ", allow_default=False ):
    data_str = input(prompt)

    # if user does not type anything
    if allow_default and data_str.strip() == "":
        return datetime.today().strftime(DATE_FORMAT) # converting datetime to string format
    
    # user entered something
    try:
        # Tries to convert the entered string into a real datetime object.
        # strptime() = “string parse time”
        # If the format is wrong (e.g., 2025/07/23), it will raise a ValueError.
        valid_date = datetime.strptime(data_str, DATE_FORMAT)
        return valid_date.strftime(DATE_FORMAT)
    
    # If format is wrong it will raise error
    except ValueError:
        print("❌ Invalid format. Try again.")
        return get_date(prompt, allow_default)
    

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if( amount <= 0 ):
            raise ValueError ("Amount must be greater than Zero")
        return amount
    except ValueError as e:
        print("❌", e)
        return get_amount()


def get_category():
    category = input("Enter 'I' for Income or 'E' for Expense: ").upper()
    if category == "I":
        return "Income"
    elif category == "E":
        return "Expanse"
    else:
        print("❌ Invalid choice. Try again.")
        return get_category()

    

def get_description():
    return input("Get any description (Optional): ")


 