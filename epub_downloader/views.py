from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
# for downloading
import os
from django.conf import settings
from bs4 import BeautifulSoup
import re
import requests

# converting text to epub format
import ebooklib
from ebooklib import epub

# Create your views here.
def index(request):
    return render(request, 'epub_downloader/index.html')


def convert_url_text(request):
    response = requests.get(request.POST.get('url'))
    response.raise_for_status() # raise httperror for bad responses
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # get p and H1-H4 elements only
    text_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'img']

    all_elements = soup.find_all(text_tags)
    
    html_parts = [];
    for element in all_elements:
        html_parts.append(str(element))

    image_counter = 1
    image_map = {}

    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        if img_url:
            try:
                img_response = requests.get(img_url)
                img_response.raise_for_status()
                image_ext = os.path.splitext(img_url)[1].split('?')[0] or '.jpg'
                image_filename = f'image_{image_counter}{image_ext}'
                image_counter += 1

                # Embed image in EPUB
                img_item = epub.EpubImage()
                img_item.file_name = image_filename
                img_item.content = img_response.content
                img_item.media_type = f'image/{image_ext.strip(".")}'
                book.add_item(img_item)

                # Rewrite src in the soup
                img_tag['src'] = image_filename
            except Exception as e:
                print(f"Skipping image {img_url}: {e}")

    combined_html_content = "\n".join(html_parts)

    # limit string to 6 words
    file_name = " " .join(all_elements[0].get_text(strip=True).split()[:6])
    file_name = file_name.replace("'", "")

    ### using ebooklib to create the book
    book = epub.EpubBook()
    
    current_datetime = timezone.now()

    book.set_identifier(current_datetime.strftime('%Y%m%d%H%M%S'))
    book.set_title(file_name)
    book.set_language("en")

    book.add_author("Edmund Chan")

    # create chapter
    c1 = epub.EpubHtml(title="Intro", file_name=f"{file_name}.xhtml", lang="hr", uid=current_datetime.strftime('%Y%m%d%H%M%S'))
    c1.content = combined_html_content


    # not using yet - for images
    # # create imag`e from the local image
    # image_content = open("ebooklib.gif", "rb").read()
    # img = epub.EpubImage(
    #     uid="image_1",
    #     file_name="static/ebooklib.gif",
    #     media_type="image/gif",
    #     content=image_content,
    # )

    # add chapter
    book.add_item(c1)

    # # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # # define CSS style
    style = "BODY {color: white;}"
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style,
    )

    # # add CSS file
    book.add_item(nav_css)

    # # basic spine
    book.spine = ["nav", c1]

    # write to the file
    file_directory = os.path.join(settings.BASE_DIR, 'downloads')

    os.makedirs(file_directory, exist_ok=True)

    file_name += ".epub"
    file_path = os.path.join(file_directory, file_name)
    
    try:
        # with open(file_path, 'wb') as file:
        epub.write_epub(file_path, book, {})
        print(f"Success: {file_path}")
        return download(file_name, file_path)
    except IOError as e:
        print(f"Error writing file: {e}")

    # epub.write_epub("f{file_name}.epub", book, {})

    # # concatenate the text content 
    # concatenated_text = ""
    # for element in all_elements:
    #     concatenated_text += element.get_text(strip=True) + "\n"

    # text_only = concatenated_text #.get_text(strip=True)

    return download(file_name, epub)
    # return render(request, 'index.html', {'download': 'Success'})


# def write_text_to_epub(file_name, epub):
    # file_directory = os.path.join(settings.BASE_DIR, 'downloads')

    # os.makedirs(file_directory, exist_ok=True)

    # file_path = os.path.join(file_directory, file_name)
    # try:
    #     with open(file_path, 'w') as file:
    #         file.write(text_only)
    #     print(f"Success: {file_path}")
    #     return download(file_name, file_path)
    # except IOError as e:
    #     print(f"Error writing file: {e}")
    

def download(file_name, file_path):
    file_directory = os.path.join(settings.BASE_DIR, 'downloads')

    # check file exists
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'rb') as fh:
            # response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response = HttpResponse(fh.read(), content_type="application/epub+zip")
            # Set the Content-Disposition header to force download and suggest filename
            response['Content-Disposition'] = f'attachment'; filename="{os.path.basename(file_path)}"
            return response
    else:
        raise Http404("File not found")

    # return render(request, 'index.html', {'download': 'it worked'})