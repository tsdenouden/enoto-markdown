from flask import Flask, current_app, render_template, redirect, request, make_response, send_from_directory

import os

import markdown
from markdown.extensions.tables import TableExtension

import theme_editor
import json

from html2image import Html2Image
from PIL import Image

from random import randint
from datetime import datetime


# If user visits incorrect url or any other error occurs -> redirect them to the home page
def page_missing(e):
    return redirect("/")


#Config
app = Flask(__name__)
app.register_error_handler(404, page_missing)
app.register_error_handler(500, page_missing)
app.config["MD_FILES"] = "static/user_pages"
app.config["UPLOAD_FILES"] = "static/upload_files"
app.config["MAX_MD_SIZE"] = 1000000
app.config.update(  
    TEMPLATES_AUTO_RELOAD=True
)


# Render home page
@app.route('/')
def index():
    # Build response
    res = make_response(render_template("index.html"), 200)

    if request.cookies.get("md_file") == None:
        # Create file id
        md_file_id = str_random_gen(9)
        res.set_cookie("md_file", md_file_id)

        # Link HTML file to User's Stylesheet
        user_text = f'<!--Link to Theme: -->\n<link rel="stylesheet" href="{md_file_id}.css">\n\nStart writing here.'
        res.set_cookie("md_text", user_text)

        # Reset theme editor dict
        user_css = dict.fromkeys([
            "font_type",
            "font_size",
            "body_text",
            "body_bg",
            "title_font",
            "title_size",
            "title_color",
            "image_width",
            "image_border",
            "image_radius",
            "image_color",
            "table_width",
            "table_border",
            "heading_bg",
            "heading_color",
            "zebra_color"
        ], "")

        # Set dict to json object
        user_css = json.dumps(user_css, indent=4)
        res.set_cookie("css", user_css)

    return res


# Render editor 
@app.route('/editor', methods=['GET', 'POST'])
def editor():
    # Clean up files, delete old files
    clean_files()

    # Gets address of user's file
    # IF this fails, redirect user to home page to generate file id
    try:
        user_file = format_address(request.cookies.get("md_file"), "html")
    except:
        return redirect("/")

    if request.method == "POST":

        # Write user's text input into an HTML file.
        user_text = request.form['text']
        file_md = open(user_file, "w")
        file_md.write(markdown.markdown(user_text, extensions=['tables']))
        file_md.close()

        # Build response & save user's text input in a cookie
        res = redirect("/editor")
        res.set_cookie("md_text", user_text)

        return res
    else:
        # If user's temporary html file doesn't exist on server -> render placeholder file
        if os.path.exists(user_file) != True:
            user_file = "static/user_pages/file.html"
        
        # Get user input & file css to render editor page with the user's changes
        user_text = request.cookies.get("md_text")
        
        # Get user css JSON object and convert it to dict
        user_css = request.cookies.get("css")
        user_css = json.loads(user_css)

        # Build response
        res = make_response(render_template("editor.html", text=user_text, mdfile=user_file, css=user_css), 200)

        # Render template  
        return res


# Theme Editor
@app.route('/theme', methods=['GET','POST'])
def set_theme():
    if request.method == "POST":
        # Location of user's css file so the theme editor can write to it
        css_file = format_address(request.cookies.get("md_file"), "css")
        
        # Get user's css from the theme editor
        user_css = request.form.to_dict()

        # Update document's theme with new css
        theme_editor.setTheme(user_css, css_file)

        # Build response
        res = redirect("/editor")

        # Convert updated css dict back to JSON object & save as cookie
        user_css = json.dumps(user_css, indent=4)
        res.set_cookie("css", user_css)

        return res
    else:
        return redirect("/")


