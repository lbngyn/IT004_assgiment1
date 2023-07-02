# import 
import random
import os
from datetime import datetime, timedelta
import pandas as pd
from unidecode import unidecode
import string
import sys
import mysql.connector

#Note block
    #Line 78 -> 95: Tạo dữ liệu cho bảng TRUONG 
    #Line 97 -> 127: Tạo dữ liệu cho bảng HS 
    #Line 129 -> 166 : Tạo dữ liệu cho bảng HOC  

# Kết nối tới cơ sở dữ liệu MySQL
print("Nhập localhost: ", end=""); localhost = input() 
print("Nhập user: ", end=""); your_username = input() 
print("Nhập password: ", end=""); your_password = input() 

connection1 = mysql.connector.connect(
    host = localhost,
    user = your_username,
    password = your_password,
    database = 'truonghoc1'
)

connection2 = mysql.connector.connect(
    host = localhost,
    user = your_username,
    password = your_password,
    database = 'truonghoc2'
)
# Tạo đối tượng cursor
cursor1 = connection1.cursor()
cursor2 = connection2.cursor()

#Tạo method random ngày tháng năm 
def random_ngay_sinh():
    ngay = random.randint(1, 28)  # Random ngày từ 1 đến 28
    thang = random.randint(1, 12)  # Random tháng từ 1 đến 12
    nam = random.randint(1997, 2009)  # Random năm từ 1997 đến 2009
    
    # Tạo đối tượng datetime từ ngày, tháng, năm
    date_obj = datetime(nam, thang, ngay)
    
    # Chuẩn hóa thành định dạng ngày trong MySQL (YYYY-MM-DD)
    ngay_sinh = date_obj.strftime('%Y-%m-%d')
    
    return ngay_sinh

#function kiểm tra độ tuổi 
def kiem_tra_du_tuoi(ngay_sinh):
    # Tạo đối tượng datetime từ chuỗi ngày sinh
    ngay_sinh_obj = datetime.strptime(ngay_sinh, '%Y-%m-%d')
    
    # Tính tuổi từ ngày sinh
    tuoi = datetime.now().year - ngay_sinh_obj.year
    
    if tuoi >= 18:
        # Sinh số CCCD độc nhất
        cccd = sinh_so_cccd()
        return cccd
    else:
        return None

#function sinh số cccd 
CCCD_unique = [] 
def kiem_tra_ton_tai_cccd(cccd):
    # Kiểm tra số CCCD có tồn tại trong danh sách hay không
    return cccd in CCCD_unique

def sinh_so_cccd():
    # Sinh số CCCD độc nhất
    while(True):
        cccd = ''.join(random.choices('0123456789', k=15))
        if not (kiem_tra_ton_tai_cccd(cccd)): return cccd


# Đường dẫn tuyệt đối của tệp tin đang thực thi
current_file_path = os.path.abspath(__file__)
#Lấy đường dẫn thư mục hiện tại
folder_path = os.path.dirname(current_file_path)

#Tạo dữ liệu cho bảng TRUONG 
#Dữ liệu được lấy từ file Truong (file từ bài đồ án 1)
truongDataFile_name = "Data\Truong.xlsx"
truongDataFile_path = os.path.join(folder_path, truongDataFile_name)

#Đọc file excel 
School_df = pd.read_excel(truongDataFile_path)

# Lọc dữ liệu của một số cột trong bảng
selected_columns = ["Ma_Truong", "Ten_Truong", "Dia_chi"]
filtered_df = School_df[selected_columns]

#Viết các câu lệnh insert
for index, row in filtered_df.iterrows():      
    values = ", ".join("'" + unidecode(str(x)) + "'" for x in row.values)    
    insert_statement = (f'INSERT INTO TRUONG VALUES ({values});\n').format(values) 
    # print (insert_statement)
    cursor1.execute(insert_statement)
    cursor2.execute(insert_statement)
    connection1.commit()
    connection2.commit()
print("Đã insert xong bảng Trường!")

