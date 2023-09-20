import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

firebaseConfig = {
    'apiKey': "AIzaSyBMkMMst87k3yp6RC6BdssxtHMfSOevItc",
    'authDomain': "flaskproject2-6ba05.firebaseapp.com",
    'databaseURL': "https://flaskproject2-6ba05-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "flaskproject2-6ba05",
    'storageBucket': "flaskproject2-6ba05.appspot.com",
    'messagingSenderId': "1029273536424",
    'appId': "1:1029273536424:web:1e2de53ebaae10a74fff9d"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
