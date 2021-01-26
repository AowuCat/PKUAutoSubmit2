import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from urllib.parse import quote
import warnings
import os
warnings.filterwarnings('ignore')


path = ""
driver = None


def quick_save(pic_name="test"):
    time.sleep(0.1)
    driver.save_screenshot(path + pic_name + ".png")


def login(user_name, password):
    iaaaUrl = 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp'
    appName = quote('北京大学校内信息门户新版')
    redirectUrl = 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'
    driver.get('https://portal.pku.edu.cn/portal2017/')

    for i in range(3):
        driver.get(f'{iaaaUrl}?appID=portal2017&appName={appName}&redirectUrl={redirectUrl}')
        driver.find_element_by_id('user_name').send_keys(user_name)
        time.sleep(0.1)
        driver.find_element_by_id('password').send_keys(password)
        time.sleep(0.1)
        driver.find_element_by_id('logon_button').click()
        try:
            WebDriverWait(driver, 3).until(ec.visibility_of_element_located((By.ID, 'all')))
            break
        except:
            print('Retrying...')
        if i == 2:
            raise Exception('门户登录失败')
    try:
        btn = driver.find_element_by_class_name("btn")
        btn.click()
    except:
        pass
    time.sleep(0.5)


def enter_Yun():
    driver.find_element_by_id('all').click()
    WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.ID, 'tag_s_epidemic')))
    driver.find_element_by_id('tag_s_epidemic').click()
    time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[-1])
    driver.set_window_size(1920, 1080)
    WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'el-main')))


def fill_blanks():
    state = "inside"
    try:
        xpath = "//label[text()='到校时间']"
        driver.find_element_by_xpath(xpath)
    except:
        state = "outside"
    if state == "inside":
        print("当前状态：已到校")
        xpath = "//label[text()='当日是否留宿宿舍']/..//span[text()='是']"
        driver.find_element_by_xpath(xpath).click()
        print("当日是否留宿宿舍：是")
        time.sleep(0.5)
        xpath = "//label[text()='是否出校（当日是否离开过学校）']/..//span[text()='否']"
        driver.find_element_by_xpath(xpath).click()
        print("是否出校（当日是否离开过学校）：否")
        time.sleep(0.5)
    else:
        print("当前状态：未到校")
        xpath = "//label[text()='是否当日返京']/..//span[text()='否']"
        driver.find_element_by_xpath(xpath).click()
        print("是否当日返京：否")
        time.sleep(0.5)

    xpath = "//span[contains(text(), '是否存在以下症状')]/../..//span[text()='否']"
    driver.find_element_by_xpath(xpath).click()
    print("是否存在以下症状：否")
    time.sleep(0.5)
    xpath = "//label[text()='疫情诊断']/..//input"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.5)
    xpath = "//span[text()='健康']"
    driver.find_element_by_xpath(xpath).click()
    print("疫情诊断：健康")
    time.sleep(0.5)

    try:
        xpath = "//span[contains(text(), '今日已填报')]"
        driver.find_element_by_xpath(xpath)
        print("【今日已填报，程序退出！】")
        return
    except:
        pass

    try:
        xpath = "//span[contains(text(), '今日填报已截止')]"
        driver.find_element_by_xpath(xpath)
        print("【今日填报已截止，程序退出！】")
        return
    except:
        pass

    xpath = "//span[contains(text(), '保存今日信息')]"
    driver.find_element_by_xpath(xpath).click()
    print("【填报完成！】")


if __name__ == "__main__":
    path = ""
    if os.name == "nt":
        driver_path = path + "phantomjs.exe"
    else:
        driver_path = path + "phantomjs"
    setup_path = path + "setup.txt"
    f = open(setup_path, encoding="utf8")
    setup_str = f.read().split('\n')

    print("---------------")
    for i in setup_str:
        [user_name, password] = i.split(' ')
        if user_name == '#':
            continue
        else:
            driver = webdriver.PhantomJS(executable_path=driver_path)
            driver.set_window_size(1920, 1080)
            print("初始化完成")
            login(user_name, password)
            print(f"{user_name} 登录成功")
            enter_Yun()
            print("进入云战役填报界面")
            fill_blanks()
            quick_save(user_name)
            driver.quit()
            print(f"{user_name} 任务结束！")
            print("---------------")
