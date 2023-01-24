from bs4 import BeautifulSoup
import requests
import json

# Engen
print("-" * 50)
print("Engen")
print("-" * 50)

engen_price_list_json = requests.get(
    "https://engen-admin.engen.co.za/api/country/fuel-prices"
).text

engen_json = json.loads(engen_price_list_json)
prices = engen_json["response"]["data"]["prices"]

for price in prices:
    fuel_type = price["fuel_type"]
    fuel_price = price["price"]
    fuel_region = price["region"].capitalize()
    print(
        f"Fuel Type: {fuel_type}\nFuel Price: R{fuel_price}\nFuel Region: {fuel_region}\n"
    )

# Caltex
print("-" * 50)
print("Caltex")
print("-" * 50)

html_caltex = requests.get(
    "https://caltex.co.za/motorists/products-and-services/fuel-price.html"
).text

soup = BeautifulSoup(html_caltex, "lxml")
petrol_table = soup.find("div", class_="price-detail")
petrol_item_bases = petrol_table.find_all("div", class_="price-item")
for petrol_item_base in petrol_item_bases:
    petrol_item = petrol_item_base.find_all("div", class_="wrapper")

    petrol_name = petrol_item[0].text.strip()
    petrol_price_coastal = (
        petrol_item[1].text.strip().replace("cpl", "R").replace("-", "N/A")
    )
    petrol_price_inland = petrol_item[2].text.strip().replace("cpl", "R")

    print(
        f"Fuel Type: {petrol_name}\nFuel Price Coastal: {petrol_price_coastal}\nFuel Price Inland: {petrol_price_inland}\n"
    )

# Shell
print("-" * 50)
print("Shell")
print("-" * 50)

html_shell = requests.get(
    "https://www.shell.co.za/motorists/shell-fuels/petrol-price.html"
).text

soup = BeautifulSoup(html_shell, "lxml")
petrol_table_inland = soup.find_all("tbody")[0]
petrol_table_coastal = soup.find_all("tbody")[1]

table_heading_inland = petrol_table_inland.find_all("tr")[0].text.strip()
table_heading_coastal = petrol_table_coastal.find_all("tr")[0].text.strip()

petrol_names_inland = table_heading_inland.split("\n")
table_retail_prices_inland = petrol_table_inland.find_all("tr")[21].text.strip()
petrol_prices_inland = table_retail_prices_inland.split("\n")

petrol_names_coastal = table_heading_coastal.split("\n")
table_retail_prices_coastal = petrol_table_coastal.find_all("tr")[21].text.strip()
petrol_prices_coastal = table_retail_prices_coastal.split("\n")

print("Inland Prices")
print("-" * 50)

for i in range(1, 6):
    price = petrol_prices_inland[i].replace("-", "N/A")
    print(f"Petrol Name: {petrol_names_inland[i]}\nPetrol Price: cpl {price}\n")

print("Coastal Prices")
print("-" * 50)

for i in range(1, 6):
    price = petrol_prices_coastal[i].replace("-", "N/A")
    print(f"Petrol Name: {petrol_names_coastal[i]}\nPetrol Price: cpl {price}\n")
