from http import HTTPStatus

from flask import jsonify, Request


class JsonService:
    @staticmethod
    def return_user_not_found():
        """Возвращает ответ пользователю, если пользователь не найден."""
        return {"msg": "User not found"}, HTTPStatus.NOT_FOUND

    @staticmethod
    def return_role_not_found():
        """Возвращает ответ пользователю, если роль не найдена."""
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND

    @staticmethod
    def return_password_verification_failed():
        """Возвращает ответ пользователю, если введенный пароль не верен."""
        return {"msg": "Invalid password"}, HTTPStatus.UNAUTHORIZED

    @staticmethod
    def return_success_response(**kwargs):
        """Возвращает ответ пользователю,сообщающий о выполнении успешной операции."""
        return jsonify(**kwargs)

    @staticmethod
    def return_user_exists():
        """Возвращает ответ пользователю, если такой логин уже используется."""
        return {"msg": "User with this username already exists!"}, HTTPStatus.CONFLICT

    @staticmethod
    def return_invalid_refresh_token() -> (str, int):
        """Возвращает невалидный refresh-токен."""
        return {"msg": "Invalid refresh token"}, HTTPStatus.UNAUTHORIZED

    @staticmethod
    def get_refresh_token(request: Request):
        """Возвращает refresh-token из заголовка запроса."""
        headers = request.headers
        bearer = headers.get('Authorization')
        return bearer.split()[1]
