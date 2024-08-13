import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_google_reviews(place_id, api_key):
    """
    Fetch reviews from Google Places API
    """
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=rating,user_ratings_total&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = data.get('result', {})
        rating = result.get('rating', 0)
        review_count = result.get('user_ratings_total', 0)
        return rating, review_count
    else:
        print(f"Error fetching Google reviews: {response.status_code}")
        return 0, 0

def fetch_tripadvisor_reviews(url):
    """
    Fetch reviews from TripAdvisor using web scraping
    Note: This method may break if TripAdvisor changes their HTML structure
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        rating_element = soup.find('span', class_='ui_bubble_rating')
        review_count_element = soup.find('a', class_='seeAllReviews')
        
        if rating_element and review_count_element:
            rating = float(rating_element['alt'].split()[0]) / 5 * 10  # Convert to 5-star scale
            review_count = int(review_count_element.text.split()[0].replace(',', ''))
            return rating, review_count
    
    print(f"Error fetching TripAdvisor reviews: {response.status_code}")
    return 0, 0

def fetch_booking_com_reviews(url):
    """
    Fetch reviews from Booking.com using Selenium
    Note: This method requires ChromeDriver to be installed and in PATH
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'bui-review-score__badge')))
        
        rating_element = driver.find_element(By.CLASS_NAME, 'bui-review-score__badge')
        review_count_element = driver.find_element(By.CLASS_NAME, 'bui-review-score__text')
        
        if rating_element and review_count_element:
            rating = float(rating_element.text.replace(',', '.'))
            review_count = int(review_count_element.text.split()[0].replace(',', ''))
            return rating, review_count
    except Exception as e:
        print(f"Error fetching Booking.com reviews: {str(e)}")
    finally:
        driver.quit()
    
    return 0, 0
