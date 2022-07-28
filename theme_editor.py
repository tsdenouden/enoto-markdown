# Theme Editor Module
# The theme editor interacts with this module to write the user's css to their unique css file.
# The user's css file is based on a basic template where the values are overwritten
# with the values they passed into the theme editor.


# Default - empty file
user_css = '''null'''


# CSS Template, the symbols will be replaced with the user's input values
theme_template = '''
body {
    font-family: $;
    font-size: #;
    color: >;
    background-color: @;
    margin: 25px;
}

h1 {
    font-family: *;
    font-size: ^;
    color: &;
}

a {
    font-family: $;
    font-size: #;
    color: >;
}

img {
    border: !px solid ?;
    border-radius: O%;
    width: <%;
    max-width: 100%
    height: auto;
}

table {
    width: /%;
    height: auto;  
}

table, th, td {
    border: =px solid;
    border-collapse: collapse;
    padding: 3px;
}

th {
    background-color: [;
    color: ];
}

tr:nth-child(even) {background-color: +;}
'''


# Set theme css
def setTheme(user_input, css_file):

    # Dictionary of symbols to values
    # Each symbol represents a different CSS property
    theme_id = {
        "$": "font",
        "#": "font_size",
        ">": "text_color",
        "@": "bg_color",

        "*": "title_font",
        "^": "title_size",
        "&": "title_color",

        "!": "img_border",
        "?": "img_border_color",
        "O": "img_radius",
        "<": "img_width",

        "/": "table_width",
        "=": "table_border",
        "[": "heading_bg",
        "]": "heading_color",
        "+": "zebra_color"
    }

    # Update dictionary values with user input
    # (replaces placeholders e.g replaces "font" with the user's desired font)
    updateDict(theme_id, user_input)

    # Reset css to default template
    user_css = theme_template

    # For every symbol found in the template, replace it with the user's corresponding input value
    # E.g % -> #00FF00
    for key in theme_id:
        user_css = user_css.replace(key, theme_id[key])
    
    # Write to css file
    css = open(css_file, "w")
    css.write(user_css)
    css.close()
    

# Update dictionary
def updateDict(oldDict, new_values):
    i = 0
    for key in oldDict:
        oldDict[key] = new_values[i]
        i += 1
