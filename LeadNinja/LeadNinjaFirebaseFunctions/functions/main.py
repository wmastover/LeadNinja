# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import firestore_fn, https_fn

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
import google.cloud.firestore

app = initialize_app()


@firestore_fn.on_document_created(document="Users/{pushId}")
def sendInitialEmail(event: firestore_fn.Event[firestore_fn.DocumentSnapshot | None]) -> None:
    """
    This function is triggered when a new document is created in the 'Users' collection.
    It sends an initial email to the user.
    
    Args:
        event (firestore_fn.Event[firestore_fn.DocumentSnapshot | None]): The event data from the document created.
    """
    # Importing smtplib for the actual sending function
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import requests
    import os

    if event.data is None:
        return
    try:
        to_email = event.data.get("email")
        from_email = "will@messageninja.ai"
        subject = "🥷 Welcome to Lead Ninja"
        body = """Did somebody order some leads?
        
Here you go, you're welcome 😎


        """

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Download the file from Dropbox
        db = firestore.client()
        dropbox_ref = db.collection(u'DropboxLinks')
        docs = dropbox_ref.get()
        # Find the document with the most recent created date
        most_recent_doc = max(docs, key=lambda doc: doc.get('created_date'))

        # Set the url to the link property of the most recent document
        url = most_recent_doc.get('link').replace("dl=0", "dl=1")

        
        response = requests.get(url)
        file_name = "leads.csv"
        open(file_name, 'wb').write(response.content)

        # Attach the file to the email
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file_name, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name)
        message.attach(part)

        # Establish a secure session with Gmail's outgoing SMTP server
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, "zeliaodsjequfwkt")  # replace with your email password or app password
            text = message.as_string()
            server.sendmail(from_email, to_email, text)
            print("Email sent successfully")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()

        # Delete the file after sending the email
        os.remove(file_name)

    except KeyError:
        # No email field, so do nothing.
        return
    # Email settings
   

@firestore_fn.on_document_created(document="DropboxLinks/{pushId}")
def sendRecuringEmail(event: firestore_fn.Event[firestore_fn.DocumentSnapshot | None]) -> None:
    """
    This function is triggered when a new document is created in the 'Users' collection.
    It sends an initial email to the user.
    
    Args:
        event (firestore_fn.Event[firestore_fn.DocumentSnapshot | None]): The event data from the document created.
    """
    # Importing smtplib for the actual sending function
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import requests
    import os
    from firebase_admin import firestore

    # Use the application default credentials

    if event.data is None:
        return
    
    try:
        url = event.data.get("link").replace("dl=0", "dl=1")
        
        response = requests.get(url)
        file_name = "leads.csv"
        open(file_name, 'wb').write(response.content)

        db = firestore.client()
        users_ref = db.collection(u'Users')
        docs = users_ref.get()


        emails = []
        for doc in docs:
            email = doc.to_dict().get('email')
            emails.append(email)
            
        for to_email in emails:
            if to_email is None:
                continue
            try:
                from_email = "will@messageninja.ai"
                subject = "🥷 Daily Lead List"
                body = """Heres your daily lead list.
                
You're welcome 😎"""

                # Setup the MIME
                message = MIMEMultipart()
                message['From'] = from_email
                message['To'] = to_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))

                # Download the file from Dropbox
                

                # Attach the file to the email
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(file_name, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name)
                message.attach(part)

                # Establish a secure session with Gmail's outgoing SMTP server
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(from_email, "zeliaodsjequfwkt")  # replace with your email password or app password
                    text = message.as_string()
                    server.sendmail(from_email, to_email, text)
                    print("Email sent successfully")
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    server.quit()

                # Delete the file after sending the email
                

            except KeyError:
                # No "original" field, so do nothing.
                continue

            
    except KeyError:
        # No "original" field, so do nothing.
        return

    os.remove(file_name)

    # Email settings