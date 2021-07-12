# coding: utf-8

import uuid


def make_uuid():
    uuid1_str = uuid.uuid1().hex
    return uuid.uuid3(uuid.NAMESPACE_DNS, uuid1_str).hex
