
from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import album


@route("/albums/<artist>")
def find_artist(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [field.album for field in albums_list]
        result = "Нашлось альбомов {} - {}.<br><br>Список альбомов:<br><br>".format(artist, len(albums_list))
        result += "<br>".join(album_names)
    return result


@route("/albums", method="POST")
def request_artist():
    artist_data = album.Album(
        year = request.forms.get("year"),
        artist = request.forms.get("artist"),
        genre = request.forms.get("genre"),
        album = request.forms.get("album")
    )

    if artist_data.year < "1900" or artist_data.year > "2020":
        return HTTPError(404, "Ошибка. Неправильный формат года выпуска альбома.")
    else:
        return album.save(artist_data)


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
