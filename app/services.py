import json


class CreateConnections:

    def __init__(self, url, token):
        self.url = url
        self.token = token

    async def create_and_get_connections_info(self, name, client_id, client_secrets, bot_token=None):
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

    async def form_blueprint(self, service_list):
        with open("../data/blueprint.json", 'r') as file:
            blueprint_data = json.load(file)
        for el in service_list:
            if el['name'] == 'google':
                for module in blueprint_data:
                    if module['id'] == 17:
                        module['parameters']['__IMTCONN__'] = el['connection_id']






