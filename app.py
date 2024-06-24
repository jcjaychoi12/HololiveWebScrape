import requests
from bs4 import BeautifulSoup


HOLOLIVE_TALENT_MAIN: str = "https://hololive.hololivepro.com/en/talents"


def main() -> None:
    r = requests.get(HOLOLIVE_TALENT_MAIN)
    print(r)

    soup = BeautifulSoup(r.content, "html.parser")
    talent_list = soup.find("ul", class_="talent_list clearfix")
    talent_list_item = talent_list.find_all("li")

    talent_link = [link.find("a").get("href") for link in talent_list_item]
    print(talent_link)

    print(getInfo(talent_link[0]))


def getInfo(url: str) -> dict:
    result: dict = {}

    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")
    talent_article = soup.find("article", class_="in_talent single")

    external_links_list = talent_article.find("ul", class_="t_sns clearfix")
    external_links_list_item = [link.find("a").get("href") for link in external_links_list.find_all("li")]

    result["Youtube"] = external_links_list_item[0].split('?', 1)[0]
    result["Twitter/X"] = external_links_list_item[1]

    return result


if __name__ == "__main__":
    main()