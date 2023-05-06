import cloudscraper, zipfile, questionary, io, sys, os, time
from guessit import guessit
from bs4 import BeautifulSoup
from questionary import Style


custom_style_fancy = Style([
    ('qmark', 'fg:lime'),       # token in front of the question
    ('answer', 'fg:#f44336'),      # submitted answer text behind the question
    ('pointer', 'fg:#f44336'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#f44336'), # pointed-at choice in select and checkbox prompts
])

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

        #now getting the page for Movie Subtitles in Arabic using scraper instead of requests
        scraper = cloudscraper.create_scraper()
        url = scraper.get('https://www.subscene.com/subtitles/'+legal_movie_name+"/arabic")
        #url = requests.get('https://www.subscene.com/subtitles/'+legal_movie_name+"/arabic")
        if url.status_code != 200:
            legal_movie_name = legal_movie_name +'-'+ str(movie_year)
            time.sleep(2)
            url = scraper.get('https://www.subscene.com/subtitles/'+legal_movie_name+"/arabic")

        url_soup = BeautifulSoup(url.content,'html.parser')

        #getting all the urls of arabic subtitles of the movie name
        urls = []
        for link in url_soup.select('.a1 a', href=True):
            urls.append(link['href'])
        uploaders = []
        for uploader in url_soup.select('.a5 a'):
            uploaders.append(uploader.text.strip())

        my_urls_uploaders = list(map(' by: '.join, zip(urls, uploaders)))
        mylist = list(dict.fromkeys(my_urls_uploaders))
        print(f'{len(mylist)} Subtitles found!')

        isEnough = False
        while isEnough== False:
            selected_subtitle = questionary.select(
                "Which Subtitle you want to download?",
                choices=mylist, style=custom_style_fancy).ask()
            # print(selected_subtitle.split(' ', 1)[0])
            #selecting first link from the list
            sub_link = 'https://www.subscene.com/'+ selected_subtitle.split(' ', 1)[0]
            sub_url = scraper.get(sub_link)
            sub_url_soup = BeautifulSoup(sub_url.content,'html.parser')

            #accessing the download button and getting download link.
            dl_btn = sub_url_soup.select('.download a')
            dl_link = dl_btn[0]['href']
            download_link = 'https://www.subscene.com'+dl_link

            #getting .srt files from the link using requests.
            r = scraper.get(download_link)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            # rename extracted file with movie filename
            zipinfos = z.infolist()
            for zipinfo in zipinfos:
                zipinfo.filename = filename_without_ext + '.srt'
                z.extract(zipinfo)

            #printing confirmation message.
            print("Subtitle downloaded successfully!")
            isEnough = questionary.confirm("Looks good and exit?").ask()


    #handling exception where subtitles are not found
    except IndexError:
        print("No File Found For:"+movie_name)


subtitles_downloader()