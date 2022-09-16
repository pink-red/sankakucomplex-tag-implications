import json

import requests
from requests.exceptions import HTTPError, ConnectionError


def main():
    tags = []
    page = 1
    while True:
        url = f"https://capi-v2.sankakucomplex.com/tags?lang=en&page={page}"
        print(url)
        for i in range(10):
            try:
                r = requests.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"}
                )
                r.raise_for_status()
                break
            except HTTPError as e:
                print(e)
                if i < 9 and r.status_code in [500, 502, 503]:
                    continue
                else:
                    raise
            except ConnectionError as e:
                print(e)
                if i < 9:
                    continue
                else:
                    raise

        new_tags = r.json()
        if new_tags:
            print(len(new_tags))
            tags += new_tags
            page += 1
        else:
            break

    with open("tags.json", "w") as f:
        json.dump(tags, f)


if __name__ == "__main__":
    main()
