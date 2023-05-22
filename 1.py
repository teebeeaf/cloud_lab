import requests
import pprint
import csv
import logging
import boto3
from botocore.exceptions import ClientError
import os
import matplotlib.pyplot as plt
import json


def make_csv():
    a = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json").json()
    b = a
    keys = list(b[0].keys())
    for i in b:
        date = str(i["exchangedate"])
        cc = str(i["cc"])
        rate = str(i["rate"])
        check = '{\n  "CC": {\n    "S": "' + cc + '"\n  },\n  "date": {\n    "S": "' + date + '"\n  },\n  "rate": {\n    "N": "' + rate + '"\n  }\n}'
        print(check)
    new_dict = {}
    for i in range(len(b) - 1):
        new_dict[f"{i}"] = b[i]

    """
    for i in range(len(b) - 1):
        new_dict[f"{i}"] = b[i]
    with open("1.json", "w", encoding="utf-8") as jsonfile:
        jsonfile.write(json.dumps(new_dict))
        pprint.pprint(new_dict)
    with open("1.csv", "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(a[0].keys())
        keys = list(a[0].keys())
        for i in a:
            temp_row = []
            for j in keys:
                temp_row.append(i[j])
            writer.writerow(temp_row)
    """


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(file_name, bucket, object_name=None):
    import boto3

    s3 = boto3.client('s3')
    s3.download_file(bucket, file_name, file_name)


def make_function(startdate, enddate, valcode="usd"):
    a = requests.get(f"https://bank.gov.ua/NBU_Exchange/exchange_site?start={startdate}"
                     f"&end={enddate}&valcode={valcode}&sort=exchangedate&order=desc&json").json()

    xs, ys =[], []
    for i in range(len(a) - 1):
        xs.append(a[i]["exchangedate"])
        ys.append(a[i]["rate"])

    xys = list(zip(xs, ys))
    plt.scatter(*zip(*xys))
    # plt.plot(*zip(*xys))
    plt.xlabel('Dates')
    plt.ylabel(f'{valcode}')
    plt.title(f'{valcode}/uah')
    # plt.show()
    plt.savefig("1.png", bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    make_csv()
    # make_function("20210101", "20211201")
    # upload_file("1.png", "data11111111aads")
    # download_file("1.csv", "data11111111aads")
