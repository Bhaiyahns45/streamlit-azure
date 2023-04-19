from azure.storage.blob import BlobServiceClient
import streamlit as st
# import pyautogui


# streamlit page

st.set_page_config(
    page_title='Azure Storage File Uploader',
    layout="wide",
    initial_sidebar_state="expanded",
    # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
)


html_temp = """
<div style="background-color:#2F396F;padding:0.7px">
<h3 style="color:white;text-align:center;" >Azure Storage File Uploader</h3>
</div><br>"""
st.markdown(html_temp,unsafe_allow_html=True)
# st.header(":bar_chart:")


st.sidebar.image('https://i.imgur.com/3XqSI3B.png', width=180)
# st.title("AI Scheduling Accelerator Dashboard")    # Main Title
# st.markdown('<style>h1{color: blue;}</style>', unsafe_allow_html=True)
# st.sidebar.title("AI Scheduling")


connection_string = st.text_input("Please enter the connection string")

try:

    if st.button("Connect") or len(connection_string) != 0:

        # Create a BlobServiceClient object to access the container
        blob_service_client = BlobServiceClient.from_connection_string(str(connection_string))

        # Use the BlobServiceClient object to interact with the Blob Storage account

        # Get a list of the containers in the storage account
        containers = [container.name for container in blob_service_client.list_containers()]

        def create_new_container(container_name):

            if st.sidebar.button('Create Container'):
                container_client = blob_service_client.get_container_client(container_name)

                if not container_client.exists():
                    # Prompt the user to create the container
                    if container_name:
                        container_client.create_container()
                        st.sidebar.success(f"Container '{container_name}' created successfully!")
                        refresh_page(sidebar=True)
                else:
                    st.sidebar.error(f"Container '{container_name}' exists!")

            pass

        def create_new_folder(folder_name):

            if st.button('Create Folder'):
                folder_client = container_client.get_blob_client(folder_name + '/')
                if not folder_client.exists():
                    # Prompt the user to create the folder
                    if folder_name:
                        folder_client.upload_blob('')
                        st.success(f"Folder '{folder_name}' created successfully!")
                        refresh_page()
                else:
                    st.error(f"Folder '{folder_name}' exists!")


            pass


        def refresh_page(sidebar = False):
            st.markdown("---")
            if sidebar:
                if st.sidebar.button("Refresh page to see changes"):
                    # pyautogui.hotkey("ctrl","F5")
                    st.experimental_rerun()
            else:
                if st.button("Refresh page to see changes"):
                    # pyautogui.hotkey("ctrl","F5")
                    js = "window.location.reload();"
                    html = '<img src onerror="{}">'.format(js)
                    div = st.empty()
                    div.write(html, unsafe_allow_html=True)



        if len(containers) == 0:

            container_name = st.sidebar.text_input("Enter container name")
            create_new_container(container_name)


        else:

            # Create a dropdown to select a container
            container_name = st.sidebar.selectbox("Select a container", containers)

            if st.sidebar.checkbox("Create New Container"):
                new_container_name = st.sidebar.text_input("Enter container name")
                create_new_container(new_container_name)
                # refresh_page(sidebar=True)



            container_client = blob_service_client.get_container_client(container_name)

            # Get a list of all blobs in the container
            blobs = container_client.list_blobs()

            # Extract the folder names from the blob names
            folders = set()
            for blob in blobs:
                folder_name = blob.name.split("/")[0]
                if folder_name:
                    folders.add(folder_name)

            # Convert the set of folder names to a list and sort it
            folders = sorted(list(folders))

            if len(folders) == 0:
                st.error(f"No folder found inside {container_name} container")
                folder_name = st.text_input("Enter folder name")
                create_new_folder(folder_name)

            else:
                # Create a dropdown to select a folder
                folder_name = st.selectbox("Select a folder", list(folders))

                new_folder_checkbox = st.checkbox("Create New Folder", key="new_folder_checkbox")

                # Check if the new folder checkbox was previously checked
                new_folder_checked = st.session_state.get("new_folder_checked", False)

                # If the new folder checkbox was previously checked, clear its state
                if new_folder_checked:
                    st.session_state.new_folder_checked = False
                    
                #  If the new folder checkbox is checked, prompt the user for a new folder name
                if new_folder_checkbox:
                    new_folder_name = st.text_input("Enter folder name")
                    create_new_folder(new_folder_name)
                    st.session_state.new_folder_checked = True
                    

        # Create a file upload widget
            holder = st.empty()
            uploaded_file = holder.file_uploader("Choose a file")

            # Upload the file to the selected folder in the selected container
            if uploaded_file is not None:
                if st.button("Upload File"):
                    blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"{folder_name}/{uploaded_file.name}")
                    blob_client.upload_blob(uploaded_file)
                    st.success(f"File uploaded successfully! to folder {folder_name} in container {container_name}")
                    holder.empty()
                    uploaded_file = None
                    st.experimental_set_query_params(upload_status="success")

            if st.experimental_get_query_params().get("upload_status") == "success":
                st.success("File uploaded successfully!")
                st.experimental_set_query_params()
            else:
                # st.info("Please choose a file and click the 'Upload File' button to upload it.")
                # if uploaded_file is not None:
                #     st.button("Upload File")  # Re-render the button so it can be clicked again
                pass

except:
    st.error("Could not connect to storage account, please try again")



