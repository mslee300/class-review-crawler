import requests
import csv
from bs4 import BeautifulSoup

# URL of the professor's page
url = 'https://www.ratemyprofessors.com/professor/2322926'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the review elements
    reviews = soup.find_all(class_='RatingsList__RatingsUL-hn9one-0 cbdtns')

    # Create a list to store the data
    data = []

    # Extract the required information from each review
    for review in reviews:
        school_name = soup.find(class_='NameTitle__Title-dowf0z-1 iLYGwn').text.strip().split("at ",1)[1]
        print(school_name)
        class_name = review.find(class_='RatingHeader__StyledClass-sc-1dlkqw1-3 eXfReS').text.strip()
        print(class_name)
        class_code = review.find(class_='Comments__StyledComments-dzzyvm-0 gRjWel').text.strip()
        print(class_code)
        professor_name = soup.find(class_='NameTitle__LastNameWrapper-dowf0z-2 glXOHH').text.strip()
        print(professor_name)
        rating_date = review.find(class_='TimeStamp__StyledTimeStamp-sc-9q2r30-0 bXQmMr RatingHeader__RatingTimeStamp-sc-1dlkqw1-4 iwwYJD').text.strip()
        print(rating_date)
        review_content = review.find(class_='CardNumRating__CardNumRatingNumber-sc-17t4b9u-2 gcFhmN').text.strip()
        print(review_content)

        # Append the data to the list
        data.append({
            'School Name': school_name,
            'Class Name': class_name,
            'Class Code': class_code,
            'Professor Name': professor_name,
            'Rating Data': rating_date,
            'Review Content': review_content
        })

    # Write the data to a CSV file
    filename = 'professor_reviews.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved successfully in '{filename}'")

else:
    print('Failed to retrieve the page.')
