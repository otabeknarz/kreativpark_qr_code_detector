BASE_URL = "https://api.otabek.me/"
API_ENDPOINT = "api/v2/"
GET_PEOPLE_URL = BASE_URL + API_ENDPOINT + "people/?format=json"
POST_PEOPLE_URL = BASE_URL + API_ENDPOINT + "people/add/"
CHECK_PEOPLE_URL = BASE_URL + API_ENDPOINT + "people/check/"

GET_QRCODES_URL = BASE_URL + API_ENDPOINT + "qrcode/?format=json"
POST_QRCODE_URL = BASE_URL + API_ENDPOINT + "qrcode/add/"
CHECK_PEOPLE_IDS = BASE_URL + API_ENDPOINT + "people/IDs/?format=json"
CHECK_QRCODE_URL = BASE_URL + API_ENDPOINT + "qrcode/check/"
CHECK_PEOPLE_HAS_QRCODE = BASE_URL + API_ENDPOINT + "qrcode/people/check/"
GET_QRCODES_DELETE_URL = BASE_URL + API_ENDPOINT + "qrcode/delete/"

ACCESS_TOKEN_URL = BASE_URL + API_ENDPOINT + "auth/token/"
REFRESH_TOKEN_URL = (
    BASE_URL + API_ENDPOINT + "auth/token/refresh/"
)

LOGIN_LIBRARY = BASE_URL + API_ENDPOINT + "login-library/"

QRCODES_PATH = "images/qr_codes/"

IBRAT_CHANNEL = "@ibratdebate"

SESSION_ID = "gqa18zwn8fl26ca6gjuwgopbtetjf2xb"
