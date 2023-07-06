import requests
import csv
from bs4 import BeautifulSoup

# Candidate url #s
start_url = 10001
end_url = 15000

# Prepare an empty list to store the review data
reviews_data = []

# Loop through all possible URLs
for i in range(start_url, end_url):

  # URL of the webpage to crawl
  url = f'https://www.ratemyprofessors.com/professor/{i}'

  # Send a GET request to the URL
  response = requests.get(url)
  
  # Create a BeautifulSoup object from the response content
  soup = BeautifulSoup(response.content, "html.parser")

  # Try to crawl the page
  try:
    
    # Find the container for all class reviews
    reviews_container = soup.find(class_="RatingsList__RatingsUL-hn9one-0 cbdtns")
    
    # Find all class review tags within the container
    class_reviews = reviews_container.find_all(class_="Rating__RatingBody-sc-1rhvpxz-0 dGrvXb")
  
    
    # Loop through the class review tags
    for review in class_reviews:
        # Extract the required data from each review
        school_name = soup.find(class_='NameTitle__Title-dowf0z-1 iLYGwn').text.strip().split("at ",1)[1]
        print(school_name)
        class_code = review.find(class_='RatingHeader__StyledClass-sc-1dlkqw1-3 eXfReS').text.strip()
        print(class_code)
        professor_name = soup.find(class_='NameTitle__LastNameWrapper-dowf0z-2 glXOHH').text.strip()
        print(professor_name)
        rating_date = review.find(class_='TimeStamp__StyledTimeStamp-sc-9q2r30-0 bXQmMr RatingHeader__RatingTimeStamp-sc-1dlkqw1-4 iwwYJD').text.strip()
        print(rating_date)
        class_rating = review.find(class_="CardNumRating__CardNumRatingNumber-sc-17t4b9u-2").text.strip()
        print(class_rating)
        review_content = review.find(class_='Comments__StyledComments-dzzyvm-0 gRjWel').text.strip()
        print(review_content)
    
        if review.find(class_="CourseMeta__StyledCourseMeta-x344ms-0 fPJDHT").text.strip():
          would_take_again_div = review.find(class_="CourseMeta__StyledCourseMeta-x344ms-0 fPJDHT").text.strip()
          if "Would Take Again" in would_take_again_div:
            would_take_again = would_take_again_div[would_take_again_div.find("Would Take Again: ") + len("Would Take Again: "):would_take_again_div.find("Grade", would_take_again_div.find("Would Take Again: "))]
            print(would_take_again)
          else:
            would_take_again = ""
    
        if review.find(class_="CourseMeta__StyledCourseMeta-x344ms-0 fPJDHT").text.strip():
          attendance_div = review.find(class_="CourseMeta__StyledCourseMeta-x344ms-0 fPJDHT").text.strip()
          if "Attendance" in attendance_div:
            attendance = attendance_div[attendance_div.find("Attendance: ") + len("Attendance: "):attendance_div.find("Would Take Again", attendance_div.find("Attendance: "))]
            print(attendance)
          else:
            attendance = ""
    
        if review.find(class_="CourseMeta__StyledCourseMeta-x344ms-0 fPJDHT").text.strip():
          grade_div = review.find(class_="CourseMeta__StyledCourseMeta-x344ms-0 fPJDHT").text.strip()
          if "Grade" in grade_div:
            grade = grade_div[grade_div.find("Grade: ") + len("Grade: "):attendance_div.find("Textbook: ", grade_div.find("Grade: "))]
            print(grade)
          else:
            grade = ""
        
        # Append the review data as a dictionary to the list
        review_data = {
            "school_name": school_name,
            "class_code": class_code,
            "professor_name": professor_name,
            "rating_date": rating_date,
            "class_rating": class_rating,
            "review_content": review_content,
            "would_take_again": would_take_again,
            "attendance": attendance,
            "grade": grade
        }
        reviews_data.append(review_data)
    
  except:
      pass
    
# Save the reviews as a CSV file
filename = "class_reviews.csv"
fieldnames = ["school_name", "class_code", "professor_name", "rating_date", "class_rating", "review_content", "would_take_again", "attendance", "grade"]
with open(filename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(reviews_data)

print("Class reviews have been saved as", filename)
