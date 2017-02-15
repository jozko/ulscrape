import os
from scrapy.http import Request, FormRequest, HtmlResponse


def response_from(path, url=None, formdata=None, meta=None):
    if url is None:
        url = "http://www.example.com"

    res_d = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.realpath(os.path.join(res_d, "../requests", path))

    if not os.path.exists(file_path):
        raise Exception("Request was not found in file \"%s\"." % file_path)

    request = Request(url=url, meta=meta)
    if formdata is not None:
        request = FormRequest(url=url, formdata=formdata, meta=meta)

    file_handler = open(file_path, 'r')
    file_content = file_handler.read()

    response = HtmlResponse(url=url, request=request,
                            encoding='utf-8', body=file_content)
    file_handler.close()
    return response
