from selenium import webdriver as web
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
import time ,asyncio
from  article_model import Article

URL = "http://e-pao.net/"

driver = web.Chrome(service= Service(ChromeDriverManager().install()))

async def extractDetail(link=None):
  try:
   if link is not None:
     await asyncio.sleep(1)
     print("Loading....")
     driver.get(link)
     xpath ='//*[@id="gen_panel"]'
     div = driver.find_element(By.XPATH,xpath)
     span =  div.find_element(By.XPATH,"./div[2]/p[1]/span[1]")
     p = div.find_element(By.XPATH,'./div[2]/p[@class="hlmheadlines"]') 
     return Article(heading=span.text,article=p.text)
   else:
     print('Link is none')
     return None
  except Exception as e:
   print("On detail extract "+str(e))
   return None

#Using Selenium (active)
async def sel():
  
 try:
   
   driver.get(URL)
   driver.implicitly_wait(10)
   xpath ='//div[@id="mayek_con"]'
   div = driver.find_element(By.XPATH,value=xpath)
   anchor_list =  div.find_elements(By.TAG_NAME,'a')
   links = [
     {
         "title":anchor.find_element(By.CLASS_NAME,"hlmheadline").text.strip(),
         "link":anchor.get_attribute("href").strip()
      }
   for anchor in anchor_list]
     
   for link in links:
     articleObj = await extractDetail(link=link.get("link"))
     print(f"Headline {articleObj.heading}")
     print(f"Body {articleObj.article}")

   driver.quit()

 except Exception as e:
  print(e)


#main call
if __name__ == "__main__": 
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sel())
    loop.close()
