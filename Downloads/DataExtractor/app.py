from flask import Flask, render_template, request, send_file
import pandas as pd
from main import scrape_truckers, scrape_truckers_selenium  # Import scraping functions

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    truckers = []
    
    if request.method == "POST":
        mc_number = request.form["mc_number"].strip()  # Get MC number from form
        
        if mc_number:
            # Construct the URL dynamically based on the MC number
            url = f"https://safer.fmcsa.dot.gov/CompanySnapshot.aspx?mc={mc_number}"
            
            # First, try scraping using BeautifulSoup (requests)
            trucker_data = scrape_truckers(url)
            if not trucker_data:
                print("Switching to Selenium...")  # If no data, use Selenium
                trucker_data = scrape_truckers_selenium(url)
            
            if trucker_data:
                truckers.append(trucker_data[0])  # Assuming the data is returned as a list of dictionaries
                
                # Save data to Excel and CSV
                df = pd.DataFrame(truckers)
                df.to_excel("static/truckers_data.xlsx", index=False)
                df.to_csv("static/truckers_data.csv", index=False)
            else:
                print("No data found.")
        
    return render_template("index.html", truckers=truckers)

@app.route("/download/<file_type>")
def download_file(file_type):
    file_path = f"static/truckers_data.{file_type}"
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
