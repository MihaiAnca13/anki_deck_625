from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import numpy as np
import unidecode

N_IMAGES = 5

class ImageDownloader:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://google.co.uk/imghp")

        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[contains(text(),'Reject')]"))).click()

        c = self.driver.find_elements(By.XPATH, "//div[contains(text(),'Reject')]")[1]
        c.click()

    def get_images(self, search_word):
        elem = self.driver.find_element(By.XPATH, "//input[@title='Search']")
        elem.clear()
        elem.send_keys(search_word)
        elem.send_keys(Keys.RETURN)

        self.driver.implicitly_wait(2)
        images = self.driver.find_elements(By.CSS_SELECTOR, 'h3')

        base64_imgs = []
        for i, img in enumerate(images):
            if i > N_IMAGES:
                break
            h_img = img.find_element(By.XPATH, '..').find_element(By.CSS_SELECTOR, 'img')
            base64_img = h_img.get_attribute("src")
            base64_imgs.append(base64_img)

        img_idx = np.random.randint(low=0, high=N_IMAGES)
        base64_img = base64_imgs[img_idx]
        comma_idx = base64_img.find(',') + 1
        base64_img = base64_img[comma_idx:]
        unaccented_word = unidecode.unidecode(search_word)
        with open(f"images/{unaccented_word}.png", "wb") as fh:
            fh.write(base64.b64decode(base64_img))

    def __del__(self):
        self.driver.close()
