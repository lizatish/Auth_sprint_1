from http import HTTPStatus

from flask import jsonify


class JsonService:
    @staticmethod
    def return_user_not_found():
        """Возвращает ответ пользователю, если пользователь не найден."""
        return "User not found", HTTPStatus.NOT_FOUND

    @staticmethod
    def return_password_verification_failed():
        """Возвращает ответ пользователю, если введенный пароль не верен."""
        return "Invalid password", HTTPStatus.UNAUTHORIZED

    @staticmethod
    def return_success_response(**kwargs):
        """Возвращает ответ пользователю,сообщающий о выполнении успешной операции."""
        return jsonify(**kwargs)

    @staticmethod
    def return_user_exists(**kwargs):
        """Возвращает ответ пользователю,сообщающий о выполнении успешной операции."""
        return {"message": "User with this username already exists!"}, HTTPStatus.CONFLICT
