import requests
from bs4 import BeautifulSoup


HOLOLIVE_TALENT_MAIN: str = "https://hololive.hololivepro.com/en/talents"


def main() -> None:
    r = requests.get(HOLOLIVE_TALENT_MAIN)
    print(r)

    soup = BeautifulSoup(r.content, "html.parser")
    talent_list = soup.find("ul", class_="talent_list clearfix")
    talent_list_item = talent_list.find_all("li")

    talent_link = []
    for t in talent_list_item:
        talent_link.append(t.find_all("a")[0].get("href"))

    print(talent_link)


def getInfo(url: str) -> None:
    pass


if __name__ == "__main__":
    main()