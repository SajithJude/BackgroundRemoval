import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## Remove background from your image")
st.write(
    ":dog: Try uploading an image to watch the background magically removed. Full quality images can be downloaded from the sidebar. This code is open source and available [here](https://github.com/tyler-simons/BackgroundRemoval) on GitHub. Special thanks to the [rembg library](https://github.com/danielgatis/rembg) :grin:"
)
st.sidebar.write("## Upload and download :gear:")
images = [
    [Image.open('1.jpg'), Image.open('2.jpg')],
    [Image.open('3.jpg'), Image.open('4.jpg')],
]


# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def join_images(*rows, bg_color=(0, 0, 0, 0), alignment=(0.5, 0.5)):
    rows = [
        [image.convert('RGBA') for image in row]
        for row
        in rows
    ]

    heights = [
        max(image.height for image in row)
        for row
        in rows
    ]

    widths = [
        max(image.width for image in column)
        for column
        in zip(*rows)
    ]

    tmp = Image.new(
        'RGBA',
        size=(sum(widths), sum(heights)),
        color=bg_color
    )

    for i, row in enumerate(rows):
        for j, image in enumerate(row):
            y = sum(heights[:i]) + int((heights[i] - image.height) * alignment[1])
            x = sum(widths[:j]) + int((widths[j] - image.width) * alignment[0])
            tmp.paste(image, (x, y))

    return tmp


def join_images_horizontally(*row, bg_color=(0, 0, 0), alignment=(0.5, 0.5)):
    return join_images(
        row,
        bg_color=bg_color,
        alignment=alignment
    )


def join_images_vertically(*column, bg_color=(0, 0, 0), alignment=(0.5, 0.5)):
    return join_images(
        *[[image] for image in column],
        bg_color=bg_color,
        alignment=alignment
    )

# def fix_image(upload):
# join_images(
# *upload,
# bg_color='green',
# alignment=(0.5, 0.5)
# )
    # image1 = Image.open(upload)
    # image2 = Image.open(upload)
    # image1 = image1.resize((426, 240))
    # image1 = image1.resize((426, 240))

    # image1_size = image1.size   
    # image2_size = image2.size
    # new_image = Image.new('RGB',(*image1_size[0], image1_size[1]), (250,250,250))
    # new_image.paste(image1,(0,0))
    # new_image.paste(image2,(image1_size[0],0))
    # col1.write("Original Image :camera:")
    # col1.image(image1)
    


col1, col2 = st.columns(2)
uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files=True)

    # st.write(bytes_data)

if uploaded_files is not None:
    imagearrray=[]

    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        imagearrray.append(Image.open(uploaded_file))
        fixed = join_images(
    *imagearrray,
    bg_color='green',
    alignment=(0.5, 0.5)
    )
        col2.write("Fixed Image :wrench:")
        col2.image(fixed)
        st.sidebar.markdown("\n")
        st.sidebar.download_button("Download = image", convert_image(fixed), "fixed.png", "image/png")


    
 
    # fix_image(upload=my_upload)
else:
    fixed = join_images(
*images,
bg_color='green',
alignment=(0.5, 0.5)
)


# fixed = new_image
    col2.write("Fixed Image :wrench:")
    col2.image(fixed)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download = image", convert_image(fixed), "fixed.png", "image/png")

