import time
import structures
from css_html_js_minify import html_minify, js_minify, css_minify
from rjsmin import jsmin
import ntrlang

class Cache():
    def __init__(self, settings):
        self.cached = {}
        self.settings = settings

    def clear(self):
        self.cached = {}

    def delete(self, path):
        self.cached.pop()

    def getFile(self, path):
        if (path in self.cached):
            # TODO: Check if cache has expired
            return self.cached[path]["data"]
        else:

            isBytes = False

            try:
                f = open(self.settings.get("webdir") + path, "r")
                data = f.read()
                f.close()
            except UnicodeDecodeError:
                f = open(self.settings.get("webdir") + path, "rb")
                data = f.read()
                f.close()

                isBytes = True

            extension = path.split(".")[len(path.split(".")) - 1]

            if (self.settings.get("minify")):
                if (extension in structures.FileTypes.html.value):
                    data = html_minify(data)
                elif (extension in structures.FileTypes.js.value):
                    data = jsmin(data)
                elif (extension in structures.FileTypes.css.value):
                    data = css_minify(data)
            
            if (self.settings.get("natura_lang") and extension in structures.FileTypes.ntr.value):
                return ntrlang.int_process(data)

            
            # TODO: Check if path is in don't cache list, and check if cache enabled in settings

            if (not isBytes):
                data = data.encode()

            if (self.settings.get("cache")):    
                self.cached[path] = {
                    "data": data,
                    "exp": 100000,
                    "date": time.time()
                }

            return data