import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from loguru import logger


def get_service_sacc():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds_service = ServiceAccountCredentials.from_json_keyfile_name('filestoread/dnd.json', scopes).authorize(httplib2.Http())
    return googleapiclient.discovery.build('sheets', 'v4', http=creds_service)


def delete_answers(alias: str, sheet: str):
    resp = get_service_sacc().spreadsheets().values().get(spreadsheetId='17pVHk1aAVC07W_1dWaVCkxJCku_CaOzFD6-7pT_W2hE',
                                                          range=f"{sheet}!A2:K500").execute()
    logger.info(f"Get value from Google Sheet, collecting data from A2 to K500")

    answers = resp['values']
    for i in range(len(answers)):
        if len(answers[i]) != 0:
            if answers[i][-1] == alias:
                get_service_sacc().spreadsheets().values().clear(
                    spreadsheetId="17pVHk1aAVC07W_1dWaVCkxJCku_CaOzFD6-7pT_W2hE",
                    range=f"{sheet}!A{i+2}:K{i+2}").execute()
                logger.success(f"Deleted from {sheet} value fromm A{i+2} to K{i+2}")
