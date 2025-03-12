import pandas as pd

# 📌 Load the data
data_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\fac_buss_al.csv"
df = pd.read_csv(data_path)

# 📌 Define the category to sector mapping based on core keywords
category_keywords = {
    "Retail and Consumer Goods": ["Grocery", "Supermarket", "Clothing", "Furniture", "Appliance", 
                                  "Jewelry", "Shoe", "Hardware", "Discount", "Sporting", "Goods", 
                                  "Book", "Music", "Toy", "Electronics", "Art", "Shopping", "Mall", 
                                  "Convenience", "Gift", "Shop", "Store", "Antique", "Florist", "Liquor", 
                                  "Tobacco", "Boutique", "Thrift", "Gas", "Home", "Cell", "Phone", "Vaporizer",
                                  "Flooring", "Gun", "Dollar", "Market", "Flea", "Ice Cream", "Winery", "Deli", 
                                  "Promotional products", "Ice", "Coffee", "Pizza", "Pizza Delivery", "Sandwich", 
                                  "Donuts", "Barbecue", "Beverage", "Cookie"],

    "Services": ["Restaurant", "Fast", "Food", "Café", "Beauty", "Barber", "Nail", "Cleaning", 
                 "Dry", "Cleaner", "Moving", "Truck", "Rental", "Plumbing", "Wedding", "Event", "Planning", 
                 "Car", "Repair", "Fitness", "Yoga", "Health", "Medical", "Equipment", "Coffee", "Hair", 
                 "Employment", "Massage", "Physical therapist", "Driving", "Home improvement", "Caterer", "Diner",
                 "Hotel", "Motel", "Bed", "RV", "Restaurant", "Supply", "Catering", "Inn", "Brewery", "Cafe"],

    "Manufacturing and Industrial": ["Manufacturer", "Machine", "Plastic", "Fabrication", "Metal", 
                                     "Welding", "Printing", "Food", "Processing", "Equipment", "Chemical", 
                                     "Industrial", "Textile", "Steel", "Mining", "Factory", "Custom label", 
                                     "Packaging", "Molding", "Mill"],

    "Transportation and Warehousing": ["Logistics", "Shipping", "Trucking", "Freight", "Auto", "Parts", 
                                       "Moving", "Car", "Tire", "Warehouse", "Truck dealer", "Vehicle", "repair", 
                                       "Towing", "Mechanic", "Railroad", "ATV", "Forklift", "Storage", "Container", 
                                       "Dock", "Builder"],

    "Agriculture and Farming": ["Farm", "Agricultural", "Livestock", "Organic", "Equipment", "Plant", 
                                "Nursery", "Animal", "Feed", "Poultry", "Meat processor", "Chicken", "Orchard"],

    "Healthcare and Social Services": ["Healthcare", "Nursing", "Child", "Care", "Rehabilitation", 
                                       "Social", "Pharmacy", "Medical", "Clinic", "Health", "Wellness"],

    "Real Estate and Property": ["Real", "Estate", "Property", "Construction", "Home", "Improvement", 
                                 "Landscaping", "Supply", "Archery", "Roofing", "Realty", "Developer"],

    "Government and Non-Profit": ["Government", "Non-profit", "Public", "Administration", "Police", 
                                  "Fire", "Chamber", "Commerce", "Public", "services", "Religious", "Public utility"],

    "Technology and IT": ["IT", "Software", "Computer", "Tech", "Electronics", "Tech repair", "Hardware", 
                          "Internet", "Network", "Digital", "Telecom"],

    "Entertainment and Recreation": ["Movie", "Theater", "Amusement", "Bowling", "Event", "Art", "Nightclub", 
                                     "Golf", "Skate", "Festival", "Sports", "Sporting", "Fitness", "Tourist", 
                                     "Attraction", "Park", "Boat", "RV"],

    "Wholesale and Distribution": ["Wholesale", "Bakery", "Grocer", "Packaging", "Distribution", "Safety", 
                                   "Propane", "Sign", "Produce", "Packaging", "Material", "Handling", "Grocery", 
                                   "Wholesale distributor"],

    "Construction and Building": ["Contractor", "Construction", "Building", "Materials", "Plumbing", 
                                  "Electrician", "Roofing", "Lumber", "Excavating", "Siding", "Builder", 
                                  "Remodeler", "Handyman", "Concrete", "Paving"],

    "Utilities": ["Gas", "Water", "Electricity", "Power", "Utility", "Energy", "Solar", "Hydraulic"]
}

# 📌 Create the "Class" column by checking if any of the core category keywords are in the 'Category' column
def get_class(category):
    if isinstance(category, str):  # Ensure category is a valid string
        for class_name, keywords in category_keywords.items():
            if any(keyword.lower() in category.lower() for keyword in keywords):  # Check if the keyword matches
                return class_name
    return 'Other'  # Return 'Other' if no match found or category is not a string

df['Class'] = df['Category'].apply(get_class)

# 📌 Add all 'Other' categories to 'Utilities'
df['Class'] = df['Class'].apply(lambda x: 'Utilities' if x == 'Other' else x)

# 📌 Save the updated dataframe with the new "Class" column to a new CSV file
output_file_path = r"D:\Mobility Report & Dashboard\Dashboard_Code\Establishment\fac_buss_all_with_class_updated_v2.csv"  # Change the path if needed
df.to_csv(output_file_path, index=False)

print(f"✅ Updated file with 'Class' column saved at: {output_file_path}")
