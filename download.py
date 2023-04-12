from http.server import executable
import re
import os
from requests import get
from base64 import b64decode
import aiohttp
import asyncio
import aiofiles

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Host": "www.pstream.net",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/69.0"
}


def pstream_m3u8(link) -> dict:
    """
    link : pstream link (www.pstream.net/e/<video ID>)
    output a dict containing different resolution as key and m3u8 links as value
    """
    page = get("https://www.pstream.net/e/" + link, headers=header)
    playerscript = "https://www.pstream.net/u/player-script" + re.findall(
        'https:\/\/www\.pstream\.net\/u\/player-script([^;]*)" ', page.text)[0]  # parse the page for the playerjs source
    playerscript = get(playerscript, headers=header)  # get the playerjs
    video_info = str(b64decode(re.findall(
        r'\)\)\}\(\"([^;]*)\"\)\,', playerscript.text)[0]))  # parse and decode a b64 string containing information about the video
    resolution_header = "https://www.pstream.net/m/" + \
        re.findall(r'm\\\\\/([^;]*)"', video_info)[
            0]  # parsing the link for the page containing different m3u8 link for different resolutions of the video
    resolution_header = get(resolution_header, headers=header)
    resolutions = {}
    for i in re.findall('(?<=NAME\=\").*?(?=\")', resolution_header.text):                 #
        resolutions[i] = "https://www.pstream.net/h/" + i + "/" + re.findall(              # get all the different resolution in the header , then create a key in the dict
            'https\:\/\/www\.pstream\.net\/h\/' + i + '\/(.*)', resolution_header.text)[0]  # to associate it to the right video as value

    return resolutions


def download_path_checker(anime_name, ep_number):

    Download_again = "Y"  # default value in case of a change in file name
    if os.path.exists("./Downloads") == False:
        os.mkdir("./Downloads")
    if os.path.exists("./Downloads/" + anime_name + "/" + anime_name + "_ep" + ep_number + ".mp4") == True:
        Download_again = input(
            "The episode has already been downloaded do you want to download it again ? Y|N : ")
        if Download_again == "N":
            return False
        elif Download_again != "Y" and Download_again != "N":
            download_path_checker(anime_name, ep_number)
    if os.path.exists("./Downloads/" + anime_name) == False:
        os.mkdir("./Downloads/" + anime_name)
        return True
    if Download_again == "Y":
        return True


async def ts_fetcher(session, url, part_number):
    async with session.get(url) as resp:
        f = await aiofiles.open("./Downloads/" + "hehehe/" + str(part_number) + ".ts", mode="wb")
        await f.write(await resp.read())
        await f.close()


async def ts_manager(ts_links):
    part_number = 0
    async with aiohttp.ClientSession() as session:
        tasks = []
        for link in ts_links:
            url = link
            tasks.append(asyncio.ensure_future(
                ts_fetcher(session, url, part_number)))
            await asyncio.gather(*tasks)
            part_number += 1


def ts_listing(m3u8_link):

    ts_list = []
    ts_header = get(m3u8_link["1080"], headers=header).text
    for line in ts_header.split("\n"):
        if len(line) >= 1:
            if line[0] != "#":
                ts_list.append(line)
    return ts_list


def ffmpeg_dl(m3u8_resolutions, resolution, episode_info):
    anime_name = episode_info["anime_name"]
    ep_number = episode_info["ep_number"]
    if download_path_checker(anime_name, ep_number) == True:
        path = "./Downloads/" + anime_name + "/"
        m3u8_downloader = get(m3u8_resolutions[resolution], headers=header)
        with open(path + anime_name + "_ep" + ep_number + ".m3u8", "w") as f:
            f.write(m3u8_downloader.text)
            f.close
        


# ffmpeg -protocol_whitelist file,https,tls,tcp -i movie.m3u8 -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 mooooe.mp4
#link = ts_listing(pstream_m3u8("3MBbZgoAByQP5qj"))
#ts_manager(uwu)
episode_info = {
    "anime_name": "uwu",
    "ep_number": "3"
}
ts_links = ts_listing(pstream_m3u8("3MBbZgoAByQP5qj"))
asyncio.run(ts_manager(ts_links))
