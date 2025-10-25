import pyrebase

config = {
    "apiKey":"AIzaSyDlM84g5Ektc0ZdRLgyFdXvlme1I0hBEaE",
    "authDomain":"plumeriadate.firebaseapp.com",
    # "databaseURL":"https://plumeria.firebaseio.com/",
    "projectId":"plumeriadate",
    "storageBucket":"plumeriadate.appspot.com",
    "messagingSenderId":"949980353182",
    # "appId":"949980353182-1nb8435c0066orbqbv0ob7llmn7gnufi.apps.googleusercontent.com",

    # "apiKey": "AIzaSyDlM84g5Ektc0ZdRLgyFdXvlme1I0hBEaE",
    # "authDomain": "plumeriadate.firebaseapp.com",
    # "projectId": "plumeriadate",
    # "storageBucket": "plumeriadate.appspot.com",
    # "messagingSenderId": "949980353182",
    "appId": "1:949980353182:web:8be87fd60480989055a18f",
    "measurementId": "G-6N02QH78XB",
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
storage = firebase.storage()

# user = auth.sign_in_anonymous()

# print(auth.get_account_info())

