from nytscraper import Website, returnArticles
import jsons
from typing import List
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", type=str)
    parser.add_argument("--parseType", default='web', choices=['web', 'local'])
    parser.add_argument("--articleAmount", default=100, type=int)
    args = parser.parse_args()

    keyword = args.keyword
    parseType = args.parseType
    num = args.articleAmount
    fname = f"{keyword}.json"
    fpath = os.path.join(os.getcwd(), fname)

    if parseType == 'web':
        websites = returnArticles(num=num, keyword=keyword)
        if websites is not None:
            if os.path.isfile(fpath):
                os.remove(fpath)
            with open(fname, 'w') as file:
                file.write(jsons.dumps(websites))
                file.close()
        else:
            print("Error accessing website! Please check keyword/URL validity!")

    elif parseType == 'local':
        try:
            with open(fname, 'r') as file:
                websites = jsons.load(file.read(), List[Website])
                file.close()
        except FileNotFoundError:
            print(f"No local cache exists for {keyword}! Run script with parseType set to web first!")