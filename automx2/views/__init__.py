"""
Flask application views.
"""
from flask import Response
from flask import Response
from flask import make_response


def xml_response(data: object) -> Response:
    response: Response = make_response(data)
    response.headers['Content-Type'] = 'text/xml'
    return response