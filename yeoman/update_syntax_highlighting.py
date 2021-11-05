import os
import shutil

if os.path.exists(
    r"C:\Users\matth\AppData\Local\Programs\Microsoft VS Code\resources\app\extensions\numl\syntaxes\numl.tmLanguage.json"
):
    os.remove(
        r"C:\Users\matth\AppData\Local\Programs\Microsoft VS Code\resources\app\extensions\numl\syntaxes\numl.tmLanguage.json"
    )

shutil.copyfile(
    os.path.dirname(__file__) + "/numl/syntaxes/numl.tmLanguage.json",
    r"C:\Users\matth\AppData\Local\Programs\Microsoft VS Code\resources\app\extensions\numl\syntaxes\numl.tmLanguage.json",
)
