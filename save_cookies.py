# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# import pickle
# from time import sleep

# # Use the Service object to specify the path to chromedriver
# service = Service(executable_path=r"D:\Crawl_Facebook\Crawl-Facebook-Data\chromedriver.exe")
# # or, for automatic finding of the driver :
# # service = Service()

# # Pass the Service object to the webdriver
# browser = webdriver.Chrome(service=service)

# ### Log in to Facebook
# # Open facebook website
# browser.get('https://www.facebook.com/')

# # Stop the program in 5 seconds
# sleep(10)

# # Enter the login information
# user = browser.find_element(By.ID, "email")
# user.send_keys("backup.iphone915@gmail.com") # enter your email

# password = browser.find_element(By.ID, "pass")
# password.send_keys("kaggle2004") # enter your password

# # Login
# login_button = browser.find_element(By.NAME, "login")
# login_button.click()

# sleep(60)

# pickle.dump(browser.get_cookies(), open("my_cookies.pkl", "wb"))

# browser.close()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pickle
from time import sleep

# Cấu hình Chrome Profile
USER_PROFILE_PATH = r"D:\Crawl_Facebook\ChromeProfile"  # Đường dẫn tới thư mục profile

options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={USER_PROFILE_PATH}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

service = Service(executable_path=r"D:\Crawl_Facebook\Crawl-Facebook-Data\chromedriver.exe")
browser = webdriver.Chrome(service=service, options=options)

# Đăng nhập và lưu cookies
browser.get('https://www.facebook.com/')
sleep(15)  # Đủ thời gian đăng nhập thủ công

# Sau khi đăng nhập thành công, lưu cookies
pickle.dump(browser.get_cookies(), open("my_cookies.pkl", "wb"))
print("Cookies đã được lưu!")

# Giữ trình duyệt mở
input("Nhấn Enter để đóng trình duyệt...")
browser.quit()