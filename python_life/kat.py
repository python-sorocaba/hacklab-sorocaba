import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote


class KickAssTorrent(object):
    def __init__(self):
        self.base_url = "http://kickass.to/"
        self.search_url = "http://kickass.to/usearch/"


class Torrent(KickAssTorrent):
    def __init__(self, tv_show=None, uploader=None, episode=None,
                 quality="HDTV", category="tv"):
        super().__init__()
        if tv_show is not None:
            self.tv_show = tv_show
        else:
            self.tv_show = ''

        if uploader is not None:
            self.uploader = uploader
        else:
            self.uploader = ''

        if episode is not None:
            self.episode = episode
        else:
            self.episode = ''

        if category is None:
            category = "tv"

        if quality is None:
            quality = "HDTV"

        self.category = category
        self.quality = quality

    def __search_page_result(self, words=None, order_by_time=None,
                             order_by_seeders=None):
        url = quote(self.search_url + words, '/:%')
        url += quote(" category:" + self.category.lower(), '/:')

        if order_by_time is not None:
            if order_by_time == 1:
                url += quote('/?field=time_add&sorderW=asc', '/=&?')
            elif order_by_time == -1:
                url += quote('/?field=time_add&sorder=desc', '/=&?')
        if order_by_seeders is not None:
            if order_by_seeders == 1:
                url += quote('/?field=seeders&sorderW=asc', '/=&?')
            elif order_by_seeders == -1:
                url += quote('/?field=seeders&sorder=desc', '/=&?')

        print(url)
        data = requests.get(url)
        if data.status_code == 200:
            return data.content
        return None

    @property
    def torrent_links(self):
        words = quote(
            "{0} {1} {2} {3}".format(
                self.tv_show, self.episode, self.quality, self.uploader), '/')

        html_doc = self.__search_page_result(
            words=words, order_by_seeders=-1)

        torrents = []
        if html_doc is not None:
            soup = BeautifulSoup(html_doc)

            expression = r".*{0}.*".format(self.episode)
            pattern = re.compile(expression, re.IGNORECASE)

            for link in soup.find_all('a'):
                if (link.get('title') == "Download torrent file" and
                        pattern.match(link.get('href'))):
                    torrents.append(link.get('href'))
        return torrents

    def download_files(self, path="."):
        if path is None:
            path = "."

        torrents = self.torrent_links

        for torrent in torrents:
            name = torrent.split("=")[-1]
            fullpath = ("{0}/{1}.torrent").format(path, name)
            response = requests.get(torrent)
            if response.status_code != 200:
                continue
            with open(fullpath, 'wb') as fp:
                fp.write(response.content)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Download torrent files from KickAssTorrent')

    parser.add_argument('-t', metavar='TITLE', required=True,
                        dest='tv_show', action='store',
                        help='tv_show title')
    parser.add_argument('-u', metavar='NAME', required=False,
                        dest='uploader', action='store',
                        help='uploader name')
    parser.add_argument('-e', metavar='EPISODE', required=False,
                        dest='episode', action='store',
                        help='season and episode (format SXXEXX)')
    parser.add_argument('-q', metavar='QUALITY', required=False,
                        dest='quality', action='store',
                        help='quality of video')
    parser.add_argument('-c', metavar='CATEGORY', required=False,
                        dest='category', action='store',
                        help='category type of tv_show (movies, '
                             'tv, music, books, games, applications '
                             'and xxx)')
    parser.add_argument('-d', metavar='DESTINY_PATH', required=False,
                        dest='destpath', action='store',
                        help='destiny path of torrent files')
    parser.add_argument('--list', required=False,
                        dest='list', action='store_true',
                        help='list torrents')
    args = parser.parse_args()

    torrents = Torrent(
        tv_show=args.tv_show,
        uploader=args.uploader,
        episode=args.episode,
        quality=args.quality,
        category=args.category,
        )

    if args.list:
        for torrent in torrents.torrent_links:
            print(torrent)
    else:
        torrents.download_files(path=args.destpath)
