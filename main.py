import easyocr
import PIL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--incognito')
driver = webdriver.Chrome(options=options)
PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

reader = easyocr.Reader(['ko','en']) # need to run only once to load model into memory
result = reader.readtext('te1.png')
recognized_text = ' '.join([text[1] for text in result])
print(recognized_text)

url = 'http://nara-speller.co.kr/speller/'
driver.get(url)

type = driver.find_element_by_xpath('//*[@id="text1"]').send_keys(recognized_text)
click = driver.find_element_by_xpath('//*[@id="btnCheck"]').click()
i = 0
while True:
    xpath = f"//*[@id='tdReplaceWord_{i}']/ul/li/a"
    try:
        # 요소가 존재할 때까지 기다린 후 클릭
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        element.click()
        i += 1
    except Exception as e:
        print('No more elements to click or an error occurred.')
        break
        
final = driver.find_element_by_xpath('//*[@id="tdCorrection1stBox"]')
text = final.text

if text == recognized_text:
    print('FAIL')
else:
    print('SUCCESS')
    print(text)