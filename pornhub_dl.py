#!/usr/bin/env python
from lib_pornhub import *
import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, help = 'URL of Pornhub video')
    parser.add_argument('--playlist', choices = ['most-viewed', 'best', 'top-rated', 'longest'], type=str, help = 'Optional ordering of videos')
    parser.add_argument('--limit', type=int, help = 'Maximum number of videos', default=0)
    parser.add_argument('--dir', type=str, help = 'Output directory')
    args = parser.parse_args()

    ################################
    ascii_banner("PornHub-dl")
    print("                        Made by tnt2402\n\n\n########################################################")
    ################################
    ph_config_dl_dir(args.dir)
    if (args.url == None and args.playlist != None):
        print("URL cannot be empty !")
        sys.exit()
    elif (args.playlist != None):
        ph_get_playlist(args.url, args.playlist, args.limit)
    elif (args.url != None):
        ph_get_video(args.url)
    

if __name__ == '__main__':
    main()
