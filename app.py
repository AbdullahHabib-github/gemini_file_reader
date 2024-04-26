import streamlit as st
import os
import random
import string
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel, Part


credentials_file = None
# Iterate through all files to find the credentials file
for filename in os.listdir(os.getcwd()):
    # Check if the file ends with .json extension
    if filename.endswith('.json'):
        credentials_file = filename

if not  credentials_file:
    raise Exception ("Please download the credentials file from Cloud Console")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_file 


def upload_blob(source_file_name, destination_blob_name, bucket_name="gemini_pdf_upload"):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    # print(
    #     f"File {source_file_name} uploaded to {destination_blob_name}."
    # )


def process_file(system_prompt, filename,file_extension):
    filename = "gs://gemini_pdf_upload/"+filename

    project_id = "demos-403615"

    vertexai.init(project=project_id, location="us-central1")

    model = GenerativeModel(model_name="gemini-1.5-pro-preview-0409")


    if file_extension == ".pdf" or file_extension == ".PDF":
        file = Part.from_uri(filename, mime_type="application/pdf")

    elif file_extension in [".mp3",".MP3",".Mp3",".mP3",".mp1",".MP1",".Mp1",".mP1",".mp2",".MP2",".Mp2",".mP2"]:
        file = Part.from_uri(filename, mime_type="audio/mpeg")

    elif file_extension in [".jpg", ".JPG", ".Jpg", ".jPg",".jpeg", ".JPEG", ".Jpeg", ".jPeg"]:
        file = Part.from_uri(filename, mime_type="image/jpeg")

    elif file_extension in [".png", ".PNG", ".Png", ".pNg"]:
        file = Part.from_uri(filename, mime_type="image/png")    

    elif file_extension in [".mp4", ".MP4", ".Mp4", ".mP4"]:
        file = Part.from_uri(filename, mime_type="video/mp4")

    else:
        return "{file_extension} fromat is not currently supported"
    
    contents = [file, system_prompt]

    response = model.generate_content(contents)
    # print(response.text)
    return response.text

# Streamlit App Structure
st.title("File Prompt Processor")

system_prompt = st.text_area("Enter your system prompt:", height=100)  # Multi-line input
data_file = st.file_uploader("Upload a file:")

if system_prompt and data_file and st.button("Submit"):
    # Save the uploaded file locally
    # Save the uploaded file
    with st.spinner("Saving the file locally..."): 

        random_prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

        # Extract the original filename and extension
        filename, file_extension = os.path.splitext(data_file.name)

        # Create the new filename with the random prefix
        new_filename = f"{random_prefix}{filename}{file_extension}"

        # Create the "datafiles" directory if it doesn't exist
        os.makedirs("datafiles", exist_ok=True)

        # Save the file with the new random filename
        save_path = os.path.join("datafiles", new_filename)
        with open(save_path, "wb") as f:
            f.write(data_file.getvalue()) 

    with st.spinner("Uploading the file to the cloud storage..."): 
        upload_blob(source_file_name=save_path,destination_blob_name=new_filename)
        os.remove(save_path)

    with st.spinner("Wating for response from Gemini..."): 
        output_text = process_file(system_prompt, new_filename,file_extension)
    st.markdown(output_text) 

