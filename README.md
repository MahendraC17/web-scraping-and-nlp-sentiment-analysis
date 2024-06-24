# Web Scraping of Amazon Product Reviews and Sentiment Analysis

## 1. Web Scraping
- Web scraping was performed using Selenium to extract Amazon product reviews. The script navigates through 10 pages of reviews using CSS selectors, fetching 100 reviews with ratings ranging from 1 to 5. The scraped data was exported to a CSV file named after the product.

Usage:
To use the web scraping script:

Replace '@@@@@' with your Amazon username.
Replace 'xxxxx' with your Amazon password.

## 2. Sentiment Analysis
Sentiment analysis was conducted using Natural Language Processing (NLP) techniques on the scraped reviews dataset. The following steps were implemented:

- `Data Preprocessing`: Tokenization, stop words removal, and lemmatization were applied to clean the reviews.
- `Exploratory Data Analysis (EDA)`: Distribution of ratings and a word cloud of most frequent words were analyzed.
- `Sentiment Labeling`: Reviews were categorized into positive, negative, and neutral based on their ratings.
- `Machine Learning Model`: TF-IDF vectorization and logistic regression were used to train a model to predict sentiment.

## 3. Summary Report
The sentiment analysis provided insights into the Amazon product's reception over the years 2022 to 2024. Key findings include:

- Positive Sentiment: The product was positively reviewed for aspects such as Price, indicating good value for money.
- Negative Sentiment: Battery was a common negative sentiment, suggesting issues with battery performance.
- Neutral Sentiment: Amazon related issues indicated concerns with service and delivery
- The product's quality remained the same. Asserting that the some of the products functions were still better in the 3 years time, while some negative sentiment prevailed signifying that product's improvement is necessary.


 
