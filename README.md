# Not my personal project (avoid being crawl)

## 📌 Introduction

The **Not my personal project** project is an automated tool designed to scrape data from Facebook using Selenium. This tool is capable of extracting posts, comments, images, and videos from specific Facebook pages.

## 🚀 Features

- Automated Facebook login using Selenium WebDriver.
- Stores and utilizes cookies to prevent repeated logins.
- Scrapes posts, comments, images, and videos from a given Facebook page.
- Supports data extraction from standard posts, videos, and reels.
- Saves data in a structured directory for easy access and organization.

## 🛠️ Installation

### 1. Install Required Dependencies

Ensure you install all necessary Python libraries before running the script:

```bash
pip install -r requirements.txt
```

### 2. Configure Selenium WebDriver

Download and set up the appropriate WebDriver for your browser. Place it in the project directory.

### 3. Store Facebook Cookies

Before running the crawler, store Facebook cookies by executing:

```bash
python save_cookies.py
```

## 🔍 Usage

Run `crawl.py` to initiate the data extraction process:

```bash
python crawl.py
```

Key parameters in `crawl.py`:

- `driver`: Path to the WebDriver.
- `cookies_path`: Path to the stored cookies file.
- `page_link`: URL of the Facebook page to scrape.
- `page_name`: Name of the folder where data will be stored.

## 📂 Directory Structure

```
Crawl-Facebook-Data/
│── configuration/        # Login configurations and data processing
│── crawl.py              # Main script for data extraction
│── save_cookies.py       # Script for storing cookies
│── requirements.txt      # Required dependencies
│── README.md             # Documentation file
```

## 🔄 Differences Between `crawl.py` and `crawl1.py`(the old one)

### 1. **Fetching Post Links**

- `crawl.py` retrieves post URLs, video URLs, and reel URLs separately.
- `crawl1.py` only retrieves post URLs.

### 2. **Processing Structure**

- `crawl.py` uses separate loops for posts, videos, and reels.
- `crawl1.py` processes all posts in a single loop, maintaining the original order from the Facebook page.

### 3. **Error Handling**

- `crawl.py` has enhanced exception handling for caption extraction, comments retrieval, and video downloads.
- `crawl1.py` has minimal error handling.

### 4. **Execution Order**

- `crawl.py` processes posts, videos, and reels separately, which may change the order of data extraction.
- `crawl1.py` maintains the order of posts as they appear on Facebook.

### 5. **Performance Optimization**

- `crawl.py` utilizes `os.makedirs(..., exist_ok=True)`, an optimized method for directory creation.
- `crawl1.py` manually checks and creates directories using `if not os.path.exists(folder)`, which is less efficient.

## ⚠️ Important Notes

- This project is intended solely for research and educational purposes.
- Ensure compliance with Facebook’s terms and policies when scraping data.

## 📧 Contact

For inquiries or issues, please reach out via GitHub Issues or email.

