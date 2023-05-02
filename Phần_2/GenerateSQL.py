import pandas as pd
import numpy as np
import os

folder_path = r'D:\nguyen\Material\IT004.N21.CTTN\Assgiment1\Data'
# folder_path = input("Nhập đường dẫn thư mục: ")

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
            for index, row in df.iterrows():           

                if isDM: 
                    f.write('use TRUONGHOC;') 
                    values = ", ".join("'" + str(x) + "'" for x in row.values)              
                    insert_statement = (f'INSERT INTO {excel_file[0:len(excel_file)-5]} VALUES ({values});\n').format(values)
                    ma = str(row['Ma'])
                    ten = str(row['Ten'])
                    dictionary[ten] = ma 
                    f.write(insert_statement)

                else : 
                    f.write('use TRUONGHOC;') 
                    ma = str(row['Ma_Truong'])
                    ten = str(row['Ten_Truong'])
                    dc = str(row['Dia_chi'])   
                    lh = dictionary[str(row['Loai_hinh'])] #if str(row['Loai_hinh']) != 'nan' else 'NULL'
                    lt = dictionary[str(row['Loai_Truong'])] #if str(row['Loai_Truong']) != 'nan' else 'NULL'
                    pgd = dictionary[str(row['Phong_GDDT'])] #if str(row['Phong_GDDT']) != 'nan' else 'NULL'

                    values = f'"{ma}", "{ten}", "{dc}", "{pgd}", "{lh}", "{lt}"'
                    insert_statement = (f'INSERT INTO {excel_file[0:len(excel_file)-5]} VALUES ({values});\n').format(values)
                    f.write(insert_statement)

readFile(True) #đọc file danh mục 
readFile(False) # đọc các file còn lại 