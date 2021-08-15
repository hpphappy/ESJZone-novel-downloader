import sys
import os
import numpy as np
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from stat import S_IREAD

# Read URL from console
if '-url' in sys.argv:
    content_url = sys.argv[sys.argv.index('-url') + 1]

else:
    raise 'URL not found'
    
if '-skip' in sys.argv:
    skip_list_as_string = sys.argv[sys.argv.index('-skip') + 1]
    skip = list(map(int, skip_list_as_string.strip('[]').split(',')))
else:
    skip=np.array([])

# Deifne the function for downloads
def extract_html(url, save_folder, chapter_name):  
    """
    Given the url of a chapter, 
    the chapter will be saved to save_folder with the file name chapter_name.html
    """
    
    # send a request to the web server to get a response, r. 
    # r is the html soruce code of the webpage with the provide url
    r=requests.get(url)
    
    # set the encoding of r 
    r.encoding='utf-8'
    
    # decoding r into readable text by doing r.text
    # create a BeautifulSoup soup object to make r.text a nested data structure
    soup = BeautifulSoup(r.text, 'html.parser')
 
    # find the text in the first tag of 'h2'; the text is the title of the chapter
    title_h2 = soup.find_all("h2")[0].get_text()
    
    # find what's in the tag 'div' with the attribute, 'class': 'forum-content mt-3';
    # this is the text of the novel
    content = soup.find('div',attrs={'class': 'forum-content mt-3'})
    
    # create a file and write the chapter title and the text to the file
    with open(os.path.join(save_folder, f'{chapter_name}.html'), 'w', encoding="utf-8") as f:
        f.write(title_h2)
        f.write(content.__str__())
    
    # make the file read-only
    os.chmod(os.path.join(save_folder, f'{chapter_name}.html'), S_IREAD)
    

# create the BeautifulSoup object (same process as explained in extract_html function)
response = requests.get(content_url)
response.encoding='utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# find the novel name
novel_dict = soup.find('div', attrs={'class': 'product-gallery text-center mb-3'})
novel_name = novel_dict.find('img', alt=True)['alt']

# Check novel_name
print(novel_name)

# create a folder with the novel name if the folder isn't existed
save_folder = os.path.join("ESJZone", novel_name)
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
    
content = soup.find('div', attrs={'id': 'chapterList'})
urls = content.find_all('a')
chapters = content.find_all('p', attrs={'class': None})

hash_map = {}
for i_chapter, chapter in enumerate(tqdm(chapters)):
    # skip the list in some chapters
    if i_chapter in skip:
        continue    
        
    chapter_name = chapter.get_text()
    # check if there're illegal characters in the name of the chapter as a file name
    chapter_name = "".join(x for x in chapter_name if x.isalnum() or x in "._-")
    
    # check if the name of the chapter is used before, add a suffix to the name if the current chapter name is used before
    if chapter_name not in hash_map:
        hash_map[chapter_name] = 1
        
    else:
        hash_map[chapter_name] = hash_map[chapter_name] + 1
        chapter_name = chapter_name + f"-{hash_map[chapter_name]}"
    
    # call the function, extract_html, pass the url of each chapter, the folder that we want to save the novel and the chapter name iteratively
    url = urls[i_chapter].get('href')
    extract_html(url, save_folder, chapter_name)
