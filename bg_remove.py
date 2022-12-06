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
    # img.save(buf, format="PNG")
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


col1, col2 = st.columns(2)
big=[]
imagear = []
imglst = []
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
# my_upload2 = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
# my_upload3 = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
# my_upload4 = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])


# # uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
number=0
for uploaded_file in my_upload:
    if number< 2:
        number+=1
        imglst.append(convert_image(uploaded_file))
    else:
        number+=1
        imagear.append(convert_image(uploaded_file))

    
big.append(imagear)
big.append(imglst)
st.write(big)

    

if my_upload is not None:
    # imageArra = []
    # imageArra.append(Image.open(my_upload))
    # st.write(imageArra)
    fixed = join_images(
*big,
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
    col2.write("Fixed Image :wrench:")
    col2.image(fixed)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download = image", convert_image(fixed), "fixed.png", "image/png")


