from flask import Flask, render_template
from drive_reader import get_excel_files_from_drive

app = Flask(__name__)

@app.route('/')
def home():
    folder_id = 'hit_competition '  # 替換為您的 Google Drive 資料夾 ID
    files_data = get_excel_files_from_drive(folder_id)
    tables = []
    for file_data in files_data:
        table_html = file_data['data'].to_html(classes='table table-striped', index=False)
        tables.append({'name': file_data['name'], 'table': table_html})
    return render_template('display.html', tables=tables)

if __name__ == '__main__':
    app.run(debug=True)
