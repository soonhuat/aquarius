import json
from provider_backend.constants import BaseURLs

json_dict = {"title": "example",
             "publisherId": "0x692e6b31dbaeb6fddd9b28c79c90dd19076663d3a0a5419d9245d48679134900a20e9534964fee74e40f493554c5619ee9749749fdc1a6083e0dbf1c014a79a2"}
json_before = {"title": "example",
               "publisherId": "0x692e6b31dbaeb6fddd9b28c79c90dd19076663d3a0a5419d9245d48679134900a20e9534964fee74e40f493554c5619ee9749749fdc1a6083e0dbf1c014a79a3"}
json_update = {"title": "example_update",
               "publisherId": "0x692e6b31dbaeb6fddd9b28c79c90dd19076663d3a0a5419d9245d48679134900a20e9534964fee74e40f493554c5619ee9749749fdc1a6083e0dbf1c014a79a2"}


def test_create_asset(client):
    """Test creation of asset"""
    post = client.post(BaseURLs.BASE_PROVIDER_URL + '/assets/metadata',
                       data=json.dumps(json_dict),
                       content_type='application/json')
    rv = client.get(
        BaseURLs.BASE_PROVIDER_URL + '/assets/metadata/%s' % json.loads(post.data.decode('utf-8'))['assetId'],
        content_type='application/json')
    assert 'example' in json.loads(rv.data.decode('utf-8'))['data']['data']['title']
    client.delete(BaseURLs.BASE_PROVIDER_URL + '/assets/metadata/%s' % json.loads(post.data.decode('utf-8'))['assetId'])


def test_update_asset_metadata(client):
    post = client.post(BaseURLs.BASE_PROVIDER_URL + '/assets/metadata',
                       data=json.dumps(json_before),
                       content_type='application/json')
    client.put(BaseURLs.BASE_PROVIDER_URL + '/assets/metadata/%s' % json.loads(post.data.decode('utf-8'))['assetId'],
               data=json.dumps(json_update),
               content_type='application/json')
    rv = client.get(
        BaseURLs.BASE_PROVIDER_URL + '/assets/metadata/%s' % json.loads(post.data.decode('utf-8'))['assetId'],
        content_type='application/json')
    assert 'example_update' in json.loads(rv.data.decode('utf-8'))['data']['data']['title']
    client.delete(BaseURLs.BASE_PROVIDER_URL + '/assets/metadata/%s' % json.loads(post.data.decode('utf-8'))['assetId'])


import os
import io

#
# from database.instance import get_oceandb_instance, sanitize_record
#
# get_oceandb_instance(database_name='ocean_test',
#                       config_file=os.path.join("..", "/test-config.json"))
#
# import app
# app = app.app

#
# def insert_boundary(boundary, buff, at_end=False):
#     buff.write(b'--')
#     buff.write(boundary.encode())
#     if at_end:
#         buff.write(b'--\r\n')
#     else:
#         buff.write(b'\r\n')
#
#
# def create_file_request_data_and_headers(data, fieldname, filename, content_type):
#     boundry = '----WebKitFormBoundary1modcYGLAATJpapo8jhD4UwHbF5asu4u'
#     buff = io.BytesIO()
#
#     insert_boundary(boundry, buff)
#     buff.write(('Content-Disposition: form-data; name="%s"; filename="%s"' %
#                 (fieldname, filename)).encode())
#     buff.write(b'\r\n')
#     buff.write(('Content-Type: %s' % content_type).encode())
#     buff.write(b'\r\n')
#     buff.write(b'\r\n')
#     buff.write(data)
#     buff.write(b'\r\n')
#
#     insert_boundary(boundry, buff, at_end=True)
#
#     headers = dict()
#     headers['content-type'] = 'multipart/form-data; boundary=%s' % boundry
#     headers['Content-Length'] = str(buff.tell())
#
#     return buff.getvalue(), headers


# class TestAssets(object):
#
#     def test_get_asset(self, database_instance):
#         pass
