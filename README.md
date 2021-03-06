# ESJZone-novel-downloader

ESJ Zone is removing novels recently. Learn how to use the python packages, requests and BeatifulSoup and bakup up the novels!

## Example input in the console:
```
python ESJZone_downloader.py -url https://www.esjzone.cc/detail/1543764573.html -skip [2,4,6]                                                   
```

* Pass the url of the novel content page.
```
-url https://www.esjzone.cc/detail/1543764573.html 
```

* Some chapters might not be saved in the ESJZone page so you want to skip those. Use skip and pass a list of chapters that you want to skip.  The list should not have spaces included.
```
-skip [2,4,6]
```

## Here you go

![image](https://user-images.githubusercontent.com/18532018/129462653-d6612ebe-066a-471b-b89c-1a9d9f232604.png)

## Links to the docs of requests and BeatifulSoup
<a href="https://docs.python-requests.org/en/master/" target="_blank">requests</a>

<a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/" target="_blank">BeatifulSoup</a>
