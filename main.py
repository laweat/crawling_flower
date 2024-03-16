import os
import time
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import json
import logging

def image_download(driver, keyword, image_cnt):
    # 이미지 저장 경로
    logging.info(keyword + ' Download Start')
    save_dir = os.path.join(os.getcwd(), "flower_img", keyword)
    os.makedirs(save_dir, exist_ok=True)

    downlaod_cnt = 0
    while downlaod_cnt < image_cnt:
        time.sleep(3)
        # 페이지 맨 아래로 스크롤
        driver.find_element(By.XPATH, '//body').send_keys(Keys.END)
        logging.info('scroll down')

        time.sleep(3)
        try:
            # '더보기' 버튼이 보이면 클릭
            load_more_button = driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input')
            if load_more_button.is_displayed():
                load_more_button.click()
                time.sleep(3)
                logging.info('button click')
        except:
            pass
        
        time.sleep(3)
        try:
            # 이미지 없을시 break
            no_more_content = driver.find_element(By.XPATH, '//div[@class="K25wae"]//*[text()="더 이상 표시할 콘텐츠가 없습니다."]')
            if no_more_content.is_displayed():
                logging.info('content end')
                break
        except:
            pass

        # 이미지 정보 추출
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        image_info_list = soup.find_all('img', class_='rg_i')

        # 이미지 다운로드
        for i in range(len(image_info_list)):
            if downlaod_cnt >= image_cnt:
                break
            if 'src' in image_info_list[i].attrs:
                save_image = image_info_list[i]['src']
                image_filename = f"{keyword.replace(' ', '_')}_{downlaod_cnt}.jpg"
                image_path = os.path.join(save_dir, image_filename)
                urllib.request.urlretrieve(save_image, image_path)
                logging.info(f'{image_filename} image download')
                downlaod_cnt += 1
        logging.info(keyword + ' Download End')

def main():
    #info.json 읽기
    with open('info.json', 'r') as f:
        info = json.load(f)

    keywords = info["keyword"]
    image_cnt = info["image_cnt"]
    log_file = info["log_file"]

    # 로그 저장 경로
    log_file_path = os.path.join(os.getcwd(), log_file)

    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info('Task Start')

    driver = webdriver.Chrome()  # Chrome 웹 드라이버 실행
    URL = 'https://www.google.com/search?tbm=isch&q='

    for keyword in keywords:
        logging.info(keyword + ' Task Start')
        driver.get(URL + keyword)  # 검색어를 포함한 URL로 이동
        image_download(driver, keyword, image_cnt)
        logging.info(keyword + ' Task End')

    logging.info('Task End')
    driver.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.info(e)
