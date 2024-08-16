from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# 設定檔案上傳的目錄
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 第 1 個網頁：上傳 .xlsx 檔案
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # 檢查是否有文件上傳
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return 'No selected file'
            
            # 儲存上傳的檔案
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            return 'File uploaded successfully'

    return render_template('upload.html')


# 第 2 個網頁：編輯 .xlsx 檔案
@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return 'File not found'
    
    # 讀取 Excel 檔案
    df = pd.read_excel(filepath)

    if request.method == 'POST':
        # 保存修改的數據
        updated_data = {}
        for key, value in request.form.items():
            if key != 'save':
                row, col = key.split('_')
                updated_data[int(row)] = updated_data.get(int(row), {})
                updated_data[int(row)][int(col)] = value

        for row_idx, row_data in updated_data.items():
            for col_idx, value in row_data.items():
                df.iat[row_idx, col_idx] = value
        
        df.to_excel(filepath, index=False)
        return render_template('edit.html', df=df, filename=filename, message="File saved successfully")

    return render_template('edit.html', df=df, filename=filename)


# 第 3 個網頁：顯示 .xlsx 檔案內容（僅讀取）
@app.route('/view/<filename>')
def view(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return 'File not found'
    
    # 讀取 Excel 檔案
    df = pd.read_excel(filepath)

    # 顯示檔案內容
    return render_template('view.html', tables=[df.to_html(classes='data')], filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
