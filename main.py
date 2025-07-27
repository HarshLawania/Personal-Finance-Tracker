import csv
import pandas as pd
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
             # index=False = don’t write row numbers to file
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        with open(cls.CSV_FILE, "a", newline="") as file:
            # csv.DictWriter: Lets you write rows from dictionaries
            writer = csv.DictWriter(file, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
            print("✅ Data Entered Successfully")

    @classmethod
    def read_all_entries(cls):
        try:
            df = pd.read_csv(cls.CSV_FILE)
            print("\n📄 All Transactions:")
            print(df)
        except FileNotFoundError:
            print("❌ No data file found.")

    @classmethod
    def filter_by_date(cls, start, end):
        try:
            df = pd.read_csv(cls.CSV_FILE)
            df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)

            start_date = datetime.strptime(start, cls.FORMAT)
            end_date = datetime.strptime(end, cls.FORMAT)

            filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
            # Convert dates back to string format for display
            filtered["date"] = filtered["date"].dt.strftime(cls.FORMAT)
            print("\n📅 Filtered Transactions:")
            print(filtered)
        except Exception as e:
            print("❌ Error filtering data:", e)

    @classmethod
    def category_summary(cls):
        try:
            df = pd.read_csv(cls.CSV_FILE)
            df["category"] = df["category"].replace("Expance", "Expense")

            income = df[df["category"] == "Income"]["amount"].sum()
            expense = df[df["category"] == "Expense"]["amount"].sum()
            net = income - expense
  
            print(f"\n🟩 Total Income  : ₹{income}")
            print(f"🟥 Total Expense : ₹{expense}")
            print(f"🟨 Net Balance   : ₹{net}")
        except:
            print("❌ Error calculating summary.")

    # Category wise Total Expance
    @classmethod
    def detailed_category_summary(cls):
        try:
            df = pd.read_csv(cls.CSV_FILE)
            df["category"] = df["category"].replace("Expance", "Expense")
            grouped = df.groupby("category")["amount"].sum()
            print("\n📊 Category-wise Totals:")
            print(grouped)
        except:
            print("❌ Error generating summary.")

    @classmethod
    def show_pie_chart(cls):
        try:
            df = pd.read_csv(CSV.CSV_FILE)
        except FileNotFoundError:
            print("No data file found")
            return

        if df.empty:
            print("No data to Display")
            return
        
        totals = df.groupby("category")["amount"].sum()

        if totals.empty:
            print("No data to Plot")
            return
        
        plt.figure(figsize=(6,6))

        '''
            pie(): A function that creates a pie chart.
            
            Index = category (e.g., "Income", "Expense"), Values = total amount per category
            
            labels=: Names of the pie slices.
            totals.index: The category names ("Income", "Expense") from the Pandas Series
            
            autopct=: Format for showing percentage on each slice.
            "%1.1f%%":  -> %1.1f → Show 1 decimal place (e.g., 75.0)
                        -> %% → Escaped % symbol (so it prints %)
            
            startangle=140 -> Rotates the pie chart 140 degrees so the first slice starts at a different angle.

        ''' 
        plt.pie(totals, labels=totals.index, autopct="%1.1f%%", startangle=140, colors=["#76c893", "#f28482"])
        plt.title("Income vs Expense")
        plt.show()


    @classmethod
    def show_bar_chart(cls):
        try:
            df = pd.read_csv(CSV.CSV_FILE)
        except FileNotFoundError:
            print("No data file found")
            return
        
        if df.empty:
            print("No data to display")
            return
        
        grouped = df.groupby("category")["amount"].sum()

        plt.figure(figsize=(8, 5))
        plt.bar(grouped.index, grouped.values, color=["#6a5acd", "#ffa07a"])
        plt.title("Total by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        plt.show()

def add_transection():
    CSV.initialize_csv()
    date = get_date()
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def menu():
    while True:
        print("\n==== Personal Finance Tracker ====")
        print("1. Add a new transaction")
        print("2. View all entries")
        print("3. Filter by date range")
        print("4. Show category-wise summary")
        print("5. Show total balance")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == "1":
            add_transection()
        elif choice == "2":
            CSV.read_all_entries()
        elif choice == "3":
            start = get_date("Start date (dd-mm-yy): ", allow_default=False)
            end = get_date("End date (dd-mm-yy): ", allow_default=False)
            CSV.filter_by_date(start, end)
        elif choice == "4":
            CSV.show_pie_chart()
        elif choice == "5":
            CSV.show_bar_chart()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("❌ Invalid option. Try again.")

 
if __name__ == "__main__":
    menu()
