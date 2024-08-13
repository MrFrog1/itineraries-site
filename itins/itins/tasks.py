import logging
from celery import shared_task
from django.conf import settings
from .models import Hotel, ExternalReview, ExternalReviewSource
from .utils.reviews_fetch import fetch_google_reviews, fetch_tripadvisor_reviews, fetch_booking_com_reviews
from requests.exceptions import RequestException
from selenium.common.exceptions import WebDriverException

# Set up logging
logger = logging.getLogger(__name__)

@shared_task
def update_external_reviews():
    logger.info("Starting update of external reviews for all hotels")
    hotels = Hotel.objects.all()
    for hotel in hotels:
        try:
            update_google_reviews(hotel)
            update_tripadvisor_reviews(hotel)
            update_booking_com_reviews(hotel)
        except Exception as e:
            logger.error(f"Error updating reviews for hotel {hotel.id}: {str(e)}")
    logger.info("Finished updating external reviews for all hotels")

def update_google_reviews(hotel):
    if hotel.google_place_id:
        try:
            rating, review_count = fetch_google_reviews(hotel.google_place_id, settings.GOOGLE_API_KEY)
            ExternalReview.objects.update_or_create(
                hotel=hotel,
                source=ExternalReviewSource.objects.get(name="Google"),
                defaults={'rating': rating, 'review_count': review_count}
            )
            logger.info(f"Successfully updated Google reviews for hotel {hotel.id}")
        except RequestException as e:
            logger.error(f"Network error fetching Google reviews for hotel {hotel.id}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching Google reviews for hotel {hotel.id}: {str(e)}")

def update_tripadvisor_reviews(hotel):
    if hotel.tripadvisor_url:
        try:
            rating, review_count = fetch_tripadvisor_reviews(hotel.tripadvisor_url)
            ExternalReview.objects.update_or_create(
                hotel=hotel,
                source=ExternalReviewSource.objects.get(name="TripAdvisor"),
                defaults={'rating': rating, 'review_count': review_count}
            )
            logger.info(f"Successfully updated TripAdvisor reviews for hotel {hotel.id}")
        except RequestException as e:
            logger.error(f"Network error fetching TripAdvisor reviews for hotel {hotel.id}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching TripAdvisor reviews for hotel {hotel.id}: {str(e)}")

def update_booking_com_reviews(hotel):
    if hotel.booking_com_url:
        try:
            rating, review_count = fetch_booking_com_reviews(hotel.booking_com_url)
            ExternalReview.objects.update_or_create(
                hotel=hotel,
                source=ExternalReviewSource.objects.get(name="Booking.com"),
                defaults={'rating': rating, 'review_count': review_count}
            )
            logger.info(f"Successfully updated Booking.com reviews for hotel {hotel.id}")
        except WebDriverException as e:
            logger.error(f"Selenium error fetching Booking.com reviews for hotel {hotel.id}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching Booking.com reviews for hotel {hotel.id}: {str(e)}")

@shared_task
def update_single_hotel_reviews(hotel_id):
    logger.info(f"Starting update of external reviews for hotel {hotel_id}")
    try:
        hotel = Hotel.objects.get(id=hotel_id)
        update_google_reviews(hotel)
        update_tripadvisor_reviews(hotel)
        update_booking_com_reviews(hotel)
        logger.info(f"Finished updating external reviews for hotel {hotel_id}")
    except Hotel.DoesNotExist:
        logger.error(f"Hotel with id {hotel_id} does not exist")
    except Exception as e:
        logger.error(f"Unexpected error updating reviews for hotel {hotel_id}: {str(e)}")