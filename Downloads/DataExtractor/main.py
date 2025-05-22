import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from main import scrape_truckers, scrape_truckers_selenium

# Function to extract data using requests & BeautifulSoup (for static sites)
def scrape_truckers(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            truckers = []

            # Modify these selectors based on actual website structure
            for row in soup.find_all("div", class_="trucker-info"):
                try:
                    name = row.find("h2", class_="trucker-name").text.strip()
                    location = row.find("span", class_="location").text.strip()
                    email = row.find("span", class_="email").text.strip() if row.find("span", class_="email") else "Not Available"
                    mc_number = row.find("span", class_="mc-number").text.strip() if row.find("span", class_="mc-number") else "Not Available"
                    mc_date = row.find("span", class_="mc-date").text.strip() if row.find("span", class_="mc-date") else "Unknown"

                    # Calculate MC age
                    mc_age = "Unknown"
                    if mc_date != "Unknown":
                        try:
                            mc_date_obj = datetime.strptime(mc_date, "%Y-%m-%d")
                            mc_age = (datetime.now() - mc_date_obj).days // 365
                        except ValueError:
                            pass

                    truckers.append({"Name": name, "Location": location, "Email": email, "MC Number": mc_number, "MC Age (Years)": mc_age})
                except AttributeError:
                    continue  # Skip missing data

            return truckers
        else:
            print(f"Error: Failed to fetch the webpage (Status Code: {response.status_code})")
            return []
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return []

# Function to extract data using Selenium (for JavaScript-heavy sites)
def scrape_truckers_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in the background
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        truckers = []

        # Modify selectors based on actual website structure
        rows = driver.find_elements(By.CLASS_NAME, "trucker-info")
        for row in rows:
            try:
                name = row.find_element(By.CLASS_NAME, "trucker-name").text.strip()
                location = row.find_element(By.CLASS_NAME, "location").text.strip()
                email = row.find_element(By.CLASS_NAME, "email").text.strip() if row.find_elements(By.CLASS_NAME, "email") else "Not Available"
                mc_number = row.find_element(By.CLASS_NAME, "mc-number").text.strip() if row.find_elements(By.CLASS_NAME, "mc-number") else "Not Available"
                mc_date = row.find_element(By.CLASS_NAME, "mc-date").text.strip() if row.find_elements(By.CLASS_NAME, "mc-date") else "Unknown"

                # Calculate MC age
                mc_age = "Unknown"
                if mc_date != "Unknown":
                    try:
                        mc_date_obj = datetime.strptime(mc_date, "%Y-%m-%d")
                        mc_age = (datetime.now() - mc_date_obj).days // 365
                    except ValueError:
                        pass

                truckers.append({"Name": name, "Location": location, "Email": email, "MC Number": mc_number, "MC Age (Years)": mc_age})
            except:
                continue  # Skip errors

        driver.quit()
        return truckers

    except Exception as e:
        print(f"Selenium Error: {e}")
        driver.quit()
        return []

# Choose a target website
url = "https://safer.fmcsa.dot.gov/CompanySnapshot.aspx"  # Replace with the actual working URL

# Try BeautifulSoup first, use Selenium if necessary
truckers_data = scrape_truckers(url)
if not truckers_data:
    print("Switching to Selenium...")
    truckers_data = scrape_truckers_selenium(url)

# Apply filters if data is retrieved
if truckers_data:
    df = pd.DataFrame(truckers_data)
    
    # Get user input for filtering
    try:
        mc_age_filter = int(input("Enter MC Age filter (show truckers older than X years): "))
        
        # Apply filter
        filtered_df = df[df["MC Age (Years)"] != "Unknown"]
        filtered_df = filtered_df[filtered_df["MC Age (Years)"].astype(int) > mc_age_filter]

        # Save filtered data in Excel
        filtered_df.to_excel("filtered_truckers_data.xlsx", index=False)
        print(f"Filtered data saved to 'filtered_truckers_data.xlsx' (MC Age > {mc_age_filter} years).")

    except ValueError:
        print("Invalid input! Please enter a valid number for MC Age filter.")
else:
    print("No data found.")
