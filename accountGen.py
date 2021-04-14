import requests
import random
import string
import json
import lxml
import bs4
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

class discordGen:
    def __init__(self, amount):
        #load wordlist used for random usernames
        with open("words_dictionary.json") as f:
            self.word_list = list(json.load(f).keys())
            f.close
        #initialize web-driver and requests
        options = webdriver.FirefoxOptions()
        options.set_headless()#comment this for debug
        path = GeckoDriverManager().install()

        #loop untill all accounts generated
        for i in range(amount):
            #capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
            self.driver = webdriver.Firefox(executable_path=path, firefox_options=options)

            email,password,token = self.createAccount(*self.randomCredentials())
            self.driver.close()
            if email:#if it worked
                print(f"Account generated:\nEmail: {email}\nPassword: {password}\nToken: {token}\n")
                with open("tokens.txt","a+") as f:#open file to store generated accounts
                    f.write(f"{email},{password},{token}\n")
            else:
                print("No account created")
            print("waiting to create next account")

            time.sleep(2*60)

    def randomCredentials(self):
        #generate username
        username = []
        for i in range(2):
            username.append(random.choice(self.word_list))
        username.append(random.randint(10,999))
        username = ''.join([str(c) for c in username])
        #generate email
        email = username + random.choice(
            ['@gmail.com']*5 + #These multipliers decide the probability
            ['@yahoo.com']*2 + 
            ['@outlook.com']*2 + 
            ['@aol.com']*1
        )
        #generate password
        characters = string.ascii_letters + string.digits
        password = []
        for i in range(10):#10 character password
            password.append(random.choice(characters))
        password =  ''.join([str(c) for c in password])
        return email, username, password

    def createAccount(self, email, username, password):
        months = [
            "January","Feburary","March","April","May","June","July",
            "August","September","October","November","December"
        ]
        #The input fields for registration. These are subject to change.
        tos_input = "/html/body/div/div[2]/div/div[2]/div/form/div/div[2]/div[5]/label/input"
        try:
            self.driver.get('https://discord.com/register')
            self.driver.find_element_by_name("email").send_keys(email)
            self.driver.find_element_by_name("username").send_keys(username)
            self.driver.find_element_by_name("password").send_keys(password)
            self.driver.find_element_by_id("react-select-2-input").send_keys(random.choice(months))
            self.driver.find_element_by_id("react-select-3-input").send_keys(random.randint(1,28))#screw people born on the 29th-31st
            self.driver.find_element_by_id("react-select-4-input").send_keys(random.randint(1980,2001))#random age over 18y/o
            try:
                driver.find_element_by_xpath(tos_input).click()
            except:
                pass
            time.sleep(15)#wait a bit of time to not be detected as a bot.
            self.driver.find_element_by_css_selector(".button-3k0cO7").click()

            #wait for it to redirect
            redirect = EC.url_contains("https://discord.com/channels/@me")
            WebDriverWait(self.driver, timeout=45).until(redirect)#make sure it doesnt just wait forever

            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                'Host': 'discord.com',
                'Accept': '*/*',
                'Accept-Language': 'en-US',
                'Content-Type': 'application/json',
                'Referer': 'https://discord.com/register',
                'Origin': 'https://discord.com',
                'DNT': '1',
                'Connection': 'keep-alive'
            }
            login = {'email':email,'password':password}
            res = requests.post('https://discord.com/api/v8/auth/login', headers=headers, json=login).json()
            token = res['token']#this will raise an exception if account creation failed
            
            time.sleep(5)
            link = 'https://discord.com/invite/r4PSgztA'
            self.driver.get(link)
            time.sleep(3)
            self.driver.find_element_by_css_selector(".marginTop40-i-78cZ").click()

        except TimeoutException:
            print("Captcha detected.")
            return False, False, False
#        except Exception as error:
#            print("Failed to generate account:")
#            print(error)
#            return False, False, False
        
        return email, password, token

discordGen(100)
