from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# 設定檔案上傳的目錄
UPLOAD_FOLDER = 'competitions'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_xlsx_files():
    return [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.xlsx')]


# 第 1 個網頁：上傳 .xlsx 檔案
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return 'No selected file'
            
            # 儲存上傳的檔案
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            return redirect(url_for('edit'))

    return render_template('upload.html')


# 第 2 個網頁：編輯 .xlsx 檔案
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    files = get_xlsx_files()
    
    if request.method == 'POST':
        selected_file = request.form.get('file_select')
        if selected_file:
            return redirect(url_for('edit_file', filename=selected_file))
    
    return render_template('edit.html', files=files)


# 第 2.1 個網頁：編輯特定 .xlsx 檔案
@app.route('/edit_file/<filename>', methods=['GET', 'POST'])
def edit_file(filename):
    filename_with_ext = filename if filename.endswith('.xlsx') else filename + '.xlsx'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_with_ext)
    if not os.path.exists(filepath):
        return 'File not found'
    
    # 讀取 Excel 檔案
    df = pd.read_excel(filepath)

    # 將 NaN 值替換為空字符串
    df.fillna("", inplace=True)

    if request.method == 'POST':
        if 'save' in request.form:
            # 保存修改的數據
            updated_data = {}
            for key, value in request.form.items():
                if key not in ['save', 'add_row_after', 'delete_row']:
                    row, col = key.split('_')
                    row = int(row)
                    col = int(col)
                    updated_data[row] = updated_data.get(row, {})
                    updated_data[row][col] = value

            # 確保 DataFrame 的大小與表單中的數據一致
            max_row = max(updated_data.keys(), default=-1)
            if max_row >= df.shape[0]:
                # 添加新的空白行到 DataFrame
                for _ in range(max_row - df.shape[0] + 1):
                    df.loc[df.shape[0]] = [""] * len(df.columns)

            # 更新 DataFrame
            for row_idx, row_data in updated_data.items():
                for col_idx, value in row_data.items():
                    df.iat[row_idx, col_idx] = value

            df.to_excel(filepath, index=False)
            return render_template('edit_file.html', df=df, filename=filename, message="File saved successfully")
        
        elif 'add_row_after' in request.form:
            # 在特定行後添加新行
            row_to_add_after = int(request.form['add_row_after'])
            new_row = pd.Series([""] * len(df.columns), index=df.columns)
            # 使用 DataFrame 的 loc 來插入新行
            df = pd.concat([df.iloc[:row_to_add_after + 1], pd.DataFrame([new_row]), df.iloc[row_to_add_after + 1:]]).reset_index(drop=True)
            return render_template('edit_file.html', df=df, filename=filename, message=f"Row added after {row_to_add_after + 1}")
        
        elif 'delete_row' in request.form:
            # 刪除指定的行
            row_to_delete = int(request.form['delete_row'])
            if 0 <= row_to_delete < df.shape[0]:
                df = df.drop(index=row_to_delete).reset_index(drop=True)
            df.to_excel(filepath, index=False)  # 保存刪除行後的結果
            return render_template('edit_file.html', df=df, filename=filename, message=f"Row {row_to_delete + 1} deleted")

    return render_template('edit_file.html', df=df, filename=filename)



# 第 3 個網頁：顯示 .xlsx 檔案內容（僅讀取）
@app.route('/view/<filename>')
def view(filename):
    filename_with_ext = filename if filename.endswith('.xlsx') else filename + '.xlsx'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_with_ext)
    if not os.path.exists(filepath):
        return 'File not found'
    
    # 讀取 Excel 檔案
    df = pd.read_excel(filepath)
    # print(df)
    # 顯示檔案內容
    return render_template('view.html', tables=[df.to_html(classes='data')], filename=filename)

# 第 3 個網頁：顯示所有.xlsx檔案表格
@app.route('/display')
def overview():
    folder_path = UPLOAD_FOLDER
    tables = []

    # 遍歷資料夾中的所有 .xlsx 文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file_name)
            # 讀取 Excel 文件的所有列
            df = pd.read_excel(file_path)
            # 刪除第 5 和第 6 列都非空的行
            df_filtered = df[~(df.iloc[:, 4].notna() & df.iloc[:, 5].notna())]
            # 只保留前 4 列
            df_filtered = df_filtered.iloc[:, :4]
            # 將 DataFrame 轉換為 HTML 表格
            table_html = df_filtered.to_html(classes='table table-striped', index=False)
            tables.append({
                'name': file_name,
                'table': table_html
            })

    # 將表格和文件名傳遞給模板
    return render_template('display.html', tables=tables)


@app.route('/score')
def index():
    return render_template('score.html')

if __name__ == '__main__':
    app.run(debug=True)
