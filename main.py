import random

from selenium import webdriver
import time
import requests

class PingJiao :
    def __init__(self):
        #此处自定义对老师的评价
        self.text = ["老师的课对我帮助很大", "老师讲的很细心", "老师每次都认真回复我的提问，很温暖", "老师教的非常好", "老师是一个很有耐心的人"]
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
    def login(self,username,password) :
        #发送登录请求
        self.driver.get("http://172.16.16.4:7872/login")
        time.sleep(3)
        self.driver.find_element_by_id("input_username").send_keys(username)
        self.driver.find_element_by_id("input_password").send_keys(password)
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id=\"formContent\"]/form[1]/input[4]").click()
        #跳转评教页面
        self.driver.get("http://172.16.16.4:7872/student/teachingEvaluation/evaluation/index")


    def pj(self):#进行评教
        while True :
            time.sleep(3)
            pj_list = self.driver.find_elements_by_xpath("//div[@id=\"page_div\"]//button[@class=\"btn btn-xs btn-round btn-purple\"]")
            if len(pj_list) == 0 :
                print("评教完成")
                return
            else:
                print("评教剩余{}个".format(len(pj_list)))
            pj_list[0].click()
            tr = 3
            while tr < len(self.driver.find_elements_by_xpath("//tbody//tr"))-2:
                radios = self.driver.find_elements_by_xpath("//tbody/tr[{}]//span[@class='lbl']".format(tr))
                if random.randint(1, 100) < 95:#控制评优率
                    radios[0].click()
                else:
                    radios[1].click()
                time.sleep(random.randint(1,5))#随机评教延迟
                tr += 2
            #随机抽取评价并填写
            self.driver.find_element_by_xpath("//textarea").send_keys(self.text[random.randint(0, len(self.text) - 1)])
            #获取页面剩余等待时间
            M = self.driver.find_element_by_id("RemainM").text
            S = self.driver.find_element_by_id("RemainS").text
            time.sleep( int(M)*60+int(S)+3)
            #提交表单
            self.driver.find_element_by_id("buttonSubmit").click()
            time.sleep(3)



if __name__ == '__main__':
    username = input("输入账号：")
    password = input("输入密码：")
    pj =PingJiao()
    pj.login(username=username,password=password)
    pj.pj()




