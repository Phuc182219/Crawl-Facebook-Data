from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from time import sleep
import os
import requests
from selenium.webdriver.common.keys import Keys
import keyboard
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


def show_all_comments(driver):
    '''Change Most relevant to All comments to show all comments'''

    # Click on the Most relevant button
    view_more_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Most relevant')]")))
    view_more_btn.click()
    # Click on the All comment button
    all_comments = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'All comments')]")))
    all_comments.click()
    # Scroll to the bottom, ensure all comments are loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    return None

def click_see_more(driver):
    '''Click see more to show all captions'''

    # Click on the See more button
    see_more_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'See more')]")))
    see_more_btn.click()
    return None

def click_see_less(driver):
    '''Click see less to hide captions'''

    # Click on the See more button
    see_more_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'See less')]")))
    see_more_btn.click()
    return None

def click_view_more_comments(driver):

    view_more_cmts_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'View more comments')]")))
    view_more_cmts_btn.click()
    return None

def click_see_all(driver):
    '''Click See all button to show comments'''

    see_all_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'See all')]")))
    see_all_btn.click()
    return None

#def get_comments(driver):
    '''Get comments under a post
    Return:  - list of comments.
    '''
    comments_list = []
    last_comment_count = 0

    try:
        # Wait for comments section to be present
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1n2onr6')]"))
        )

        while True:
            # Find all comment elements with extended timeout
            comments = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'x1n2onr6 x1ye3gou x1iorvi4 x78zum5 x1q0g3np x1a2a7pz') or contains(@class, 'x1n2onr6 xurb0ha x1iorvi4 x78zum5 x1q0g3np x1a2a7pz')]"))
            )

            # Scroll to the last comment to trigger loading more
            if len(comments) > 0:
                driver.execute_script("arguments[0].scrollIntoView(true);", comments[-1])
                sleep(2)  # Allow time for new comments to load
            
            # Check if new comments have been loaded
            if len(comments) == last_comment_count:
                break  # No more comments loading

            last_comment_count = len(comments)

        try:
            # Find and click all "See more" buttons
            see_more_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "x11i0hfl"))
            )

            # Iterate and click on each button
            for button in see_more_buttons:
                try:
                    ActionChains(driver).move_to_element(button).perform()
                    button.click()
                    sleep(1)
                except Exception:
                    continue

        except:
            pass

        # Extract comment text
        for comment in comments:
            try:
                # Check if comment contains text
                text_ele = comment.find_element(By.XPATH, ".//div[contains(@class, 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs')]")
                if text_ele and text_ele.text:
                    comments_list.append(text_ele.text)
            except Exception:
                continue

    except Exception as e:
        print(f"Error extracting comments: {e}")

    return comments_list
