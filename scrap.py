from inspect import ismemberdescriptor
import os
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By



count=1

driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe') 

driver.get('https://fincaraiz.com.co/apartamentos/arriendos/cali?pagina=40') 
for i in range (39):  
    apts= driver.find_elements(By.XPATH,'//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-lg-4 MuiGrid-grid-xl-4"]')


    for apt in apts:

        try:

            price = apt.find_element(By.XPATH,'.//section[@class="MuiGrid-root MuiGrid-container"]/div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12"]/span/b').text 
            print(price)
            
            room = apt.find_element(By.XPATH,'.//section[@class="MuiGrid-root MuiGrid-container"]/div[2]/span[3]').text 

            link = apt.find_element(By.XPATH,'.//article/a[@href]')

            

            arooms= room.split('h')[0]
            aprices = price.split('$')[-1]
            aaprices = aprices.replace('.', "")
            aaaprices= int(aaprices)/ int(arooms)

            oprices= round(aaaprices)

            demo= str(link.get_attribute("href"))
            ids= demo.split('/')[-1]
            print(ids)
            
            link = apt.find_element(By.XPATH,'.//article/a[@href]')
            url= link.get_attribute("href")
            

            driver.execute_script("window.open('');") 
            driver.switch_to.window(driver.window_handles[1]) 
            driver.get(url)



            img= driver.find_element(By.XPATH, './/*[@id="location"]/div/div[1]/div/img')
                        
            imglink= img.get_attribute("src")
            print(imglink)

            coord= imglink.split('/')[-2]
            print(coord)

            
            long= coord.split('x')[-2]
            print(long)

            lat= coord.split('x')[-1]
            print(lat)

            driver.close() 
            driver.switch_to.window(driver.window_handles[0])
            
            with open(f'Informacion_apartamentitos.csv', 'a', encoding='utf-8') as f:
                f.write(link.get_attribute("href")+","+ str(ids)+ "," + str(aaprices)+ ","+ str(arooms)+ ","+ str(long)+ ","+ str(lat))
                f.write('\n')
                count = count +1

            
            

            

        except:
            driver.switch_to.window(driver.window_handles[0]) 
            
            continue

        



    try:
        boton = driver.find_element(By.XPATH, '//button[@class="MuiButtonBase-root MuiPaginationItem-root MuiPaginationItem-page MuiPaginationItem-outlined MuiPaginationItem-rounded"]')
        boton.click()
        sleep(random.uniform(10.0, 15.0))
    except:
        break


"""driver.switch_to.window(driver.window_handles[0]) 
            apt.close(driver.window_handles[1])"""