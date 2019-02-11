import os
import urllib.request
import threading
import datetime
from queue import Queue


class DownloadThread(threading.Thread):


    def __init__(self, queue, destfolder):

        super(DownloadThread, self).__init__()
        self.queue = queue
        self.destfolder = destfolder
        self.daemon = True


    def run(self):

        while True:
            url = self.queue.get()
            try:
                self.download_url(url)
            except Exception as e:
                print("Error:", e)
            self.queue.task_done()


    def download_url(self, url):

        # set Name and Destination folder for file
        name = url.split('/')[-1]
        fullPath = os.path.join(self.destfolder, name)

        print("[%s] Downloading %s -> %s" % (self.ident, url, fullPath))

        urllib.request.urlretrieve(url, filename=fullPath)


def download(numthreads=8):

    queue = Queue()

    # Reading links for download and add them to queue
    with open("URLs.txt") as urls:
        url_list = urls.read().split()
    for url in url_list:
        queue.put(url)

    # Create folder
    now = datetime.datetime.now()
    destfolder = "videos-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(now.minute)

    if not os.path.exists(destfolder):
        os.makedirs(destfolder)
    else:
        print("Directory already exist")

    for i in range(numthreads):
        t = DownloadThread(queue, destfolder)
        t.start()

    queue.join()


if __name__ == "__main__":

    download()