# Download user's files
@app.route('/download', methods=['GET', 'POST'])
def download_file():
    # User's file id
    file_id = request.cookies.get("md_file")

    # Check if user's file exists
    try:
        if os.path.exists(format_address(file_id, "html")) != True:
            return redirect("/editor")
    except:
        return redirect("/")

    # Get user's desired file type
    file_type = request.args.get("file_type")
        
    # Write markdown file
    if file_type == "md":
        user_text = request.cookies.get("md_text")
        md_file = format_address(file_id, "md")
        file_md = open(md_file, "w")
        file_md.write(user_text)
        file_md.close()
       
    # Write pdf file
    if file_type == "pdf":
        # Address of pdf file
        pdf_file = format_address(file_id, "pdf")
        
        # Create pdf file
        init_pdf = open(pdf_file, "w")
        init_pdf.close()
            
        # Address of image file
        img_address= format_address(file_id, "png")
        
        # Take a screenshot of the user's html file
        try:
            html_file = format_address(file_id, "html")
            css_file = format_address(file_id, "css")
            img_file = file_id + ".png"
            hti = Html2Image(output_path='static/user_pages')
            hti.screenshot(html_file=html_file, css_file=css_file, save_as=img_file)
        except:
            return redirect("/editor")

        # Convert PNG to PDF
        html_image = Image.open(img_address)
        html_image1 = html_image.convert('RGB')
        html_image1.save(pdf_file)

    # Get the file the user wants to download e.g Example.md , Example.html
    user_file = file_id + "." + file_type
        
    # Get directory of where the file is located
    user_pages = os.path.join(current_app.root_path, app.config["MD_FILES"])
        
    # Download file
    return send_from_directory(
        directory=user_pages, path=user_file, as_attachment=True
    )


# Upload user's files
@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        if request.files:
            # Get uploaded file
            md_upload = request.files["md_upload"]
        
            # Check if file size exceeds limit
            try:
                if not file_size_check(request.cookies.get("fileSize")):
                    return redirect("/editor")
            except:
                return redirect("/editor")
            
            # Get contents of uploaded file & save it to cookie
            user_text = md_upload.read()
            res = redirect("/editor")
            res.set_cookie("md_text", user_text)
            
            return res
        # Refresh page
        return redirect("/editor")
    else:
        return redirect("/")


# Delete
@app.route('/delete')
def delete():
    # User's file id
    file_id = request.cookies.get("md_file")

    # Check if user's file exists
    try:
        if os.path.exists(format_address(file_id, "html")) != True:
            return redirect("/")
    except:
        return redirect("/")

    formats = ["html", "css", "md", "pdf", "png"]

    # Delete all files under the user's file id
    for counter in range(len(formats)):
        curr_file = format_address(file_id, formats[counter])
        if os.path.exists(curr_file) == True:
            os.remove(curr_file)

    return redirect('/editor')


# About page
@app.route('/about')
def about():
    return render_template("about.html")


# Faq page
@app.route('/faq')
def faq():
    return render_template("faq.html")


# Placeholder file
@app.route('/file')
def file():
    return render_template("file.html")


# Deletes old files
def clean_files():
    # Get directory of all user files
    file_dir = os.path.join(current_app.root_path, app.config["MD_FILES"])

    # Delete files in the directory that are more than a day old.
    for file in os.listdir(file_dir):
        file_date = os.path.getmtime(os.path.join(file_dir, file))
        if file != "file.html":
            dt_date = datetime.fromtimestamp(file_date)
            curr_dt = datetime.now()
            delta = curr_dt - dt_date
            if delta.days >= 1:
                os.remove(os.path.join(file_dir, file))


# Check if file size is below the limit (1mb)
def file_size_check(size):
    if int(size) <= app.config["MAX_MD_SIZE"]:
        return True
    else:
        return False


# Used to generate a file id
def str_random_gen(power):
    return str(randint(1,10**power))


# Used to format a file id into a file address
def format_address(file,file_type):
    return "static/user_pages/" + file + "." + file_type


if __name__ == "__main__":
    app.run(debug=True)
