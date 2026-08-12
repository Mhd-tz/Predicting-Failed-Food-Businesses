"""Filter the verified Vancouver Business Licences sample to REAL food-related businesses
and save as the food-bank proposal dataset.
"""
import pandas as pd

src = "vancouver_business_licences_sample.csv"
df = pd.read_csv(src)

# keep only genuine food businesses
food_types = [
    "Restaurant",
    "Wholesale Dealer - Food",
    "Retail Dealer - Food",
    "Limited Service Food Establishment",
    "Food Market",
    "Food Manufacturer Assembler and Processor",
]
sub = df[df["businesstype"].isin(food_types)].copy()

# label like failed = 1 if Cancelled or Gone Out of Business
sub["failed"] = sub["status"].isin(["Cancelled", "Gone Out of Business"]).astype(int)

print("food-business rows:", len(sub))
print("failed rate:", round(sub["failed"].mean(), 3))

# keep a tidy column subset for the proposal
keep = [
    "licencenumber", "businessname", "businesstype", "localarea",
    "status", "failed", "numberofemployees", "issueddate", "expireddate",
    "feepaid", "folderyear", "postalcode",
]
out = sub[keep].copy()
out.to_csv("vancouver_food_businesses_sample.csv", index=False)
print("saved vancouver_food_businesses_sample.csv", out.shape)
print(out.head(3).to_string())
