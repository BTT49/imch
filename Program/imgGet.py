import urllib.request
from PIL import Image
import requests
from bs4 import BeautifulSoup



def download_image(url, user, folderName):
    temp = f'{folderName}/{user}.png'
    #Download image to the 'userIMG' folder
    urllib.request.urlretrieve(url, temp)
    print(f"Image downloaded and saved as {temp}")


def get_image_url(user, folderName):
    url = "https://github.com/" + user
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #find the avatar image of class 'avatar'
    image = soup.find('img', {'class': 'avatar'})
    if image:
        image_url = image['src']
        print("Avatar Image URL:", image_url)
        download_image(image_url, user, folderName)
        
