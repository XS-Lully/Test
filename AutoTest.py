from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import chromedriver_autoinstaller
import base64
import os


class Test:
    def __init__(self):
        chromedriver_autoinstaller.install(cwd=True)
        self.driver = None

    def test1(self):
        try:
            print("test1 start")
            self.driver = webdriver.Chrome()
            self.driver.get('https://www.cathaybk.com.tw/cathaybk/')
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            screenshot_path = "full_page_screenshot.png"
            screenshot_data = self.driver.execute_cdp_cmd("Page.captureScreenshot",
                                                          {"captureBeyondViewport": True, "fromSurface": True})
            with open(screenshot_path, "wb") as file:
                file.write(base64.b64decode(screenshot_data["data"]))
            print(f"完整頁面截圖已保存至 {screenshot_path}")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"test1 錯誤：{e}")
        finally:
            print("test1 end")

    def test2(self):
        try:
            print("test2 start")
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(("class name", "cubre-o-menu__btn"))
            )
            if len(elements) > 1:
                elements[1].click()  # 點擊產品介紹
            else:
                raise IndexError("找不到足夠的 cubre-o-menu__btn 元素")

            time.sleep(0.3)
            parent_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(("class name", "cubre-o-menuLinkList__item"))
            )
            child_elements = parent_elements[1].find_elements("class name", "cubre-o-menuLinkList__content")
            print("共有{}項目".format(len(child_elements[0].text.split('\n')) if child_elements else 0))
            screenshot_path = "screenshot_test2.png"
            self.driver.save_screenshot(screenshot_path)
        except (NoSuchElementException, TimeoutException, IndexError) as e:
            print(f"test2 錯誤：{e}")
        finally:
            print("test2 end")

    def test3(self):
        try:
            print("test3 start")
            card_intro = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(("xpath", "//*[text()='卡片介紹']"))
            )
            card_intro.click()

            stop_card = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(("xpath", "//*[text()='停發卡']"))
            )
            stop_card.click()
            self.driver.set_window_size(600, 900)

            parent_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(("class name", "cubre-o-block__wrap"))
            )
            child_elements = parent_elements[5].find_elements("class name", "swiper-pagination-bullet")

            successful_screenshots = 0
            for index, element in enumerate(child_elements):
                screenshot_path = f"test3_card{index + 1}.png"

                if index == 0:
                    time.sleep(0.5)
                    # 第一次迭代，僅截圖而不進行點擊
                    self.driver.save_screenshot(screenshot_path)
                else:
                    try:
                        # 從第二次迭代開始執行點擊和截圖
                        element.click()
                        time.sleep(0.5)
                        self.driver.save_screenshot(screenshot_path)
                        successful_screenshots += 1
                    except ElementClickInterceptedException:
                        print(f"無法點擊第 {index + 1} 張卡的分頁，跳過此項")
                        continue

            print(f"成功截取 {successful_screenshots + 1} 張卡片的截圖")  # 加上第一次的截圖
        except (NoSuchElementException, TimeoutException, IndexError) as e:
            print(f"test3 錯誤：{e}")
        finally:
            print("test3 end")

    def Main_(self):
        try:
            self.test1()
            self.test2()
            self.test3()
        finally:
            if self.driver:
                self.driver.quit()


if __name__ == '__main__':
    obj = Test()
    obj.Main_()
