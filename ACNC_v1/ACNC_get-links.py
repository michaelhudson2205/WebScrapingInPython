import asyncio
import pandas as pd

# from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# ! Set this variable to the desired year
ais_year = 2024
ais_label = f"Annual Information Statement {ais_year}"


# Define the scraping function for one URL
async def scrape_ais_link(target_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(target_url)

        try:
            await page.wait_for_selector("div.table-responsive", timeout=10000)
        except Exception:
            print(f"Timeout or missing content for {target_url}")
            await browser.close()
            return None

        html = await page.content()
        await browser.close()

        soup = BeautifulSoup(html, "html.parser")

        # Find the target table
        table = soup.select_one("div.table-responsive table")
        if not table:
            print(f"Table not found for {target_url}")
            return None

        # Iterate over rows
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 4 and ais_label in cells[0].get_text(strip=True):
                link_tag = cells[3].find("a")
                if link_tag and link_tag.has_attr("href"):
                    return "https://www.acnc.gov.au" + link_tag["href"]
        return None


## Main function to run the scraper
async def main():
    input_csv = "file1_phn_static_links.csv"
    df = pd.read_csv(input_csv)

    results = []
    for _, row in df.iterrows():
        phn_name = row["PHN_Name"]
        target_url = row["URL"]
        print(f"Scraping: {phn_name}")
        ais_link = await scrape_ais_link(target_url)
        if ais_link:
            results.append({"PHN_Name": phn_name, "AIS_Link": ais_link})
        else:
            results.append({"PHN_Name": phn_name, "AIS_Link": None})

    output_df = pd.DataFrame(results)
    # date_str = datetime.now().strftime("%Y-%m-%d")
    # output_csv = f"file2_ais{ais_year}_links_{date_str}.csv"
    output_csv = f"file2_ais{ais_year}_links.csv"
    output_df.to_csv(output_csv, index=False)
    print(f"\nDone. Results saved to {output_csv}")


## Run the main function
if __name__ == "__main__":
    asyncio.run(main())
