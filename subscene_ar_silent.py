import requests, zipfile, io, sys, os, time
from guessit import guessit
from bs4 import BeautifulSoup

# time.sleep(50)
def subtitles_downloader():

    try:
        # Get Movie Name For Subtitles
        filename = os.path.basename(str(sys.argv[1]))
        filename_without_ext = os.path.splitext(filename)[0]
        movie = guessit(filename)
        movie_name = movie.get('title')
        movie_year = movie.get('year')
        # movie_name = input("Enter Movie Name:")
        #replacing spaces with hyphen to get valid link
        legal_movie_name = movie_name.replace(" ","-")

        #now getting the page for Movie Subtitles in Arabic
        url = requests.get('https://www.subscene.com/subtitles/'+legal_movie_name+"/arabic")
        if url.status_code != 200:
            legal_movie_name = legal_movie_name +'-'+ str(movie_year)
            time.sleep(2)
            url = requests.get('https://www.subscene.com/subtitles/'+legal_movie_name+"/arabic")

        url_soup = BeautifulSoup(url.content,'html.parser')

        #getting all the urls of arabic subtitles of the movie name
        urls = []
        for link in url_soup.select('.a1 a', href=True):
            urls.append(link['href'])

        #selecting first link from the list
        sub_link = 'https://www.subscene.com/'+urls[0]
        sub_url = requests.get(sub_link)
        sub_url_soup = BeautifulSoup(sub_url.content,'html.parser')

        #accessing the download button and getting download link.
        dl_btn = sub_url_soup.select('.download a')
        dl_link = dl_btn[0]['href']
        download_link = 'https://www.subscene.com/'+dl_link

        #getting .srt files from the link using requests.
        r = requests.get(download_link)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        # z.extractall('ccc')
        zipinfos = z.infolist()
        for zipinfo in zipinfos:
            zipinfo.filename = filename_without_ext + '.srt'
            z.extract(zipinfo)

        #printing confirmation message.
        print("Subtitles Downloaded.Check The Folder where this python file is stored.")

    #handling exception where subtitles are not found
    except IndexError:
        print("No File Found For:"+movie_name)
        time.sleep(2)


subtitles_downloader()