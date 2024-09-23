import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_amazon_product(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        title = wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text.strip()
        
        price_element = driver.find_elements(By.CLASS_NAME, "a-price-whole")
        price = price_element[0].text if price_element else ""

        description_element = driver.find_elements(By.ID, "productDescription")
        description = description_element[0].text.strip() if description_element else ""

        image_element = driver.find_elements(By.ID, "landingImage")
        image_url = image_element[0].get_attribute("src") if image_element else ""

        vendor_element = driver.find_elements(By.ID, "bylineInfo")
        vendor = vendor_element[0].text.strip() if vendor_element else "Amazon"

        asin = url.split("/dp/")[1][:10]

        return {
            'Handle': asin,
            'Title': title,
            'Body (HTML)': f'<p>{description}</p>',
            'Vendor': vendor,
            'Type': 'Home & Kitchen',
            'Tags': '',
            'Published': 'TRUE',
            'Option1 Name': 'Title',
            'Option1 Value': 'Default Title',
            'Variant Inventory Qty': '10',
            'Variant Inventory Policy': 'deny',
            'Variant Fulfillment Service': 'manual',
            'Variant Price': price,
            'Variant Requires Shipping': 'TRUE',
            'Variant Taxable': 'TRUE',
            'Image Src': image_url,
            'Image Position': '1',
            'Gift Card': 'FALSE',
            'Variant Weight Unit': 'kg',
            'Status': 'active'
        }
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None
    finally:
        driver.quit()

def create_shopify_csv(urls, output_file):
    fieldnames = [
        'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type', 'Tags', 'Published',
        'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value',
        'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty',
        'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price',
        'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position',
        'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description', 'Google Shopping / Google Product Category',
        'Google Shopping / Gender', 'Google Shopping / Age Group', 'Google Shopping / MPN',
        'Google Shopping / AdWords Grouping', 'Google Shopping / AdWords Labels', 'Google Shopping / Condition',
        'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0', 'Google Shopping / Custom Label 1',
        'Google Shopping / Custom Label 2', 'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4',
        'Variant Image', 'Variant Weight Unit', 'Variant Tax Code', 'Cost per item', 'Price / International',
        'Compare At Price / International', 'Status'
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for url in urls:
            product_data = scrape_amazon_product(url)
            if product_data:
                writer.writerow(product_data)
            time.sleep(5)  # Add a delay between requests to avoid being blocked

# Example usage
urls = [
    'https://www.amazon.in/dp/B0C8DJW4T1',
    'https://www.amazon.in/dp/B0CQSRGKW4'
]

create_shopify_csv(urls, 'shopify_products.csv')