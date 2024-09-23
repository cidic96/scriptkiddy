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

        # Extract all image URLs using JavaScript
        image_urls = driver.execute_script("""
            var urls = new Set();
            var images = document.querySelectorAll('#altImages img');
            for (var i = 0; i < images.length; i++) {
                var src = images[i].getAttribute('src');
                if (src) {
                    urls.add(src.replace(/._[^.]*\./, '.'));
                }
            }
            return Array.from(urls);
        """)

        # Filter and prioritize high-quality images
        high_quality_images = list({url for url in image_urls if '_AC_SX679_' in url or '_AC_SL1500_' in url})
        if not high_quality_images:
            high_quality_images = list(set(image_urls))

        vendor_element = driver.find_elements(By.ID, "bylineInfo")
        vendor = vendor_element[0].text.strip() if vendor_element else "Amazon"

        asin = url.split("/dp/")[1][:10]

        product_data = {
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
            'Gift Card': 'FALSE',
            'Variant Weight Unit': 'kg',
            'Status': 'active'
        }

        # Add unique image URLs to the product data
        for i, img_url in enumerate(high_quality_images[:10]):  # Limit to 10 images
            product_data[f'Image Src {i+1}'] = img_url
            product_data[f'Image Position {i+1}'] = str(i + 1)
            product_data[f'Image Alt Text {i+1}'] = title

        return product_data
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
                base_row = {k: v for k, v in product_data.items() if not k.startswith('Image')}
                for i in range(1, 11):  # Assuming max 10 images
                    if f'Image Src {i}' in product_data:
                        row = base_row.copy()
                        row['Image Src'] = product_data[f'Image Src {i}']
                        row['Image Position'] = product_data[f'Image Position {i}']
                        row['Image Alt Text'] = product_data[f'Image Alt Text {i}']
                        writer.writerow(row)
                    else:
                        break
            time.sleep(5)  # Add a delay between requests to avoid being blocked

# Example usage
urls = [
   'https://amazon.in/dp/B07WTXHQR1/',
'https://amazon.in/dp/B09P6MCZY4/',
'https://amazon.in/dp/B07G9Z3PC5/',
'https://amazon.in/dp/B07L2VJNKV/',
'https://amazon.in/dp/B07L2R5THK/',
'https://amazon.in/dp/B07GB2BPCR/',
'https://amazon.in/dp/B085W5TQ9L/',
'https://amazon.in/dp/B07G9GYNFY/',
'https://amazon.in/dp/B086RSPBMS/',
'https://amazon.in/dp/B07L2TCZP8/',
'https://amazon.in/dp/B073G224LC/',
'https://amazon.in/dp/B07L2RCK33/',
'https://amazon.in/dp/B076VP6VMH/',
'https://amazon.in/dp/B01HUYGBEC/',
'https://amazon.in/dp/B07F2HQGN1/',
'https://amazon.in/dp/B07L2V7W8H/',
'https://amazon.in/dp/B07L2V1WXJ/',
'https://amazon.in/dp/B09Z2RJPB4/',
'https://amazon.in/dp/B0BXFCHM68/',
'https://amazon.in/dp/B0CLZR6WFW/',
'https://amazon.in/dp/B0C8B63K52/',
'https://amazon.in/dp/B0BNNNX42J/',
'https://amazon.in/dp/B0CK5X741G/',
'https://amazon.in/dp/B07L2RTB46/',
'https://amazon.in/dp/B079NXWNB7/'
]

create_shopify_csv(urls, 'shopify_products.csv')