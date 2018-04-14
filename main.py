import flask
import typing
from http import HTTPStatus


App = flask.Flask(__name__)

App.config.update(dict(
    SECRET_KEY='test_key',
))


@App.route('/')
def frontend() -> typing.Tuple[str, int]:
    return 'Yahoo to You!', HTTPStatus.OK


if __name__ == "__main__":
    App.run()
