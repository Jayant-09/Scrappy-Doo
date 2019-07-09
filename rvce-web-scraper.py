from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv
driver = webdriver.Chrome()
count = 0
rvb=["CV","BT","CS","EC","IM"]

for i in rvb:
    branch=i
    count=0
    fname=branch+"file.csv"
    with open(fname,"a",newline="") as f:
        thewriter=csv.writer(f)
        thewriter.writerow(["USN","Name","CGPA"])
        for i in range(60,200):
            driver.get("http://results.rvce.edu.in/")
            
            #if(i<100):
            i = '{0:03}'.format(i)  # to get 001, 002, 003 etc
            
            
            usn = '1RV16'+branch+str(i)
            usn_wait = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.NAME,"usn"))) #to handle ElementNotFoundException
            usn_box = driver.find_element_by_name("usn")
            usn_box.send_keys(usn) #enter usn in text field
            driver.implicitly_wait(10)
            
            capche_wait = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"""//*[@id="envelope"]/form/label[2]""")))
            capcha = driver.find_element_by_xpath("""//*[@id="envelope"]/form/label[2]""")
            expression = capcha.text
            values = [int(s) for s in expression.split() if s.isdigit()] #extract operands from expression
            answer = 0
            if '+' in expression:
                answer = values[0]+values[1]
            elif '-' in expression:
                answer = values[0]-values[1]
            elif '*' in expression:
                answer = values[0]*values[1] 
            elif '/' in expression:
                answer = int(values[0]/values[1])
            #print(answer)
            
            
            capche_val_wait = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.NAME,"captcha")))
            capcha_box = driver.find_element_by_name("captcha")
            capcha_box.send_keys(answer) #enter the capcha answer in the text field
            
            driver.find_element_by_xpath("""//*[@id="submit"]""").click()
            #sleep(10)
            try:
                
                sem=driver.find_element_by_xpath("""//*[@id="no-more-tables"]/table[1]/tbody/tr/td[4]""")
                semt=sem.text
                count=0
                if(str(semt)=="6"):
                    n=driver.find_element_by_xpath("""//*[@id="no-more-tables"]/table[1]/tbody/tr/td[3]/b""")
                    name=n.text
                    c=driver.find_element_by_xpath("""//*[@id="no-more-tables"]/table[1]/tbody/tr/td[5]/b""")
                    cgpa=c.text
                    thewriter.writerow([str(usn),str(name),str(cgpa)])
                    #f.write(usn+"   "+name+"    "+cgpa+"\n")
                    #print(usn,name,cgpa)
            except:
                count+=1
                print(count)
                if(count==5):
                    break
                print("",end="")
f.close()
        
    

    

