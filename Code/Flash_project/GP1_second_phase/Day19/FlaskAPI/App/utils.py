import base64
import hashlib

import time

import requests


def make_data_secret(source):

    encode_content = base64.standard_b64encode(source.encode("utf-8")).decode("utf-8")

    print(encode_content)

    add_content_encode_content = "CHKa2GFL1twhMDhEZVfDfU2DoZHCLZk" + encode_content + "pOq3kRIxs26rmRtsUTJvBn9Z"

    print(add_content_encode_content)

    encode_content_twice = base64.standard_b64encode(add_content_encode_content.encode("utf-8")).decode("utf-8")

    print(encode_content_twice)

    return encode_content_twice


def send_verify_code(phone):
    url = "https://api.netease.im/sms/sendcode.action"

    nonce = hashlib.new("sha512", str(time.time()).encode("utf-8")).hexdigest()

    curtime = str(int(time.time()))

    sha1 = hashlib.sha1()

    secret = "f2f839131b19"

    sha1.update((secret + nonce + curtime).encode("utf-8"))

    check_sum = sha1.hexdigest()

    header = {
        "AppKey": "70e20855fccfff9c86d0353a5e08b996",
        "Nonce": nonce,
        "CurTime": curtime,
        "CheckSum": check_sum
    }

    post_data = {
        "mobile": phone
    }

    resp = requests.post(url, data=post_data, headers=header)

    return resp
