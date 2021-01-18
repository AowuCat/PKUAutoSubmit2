import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from urllib.parse import quote
import warnings
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


def stu_io():
    driver.find_element_by_id('all').click()
    WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.ID, 'tag_s_stuCampusExEnReq')))
    driver.find_element_by_id('tag_s_stuCampusExEnReq').click()
    time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[-1])
    driver.set_window_size(1920, 1080)
    WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))

    # 先尝试出入校申请
    xpath = "//div[@class='el-card__body']/span[text()=' 出入校申请']"
    driver.find_element_by_xpath(xpath).click()
    WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'el-main')))
    try:
        xpath = "//label[text()='出入校起点']/..//input[@disabled='disabled']"
        driver.find_element_by_xpath(xpath)
    except:
        return

    # 如果无法填报，搜索备案历史
    print("出入校申请页无法填报，搜索备案历史...")
    driver.back()
    WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))
    xpath = "//div[@class='el-card__body']/span[text()=' 申请历史']"
    driver.find_element_by_xpath(xpath).click()
    WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'el-main')))
    time.sleep(0.5)

    date_str = (datetime.datetime.today() + datetime.timedelta(days = 1)).strftime("%Y%m%d")
    xpath = f"//div[text()={date_str}]"
    driver.find_element_by_xpath(xpath).click()
    WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.CLASS_NAME, 'el-main')))


def fill_blanks(str_list):
    # 出入校起点
    xpath = "//label[text()='出入校起点']/..//input"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    xpath = f"/html/body/div[@class='el-select-dropdown el-popper']//span[text()='{str_list[0]}']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    print(f"出入校起点: {str_list[0]}")

    # 出入校终点
    xpath = "//label[text()='出入校终点']/..//input"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    xpath = f"/html/body/div[@class='el-select-dropdown el-popper' and @x-placement='bottom-start']//span[text()='{str_list[1]}']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    print(f"出入校终点: {str_list[1]}")

    # 起点/终点校门
    if str_list[0] == '燕园':
        question1 = '起点'
        question2 = '终点'
    else:
        question1 = '终点'
        question2 = '起点'
    xpath = f"//label[text()='{question1}校门']/..//input"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    xpath = f"//span[text()='{str_list[2]}']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    print(f"{question1}校门: {str_list[2]}")

    # 出入校事由
    xpath = "//label[text()='出入校事由']/..//input"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    xpath = f"//span[text()='{str_list[3]}']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    print(f"出入校事由: {str_list[3]}")

    # 出入校具体事项
    xpath = "//label[text()='出入校具体事项']/..//textarea"
    element = driver.find_element_by_xpath(xpath)
    element.clear()
    element.send_keys(str_list[4])
    time.sleep(0.1)
    print(f"出入校具体事项: {str_list[4]}")

    # 起点/终点所在省
    xpath = f"//label[text()='{question2}所在省']/..//input"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    xpath = f"//span[text()='{str_list[5]}']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    print(f"{question2}所在省: {str_list[5]}")

    # 起点/终点所在地级市
    xpath = f"//label[text()='{question2}所在地级市']/..//input"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    xpath = f"//span[text()='{str_list[6]}']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    print(f"{question2}所在地级市: {str_list[6]}")

    # 起点/终点所在区县
    xpath = f"//label[text()='{question2}所在区县']/..//input"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    xpath = f"//span[text()='{str_list[7]}']"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    print(f"{question2}所在区县: {str_list[7]}")

    # 起点/终点所在街道
    xpath = f"//label[text()='{question2}所在街道']/..//input"
    element = driver.find_element_by_xpath(xpath)
    element.clear()
    element.send_keys(str_list[8])
    time.sleep(0.1)
    print(f"{question2}所在街道: {str_list[8]}")

    # 基本轨迹
    xpath = "//label[text()='基本轨迹']/..//textarea"
    element = driver.find_element_by_xpath(xpath)
    element.clear()
    element.send_keys(str_list[9])
    time.sleep(0.1)
    print(f"基本轨迹: {str_list[9]}")

    # 邮箱
    xpath = "//label[text()='邮箱']/..//input"
    element = driver.find_element_by_xpath(xpath)
    element.clear()
    element.send_keys(str_list[10])
    time.sleep(0.1)
    print(f"邮箱: {str_list[10]}")

    # 手机号
    xpath = "//label[text()='手机号']/..//input"
    element = driver.find_element_by_xpath(xpath)
    element.clear()
    element.send_keys(str_list[11])
    time.sleep(0.1)
    print(f"手机号: {str_list[11]}")

    # 园区
    xpath = "//label[text()='园区']/..//input"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    xpath = f"//span[text()='无宿舍']/../..//span[text()='{str_list[12]}']"
    driver.find_element_by_xpath(xpath).click()
    print(f"宿舍园区: {str_list[12]}")

    # 宿舍楼和宿舍房间号
    if str_list[12] != "无宿舍":
        xpath = "//label[text()='宿舍楼']/..//input"
        element = driver.find_element_by_xpath(xpath)
        element.clear()
        element.send_keys(str_list[13])
        print(f"宿舍楼: {str_list[13]}")
        xpath = "//label[text()='宿舍房间号']/..//input"
        element = driver.find_element_by_xpath(xpath)
        element.clear()
        element.send_keys(str_list[14])
        print(f"宿舍房间号: {str_list[14]}")

    # 打勾
    str0 = "本人承诺遵守疫情防控要求，出校不前往中高风险地区，入校前14日内未曾前往中高风险地区。确认本人北京健康宝当前状态“未见异常”。"
    try:
        xpath = "//label[@class='el-checkbox is-checked']"
        driver.find_element_by_xpath(xpath)
    except:
        xpath = f"//input[@value='{str0}']/../span"
        driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)
    print(str0)

    # 保存和提交
    xpath = "//span[text()='保存 ']"  # 这TM是保存[空格]！
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.5)
    xpath = "//span[contains(text(),' 暂不提交')]"
    driver.find_element_by_xpath(xpath).click()
    time.sleep(0.1)


if __name__ == "__main__":
    path = ""
    driver_path = path + "phantomjs.exe"
    driver = webdriver.PhantomJS(executable_path=driver_path)
    driver.set_window_size(1920, 1080)
    print("初始化完成")

    user_name = ""
    password = ""
    str_list = []

    setup_path = path + "setup.txt"
    f = open(setup_path, encoding="utf8")
    setup_str = f.read().split('\n')
    count = 0
    for i in setup_str:
        [tips, inner] = i.split(' ')
        if tips == '#':
            continue
        if count == 0:
            user_name = inner
        elif count == 1:
            password = inner
        else:
            str_list.append(inner)
        count += 1

    login(user_name, password)
    print("登录成功")
    stu_io()
    print("进入出入校填报界面")
    fill_blanks(str_list)
    print("现在可以提交了")
    quick_save()

    driver.quit()
