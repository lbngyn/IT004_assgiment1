import pandas as pd
import numpy as np
import os
from unidecode import unidecode

folder_path = input("Nhập đường dẫn thư mục: ")

# Lấy danh sách các file Excel trong thư mục
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')] 

#create dictionary
dictionary = {}

# đọc file 
def readFile( isDM ): 
    for excel_file in excel_files: 

        if ((str(excel_file[0:2]) == 'DM') != isDM ) : continue 
        df = pd.read_excel(os.path.join(folder_path, excel_file))                       
        sql_file = os.path.splitext(excel_file)[0] + '.sql'                             
        
        with open(os.path.join(folder_path, sql_file), 'w', encoding='utf-8') as f:      
            f.write('use TRUONGHOC;\n') 
            for index, row in df.iterrows():           

                if isDM: 
                    values = ", ".join("'" + unidecode(str(x)) + "'" for x in row.values)              
                    insert_statement = (f'INSERT INTO {excel_file[0:len(excel_file)-5]} VALUES ({values});\n').format(values)
                    ma = unidecode(str(row['Ma']))
                    ten = unidecode(str(row['Ten']))
                    dictionary[ten] = ma 
                    f.write(insert_statement)

                else : 
                    ma = unidecode(str(row['Ma_Truong']))
                    ten = unidecode(str(row['Ten_Truong']))
                    dc = unidecode(str(row['Dia_chi']))   
                    lh = dictionary[unidecode(str(row['Loai_hinh']))] 
                    lt = dictionary[unidecode(str(row['Loai_Truong']))] 
                    pgd = dictionary[unidecode(str(row['Phong_GDDT']))] 

                    values = f'"{ma}", "{ten}", "{dc}", "{pgd}", "{lh}", "{lt}"'
                    insert_statement = (f'INSERT INTO {excel_file[0:len(excel_file)-5]} VALUES ({values});\n').format(values)
                    f.write(insert_statement)

readFile(True) #đọc file danh mục 
readFile(False) # đọc các file còn lại 
