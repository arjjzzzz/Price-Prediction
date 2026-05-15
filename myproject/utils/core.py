from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def get_flipkart_price(product_name):
    search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
    
    # Configure Selenium to avoid detection
    options = Options()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)

    try:
        # Wait for price to load (up to 15 seconds)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '₹')]"))
        )

        # Scroll to trigger lazy loading
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(2)  # Let dynamic content load

        # Find price using XPath (more reliable than class)
        price_element = driver.find_element(
            By.XPATH, 
            "(//div[contains(text(), '₹') or contains(@class, '_30jeq3')])[1]"
        )
        
        if price_element:
            price_text = price_element.text.strip()
            price = re.sub(r"[^\d]", "", price_text)  # Extract digits
            return float(price)

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    finally:
        driver.quit()  # Ensure browser closes

def get_amazon_price(product_name):
    """Scrapes Amazon for the product price using Selenium."""
    search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"

    options = Options()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)

    time.sleep(3)  # Allow time for page to load

    try:
        price_element = driver.find_element(By.CLASS_NAME, "a-price-whole")
        price = price_element.text.replace(",", "").strip()
        driver.quit()
        return float(price)
    except:
        driver.quit()
        return None

def compare_prices(product_name):
    amazon_price = get_amazon_price(product_name)
    flipkart_price = get_flipkart_price(product_name)

    isFlipKartLower = 5
    lowestPrice = -1
    print("\nPrice Comparison:")
    if amazon_price:
        print(f"Amazon: ₹{amazon_price}")
    else:
        isFlipKartLower = 3
        print("Amazon price not found.")
        if flipkart_price:
            lowestPrice = flipkart_price
        else:
            isFlipKartLower = 5

    if flipkart_price:
        print(f"Flipkart: ₹{flipkart_price}")
    else:
        isFlipKartLower = 4
        print("Flipkart price not found.")
        if amazon_price:
            lowestPrice = amazon_price
        else:
            isFlipKartLower = 5


    if amazon_price and flipkart_price:
        if amazon_price < flipkart_price:
            print("Amazon has the lower price.")
            lowestPrice = amazon_price
            isFlipKartLower = 0
        elif flipkart_price < amazon_price:
            print("Flipkart has the lower price.")
            lowestPrice = flipkart_price
            isFlipKartLower = 1
        else:
            lowestPrice = flipkart_price
            print("Both prices are the same.")
            isFlipKartLower = 2
    return {'amazon_price' : amazon_price , 'flipkart_price' : flipkart_price, 'isFlipKartLower' : isFlipKartLower, 'product_name' : product_name, 'lowestPrice' : lowestPrice}
    

if __name__ == "__main__":
    product_name = input("Enter product name: ")
    res = compare_prices(product_name)
    print(res)
