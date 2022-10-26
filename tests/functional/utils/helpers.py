import json
from typing import Generator


def get_es_fw_bulk_query(es_data: list, es_index: str, es_id_field: str) -> Generator:
    """Генерирует документы для единовременной записи в es."""
    for doc in es_data:
        yield {
            '_op_type': 'index',
            '_id': doc[es_id_field],
            '_index': es_index,
            '_source': doc,
        }


def prepare_redis_person(person: bytes) -> dict:
    """Преобразует персону из редиса к необходимому виду."""
    person = json.loads(person)
    return {
        'uuid': person['id'],
        'full_name': person['full_name'],
        'films': person['films'],
    }


def prepare_redis_film(film: bytes) -> dict:
    """Преобразует фильм из редиса к необходимому виду."""
    film = json.loads(film)
    return {
        'uuid': film['id'],
        'title': film['title'],
        'imdb_rating': film['imdb_rating'],
    }


def prepare_redis_genre(genre: bytes) -> dict:
    """Преобразует жанр из редиса к необходимому виду."""
    genre = json.loads(genre)
    genre.pop('description', None)
    genre['uuid'] = genre.pop('id')
    return genre


def check_nested_filteres(redis_data: list, filter_name: dict) -> bool:
    """Проверка на наличие фильтров в ответе."""
    for item in redis_data:
        for filter_ in filter_name:
            data = json.loads(item)
            tmp = [i['id'] for i in data[filter_]]
            if filter_name[filter_] in tmp:
                continue
            else:
                return False
    return True


def check_simple_filteres(redis_data: list, filter_name: dict) -> bool:
    """Проверка на наличие фильтров в ответе."""
    if filter_name:
        for item in redis_data:
            for filter_ in filter_name:
                data = json.loads(item)
                if str(filter_name[filter_]) in str(data[filter_]) or filter_name[filter_] == data[filter_]:
                    continue
                else:
                    return False
    return True
