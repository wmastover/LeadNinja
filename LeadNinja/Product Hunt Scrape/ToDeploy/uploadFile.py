import dropbox
from datetime import datetime

def get_new_access_token(refresh_token, app_key, app_secret):

    dbx = dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=app_key, app_secret=app_secret)
    dbx.check_and_refresh_access_token()
    return dbx._oauth2_access_token

def upload_file_to_dropbox(local_file_path, dropbox_path, access_token):
  
    dbx = dropbox.Dropbox(access_token)

    with open(local_file_path, 'rb') as f:
        try:
            dbx.files_upload(f.read(), dropbox_path)
            print(f"Uploaded {local_file_path} to Dropbox as {dropbox_path}")
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
            return shared_link_metadata.url
        except dropbox.exceptions.ApiError as error:
            print(f"An API error occurred: {error}")

def uploadFile():
    app_key = '2jsx26yqzuf0qc6'  # Replace with your app key
    app_secret = 'k15kj3ip6jrjpyc'  # Replace with your app secret
    refresh_token = 'fwV_sg7GKn0AAAAAAAAAAa70sEhyE8bOgzo__3CzEUfF7-UGezQFezdL_DIj2uUH'

    # Get a new access token
    access_token = get_new_access_token(refresh_token, app_key, app_secret)

    print(access_token)

    # Get today's date and format it as YYYYMMDD
    date_today = datetime.now().strftime('%Y%m%d')
    local_file_path = f'{date_today}.csv'
    dropbox_path = f'/LeadNinja/{date_today}.csv'  # Path where you want the file in Dropbox

    file_url = upload_file_to_dropbox(local_file_path, dropbox_path, access_token)
    if file_url:
        print(f"Access URL: {file_url}")
    else:
        print("Failed to upload the file.")

    return file_url

# Replace the following placeholders with your actual details
# uploadFile()


