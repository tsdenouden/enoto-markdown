# 📒Enoto


## Enoto is a web-based Markdown editor with an easy-to-use theme editor.

The latest version of Enoto can be found [here](https://enoto-markdown.herokuapp.com).

## Features:

#### 📝 Text editor
Users write Markdown inside the text editor. When they click save, their Markdown string is converted to HTML using the parser and saved
to the server as a temporary HTML file. This file is then read by the preview and rendered on to the screen.

#### 🎨 Theme editor
Users can style their document by using the theme editor. They simply select a few options, enter some values and upon saving the theme, Enoto will pass their input into a CSS template and save it to a temporary CSS file. The user's stylesheet is automatically linked to their Markdown file when the text editor is rendered for the first time.

#### 🧾 Insert bar
Users can append common Markdown syntax to their string in the text editor.

* Bold, Italic Text
* Lists: numbered lists & bulleted lists
* Links
* Images
* Tables

Additionally, on mobile & smaller screen sizes, the way the insert bar is presented to the user is modified by a few Javascript functions.
Instead of being an array of buttons, it becomes a dropdown menu that can be open & closed. On mobile, this dropdown menu is always invisible when the DOM is first loaded.

#### 🔽 Download Files

Users can download their file in a few formats.

* .MD
* .HTML
* .CSS
* .PDF

#### 🔼 Upload Files

Users can upload Markdown files as long as it doesn't exceed the 1MB limit.

#### 🐱‍💻How user data & files are saved
Most of the user's input/information is saved locally on their browser via cookies. However, their input is also saved to actual files on the server so it can be shown, downloaded, updated, etc. Unlike cookies, these files are temporary and are automatically deleted when the user closes the web app or when the files are more than a day old.

## 💻 Tech stack

* [Flask](https://flask.palletsprojects.com/en/2.1.x/) - a lightweight Python framework for writing web applications.
* [TailwindCSS](https://tailwindcss.com) - a utility-first CSS framework for rapidly building custom user interfaces.
* [PythonMarkdown](https://python-markdown.github.io) - a Markdown parser written in Python. Provides an Extension API for developers to extend the behaviour of the parser.
* Theme Editor - a mini Python module I wrote for writing basic CSS templates.

Languages: HTML, CSS, Javascript, Python

## 📱 Mobile support

Enoto uses breakpoints in Tailwind to apply different utility classes
based on the user's screen size to create responsive design.  
Additionally, Enoto uses Javascript to detect whether the user is on Desktop or on Mobile, and change how certain things are displayed & interacted with.

## 🛠 Web server hosting

Enoto runs on a web server which is hosted in Heroku, a container-based cloud PaaS which developers use to deploy, manage, and scale modern apps.

## Example workflow
For example, let's say a user wanted to make a basic website with Enoto. They would write the contents of their document out in Markdown inside the text editor and save it, so they can preview their HTML file.

Then if they wanted to design their website, they could create a theme in the theme editor. For example, they could choose a specific font for the title or crop some images or change the size of their tables. Then they would save it to apply the CSS to their website.

Finally, they can download their HTML & CSS files by selecting those formats in the dropdown menu below & clicking the download button. The user would now have a basic website they could open up on their browser.

## Program design

Enoto is written mainly in Python. I've used HTML, CSS and JS for the frontend but most of the app's logic is in Python.

### 🔴 Important files:

* editor.html, the Markdown editor. This is where users will be writing their Markdown files. It consists of the text editor, theme editor, preview, insert bar and download & upload buttons.
* app.py, this is where the backend code goes. From handling different HTTP requests to setting cookies, all the server-side scripting goes here.
* theme_editor.py, I wrote this module for writing basic CSS stylesheets.

### 🌱 Project structure:

Root folder - Flask app.py & theme editor module  
Templates - HTML pages  
Static - CSS, images & temporary user files

## What I've learnt & final thoughts

I had a lot fun coding this web app, and I learnt a lot from this project. I'm also glad I decided to learn Tailwind, it made writing CSS a whole lot more fun for me and I now have a better understanding of how web pages are organised.

I would definitely like to improve this in the future, I think if I had to work on this project again I would take the time to learn a Javascript UI framework like React or Vue. I would also make the file preview realtime instead of requiring the user to save their file.
