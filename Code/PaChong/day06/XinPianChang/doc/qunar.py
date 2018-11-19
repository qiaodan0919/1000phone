import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.qunar.com/')

dest = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="qunar-qcbox"]/input[@name="toCity"]')))[0]
dest.send_keys("深圳")
time.sleep(1)
dest.send_keys(Keys.RETURN)
button = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="js_flighttype_tab_domestic"]//button[@class="button-search"]')))[0]
button.click()

air_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="mb-10"]/div/div')))

for air in air_list:
    fdata = {}
    airlines = air.find_elements_by_xpath('.//div[@class="d-air"]')
    fdata['airlines'] = [airline.text.replace('\n', '-') for airline in airlines]
    fdata['depart'] = air.find_element_by_xpath('.//div[@class="sep-lf"]').text
    fdata['duration'] = air.find_element_by_xpath('.//div[@class="sep-ct"]').text
    fdata['dest'] = air.find_element_by_xpath('.//div[@class="sep-rt"]').text
    fake_price = list(air.find_element_by_xpath('.//span[@class="prc_wp"]/em/b[1]').text)
    b1 = list(air.find_element_by_xpath('.//em[@class="rel"]/b[1]').text)
    convers = air.find_elements_by_xpath('.//em[@class="rel"]/b[position()>1]')
    for conver in convers:
        index = int(conver.value_of_css_property('left')[:-2])//conver.size['width']
        b1[index] = conver.text
    fdata['price'] = ''.join(b1)
    print(fdata['pricel'])
    # origer_price = "".join(i for i in b1.find_elements_by_xpath('.//i/text()'))
    # print(origer_price)