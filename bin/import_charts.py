#!/usr/bin/env python3
#
# Before running: pip install requests pillow tqdm
#

import argparse
import base64
import io

from PIL import Image
import requests
from tqdm import tqdm

chart_types = {
    'chart', 'box_plot', 'other_plot', 'dot_plot', 'linear_plot', 'pie_chart',
    'diagram', 'column_plot'
}

parser = argparse.ArgumentParser(description="Import charts")
parser.add_argument("--gathering-api",
                    "-G",
                    type=str,
                    required=True,
                    help="Address of Gathering API")
parser.add_argument("--compare-api",
                    "-C",
                    type=str,
                    required=True,
                    help="Address of Compare API",
                    default="http://localhost")
parser.add_argument("--gathering_user",
                    "-U",
                    type=str,
                    required=True,
                    help="Gathering username")
parser.add_argument("--gathering_password",
                    "-P",
                    type=str,
                    required=True,
                    help="Gathering password")
parser.add_argument("--compare-user",
                    "-u",
                    type=str,
                    required=True,
                    help="Compare username",
                    default="admin")
parser.add_argument("--compare-password",
                    "-p",
                    type=str,
                    required=True,
                    help="Compare password",
                    default="admin")


def gathering_login(host, username, password):
    res = requests.post(host + "/api/users/login",
                        data={
                            "username": username,
                            "password": password
                        })
    res = res.json()
    return res["token"]


def gathering_pages(host, token):
    next_url = host + "/api/publications/pages"
    results = list()

    while next_url:
        res = requests.get(next_url,
                           headers={
                               "Authorization": "Token " + token
                           }).json()
        next_url = res["next"]
        results.extend(res["results"])

    return results


def gathering_annos(host, token):
    next_url = host + "/api/publications/annotations"
    results = list()

    while next_url:
        res = requests.get(next_url,
                           headers={
                               "Authorization": "Token " + token
                           }).json()
        next_url = res["next"]
        results.extend(res["results"])

    return results


def compare_login(host, username, password):
    res = requests.post(host + "/api/v1/login/access-token", {
        "username": username,
        "password": password
    })
    res = res.json()
    return res["access_token"]


def compare_add_charts(host, token, charts):
    res = requests.post(host + "/api/v1/charts",
                        json=charts,
                        headers={
                            "Authorization": "Bearer " + token
                        }).json()
    print(res)


def main():
    args = parser.parse_args()
    gathering_token = gathering_login(args.gathering_api, args.gathering_user,
                                      args.gathering_password)
    compare_token = compare_login(args.compare_api, args.compare_user,
                                  args.compare_password)
    pages = gathering_pages(args.gathering_api, gathering_token)
    pages = {p['id']: p for p in pages}
    annos = gathering_annos(args.gathering_api, gathering_token)

    charts = list()

    for anno in tqdm(annos):
        try:
            data = anno["data"]
            if isinstance(data, list):
                data = data[0]

            if "type" not in data:
                continue
            type_ = data["type"]
            is_chart = False
            if isinstance(type_, list):
                is_chart = any([t in chart_types for t in type_])
            else:
                is_chart = type_ in chart_types

            if is_chart:
                if anno["page"] not in pages:
                    # print(f"Missing page: {anno['page']}")
                    continue
                page = pages[anno["page"]]

                image = requests.get(page["image"]).content
                image_io = io.BytesIO(image)

                img = Image.open(image_io)
                w, h = img.size

                x1 = data["x1"] * w
                x2 = data["x2"] * w
                y1 = data["y1"] * h
                y2 = data["y2"] * h
                cropped_img = img.crop((x1, y1, x2, y2))

                cropped_image_io = io.BytesIO()
                cropped_img.save(cropped_image_io, format=img.format)
                charts.append({
                    "type":
                    type_,
                    "file_name":
                    page["image"],
                    "file_contents":
                    base64.b64encode(cropped_image_io.getvalue()).decode(),
                    "mimetype": "image/jpeg"
                })

        except Exception as err:
            print(anno)
            raise err

    print(f"Found {len(charts)} charts")
    compare_add_charts(args.compare_api, compare_token, charts)


if __name__ == "__main__":
    main()
