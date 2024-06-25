import requests
import re
import concurrent.futures as cf
from bs4 import BeautifulSoup


HOLOLIVE_TALENT_MAIN: str = "https://hololive.hololivepro.com/en/talents"


def main() -> None:
    r = requests.get(HOLOLIVE_TALENT_MAIN)

    soup = BeautifulSoup(r.content, "html.parser")
    talent_list = soup.find("ul", class_="talent_list clearfix")
    talent_list_item = talent_list.find_all("li")

    talent_link = [link.find("a").get("href") for link in talent_list_item]

    talent_info = []
    with cf.ThreadPoolExecutor(max_workers=64) as executor:
        futures = [executor.submit(getInfo, url, talent_link.index(url)) for url in talent_link]

        for future in cf.as_completed(futures):
            try:
                talent_info.append(future.result())
            except Exception as e:
                print("%r: ERROR -> %s", (future, e))

    print(talent_info)


def getInfo(url: str, url_index: int) -> dict:
    result: dict = {"Index": url_index}

    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")
    talent_article = soup.find("article", class_="in_talent single")

    talent_name = talent_article.find("div", class_="talent_top").find("h1")

    # For some reason, the simple talent_name.get_text(strip=True) returns both the English and Japanese names concatenated
    # r"^[A-Za-z\s]+&" did not work either
    talent_name_en = [re.sub(r"^Alum ", "", char) for char in talent_name.get_text(strip=True) if "A" <= char <= "Z" or "a" <= char <= "z" or char == " "]
    result["English Name"] = "".join(talent_name_en)
    result["Japanese Name"] = talent_name.find("span").get_text(strip=True)

    external_links_list = talent_article.find("ul", class_="t_sns clearfix")
    external_links_list_item = [link.find("a").get("href") for link in external_links_list.find_all("li")]

    result["Youtube"] = external_links_list_item[0].split('?', 1)[0]
    result["Twitter/X"] = external_links_list_item[1]

    talent_data_box = talent_article.find("div", class_="talent_data").find("div", class_="table_box")
    talent_data_list = talent_data_box.find_all("dl")
    
    for dl in talent_data_list:
        dt = dl.find("dt").get_text(strip=True)
        dd = dl.find("dd").get_text(strip=True)
        result[dt] = dd

        if dl.find("a") is not None:
            link = dl.find("a").get("href")
            result[dt + " Link"] = link

    return result


if __name__ == "__main__":
    main()