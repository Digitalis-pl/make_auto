import json
import pprint

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

    def create_scenario_in_make(self, blueprint):
        response = requests.post(self.url, data=blueprint, headers=self.token)
        return json.loads(response.text)


test_data = [{'service': 'tiktok', 'client_id': 'idtik', 'client_secrets': 'tok', 'tt_account_id': 'tik', 'CONN_ID': 1},
             {'service': 'google-drive', 'client_id': 'cig', 'client_secrets': 'csg', 'gd_folder_id': 'str', 'CONN_ID': 2},
             {'service': 'instagram', 'client_id': 'idiiii', 'client_secrets': 'ciii', 'fb_inst_page_id': 'page', 'CONN_ID': 3},
             {'service': 'telegram', 'tg_bot_token': 'tokbot', 'tg_chat_id': 'bot', 'CONN_ID': 4},
             {'service': 'youtube', 'client_id': 'yid', 'client_secrets': 'secr', 'yt_channel_id': 'kanal', 'CONN_ID': 5}]


def form_flow(service_list):
    """Создает чертеж"""
    flow = []
    for el in service_list:
        if el['service'] == 'youtube':
            module = {
                "id": 8,
                "module": "youtube:UploadVideo",
                "version": 1,
                "parameters": {
                    "__IMTCONN__": el["CONN_ID"],
                    "channel_id": el['yt_channel_id'],
                    "video_url": "{{3.file_url}}",
                    "title": "New Video",
                    "description": "Check out this new video!"
                },
                "metadata": {
                    "designer": {
                        "x": 800,
                        "y": 200,
                        "name": "Publish on YouTube"
                    }
                }
            }
            flow.append(module)
        elif el['service'] == 'facebook':
            module = {
                "id": 6,
                "module": "facebook-pages:CreateAPost",
                "version": 1,
                "parameters": {
                    "__IMTCONN__": el["CONN_ID"],
                    "page_id": el['fb_inst_page_id'],
                    "message": "Check out this content!",
                    "link": "{{3.file_url}}"
                },
                "metadata": {
                    "designer": {
                        "x": 800,
                        "y": 0,
                        "name": "Publish on Facebook"
                    }
                }
            }
            flow.append(module)
        elif el['service'] == 'instagram':
            module = {
                "id": 5,
                "module": "instagram-business:CreateAReelPost",
                "version": 1,
                "parameters": {
                    "__IMTCONN__": el["CONN_ID"],
                    "account_id": el['fb_inst_page_id'],
                    "video_url": "{{3.file_url}}"
                },
                "metadata": {
                    "designer": {
                        "x": 800,
                        "y": -100,
                        "name": "Publish on Instagram"
                    }
                }
            }
            flow.append(module)
        elif el['service'] == 'tiktok':
            module = {
                "id": 7,
                "module": "tiktok:UploadVideo",
                "version": 1,
                "parameters": {
                    "__IMTCONN__": el["CONN_ID"],
                    "video_url": "{{3.file_url}}",
                    "caption": "New content uploaded!"
                },
                "metadata": {
                    "designer": {
                        "x": 800,
                        "y": 100,
                        "name": "Publish on TikTok"
                    }
                }
            }
            flow.append(module)
        elif el['service'] == 'google-drive':
            module = {
                "id": 3,
                "module": "google-drive:UploadAFile",
                "version": 1,
                "parameters": {
                    "__IMTCONN__": el["CONN_ID"],
                    "file_name": "{{2.file_name}}",
                    "file_data": "{{2.file_data}}",
                    "folder_id": el['gd_folder_id']
                },
                "metadata": {
                    "designer": {
                        "x": 400,
                        "y": 0,
                        "name": "Upload to Google Drive"
                    }
                }
            }
            flow.append(module)
    return flow


def create_blueprint(flow):
    blueprint = {"name": "Content Distribution to Multiple Platforms",
                 "flow": flow,
                 "metadata": {
                     "version": 1,
                     "scenario": {
                         "roundtrips": 1,
                         "maxErrors": 3,
                         "autoCommit": True,
                         "autoCommitTriggerLast": True,
                         "sequential": False,
                         "confidential": False,
                         "dataloss": False,
                         "dlq": False,
                         "freshVariables": False
                     },
                     "designer": {
                         "orphans": []
                     }
                 }
                 }
    return blueprint


pprint.pprint(create_blueprint(form_flow(test_data)))