#Tạo dữ liệu cho bảng Học sinh 
count = 0 
firstName = ["Nguyễn", "Đồng", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đào", "Trương", "Đoàn", "Đinh", "Vương", "Trịnh", "Lưu", "Quách", "Đoàn", "Mai", "Đinh", "Châu", "Hà", "Thái", "Âu", "Lục", "Tạ", "Tiết", "Bành", "Lỗ", "Quang", "Bạch", "Lâm", "Lý", "Lương", "Khuất", "Tô", "Dỗ", "Diệp", "Bồ", "Tống", "Khúc", "Lục", "Kỷ", "Ninh", "Hàn", "Uông", "Doãn", "Phùng", "Sầm", "Hứa", "Mạch", "Trang", "Hoằng", "Lư", "Nghê", "Phi", "Quan", "Cao", "Thủy", "Lã", "Tiêu", "Bá", "Phương", "Thượng", "Giang", "Thiều", "Lạc", "Vi", "Cung", "Tăng", "Lục", "Sơn", "Nương", "Lữ", "Thái", "Chu", "Tiến", "Kiều", "Chử", "Hồng", "Lệ", "Viên", "Khổng", "Quản", "Diêu", "Gia", "Viên", "Văn", "Tôn", "Hứa", "Du", "Vương", "Sử", "Lai"]  
lastName = ["An", "Bình", "Chí", "Cường", "Dũng", "Đạt", "Đức", "Đăng", "Gia", "Hiếu", "Hoàng", "Hùng", "Hưng", "Khải", "Khoa", "Linh", "Long", "Minh", "Nam", "Nhân", "Phúc", "Quân", "Quang", "Quốc", "Sơn", "Thắng", "Thành", "Thiên", "Thịnh", "Thủy", "Tiến", "Trí", "Trung", "Tuấn", "Việt", "Vinh", "Vũ", "Xuân", "Yên", "Ánh", "Ân", "Ôn", "Ấn", "Ẩn", "Bảo", "Bắc", "Bội", "Bửu", "Ca", "Cao", "Cát", "Chánh", "Chiến", "Chinh", "Chiến", "Chiều", "Chương", "Cơ", "Cương", "Danh", "Di", "Dinh", "Diệu", "Dũng", "Duy", "Đan", "Đạo", "Đắc", "Đạt", "Điền", "Định", "Đông", "Đức", "Giang", "Hạ", "Hải", "Hạnh", "Hầu", "Hiệp", "Hiếu", "Hoài", "Hoàn", "Hòa", "Hồng", "Hợp", "Huệ", "Hùng", "Hưởng", "Hữu", "Khải", "Khang", "Khánh", "Khắc", "Khoa", "Khôi", "Khuê", "Kiên", "Kim", "Kỳ", "Lâm", "Lân", "Lập", "Liêm", "Liên", "Linh", "Long", "Lợi", "Lộc", "Lực", "Lương", "Dương", "Nguyên","Anh","Ánh", "An", "Bảo", "Bình", "Chương", "Châu", "Chiến", "Ngọc", "Diễm", "Xuân", "Ngân", "Mai", "Minh", "Tuyền", "Thảo", "Thanh", "Trà", "Việt", "Giang", "Phát", "Đức", "Danh", "Đức", "Hạnh", "Sáng", "Khiêm", "Sa", "My", "Trinh", "Huyền", "Trâm", "Thủy", "Tú", "Hoàng", "Tin", "Ly", "Nhật", "Tuấn", "Nguyệt", "Thư", "Vy", "Như", "Trang", "Dũng", "Hiệp", "Huy", "Hải", "Kiệt", "Phúc", "Lan", "Nhi", "Hiếu", "Toàn", "Duyên", "Lệ", "Kiều", "Phương" ,"Quốc", "Hòa", "Khải", "Vinh", "Trường", "Tường", "Long", "Phước", "Quang", "Uyên", "Linh"]
middleName1 = ["", "Hoàng", "Văn", "Thị", "Hữu", "Minh", "Đức", "Đình", "Như", "Quang", "Thành", "Mạnh", "Trung", "Công", "Ngọc", "Hồng", "Thi", "Thảo", "Tùng", "Quốc", "Duy", "Thu",  "Mỹ", "An", "Thành", "Hoàng", "Hải", "Tuấn", "Lâm", "Thắng", "Bảo", "Hiếu", "Đại", "Gia", "Thúy", "Đan", "Nhân", "Linh", "Tú", "Nguyệt", "Khánh", "Sơn", "Thư", "Hoa", "Đông", "Tiến", "Thắm", "Hoài", "Nga", "Bình", "Tâm", "Hạnh", "Nhi", "Yến", "Khôi", "Thùy", "Hà", "Đức", "Hoàn", "Phong", "Cường", "Sương", "Tình", "Việt", "Bích", "Tín", "Nhiên", "Chương", "Dung", "Lan", "Nhung", "Long", "Hùng", "Thiện", "Cảnh", "Tuyết", "Nguyên", "Trọng", "Ngân", "Phúc", "Tường", "Bạch", "Phương", "Quỳnh", "Lợi", "Trí", "Danh", "Hiệp", "Hoàng", "Hạnh", "Chính", "Nguyên", "Bình", "Trâm", "Nghĩa", "Trọng", "Nhã", "Nghị", "Hậu", "Hồng", "Vân", "Trung","Bảo"] 
middleName2 = ["", "Hoàng", "Văn", "Thị", "Hữu", "Minh", "Đức", "Đình", "Như", "Quang", "Thành", "Mạnh", "Trung", "Công", "Ngọc", "Hồng", "Thi", "Thảo", "Tùng", "Quốc", "Duy", "Thu",  "Mỹ", "An", "Thành", "Hoàng", "Hải", "Tuấn", "Lâm", "Thắng", "Bảo", "Hiếu", "Đại", "Gia", "Thúy", "Đan", "Nhân", "Linh", "Tú", "Nguyệt", "Khánh", "Sơn", "Thư", "Hoa", "Đông", "Tiến", "Thắm", "Hoài", "Nga", "Bình", "Tâm", "Hạnh", "Nhi", "Yến", "Khôi", "Thùy", "Hà", "Đức", "Hoàn", "Phong", "Cường", "Sương", "Tình", "Việt", "Bích", "Tín", "Nhiên", "Chương", "Dung", "Lan", "Nhung", "Long", "Hùng", "Thiện", "Cảnh", "Tuyết", "Nguyên", "Trọng", "Ngân", "Phúc", "Tường", "Bạch", "Phương", "Quỳnh", "Lợi", "Trí", "Danh", "Hiệp", "Hoàng", "Hạnh", "Chính", "Nguyên", "Bình", "Trâm", "Nghĩa", "Trọng", "Nhã", "Nghị", "Hậu", "Hồng", "Vân", "Trung","Bảo"] 

so_luong_hoc_sinh = 1000000
index = 0
studentIndex_list = []

for _ in range(so_luong_hoc_sinh):
    studentsFirstName = unidecode(random.choice(firstName))
    studentsLastName = unidecode(random.choice(lastName))
    studentsMiddleName1 = unidecode(random.choice(middleName1))
    studentsMiddleName2 = unidecode(random.choice(middleName2))
    address = unidecode(''.join(random.choices(string.ascii_lowercase, k=20)))
    date = random_ngay_sinh()
    index = index + 1
    studentIndex = (str(index).zfill(10)) 
    studentIndex_list.append(studentIndex)
    studentFullFirstName = f"{studentsFirstName} {studentsMiddleName1} {studentsMiddleName2}"

    if kiem_tra_du_tuoi(date): 
        cccd = sinh_so_cccd() 
        values = f'"{studentIndex}", "{studentFullFirstName}", "{studentsLastName}", {cccd}, "{date}", "{address}"' 
    else:
        values = f'"{studentIndex}", "{studentFullFirstName}", "{studentsLastName}", NULL, "{date}", "{address}"' 
        
    insert_statement = (f'INSERT INTO HS VALUES ({values});\n').format(values) 
    cursor1.execute(insert_statement)    
    cursor2.execute(insert_statement)   
    if count == 200000:
            connection1.commit()
            connection2.commit()
            count = 0 
print("Đã insert xong bảng HS!")

#Tạo dữ liệu cho bảng HOC
count = 0 
schoolIndex_list = School_df['Ma_Truong']
for studentIndex in studentIndex_list : 
    year = random.randint(2018, 2024) 
    for i in range(0,3) : 

        x = schoolIndex_list.sample(n=1)
        schoolIndex = str(x.values)

        #Chuẩn hóa chuỗi nhận được s
        schoolIndex = schoolIndex.strip('[]')
        schoolIndex = schoolIndex.strip('\'\'')

        score = random.uniform(0,10) 
        if score >= 9:
            classify = "Xuat sac"
        elif score >= 8:
            classify = "Gioi"
        elif score >= 7:
            classify = "Kha"
        elif score >= 5:
            classify = "Trung binh"
        else:
            classify = "Yeu"

        #Tạo Kết quả 
        if score >= 5:
            result = "Hoan thanh"
        else:
            result = "Chua hoan thanh"
        
        #Tạo năm học 
        currentYear = (str(year+i).zfill(4))

        #Viết statement
        values = f'"{schoolIndex}", "{studentIndex}", "{currentYear}", {score}, "{unidecode(classify)}", "{unidecode(result)}"' 
        insert_statement = (f'INSERT INTO HOC VALUES ({values});\n').format(values) 
        cursor1.execute(insert_statement)
        cursor2.execute(insert_statement)
        count = count + 1 
        if count == 200000:
            connection1.commit()
            connection2.commit()
            count = 0 
print("Đã insert xong bảng HOC!")

# Đóng kết nối
cursor1.close()
cursor2.close()
connection1.close()
connection2.close()
