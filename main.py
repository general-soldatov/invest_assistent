import eel
import jinja2

eel.init('static_web_folder')

@eel.expose
def summer(x, y):
    return x + y

eel.start('main_page.html')