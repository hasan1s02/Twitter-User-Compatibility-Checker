import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from textblob import TextBlob
import pandas as pd
from googletrans import Translator
from deepface import DeepFace
import cv2
import re
import sqlite3
import chromedriver_autoinstaller
username = "selmo0"
password = "gggg"
#twitter bio varsa
istenilen_hesap = "zgggg"



driver = webdriver.Chrome()
driver.get("https://twitter.com/login")

wait = WebDriverWait(driver, 10)

# Kullanıcı adı ve şifreyi girin
username_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')))
username_field.send_keys(username)
username_field.send_keys(Keys.ENTER)
time.sleep(3)
password_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
password_field.send_keys(password)
time.sleep(3)
password_field.send_keys(Keys.ENTER)
time.sleep(3)
# profile git
driver.get(f"https://twitter.com/{istenilen_hesap}/")
time.sleep(5)


# Sayfada biraz aşağı inelim ki tweetler yüklensin
"""driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")"""
time.sleep(2)

# Tweet metinlerini çekelim
tweet_texts = driver.find_elements_by_xpath('//div[@dir="auto"]/span')


translator = Translator(service_urls=['translate.google.com'])
skip_tweet = False
for tweet in tweet_texts:
    if skip_tweet:
        skip_tweet = False
        continue

    print(tweet.text)
    a = tweet.text

    if '#' in a:
        # Hashtag içeren tweet, bir sonraki tweete geç
        skip_tweet = True
        continue

    # Çeviri işlemini gerçekleştir
    translation = translator.translate(a, dest="en")
    analiz_ing = translation.text
    sentiment_text = TextBlob(analiz_ing)
    print(analiz_ing)

time.sleep(2)
# Takip Edilen elementini bul
followers_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span')))

followers_count = followers_element.text
# Takipçi sayısını ekrana yazdır
print("takip edilen:", followers_count)

#takipçi sayınının elementini bul
takip_edilen = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span')))
time.sleep(2)
Takipp= takip_edilen.text
# Takipçi sayısını ekrana yazdır
print("takipci:", Takipp)

"""#twittera katılma tarihi
katılam_tarihi = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div/span[2]/span')))
time.sleep(2)
tarih= katılam_tarihi.text
"""
"""print("katılma tarihi:", tarih)"""


#beğenilen gönderilerde ki hashtagleri bulma
# Sayfayı aşağı kaydırma
driver.get(f"https://twitter.com/{istenilen_hesap}/likes")

time.sleep(15)
body = driver.find_element_by_css_selector('body')
all_hashtag = set()  # Boş bir küme oluştur

for _ in range(25):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)

    # Tweetleri bul
    tweets = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="tweetText"]')))

    for tweet in tweets:
        tweet_text = tweet.text
        hashtags = re.findall(r'\#\S+', tweet_text)
        for hashtag in hashtags:
            all_hashtag.add(hashtag)  # Hashtag'leri kümeye ekle

# Tüm hashtag'leri görüntüle
for hashtag in all_hashtag:
    print(hashtag)


hashtagler1 = ", ".join(all_hashtag)
#profil fotoğradını indirme
driver.get(f"https://twitter.com/{istenilen_hesap}/photo")
time.sleep(3)
profile_image = driver.find_element_by_class_name('css-9pa8cd')
time.sleep(2)
profile_image_url = profile_image.get_attribute('src')
time.sleep(2)
response = requests.get(profile_image_url)



with open(f'{username}.jpg','wb')as f:
    f.write(response.content)

img_path = f"{istenilen_hesap}.jpg"

img = cv2.imread(img_path)
"""
cv2.imshow("Resim", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
age = 25
dominant_emotion = "null"
try:
    resp = DeepFace.analyze(img_path, actions=['age', 'gender', 'emotion', 'race'])

    print(resp)

    # dominant_race
    print("aa")
    age = resp[0]['age']
    gender_results = resp[0]['gender']
    dominant_gender = max(gender_results, key=gender_results.get)

    emotion_results = resp[0]['emotion']
    dominant_emotion = max(emotion_results, key=emotion_results.get)

    race_results = resp[0]['race']
    dominant_race = max(race_results, key=race_results.get)

    print("age:", age)
    print("Dominant Cinsiyet:", dominant_gender)
    print("Dominant Duygu Durumu:", dominant_emotion)
    print("Dominant Irk:", dominant_race)
    print("bb")

except Exception as e:
    print("Hata alındı:", e)
    # İşlemi kapatın ve programın kaldığı yerden devam etmesini sağlayın
    pass
age2 = int(age)

if '.' in followers_count:
    followers_count = followers_count.replace('.', '')
followers_count2 = int(float(followers_count))
Takipp2 = int(Takipp)

print("sdfg")
# SQLite bağlantısı oluştur
connection = sqlite3.connect("twitter.db")
cursor = connection.cursor()

# Kullanıcı adının veritabanında olup olmadığını kontrol etmek için sorguyu hazırla
check_query = "SELECT COUNT(*) FROM kullanicilar WHERE kullanici_adi = ?"
cursor.execute(check_query, (istenilen_hesap,))
result = cursor.fetchone()

if result[0] > 0:
    #Kullanıcı adı zaten varsa, UPDATE işlemi yap
    update_query = "UPDATE kullanicilar SET takipci = ?, takip_edilen = ?, hashtagler = ?, yas = ?, duygu = ? WHERE kullanici_adi = ?"
    cursor.execute(update_query, (Takipp2, followers_count2, hashtagler1, age2, dominant_emotion, istenilen_hesap))
else:
    #Kullanıcı adı yoksa, INSERT işlemi yap
    insert_query = "INSERT INTO kullanicilar VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(insert_query, (istenilen_hesap, Takipp2, followers_count2, hashtagler1, age2, dominant_emotion))

# Veritabanı işlemlerini kaydet
connection.commit()
#driver.close()