def get_comments(driver):
    '''Get comments under a post or Reel
    Return: list of comments.
    '''
    comments_list = []
    last_comment_count = 0

    # Extremely comprehensive list of comment container selectors
    comment_selectors = [
        "//div[contains(@class, 'x1n2onr6')]",
        "//div[contains(@class, 'x1n2onr6 x1ye3gou x1iorvi4 x78zum5 x1q0g3np x1a2a7pz')]",
        "//div[contains(@class, 'x1n2onr6 xurb0ha x1iorvi4 x78zum5 x1q0g3np x1a2a7pz')]",
        "//div[contains(@class, 'x78zum5 x1q0g3np')]",  # Reels comment container
        "//div[contains(@class, 'x1ey2m1c x1xmf6yo')]",  # Alternative Reels comment container
        "//div[contains(@class, 'x193iq5w x1nxh6w3')]",  # Another possible comment container
        "//div[contains(@class, 'x1i64zmx')]"  # Additional fallback selector
    ]

    # Comprehensive text selectors
    text_selectors = [
        ".//div[contains(@class, 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs')]",
        ".//div[contains(@class, 'x193iq5w')]",
        ".//span[contains(@class, 'x193iq5w')]",
        ".//div[contains(@class, 'x1lliihq x1q0g3np')]",
        ".//div[contains(@class, 'x78zum5 x1q0g3np')]"
    ]

    try:
        # Attempt to wait for any comments section
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1n2onr6')]"))
        )

        # Comprehensive comment collection attempt
        comments = []
        for selector in comment_selectors:
            try:
                current_comments = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, selector))
                )
                comments.extend(current_comments)
                if comments:
                    break  # Stop if we find any comments
            except:
                continue

        # Extract comment text using multiple selectors
        for comment in comments:
            for text_selector in text_selectors:
                try:
                    text_ele = comment.find_element(By.XPATH, text_selector)
                    if text_ele and text_ele.text and text_ele.text not in comments_list:
                        comments_list.append(text_ele.text)
                        break  # Stop searching if text found
                except:
                    continue

        # Attempt to expand truncated comments
        try:
            see_more_buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'x11i0hfl') and contains(text(), 'See more')]")
            for button in see_more_buttons:
                try:
                    ActionChains(driver).move_to_element(button).perform()
                    button.click()
                    sleep(1)
                except:
                    continue
        except:
            pass

    except Exception as e:
        print(f"Comprehensive comment extraction error: {e}")
        # Log additional debugging information
        try:
            page_source = driver.page_source
            print(f"Page source length: {len(page_source)}")
            # Optional: save page source for debugging
            with open('debug_page_source.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
        except:
            pass

    return comments_list


def get_captions(driver):
    """
    Crawls Facebook posts and extracts their captions.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        A list of the post's captions.
    """
    captions = []
    caption_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a') or contains(@class, 'x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a')]")
    for caption_element in caption_elements:
        caption = caption_element.text
        captions.append(caption)

    return captions


def get_emojis(driver):
    """
    Crawls a Facebook post's caption, extracting each line and any following emojis.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        A list of all emojis of the Facebook post's caption
    """
    # Find the caption element
    caption_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a') or contains(@class, 'x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a')]")

    # Get all lines and emojis, handling <br> tags for line breaks
    lines_and_emojis = []

    for caption_element in caption_elements:
            # Handle image-based emojis
            try:
                img_elements = caption_element.find_elements(By.XPATH, ".//img")  # Find <img> tags within the element
                if img_elements:
                    for img in img_elements:
                        alt_text = img.get_attribute("alt")
                        if alt_text:
                            lines_and_emojis.append(alt_text)

            except NoSuchElementException:
                pass

    return lines_and_emojis


def get_captions_emojis(driver):
    """
    Extracts text and emojis from Facebook post captions.
    """
    caption_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a') or contains(@class, 'x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a')]")

    captions = []
    for caption_element in caption_elements:
        try:
            soup = BeautifulSoup(caption_element.get_attribute("outerHTML"), 'html.parser')
            for div in soup.find_all('div', dir="auto"):
                result = []
                for child in div.descendants:
                    if child.name == 'img' and 'alt' in child.attrs:
                        result.append(child['alt'])  # Extract emoji from 'alt' attribute
                    elif child.name is None:  # This is text
                        text = child.strip()
                        if text:
                            result.append(text)
            
                captions.append(' '.join(result))
        except AttributeError as e:
            print(f"Error processing caption: {e}")

    return captions

def get_captions_spe(driver):
    """
    Extracts text and emojis from Facebook post captions, including reels.
    """
    captions = []

    # Try getting caption from regular posts
    try:
        caption_title = driver.find_element(By.XPATH, "//div[contains(@class, 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs')]")
        try:
            soup = BeautifulSoup(caption_title.get_attribute("outerHTML"), 'html.parser')
            for div in soup.find_all('div', dir="auto"):
                result = []
                for child in div.descendants:
                    if child.name == 'img' and 'alt' in child.attrs:
                        result.append(child['alt'])  # Extract emoji from 'alt' attribute
                    elif child.name is None:  # This is text
                        text = child.strip()
                        if text:
                            result.append(text)
            
                captions.append(' '.join(result))
        except AttributeError as e:
            print(f"Error processing regular caption: {e}")
    except:
        pass

    # Try getting caption from both regular posts and reels
    caption_selectors = [
        "//div[contains(@class, 'x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s')]",  # Regular posts
        "//div[contains(@class, 'x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1ms8i2q xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj')]",  # Reels specific
        "//div[contains(@class, 'x78zum5 xdt5ytf x1n2onr6')]//div[contains(@class, 'x1lliihq')]",  # Another reels caption class
        "//div[contains(@class, 'x78zum5')]//span[contains(@class, 'x193iq5w')]"  # Additional reels caption location
    ]

    for selector in caption_selectors:
        caption_elements = driver.find_elements(By.XPATH, selector)
        for caption_element in caption_elements:
            try:
                soup = BeautifulSoup(caption_element.get_attribute("outerHTML"), 'html.parser')
                for div in soup.find_all(['div', 'span'], dir="auto"):
                    result = []
                    for child in div.descendants:
                        if child.name == 'img' and 'alt' in child.attrs:
                            result.append(child['alt'])  # Extract emoji from 'alt' attribute
                        elif child.name is None:  # This is text
                            text = child.strip()
                            if text:
                                result.append(text)
                
                    caption_text = ' '.join(result)
                    if caption_text and caption_text not in captions:  # Avoid duplicates
                        captions.append(caption_text)
            except AttributeError as e:
                print(f"Error processing caption: {e}")
            except Exception as e:
                print(f"Unexpected error processing caption: {e}")

    return captions

def get_captions_and_hashtags(driver):
    """
    Extracts captions and hashtags separately from Facebook posts and reels.
    Returns both the full caption and a list of hashtags.
    """
    captions = get_captions_spe(driver)
    hashtags = []
    
    # Extract hashtags from captions
    for caption in captions:
        # Find all hashtags using regex
        found_hashtags = re.findall(r'#\w+', caption)
        hashtags.extend(found_hashtags)
    
    return captions, list(set(hashtags))

def get_image_urls(driver):
    """
    Crawls a Facebook post and extracts image URLs.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        A list of image URLs found in the post.
    """

    # Find image elements
    image_elements = driver.find_elements(By.XPATH, ".//div[contains(@class, 'x10l6tqk x13vifvy')]/img")
    image_urls = []
    for img in image_elements:
        image_urls.append(img.get_attribute('src'))

    return image_urls

def download_images(image_urls, download_dir="images"):
    """
    Downloads images from a list of URLs.

    Args:
        image_urls: A list of image URLs.
        download_dir: The directory to save the images to.
    """
    if not image_urls:
        print("No image URLs provided.")
        return

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes

            with open(os.path.join(download_dir, f"image_{i+1}.jpg"), "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            # print(f"Downloaded image {i+1} from {url}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading image from {url}: {e}")

# def get_video_urls(driver):
#     video_urls = []
    
#     try:
#         # Try clicking video button if exists
#         try:
#             button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.CLASS_NAME, "inline-video-icon"))
#             )
#             button.click()
#         except:
#             pass
        
#         # Regular videos
#         video_elements = driver.find_elements(By.XPATH, ".//div[contains(@class, 'inline-video-container')]/video")
#         for video in video_elements:
#             src = video.get_attribute("src")
#             if src:
#                 video_urls.append(src)
                
#         # Reels videos - thêm selector mới cho Reels
#         reels_selectors = [
#             ".//div[contains(@class, 'x78zum5')]//video",  # Reels video container
#             ".//div[contains(@class, 'x1ey2m1c')]//video",  # Another possible Reels container
#             ".//video[contains(@class, 'xh8yej3')]"  # Direct video element in Reels
#         ]
        
#         for selector in reels_selectors:
#             reels_elements = driver.find_elements(By.XPATH, selector)
#             for reel in reels_elements:
#                 src = reel.get_attribute("src")
#                 if src and src not in video_urls:  # Avoid duplicates
#                     video_urls.append(src)

#     except Exception as e:
#         print(f"Error getting video URLs: {e}")
    
#     return video_urls


def get_video_urls(driver):
    """
    Extracts video URLs from both desktop and mobile Facebook interfaces.
    Handles regular videos and reels with multiple fallback approaches.
    """
    video_urls = []
    
    def extract_from_selectors(selectors):
        """Helper function to extract URLs from a list of selectors"""
        for selector in selectors:
            try:
                video_elements = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, selector))
                )
                for video in video_elements:
                    src = video.get_attribute("src")
                    if src and src not in video_urls:
                        video_urls.append(src)
            except (TimeoutException, Exception):
                continue

    try:
        # First attempt: Try standard video elements
        standard_selectors = [
            # Desktop selectors
            ".//div[contains(@class, 'inline-video-container')]/video",
            ".//div[contains(@class, '_53mw')]//video",
            ".//div[contains(@class, 'x1lliihq')]//video",
            # Mobile selectors
            ".//div[contains(@class, 'story_body_container')]//video",
            ".//div[contains(@class, '_5rgt')]//video",
            # Reels selectors
            ".//div[contains(@class, 'x78zum5')]//video",
            ".//div[contains(@class, 'x1ey2m1c')]//video",
            ".//video[contains(@class, 'xh8yej3')]"
        ]
        extract_from_selectors(standard_selectors)

        # Second attempt: Try source elements
        if not video_urls:
            source_selectors = [
                ".//video//source",
                ".//div[contains(@class, '_53mw')]//video//source",
                ".//div[contains(@class, 'story_body_container')]//video//source"
            ]
            for selector in source_selectors:
                try:
                    source_elements = driver.find_elements(By.XPATH, selector)
                    for source in source_elements:
                        src = source.get_attribute("src")
                        if src and src not in video_urls:
                            video_urls.append(src)
                except Exception:
                    continue

        # Third attempt: Try data attributes
        if not video_urls:
            data_selectors = [
                "//*[@data-video-url]",
                "//*[@data-video-source]",
                "//div[contains(@class, '_53mw')]//*[@data-url]"
            ]
            for selector in data_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        for attr in ["data-video-url", "data-video-source", "data-url"]:
                            url = element.get_attribute(attr)
                            if url and url not in video_urls:
                                video_urls.append(url)
                except Exception:
                    continue

        # Fourth attempt: Check iframes
        try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                try:
                    driver.switch_to.frame(iframe)
                    video = driver.find_element(By.TAG_NAME, "video")
                    src = video.get_attribute("src")
                    if src and src not in video_urls:
                        video_urls.append(src)
                    driver.switch_to.default_content()
                except Exception:
                    driver.switch_to.default_content()
                    continue
        except Exception:
            pass

        # Final attempt: Check video player containers
        if not video_urls:
            player_selectors = [
                "//div[contains(@class, '_1o0y')]",  # Mobile video player
                "//div[contains(@class, 'x1lliihq')]",  # General video container
                "//div[contains(@class, '_53mw')]"  # Another mobile video container
            ]
            for selector in player_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        video_elements = element.find_elements(
                            By.XPATH, ".//*[contains(@href, 'video') or contains(@src, 'video')]"
                        )
                        for video_element in video_elements:
                            for attr in ["href", "src"]:
                                url = video_element.get_attribute(attr)
                                if url and url not in video_urls:
                                    video_urls.append(url)
                except Exception:
                    continue

    except Exception as e:
        print(f"Error in video URL extraction: {e}")
        try:
            with open('debug_video_page.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
        except Exception as debug_error:
            print(f"Could not save debug info: {debug_error}")

    return video_urls

def download_videos(video_urls, download_dir="videos", include_reels=True):
    """
    Downloads videos from a list of URLs.
    
    Args:
        video_urls: A list of video URLs
        download_dir: The directory to save the videos to
        include_reels: Whether to include Reels videos (default: True)
    """
    if not video_urls:
        print("No video URLs provided.")
        return

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for i, url in enumerate(video_urls):
        try:
            # Skip non-Reels videos if include_reels is False
            if not include_reels and ('/reel/' in url or '/reels/' in url):
                continue
                
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # Determine if it's a Reel or regular video
            is_reel = '/reel/' in url or '/reels/' in url
            prefix = 'reel' if is_reel else 'video'
            
            with open(os.path.join(download_dir, f"{prefix}_{i+1}.mp4"), "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading video from {url}: {e}")

def get_post_links(driver, fanpage_url):
    post_urls = set()  # Use set to avoid duplicates
    video_urls = set()
    reels_urls = set()  # New set for reels
    
    stop_scrolling = False
    
    try:
        driver.get(fanpage_url)
        sleep(3)
        
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        while not stop_scrolling:
            # Collect current visible posts
            def collect_current_posts():
                # Regular posts
                for link in driver.find_elements(By.CSS_SELECTOR, "a[href*='/posts/']"):
                    url = link.get_attribute("href")
                    if url:
                        post_id = extract_facebook_post_id(url)
                        if post_id:
                            post_urls.add(url)
                
                # Videos and regular video posts
                for link in driver.find_elements(By.CSS_SELECTOR, "a[href*='/videos/'], a[href*='/watch/']"):
                    url = link.get_attribute("href")
                    if url:
                        post_id = extract_facebook_post_id(url)
                        if post_id:
                            video_urls.add(url)
                
                # Reels - thêm các selector cho Reels
                reels_selectors = [
                    "a[href*='/reel/']",
                    "a[href*='/reels/']",
                    "a[href*='/watch/']"  # Một số Reels có thể xuất hiện dưới dạng watch
                ]
                
                for selector in reels_selectors:
                    for link in driver.find_elements(By.CSS_SELECTOR, selector):
                        url = link.get_attribute("href")
                        if url and ('/reel/' in url.lower() or '/reels/' in url.lower()):
                            reels_urls.add(url)
                            
                print(f"Current collected: {len(post_urls)} posts, {len(video_urls)} videos, {len(reels_urls)} reels")
            
            # Collect posts before scrolling
            collect_current_posts()
            
            # Check for stop key press with WebDriverWait
            try:
                stop_key = WebDriverWait(driver, 1).until(
                    lambda d: keyboard.is_pressed("enter")
                )
                if stop_key:
                    stop_scrolling = True
                    print("Stopping the scrolling.")
                    break
            except:
                pass
                
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

            # Wait for new content to load with dynamic wait
            try:
                WebDriverWait(driver, 30).until(
                    lambda driver: driver.execute_script("return document.documentElement.scrollHeight") > last_height
                )
                sleep(10)  # Short additional wait for content to stabilize
            except TimeoutException:
                # If no new height after timeout, we've probably reached the bottom
                collect_current_posts()  # Collect one final time
                print("Reached the bottom or no new content loaded")
                break
                
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                # Double check if we're really at the bottom
                collect_current_posts()
                print("No new content loaded")
                break
                
            last_height = new_height
            
        # Convert sets to lists before returning
        post_urls_list = list(post_urls)
        video_urls_list = list(video_urls)
        reels_urls_list = list(reels_urls)
        
        print(f"Total collected: {len(post_urls_list)} posts, {len(video_urls_list)} videos, {len(reels_urls_list)} reels")
        return post_urls_list, video_urls_list, reels_urls_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return list(post_urls), list(video_urls), list(reels_urls)  # Return what we managed to collect  # Return what we managed to collect

def save_text(text_list, file_path):
    """
    Saves a list of strings to a text file, with each string on a new line.

    Args:
        text_list (list): A list of strings to save.
        file_path (str): The file path where the text will be saved.

    Returns:
        None
    """
    # Save each string in the list to a new line in the file
    with open(file_path, "w", encoding="utf-8") as file:
        for item in text_list:
            file.write(item + "\n")  # Add a newline after each string

    # print(f"Strings saved to {file_path}")

def extract_facebook_post_id(url):
    """
    Extracts the post ID from a Facebook post URL including Reels.

    Args:
        url: The Facebook post URL.

    Returns:
        The post ID, or None if no ID could be found.
    """
    # Pattern for posts, videos, and reels
    match = re.search(r"(?:posts/|videos/|pfbid|reel/|reels/)([\w\d]+)", url)
    if match:
        return match.group(1)
    return None

def remove_duplicate_links(links):
    """
    Remove links with duplicate IDs and keep only one for each unique ID.
    """
    unique_links = {}
    for link in links:
        post_id = extract_facebook_post_id(link)
        if post_id and post_id not in unique_links:
            unique_links[post_id] = link
    return list(unique_links.values())