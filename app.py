from flask import Flask, current_app, render_template, redirect, request, make_response, send_from_directory

import markdown

from markdown.extensions.tables import TableExtension

from random import randint

import os

from werkzeug.utils import secure_filename

import theme_editor

from html2image import Html2Image

from PIL import Image

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
    
    # If user doesn't have a file id -> generate file id
    # This id will later be used to create temporary files on the server
    if request.cookies.get("md_file") == None:
        md_file_id = str_random_gen(9)
        res.set_cookie("md_file", md_file_id)

        # Creates placeholder text in the editor. Also links the user's HTML file to their CSS file.
        user_text = '<!-- Link to Theme: --> \n' + '<link rel="stylesheet" href="' + md_file_id + '.css' + '">' + '\n\n' + 'Start writing here.'
        res.set_cookie("md_text", user_text)

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
        
        # Body
        body_font = request.cookies.get("css_font")
        body_font_size = request.cookies.get("css_font_size")
        body_text = request.cookies.get("css_body_text")
        body_bg = request.cookies.get("css_body_bg")

        # Title
        title_font = request.cookies.get("css_title_font")
        title_size = request.cookies.get("css_title_size")
        title_color = request.cookies.get("css_title_color")

        # Images
        img_border = request.cookies.get("css_image_border")
        img_color = request.cookies.get("css_image_border_color")
        img_radius = request.cookies.get("css_image_radius")
        img_width = request.cookies.get("css_image_width")

        # Tables
        tbl_width = request.cookies.get("css_table_width")
        tbl_border = request.cookies.get("css_table_border")
        tbl_h_bg = request.cookies.get("css_heading_bg")
        tbl_h = request.cookies.get("css_heading_color")
        tbl_zebra = request.cookies.get("css_zebra_color")

        # Build response
        res = make_response(render_template("editor.html", 
   
        text=user_text, mdfile=user_file,

        font_type=body_font, font_size=body_font_size, body_text=body_text, body_bg=body_bg,

        title_font=title_font, title_size=title_size, title_color=title_color,
   
        image_border=img_border, image_color=img_color, image_radius=img_radius, image_width=img_width,

        table_width=tbl_width, table_border=tbl_border, heading_bg=tbl_h_bg, heading_color=tbl_h, zebra_color=tbl_zebra
        ), 200)

        # Render template  
        return res


# Theme Editor
@app.route('/theme', methods=['GET','POST'])
def set_theme():
    if request.method == "POST":
        # Location of user's css file so the theme editor can write to it
        css_file = format_address(request.cookies.get("md_file"), "css")
        
        # User's CSS for html <body>
        body_font = request.form.get("font_type")
        body_font_size = request.form.get("font_size")
        body_text = request.form.get("body_text")
        body_bg = request.form.get("body_bg")

        # User's CSS for the <h1> tag
        title_font = request.form.get("title_font")
        title_size = request.form.get("title_size")
        title_color = request.form.get("title_color")

        # User's CSS for Images
        img_border = request.form.get("image_border")
        img_color = request.form.get("image_color")
        img_radius = request.form.get("image_radius")
        img_width = request.form.get("image_width")

        # User's CSS for tables
        tbl_width = request.form.get("table_width")
        tbl_border = request.form.get("table_border")
        tbl_h_bg = request.form.get("heading_bg")
        tbl_h = request.form.get("heading_color")
        tbl_zebra = request.form.get("zebra_color")

        # Write to user's css files with this array of values passed as input
        user_css = [
            body_font, body_font_size, body_text, body_bg,
            title_font, title_size, title_color,
            img_border, img_color, img_radius, img_width,
            tbl_width, tbl_border, tbl_h_bg, tbl_h, tbl_zebra
        ]

        theme_editor.setTheme(user_css, css_file)
        
        # Build response
        res = redirect("/editor")

        # Set <body> CSS cookies
        res.set_cookie("css_font", body_font)
        res.set_cookie("css_font_size", body_font_size)
        res.set_cookie("css_body_text", body_text)
        res.set_cookie("css_body_bg", body_bg)

        # Set <h1> CSS cookies
        res.set_cookie("css_title_font", title_font)
        res.set_cookie("css_title_size", title_size)
        res.set_cookie("css_title_color", title_color)

        # Set <img> CSS cookies
        res.set_cookie("css_image_border", img_border)
        res.set_cookie("css_image_border_color", img_color)
        res.set_cookie("css_image_radius", img_radius)
        res.set_cookie("css_image_width", img_width)

        # Set <table><th><tr> cookies
        res.set_cookie("css_table_width", tbl_width)
        res.set_cookie("css_table_border", tbl_border)
        res.set_cookie("css_heading_bg", tbl_h_bg)
        res.set_cookie("css_heading_color", tbl_h)
        res.set_cookie("css_zebra_color", tbl_zebra)

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
    user_text = request.cookies.get("md_text")
    md_file = format_address(file_id, "md")
    file_md = open(md_file, "w")
    file_md.write(user_text)
    file_md.close()
        
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
            
            # Check if filename meets requirements & make filename secure
            if not file_name_check(md_upload.filename):
                return redirect("/editor")
            else:
                md_upload_secure = secure_filename(md_upload.filename)
            
            # Save user's file on server
            md_upload.save(os.path.join(app.config["UPLOAD_FILES"], md_upload_secure))
            
            # Get both newly uploaded markdown file & user's current html file:
            upload_file = "static/upload_files/" + md_upload_secure
            user_file = format_address(request.cookies.get("md_file"), "html")
            
            # Overwrite html file with uploaded file
            user_text = copy_file(upload_file, user_file)
            
            # Build response
            res = make_response(render_template("editor.html", text=user_text, mdfile=user_file), 200)
            res.set_cookie("md_text", user_text)
            
            # Delete user's uploaded file
            os.remove(os.path.join(app.config["UPLOAD_FILES"], md_upload_secure))
            # Return response
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


# Copies the uploaded markdown file to the user's temp html file
# And converts each line of markdown to html using the parser
# Returns the markdown text
def copy_file(input_file, output_file):
    md_text = ""
    # Overwrite the output file with the input file
    with open(input_file, 'r') as infile:
        with open(output_file, 'w') as outfile:
            for line in infile:
                md_text += line
                outfile.write(markdown.markdown(line))
    # Return lines of markdown
    return md_text


# Check if file size is below the limit (1mb)
def file_size_check(size):
    if int(size) <= app.config["MAX_MD_SIZE"]:
        return True
    else:
        return False


# Checks if a filename meets certain requirements
def file_name_check(filename):
    # Reject files without a filename or files without a '.' to delineate filetype
    if filename == "" or not '.' in filename:
        return False
    # Reject non markdown files
    elif filename.rsplit('.',1)[1] != "md":
        return False
    else:
        return True


# Used to generate a file id
def str_random_gen(power):
    return str(randint(1,10**power))


# Used to format a file id into a file address
def format_address(file,file_type):
    return "static/user_pages/" + file + "." + file_type


if __name__ == "__main__":
    app.run(debug=False)