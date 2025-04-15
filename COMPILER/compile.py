import os
import shutil
from tkinter import Tk, simpledialog, filedialog, messagebox

TEMPLATES_DIR = 'templates'
POPUP_DIR = 'popup'
JS_TEMPLATE = os.path.join(TEMPLATES_DIR, 'ChromeFULL.js.template')
MANIFEST_TEMPLATE = os.path.join(TEMPLATES_DIR, 'manifest.json.template')

def read_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def compile_extension(crm_url, output_dir):
    extension_path = os.path.join(output_dir, 'CRM_Exporter')

    os.makedirs(extension_path, exist_ok=True)

    # Генерация JS
    js_code = read_template(JS_TEMPLATE).replace('{{CRM_URL}}', crm_url)
    write_file(os.path.join(extension_path, 'background.js'), js_code)
    write_file(os.path.join(extension_path, 'content-script.js'), js_code)

    # Генерация manifest.json
    manifest = read_template(MANIFEST_TEMPLATE).replace('{{CRM_URL}}', crm_url)
    write_file(os.path.join(extension_path, 'manifest.json'), manifest)

    # Копирование popup
    shutil.copytree(POPUP_DIR, os.path.join(extension_path, 'popup'), dirs_exist_ok=True)

    # Копирование XLSX библиотеки
    xlsx_lib = os.path.join('xlsx.full.min.js')
    if os.path.exists(xlsx_lib):
        shutil.copy(xlsx_lib, os.path.join(extension_path, 'xlsx.full.min.js'))

    return extension_path

def main():
    root = Tk()
    root.withdraw()

    crm_url = simpledialog.askstring("CRM URL", "Введите ссылку на CRM (например: https://crm.example.com)")
    if not crm_url:
        messagebox.showwarning("Ошибка", "Ссылка на CRM не указана")
        return

    output_dir = filedialog.askdirectory(title="Куда сохранить расширение?")
    if not output_dir:
        messagebox.showwarning("Ошибка", "Папка не выбрана")
        return

    path = compile_extension(crm_url, output_dir)
    messagebox.showinfo("Готово", f"Расширение собрано по пути:\n{path}")

if __name__ == "__main__":
    main()
