import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

user_links = []
size = 0
status = 0
user_data = []

def scroll_down(n):
    global user_links, size, status
    
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    driver.get(url='http://beta.layer3.xyz/leaderboard')
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH,"//span[text() = 'All-Time']").click()
    driver.implicitly_wait(10)
    user_href = "//h2[starts-with(text(),'Top users')]//following::a"
    
    while True:
        user_number = "//h2[starts-with(text(),'Top users')]//following::a[last()]/div/div/div[1]/div"
        user_xp = "//h2[starts-with(text(),'Top users')]//following::a[last()]/div/div/div[3]/div/p/span"
        
        user_links.extend([i.get_attribute("href") for i in driver.find_elements(By.XPATH,user_href)])
        length = driver.find_element(By.XPATH,user_number).text
        size = int(length)
        xp = driver.find_element(By.XPATH,user_xp).text
        
        if 'K' in xp:
            xp = int(xp[:-1])*1000
        else:
            xp = int(xp)
            
        if (n>0 and int(length) >= n) or xp == 5:
            status = 1
            driver.quit()
            break
        else:
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight);","")
            user_href = "//h2[starts-with(text(),'Top users')]//following::a[" + length + "]/div/div/div[1]/div//following::a"

def scrap_data(start,interval,n):
    global user_links,user_data,size,status
    
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    while True:
        try:
            _dict = {}
            _dict['user_rank'] = start+1
            _dict['user'] = user_links[start]
            
            driver.get(url=user_links[start])
            driver.implicitly_wait(10)
            
            info = driver.find_elements(By.XPATH,"//h2[starts-with(text(),'Achievements')]//preceding::a")[5:]
            for j in info:
                link = j.get_attribute("href")
                key = urllib.parse.urlparse(link).hostname
                _dict[key] = link
                
            user_data.append(_dict)
            
            start += interval
        except:
            pass
        
        if (status == 0 and start>=n) or (status == 1 and start>=size):
            driver.quit()            
            break