import os
import urllib.request
import threading
import datetime
from queue import Queue


class DownloadThread(threading.Thread):
    def __init__(self, queue: Queue, destination_folder: str):

        super(DownloadThread, self).__init__()
        self.queue = queue
        self.destination_folder = destination_folder
        self.daemon = True

    def run(self):
        while True:
            url = self.queue.get()
            try:
                self.download_url(url)
            except Exception as e:
                print("Error:", e)

            self.queue.task_done()

    def download_url(self, url: str):
        # set Name and Destination folder for file
        name = url.split('/')[-1]
        full_path = os.path.join(self.destination_folder, name)

        # print("[%s] Downloading %s -> %s" % (self.ident, url, full_path))
        print("[{}] Downloading {} to ./{}/".format(self.ident, url, self.destination_folder))

        urllib.request.urlretrieve(url, filename=full_path)


def download(number_of_threads=8):
    queue = Queue()

    # Reading links for download and add them to queue
    with open("URLs.txt") as urls:
        url_list = urls.read().split()

    for url in url_list:
        queue.put(url)

    # Create folder
    now = datetime.datetime.utcnow()
    destination_folder = "videos-" + now.strftime('%m-%d-%H-%M')

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    else:
        print("Directory {} already exist".format(destination_folder))

    for i in range(number_of_threads):
        t = DownloadThread(queue, destination_folder)
        t.start()

    queue.join()


if __name__ == "__main__":
    download()
