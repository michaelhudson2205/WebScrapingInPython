# Load the necessary libraries
import asyncio
import pandas as pd
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime


# Function to scrape a single ACNC page
async def scrape_acnc_data(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        try:
            await page.wait_for_selector("div")
        except Exception:
            print(f"Timeout or missing content for {url}")
            await browser.close()
            return {
                "URL": url,
                "Legal Name": None,
                "Full Time Employees": None,
                "Employee Expenses": None,
            }

        html = await page.content()
        await browser.close()

        soup = BeautifulSoup(html, "html.parser")

        # Extract legal name
        legal_name = None
        text_blocks = soup.find_all("div", class_="text-pre-line")
        if text_blocks:
            legal_name = text_blocks[0].get_text(strip=True)

        # Extract Full Time Employees from <li> elements
        full_time_employees = None
        li_tags = soup.select("ul.list-unstyled.my-0 li")
        for li in li_tags:
            text = li.get_text(strip=True)
            if "Full time employees" in text:
                full_time_employees = text.split(":")[-1].strip()
                break

        # Extract Employee Expenses from tables
        tables = soup.find_all("div", class_="table-responsive")
        employee_expenses = None

        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all(["td", "th"])
                if len(cols) < 2:
                    continue
                label = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                if "Employee expenses" in label:
                    employee_expenses = value

        print(f"Scraped: {legal_name or 'Unknown'}")

        def extract_int(value):
            try:
                if value:
                    return int(value.replace(",", "").replace("$", "").strip())
            except:
                return None
            return None

        full_time_employees = extract_int(full_time_employees)
        employee_expenses = extract_int(employee_expenses)

        return {
            "URL": url,
            "Legal Name": legal_name,
            "Full Time Employees": full_time_employees,
            "Employee Expenses": employee_expenses,
        }


# Main loop for scraping multiple pages
async def scrape_all_acnc(urls):
    results = []
    for rec in records:
        phn_name = rec["PHN_Name"]
        url = rec["URL"]
        print(f"Scraping {phn_name} - {url}...")
        try:
            data = await scrape_acnc_data(url)
            data["PHN_Name"] = phn_name
            results.append(data)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            results.append(
                {
                    "PHN_Name": phn_name,
                    "URL": url,
                    "Legal Name": None,
                    "Full Time Employees": None,
                    "Employee Expenses": None,
                }
            )
    return results


# Run the scraper
input_csv = "phn_urls_all.csv"  # Path to the input CSV file

timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
output_csv = f"acnc_scraped_data_{timestamp}.csv"  # Path to the output CSV file

df_urls = pd.read_csv(input_csv)
# urls = df_urls["URL"].dropna().tolist()  # Assuming the URLs are in a column named 'URL'
records = df_urls[["PHN_Name", "URL"]].dropna().to_dict(orient="records")

# print(f"Found {len(urls)} URLs to scrape...\n")
results = asyncio.run(scrape_all_acnc(records))

df_results = pd.DataFrame(results)
df_results.to_csv(output_csv, index=False)
print(f"\nScraping completed. Results saved to {output_csv}.")
