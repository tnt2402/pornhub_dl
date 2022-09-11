#!/usr/bin/env python
import youtube_dl
import requests as req
import sys
import os
from bs4 import BeautifulSoup
import ast
import string
import subprocess
import pyfiglet

#############
def ascii_banner(text):
    print('\n\n########################################################\n\n\n')
    ascii_banner = pyfiglet.figlet_format(text)
    print(ascii_banner) 
################################
### Configuration
ydl_opts_start = {
    'format': 'best',
    'nooverwrites': True,
    'no_warnings': True,
    'ignoreerrors': True,
}


ydl = youtube_dl.YoutubeDL(ydl_opts_start)

download_dir = os.getcwd() 

def ph_config_dl_dir(dir):
    global download_dir
    if (dir != None): 
        download_dir = dir
    print("Output directory: " + download_dir + "\model\\")
    if (os.path.exists(download_dir) != True):
        print('Invalid Directory !')
        sys.exit()
    download_dir = download_dir + "\model\\"
    if (os.path.exists(download_dir) != True):
        os.mkdir(download_dir)

### Main functions
def ph_check_valid_pornhub_url(url):
    if ('pornhub.com' not in url):
        print('Invalid Pornhub URL')
        sys.exit()
    if url.startswith('pornhub.com'):
        url = 'https://www.' + url
    return url    


def fix_title(s):
    decoded_unicode = ''.join([i if i in string.printable else ' ' for i in s])
    return decoded_unicode

def check_output_dir(model_name):
    global download_dir
    download_dir = download_dir 
    if (os.path.exists(download_dir + model_name) != True):
        os.mkdir(download_dir+model_name)

def ph_download_video(url, model_name):
    try: 
        check_output_dir(model_name)
        video = ydl.extract_info(url, download=False)
        filename = fix_title(str(video["title"])) + '.' + str(video['ext'])
        print('    [-] {}'.format(filename))
        filename = download_dir + '\\' + model_name + '\\' + filename
        url_video = video['url']
        res = subprocess.run(["downloadm3u8", "-o", filename, url_video])
    except:
        print('Cannot download video')
   
def ph_download_playlist(url, model_name, limit):
    check_output_dir(model_name)

    # tmp_playlist download
    print('... Getting playlist information...')
    playlist_download_command = ["youtube-dl", "-j", "--flat-playlist", "--no-check-certificate", url]
    res = subprocess.run(playlist_download_command, capture_output=True, text=True).stdout.split("\n")
    if (limit != 0 ):
        print("[!] Limit: {} videos".format(limit))
    count = 0
    for i in range(len(res) - 1):
        if (count == limit and limit != 0):
            break
            sys.exit()
        try:
            video_dict = ast.literal_eval(res[i])
            video = ydl.extract_info(str(video_dict["url"]), download=False)
            filename = fix_title(str(video["title"])) + '.' + str(video['ext'])
            print('\n\n\n\n#######################\n\n[-] Video #{}: {}\n\n'.format(count, filename))
            filename = download_dir + '\\' + model_name + '\\' + filename
            url_video = video['url']
            result = subprocess.run(["downloadm3u8", "-o", filename, url_video])
            count = count + 1
        except:
            print("Cannot download video")

def get_model_name(url):
    html = req.get(url).text
    soup = BeautifulSoup(html, 'lxml')

    if ("Page Not Found" in soup.title):
        print("Page not found!")
        sys.exit()

    user = soup.find(class_='userInfo')
    if (user != None):
        finder = user.find(class_='usernameBadgesWrapper')
        name = finder.find(class_='bolded').text.replace('\n', '').strip()
    else:
        user = soup.find(class_='topProfileHeader')
        finder = user.find(class_='nameSubscribe')
        name = finder.find(class_='name').text.replace('\n', '').strip()
    return name

def fix_url(url, type):
    url = ph_check_valid_pornhub_url(url)
    model_name = get_model_name(url)
    url = 'www.pornhub.com/model/' + model_name + '/videos'
    if (type == 'most-viewed'):
        url = url + '?o=mv'
    elif (type == 'top-rated'):
        url = url + '?o=tr'
    elif (type == 'longest'):
        url = url + '?o=lg'
    print("[+] Model: " + model_name)
    return (url, model_name)

def ph_get_video(url):
    url = ph_check_valid_pornhub_url(url)
    model_name = get_model_name(url)
    print("[+] Model: " + model_name)
    ph_download_video(url, model_name)

def ph_get_playlist(url, type, limit):
    url, model_name = fix_url(url, type)
    ph_download_playlist(url, model_name, limit)