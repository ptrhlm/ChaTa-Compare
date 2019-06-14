#!/usr/bin/env python3
#
# Before running: pip install requests pillow tqdm
#

import argparse
import base64
import io
from itertools import islice, chain
import json

from PIL import Image
import requests
from tqdm import tqdm

chart_types = {
    'box_plot',
    'chart',
    'column_plot',
    'diagram',
    'dot_plot',
    'linear_plot',
    'other_plot',
    'pie_chart',
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
parser.add_argument("--batch-size",
                    "-b",
                    type=int,
                    required=False,
                    help="Batch size",
                    default=10)


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

    while next_url:
        res = requests.get(next_url,
                           headers={
                               "Authorization": "Token " + token
                           }).json()
        next_url = res["next"]
        yield from res["results"]


def gathering_pubs(host, token):
    next_url = host + "/api/publications/"

    while next_url:
        res = requests.get(next_url,
                           headers={
                               "Authorization": "Token " + token
                           }).json()
        next_url = res["next"]
        yield from res["results"]


def gathering_annos(host, token):
    next_url = host + "/api/publications/annotations"

    while next_url:
        res = requests.get(next_url,
                           headers={
                               "Authorization": "Token " + token
                           }).json()
        next_url = res["next"]
        yield from res["results"]


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
                        })
    try:
        return res.json()
    except json.JSONDecodeError as e:
        print(res, res.text)
        raise e


def batch(iterable, size: int):
    if size < 1:
        raise ValueError("")

    sourceiter = iter(iterable)
    while True:
        try:
            batchiter = islice(sourceiter, size)
            yield chain([next(batchiter)], batchiter)
        except StopIteration:
            break


def filter_annos(annos, pages, pubs):
    for anno in annos:
        try:
            if not (anno['annotation_status'] == '2:annotated'
                    or anno['annotation_status'] == '3:super_annotated'):
                continue

            if anno["page"] not in pages:
                continue
            page = pages[anno["page"]]

            if page["publication"] in pubs:
                pub = pubs[page["publication"]]
                if "name" in pub:
                    description = pub["name"]
                else:
                    description = ""
            else:
                description = ""

            data = anno["data"]
            if not isinstance(data, list):
                data = [data]
            for d in data:
                if "type" not in d:
                    continue
                type_ = d["type"]
                is_chart = False
                if isinstance(type_, list):
                    type_ = [t for t in type_ if t in chart_types]
                    is_chart = len(type_) > 0
                else:
                    is_chart = type_ in chart_types
                    type_ = [type_]

                if is_chart:
                    yield {
                        'data': d,
                        'anno': anno,
                        'page': page,
                        'type_': type_,
                        'desc': description
                    }

        except Exception as err:
            print(anno)
            raise err


def process_anno(data, anno, page, type_, desc):
    try:
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
        return {
            "type": type_,
            "file_name": page["image"],
            "file_contents":
            base64.b64encode(cropped_image_io.getvalue()).decode(),
            "mimetype": "image/jpeg",
            "description": desc
        }

    except Exception as err:
        print(anno)
        raise err


def process_annos(pkgs):
    for pkg in pkgs:
        yield process_anno(**pkg)


def main():
    args = parser.parse_args()
    gathering_token = gathering_login(args.gathering_api, args.gathering_user,
                                      args.gathering_password)
    compare_token = compare_login(args.compare_api, args.compare_user,
                                  args.compare_password)
    print("Loading pages")
    pages = list(tqdm(gathering_pages(args.gathering_api, gathering_token)))
    pages = {p['id']: p for p in pages}

    print("Loading publications")
    pubs = list(tqdm(gathering_pubs(args.gathering_api, gathering_token)))
    pubs = {p['id']: p for p in pubs}

    annos = gathering_annos(args.gathering_api, gathering_token)

    print("Importing annotations")
    for b in batch(tqdm(process_annos(filter_annos(annos, pages, pubs))),
                   args.batch_size):
        compare_add_charts(args.compare_api, compare_token, list(b))


if __name__ == "__main__":
    main()
