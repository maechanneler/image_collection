import requests
import configparser
from PIL import Image
from io import BytesIO

if __name__=='__main__':
    # Read the configurations
    config = configparser.ConfigParser()
    config.read('Config.ini')

    # Push the configurations
    headers = {"Ocp-Apim-Subscription-Key" : config['keys']['key1']}

    # Search the images
    results = []
    for i in range(int(config['params']['itr'])):
        params  = {"q": config['search']['term'], "count": config['params']['count'], "offset": i*int(config['params']['offset'])}
        response = requests.get(config['search']['url'], headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"]]
        print(len(thumbnail_urls))
        results.extend(thumbnail_urls)

    # Save the results to the directries
    for i in range(len(results)):
        image_data = requests.get(results[i])
        image_data.raise_for_status()
        image = Image.open(BytesIO(image_data.content)) 
        filename = config['dir']['name']+"/"+config['file']['name']+str(i+1)+".jpg"
        image.save(filename)
