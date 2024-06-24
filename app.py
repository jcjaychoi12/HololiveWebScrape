import requests
from bs4 import BeautifulSoup


HOLOLIVE_TALENT_MAIN: str = "https://hololive.hololivepro.com/en/talents"


def main() -> None:
    r = requests.get(HOLOLIVE_TALENT_MAIN)

    soup = BeautifulSoup(r.content, "html.parser")
    talent_list = soup.find("ul", class_="talent_list clearfix")
    talent_list_item = talent_list.find_all("li")

    talent_link = [link.find("a").get("href") for link in talent_list_item]

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

    talent_data_box = talent_article.find("div", class_="talent_data").find("div", class_="table_box")
    talent_data_list = talent_data_box.find_all("dl")
    
    for dl in talent_data_list:
        dt = dl.find("dt").text
        dd = dl.find("dd").text
        result[dt] = dd

    return result


if __name__ == "__main__":
    main()