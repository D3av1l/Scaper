from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from product_builder import Product
from product_builder import ProductBuilder

def extract_product_details(driver, url):
    """
    Extracts various details of a product from its product page.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        product_url (str): URL of the product page.

    Returns:
        dict: Dictionary containing product details.
    """
    driver.get(url)
    #get name
    name = extract_product_name(driver, url)
    #get price
    price = extract_product_price(driver, url)
    
    # get details
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'rte')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    description_div = soup.find('div', class_='rte')  # Fix the SyntaxError and dictionary error

    # Description
    description = ' '.join([p.text for p in description_div.find_all('p', recursive=False)])

    # Indications
    indications_h2 = description_div.find('h2', text='INDICATIONS')
    indications = indications_h2.find_next_sibling('p').text

    # Composition
    composition_h3 = description_div.find('h3', text='What are its main ingredients?')
    composition = ' '.join([li.text for li in composition_h3.find_next_sibling('ul').find_all('li')])

    # How to Use
    how_to_use_h2 = description_div.find('h2', text='HOW TO USE')
    how_to_use = how_to_use_h2.find_next_sibling('p').text

    return {
        'name': name,
        'price': price,
        'description': description,
        'indications': indications,
        'composition': composition,
        'how_to_use': how_to_use
    }

def extract_product_name(driver: webdriver, product_url: str) -> str:
    """
    Extracts the product name from a given product URL.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        product_url (str): URL of the product page.

    Returns:
        str: Name of the product.
    """
    try:
        driver.get(product_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-name')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup.find('h1', itemprop='name').text
    except Exception as e:
        print(f"Error extracting product name: {e}")

def extract_product_price(driver: webdriver, product_url: str) -> str:
    """
    Extracts the product price from a given product URL.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        product_url (str): URL of the product page.

    Returns:
        str: Price of the product.
    """
    try:
        driver.get(product_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'our_price_display')))
        soup = BeautifulSoup(driver.page_source, 'html.parser').text
        return soup.find('span', id='our_price_display').text
    except Exception as e:
        print(f"Error extracting product price: {e}")


def get_product_urls_from_pages(page_urls, driver):
    product_urls = []

    for page_url in page_urls:
        if page_url is None:
            print("page_url is None")
            continue

        try:
            driver.get(page_url)
        except Exception as e:
            print(f"Error al acceder a la página: {page_url}, error: {e}")
            continue

        while True:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'product_img_link'))
                )
            except Exception as e:
                print(f"Error esperando elementos con la clase 'product_img_link', error: {e}")
                break

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product_elements = soup.find_all(class_='product_img_link')

            for product in product_elements:
                href = product.get('href')
                if href is not None:
                    product_urls.append(href)

            try:
                next_page_button = driver.find_element_by_class_name('next')
                next_page_button.click()
            except Exception:
                break

    return product_urls

def start(urls, driver):
    products = []
    import product_builder

    for url in urls:
        try:
            nombre, precio, descripcion, indicaciones, composicion, modo_empleo = extract_product_details(driver, url)
        except TypeError as e:
            print(f"Error al extraer detalles del producto de la URL {url}: {e}")
            continue

        try:
            product = product_builder.Product(nombre, precio, descripcion, indicaciones, composicion, modo_empleo)
        except TypeError as e:
            print(f"Error al crear instancia de Producto: {e}")
            continue

        products.append(product)

    return products


if __name__ == "__main__":
    urls = [
        'https://www.farmavazquez.com',
        'https://www.farmavazquez.com/tratamiento-de-hidratacion-3261',
        'https://www.farmavazquez.com/tratamiento-regenerador-3262',
        'https://www.farmavazquez.com/tratamiento-anticaida-1018',
        'https://www.farmavazquez.com/tratamiento-anticaspa-1016',
        'https://www.farmavazquez.com/tratamiento-antigrasa-1017',
    ]

    driver = webdriver.Firefox()  # Initialize your WebDriver
    product_urls = get_product_urls_from_pages(urls, driver)
    products = start(product_urls, driver)
    print(products)
    driver.quit()