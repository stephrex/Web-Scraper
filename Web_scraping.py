import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def download_images_from_google(query, save_folder, num_images=100):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.google.com/imghp")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)

    # Scroll to load more images
    for _ in range(num_images // 20):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    # Extract image URLs
    image_elements = driver.find_elements(
        By.XPATH, "//img[@class='rg_i Q4LuWd']")
    image_urls = [element.get_attribute("src") for element in image_elements]

    # Create directory if not exists
    os.makedirs(save_folder, exist_ok=True)

    # Download images
    for i, url in enumerate(image_urls[:num_images]):
        try:
            response = requests.get(url)
            with open(os.path.join(save_folder, f"{query}_{i}.jpg"), "wb") as f:
                f.write(response.content)
            print(f"Downloaded image {i+1}/{num_images}")
        except Exception as e:
            print(f"Failed to download image {i+1}: {e}")

    driver.quit()


if __name__ == "__main__":
    query = "cocoa crop plant"
    save_folder = "C:/Users/User/Documents/datasets for ML/Plants_Dataset/Cocoa"
    download_images_from_google(query, save_folder, num_images=100)


# import os
# import requests
# from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# options = webdriver.ChromeOptions()
# options.add_argument('--headless-new')

# # Initialize the WebDriver instance
# driver = webdriver.Chrome(service=Service(
#     ChromeDriverManager().install()), options=options)

# # Navigate to the desired webpage
# driver.get('https://www.google.com/search?q=CocoaCrop&tbm=isch')

# # Wait for the image elements to be present on the page
# image_elements = WebDriverWait(driver, 100).until(
#     EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rg_i.Q4LuWd")))
# print(image_elements)
# # Create a directory to save the images
# os.makedirs("images", exist_ok=True)

# # Iterate through the image elements
# for index, image_element in enumerate(image_elements):
#     # Extract the URL of the image
#     src = image_element.get_attribute("src")
#     # Download the image
#     response = requests.get(src)
#     # Save the image to a file
#     with open(f"images/image_{index}.jpg", "wb") as f:
#         f.write(response.content)

# # Close the WebDriver instance
# driver.quit()


# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # # from selenium.webdriver.chrome.options import Options
# # from webdriver_manager.chrome import ChromeDriverManager
# # from selenium.webdriver.common.by import By
# # import os
# # import time
# # import requests

# # # service = Service()
# # options = webdriver.ChromeOptions()
# # options.add_argument('--headless-new')


# # def scrape_google_images(query, num_images):
# #     driver = webdriver.Chrome(service=Service(
# #         ChromeDriverManager().install()), options=options)
# #     driver.get(f'https://www.google.com/search?q={query}&tbm=isch')

# #     for _ in range(3):
# #         driver.execute_script(
# #             'window.scrollTo(0, document.body.scrollHeight);')
# #         time.sleep(2)

# #     image_elements = driver.find_element(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
# #     image_urls = [element.get_attribute(
# #         'src') for element in image_elements if element.get_attribute('src')]

# #     driver.quit()
# #     return image_urls[:num_images]


# # def download_images(image_urls, save_folder):
# #     os.makedirs(save_folder, exist_ok=True)
# #     for i, image_url in enumerate(image_urls):
# #         image_path = os.path.join(save_folder, f'image_{i+1}.jpg')
# #         with open(image_path, 'wb') as f:
# #             response = requests.get(image_url)
# #             f.write(response.content)

# #         print(f'Downloaded: {image_path}')


# # if __name__ == '__main__':
# #     query = 'cocoa crop plant'
# #     num_images = 300

# #     image_urls = scrape_google_images(query, num_images)
# #     download_images(image_urls, 'Cocoa')

# # # from google_images_download import google_images_download


# # # def scrape_google_images(query, num_images):
# # #     response = google_images_download.googleimagesdownload()
# # #     arguments = {"keywords": query, "limit": num_images, "print_urls": True}
# # #     paths = response.download(arguments)
# # #     return paths[0][query]


# # # # Example usage
# # # query = "Cocoa Crop Plant"
# # # num_images = 300
# # # image_paths = scrape_google_images(query, num_images)
# # # print(image_paths)
