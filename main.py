from sys import argv
from info_gathering import *


def ask_resolution(resolutions) -> None:
    Value = input("resolution not found as arg/is invalid please select one from this list :\n" +
                  str(list(resolutions.keys())) + "\n")
    try:
        print(resolutions[Value])
    except:
        ask_resolution(resolutions)


if __name__ == "__main__":

    pstream_link_extractor_threads(episode_listing_info(
        "https://neko-sama.fr/anime/info/12-one-piece-vostfr"))
    print(pstream_list)

# https://neko-sama.fr/anime/info/17065-cyberpunk-edgerunners-vostfr
# https://neko-sama.fr/anime/episode/17065-cyberpunk-edgerunners-01-vostfr
