import eel
# from jinja2 import Environment, PackageLoader, select_autoescape, Template

# env = Environment(
#     loader=PackageLoader("eel"),
#     autoescape=select_autoescape()
# )

# template = Template("My name is {{ name }} and I am {{ age }}")

# data = template.render(name = 'that say nih', age = 2)

eel.init('front')

@eel.expose
def summer(x, y):
    return x + y


eel.start('templates/main_page.html', jinja_templates='templates')