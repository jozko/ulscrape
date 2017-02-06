import os
from scrapy.http import Request, FormRequest, Response, TextResponse, HtmlResponse

def response_from(path, url=None, formdata=None):
    if url is None:
        url = "http://www.example.com"

    responses_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.realpath(os.path.join(responses_dir, "../requests", path))

    if not os.path.exists(file_path):
        raise Exception("Request was not found in file \"%s\"." % file_path)

    request = Request(url=url)
    if formdata is not None:
        request = FormRequest(url=url, formdata=formdata)

    file_handler = open(file_path, 'r')
    file_content = file_handler.read()

    response = HtmlResponse(encoding='utf-8', url=url, request=request, body=file_content)
    file_handler.close()
    return response