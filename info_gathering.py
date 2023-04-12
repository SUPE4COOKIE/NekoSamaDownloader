import cloudscraper
import re
from concurrent.futures import ThreadPoolExecutor
scraper = cloudscraper.create_scraper()
pstream_list = []


def episode_listing_info(link) -> list:
    nekosama_page = scraper.get(link)
    episodes_string = re.findall("var episodes = ([^;]*);", nekosama_page.text)
    episodes_list_info = list(eval(episodes_string[0].replace('\\', "")))
    for episode in episodes_list_info:
        episode["url"] = "https://neko-sama.fr" + episode["url"]

    return episodes_list_info


def pstream_link_extractor(episode):
    video_page = scraper.get(episode)
    pstream_list.append(re.findall(
        r"(?<=https:\/\/www\.pstream.net\/e\/).*?(?=\')", video_page.text)[0])


def pstream_link_extractor_threads(episode, **episode_range):
    if type(episode) == list:
        if len(episode) >= 100:
            print(
                "* NOTE: For Large Number of episodes this might take a while (max 3min)")
        if len(episode_range) > 0:
            for i in range(episode_range["begin"] - 1, episode_range["end"]):
                pstream_link_extractor_threads(episode[i]["url"])
        else:
            for i in episode:
                pstream_link_extractor_threads(i["url"])
    else:
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(pstream_link_extractor, [episode])
            executor.shutdown(wait=True)
