import dearpygui.dearpygui as dpg
import os
import glob
import imchgpt as imch
import imgGet as imgGet


# ---------- USER BACKEND PLACEHOLDER ----------
def decode(Txt):
    imgGet.get_image_url(Txt, folderName="userIMG")
    file = "userIMG/" + Txt + ".png"
    temp = imch.decode_image(file)
    print("Decoded message:", temp)

def mandecode(Txt):
    temp = imch.decode_image(Txt)
    print("Decoded message:", temp)
    # upload the decoded message to the input field
    dpg.set_value("DecodedMsg", temp)



# ----- Data -----
user_bio = "This is my bio."
current_user = "you"

userIMG_folder = "userIMG"
UrPFP_folder = "UrImgOutput"
friends = []  # stores only usernames


# ----- CALLBACKS -----

def load_friends_from_folder():
    friends.clear()
    png_files = glob.glob(os.path.join(userIMG_folder, "*.png"))
    for file in png_files:
        username = os.path.splitext(os.path.basename(file))[0]
        friends.append(username)
        add_friend_button(username)


def add_friend_button(username):
    tex_tag = f"{username}_tex"
    img_path = os.path.join(userIMG_folder, f"{username}.png")
    try:
        width, height, _, data = dpg.load_image(img_path)
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width, height, data, tag=tex_tag)
    except:
        print(f"[DEBUG] Failed to load image for {username}")
        return

    with dpg.group(horizontal=True, parent="friend_list"):
        dpg.add_image_button(tex_tag, width=40, height=40, callback=select_friend, user_data=username)
        dpg.add_button(label=username, callback=select_friend, user_data=username)


def select_friend(sender, app_data, username):
    print(f"[DEBUG] Selected friend: {username}")
    imgGet.get_image_url(username, folderName=userIMG_folder)
    bio = imch.decode_image(os.path.join(userIMG_folder, f"{username}.png"))
    dpg.set_value("bio_text", bio)
    dpg.configure_item("bio_text", readonly=True)
    dpg.hide_item("update_bio_button")


def show_user_bio_popup():
    dpg.configure_item("edit_bio_popup", show=True)


def submit_bio():
    username = dpg.get_value("edit_username")
    bio = dpg.get_value("edit_bio_text")
    image_path = os.path.join(UrPFP_folder, f"{username}.png")

    if not os.path.exists(image_path):
        imgGet.get_image_url(username, "UrImgOutput")
        print(f"[DEBUG] No image for user '{username}'.")
        print("Trying again after downloading image...")
        submit_bio()  # Retry after downloading image
        return

    imch.encode_image(image_path, image_path, bio)
    print(f"[DEBUG] Bio updated for {username}")
    dpg.configure_item("edit_bio_popup", show=False)


def add_friend_popup():
    dpg.configure_item("add_friend_popup", show=True)


def add_friend_callback():
    username = dpg.get_value("new_friend_name")
    print(f"[DEBUG] Adding friend: {username}")
    imgGet.get_image_url(username, folderName=userIMG_folder)
    image_path = os.path.join(userIMG_folder, f"{username}.png")

    if os.path.exists(image_path) and username not in friends:
        friends.append(username)
        add_friend_button(username)
    else:
        print(f"[DEBUG] Failed to add friend or already added.")

    dpg.set_value("new_friend_name", "")
    dpg.configure_item("add_friend_popup", show=False)


# ----- GUI BUILD -----

dpg.create_context()

with dpg.window(tag="MainWindow"):
    with dpg.group(horizontal=True):
        with dpg.child_window(width=250, autosize_y=True):
            dpg.add_text("Friends")
            with dpg.child_window(height=300, tag="friend_list"):
                pass  # populated on load

            dpg.add_spacer(height=10)
            dpg.add_button(label="➕ Add Friend", callback=add_friend_popup)
            dpg.add_spacer(height=20)
            dpg.add_button(label="✏️ Edit My Bio", callback=show_user_bio_popup)

        with dpg.child_window(autosize_x=True, autosize_y=True):
            dpg.add_input_text(tag="bio_text", multiline=True, default_value="", readonly=True, width=-1, height=-1)
            dpg.add_button(label="Update Bio", tag="update_bio_button", callback=submit_bio, show=False)

# Add Friend Popup
with dpg.window(label="Add Friend", modal=True, show=False, tag="add_friend_popup", width=300, height=150):
    dpg.add_text("Enter Username:")
    dpg.add_input_text(label="", tag="new_friend_name")
    dpg.add_button(label="Add", callback=add_friend_callback)

# Edit Bio Popup
with dpg.window(label="Edit Your Bio", modal=True, show=False, tag="edit_bio_popup", width=350, height=220):
    dpg.add_text("Edit Bio for User")
    dpg.add_input_text(label="Username", default_value=current_user, tag="edit_username")
    dpg.add_input_text(label="Bio", multiline=True, tag="edit_bio_text", height=100)
    dpg.add_button(label="Submit Bio", callback=submit_bio)

# ----- Lifecycle -----

dpg.create_viewport(title='Friend Bio App', width=850, height=450)
dpg.setup_dearpygui()
load_friends_from_folder()
dpg.show_viewport()
dpg.set_primary_window("MainWindow", True)
dpg.start_dearpygui()
dpg.destroy_context()