#!/usr/bin/env python3
#
# Before running: pip install requests tqdm
#

import argparse
import base64
import os.path

import pandas as pd
import requests
from tqdm import tqdm

type_map = {
    'AreaGraph': 'area_plot',
    'BarGraph': 'bar_plot',
    'BoxPlot': 'box_plot',
    'BubbleChart': 'bubble_chart',
    'ColumnGraph': 'column_plot',
    'LineGraph': 'linear_plot',
    'ParetoChart': 'pareto_chart',
    'PieChart': 'pie_chart',
    'RadarPlot': 'radar_plot',
    'ScatterGraph': 'scatter_plot'
}

parser = argparse.ArgumentParser(description="Import examples")
parser.add_argument("--path",
                    "-P",
                    type=str,
                    required=True,
                    help="Location of charts directory")
parser.add_argument("--compare-api",
                    "-C",
                    type=str,
                    required=True,
                    help="Address of Compare API",
                    default="http://localhost")
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
    compare_token = compare_login(args.compare_api, args.compare_user,
                                  args.compare_password)

    charts = list()
    annos = pd.read_csv(os.path.join(args.path, "annotations.csv"), sep=';')

    for _, anno in tqdm(annos.iterrows()):
        try:
            with open(
                    os.path.join(args.path, anno['type'],
                                 str(anno['file']) + '.png'), 'rb') as f:
                image = f.read()

            charts.append({
                "type": [type_map[anno['type']]],
                "file_name": anno['type'] + '_' + str(anno['file']) + '.png',
                "file_contents": base64.b64encode(image).decode(),
                "mimetype": 'image/png',
                "title": anno['title'],
                "x_axis_title": anno['x_axis_title'],
                "y_axis_title": anno['y_axis_title'],
                "description": anno['description'],
            })

        except Exception as err:
            print(anno)
            raise err

    print(f"Found {len(charts)} charts")
    compare_add_charts(args.compare_api, compare_token, charts)


if __name__ == "__main__":
    main()
