import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date, timedelta
from datetime import datetime
import time
# Use a service account
def addUrlToFirebase(URL):


    time.sleep(15)
    cred = credentials.Certificate('./serviceAccount.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    date_today = datetime.now().strftime('%Y%m%d')

    collection = db.collection(u'DropboxLinks')
    doc_ref = collection.document(date_today)

    doc_ref.set({
        u'link': URL,
        u'created_date': datetime.now()
    })

    print("url added to firebase")


# addUrlToFirebase("https://messageninja.ai")
