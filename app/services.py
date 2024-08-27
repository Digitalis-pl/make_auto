import json
import requests


class CreateConnections:

    def __init__(self, make_url, token, endpoint):
        self.url = f'{make_url}/api/v2/{endpoint}'
        self.token = f'Token {token}'

    def create_and_get_connections_info(self, name, client_id, client_secrets, bot_token=None):
        """Создает тело запроса для создания соединений и отправляет его в make, возвращает response
        То что должны получить {
        "connection": {
        "id": 90,
        "name": "Slack test",
        "accountName": "slack",
        "accountLabel": "Slack",
        "packageName": null,
        "expire": null,
        "metadata": {
        "value": "Make User",
        "type": "string"
        },
        "teamId": 2,
        "theme": "#4a154b",
        "upgradeable": false,
        "scopes": 0,
        "scoped": true,
        "accountType": "oauth",
        "editable": false,
        "uid": 3243125312
        }
        }
        Сохраняем эти поараметры:
        "id": 90,
        "name": "Slack test",
        "accountName": "slack",
        "accountLabel": "Slack"
        """
        data = {"accountName": name,
                "accountType": name,
                "clientId": client_id,
                "clientSecret": client_secrets}
        if name == 'google-drive':
            data["scopes"] = ["https://www.googleapis.com/auth/drive.file"]
        if name == 'instagram':
            data["scopes"] = ["user_media", "instagram_content_publish"]
        if name == 'facebook':
            data["scopes"] = ["pages_manage_posts"]
        if name == 'telegram-bot':
            data["botToken"] = [bot_token]
        if name == 'tiktok':
            data["scopes"] = ["video.upload"]
        if name == 'youtube':
            data["scopes"] = ["https://www.googleapis.com/auth/youtube.upload",
                              "https://www.googleapis.com/auth/youtube.readonly"]
        response = requests.post(self.url, headers=self.token)
        return json.loads(response.text)

    def form_blueprint(self, service_list):
        """Создает чертеж"""
        pass
