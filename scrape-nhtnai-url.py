import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import argparse

# Remove incompatible punctuation from the file name
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def test_200(url):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    }
    session.headers.update(headers)
    response = session.get(url)
    try:
        print(f"Status code for {url}: {response.status_code}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error for {url}: {e}")
        return None

def manipulate_url(original_url):
    base_domain = "nhentai.net"
    parsed_url = urlparse(original_url)
    path_parts = parsed_url.path.split('/')
    image_part = path_parts[-1]

    # First attempt: Replace "t" followed by a digit with "i" and remove the trailing "t"
    first_attempt = re.sub(r't(\d)', r'i\1', original_url).replace('t.jpg', '.jpg').replace('t.png', '.png')
    second_attempt = None

    # t stands for thumbnail - we  want to remove 't' from the URLs in order to get the full sized image
    if 't' in image_part:
        # Second attempt: Change domain, condense to /g/, and change image number format
        gallery_id = path_parts[-2]
        image_number = re.sub(r't(\d)', r'\1', image_part).split('.')[0]
        image_ext = os.path.splitext(image_part)[1]  # Get the file extension
        second_attempt = f"https://{base_domain}/g/{gallery_id}/{image_number}/"
    
    return first_attempt, second_attempt

def scrape_images(url, save_path):
    # Check the connection status
    status_code = test_200(url)
    if status_code != 200:
        print(f"Failed to scrape the website. HTTP Status Code: {status_code}")
        return

    # Fetch the content from the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title text
    title_tag = soup.find('h1', class_='title')
    if not title_tag:
        print('No title found with class "title"')
        return

    title_text = title_tag.text.strip()
    sanitized_title = sanitize_filename(title_text)

    # Create a new directory with the title text
    new_save_path = os.path.join(save_path, sanitized_title)
    if not os.path.exists(new_save_path):
        os.makedirs(new_save_path)

    # Find the div with id 'thumbnail-container'
    thumbnail_container = soup.find('div', id='thumbnail-container')
    if not thumbnail_container:
        print('No div found with id "thumbnail-container"')
        return

    # Find all image tags within the thumbnail container
    img_tags = thumbnail_container.find_all('img')

    # Extract image URLs and filter out those from static.nhentai.net
    img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
    img_urls = [
        img_url for img_url in img_urls 
        if 'static.nhentai.net' not in urlparse(img_url).netloc 
        and (img_url.endswith('.jpg') or img_url.endswith('.png'))
    ]

    # Download and save images
    for i, img_url in enumerate(img_urls):
        first_attempt, second_attempt = manipulate_url(img_url)

        try:
            img_response = requests.get(first_attempt)
            if img_response.status_code == 200:
                print(f"Downloading from: {first_attempt}")
                img_ext = os.path.splitext(first_attempt)[1]  # Get the file extension
                img_name = os.path.join(new_save_path, f'image_{i+1}{img_ext}')

                with open(img_name, 'wb') as img_file:
                    img_file.write(img_response.content)

                print(f'Successfully saved: {img_name}')
                continue
        except Exception as e:
            print(f'First attempt failed for {first_attempt}. Error: {e}')

        if second_attempt:
            print(f"Second attempt URL: {second_attempt}")
            try:
                img_response = requests.get(second_attempt)
                if img_response.status_code == 200:
                    img_ext = os.path.splitext(second_attempt)[1]  # Get the file extension
                    img_name = os.path.join(new_save_path, f'image_{i+1}{img_ext}')

                    with open(img_name, 'wb') as img_file:
                        img_file.write(img_response.content)

                    print(f'Successfully saved: {img_name}')
            except Exception as e:
                print(f'Second attempt failed for {second_attempt}. Error: {e}')

def main(urls, save_path):
    for url in urls:
        # Check the connection status for each URL
        status_code = test_200(url)
        if status_code == 200:
            scrape_images(url, save_path)
        else:
            print(f"Skipping URL due to failed connection test: {url}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape images from provided URLs")
    parser.add_argument('urls', nargs='+', help='List of URLs to scrape')
    parser.add_argument('--save-path', default=r'C:\Users\bayle\Desktop\savePath', help='Directory to save images')

    args = parser.parse_args()
    main(args.urls, args.save_path)