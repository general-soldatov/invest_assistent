import os
name_proj = "test_eel"
noconsole = "" # ставим "" - если нужна консоль, " --windowed " - если не нужна
onefile = " --onefile " # указываем, что exe должен быть упакован в один файл
if __name__ == "__main__":
    cmd_txt = f'python -m eel main.py front {onefile} {noconsole} --name {name_proj}'
    os.system(cmd_txt)