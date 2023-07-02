import mysql.connector
import xml.etree.ElementTree as ET
import time
import xml.dom.minidom

#Thực hiện truy vấn
def query(): 
    # Input
    print("Nhap database: ", end = ""); your_database = input()
    print("Nhap truong: ", end = ""); truong = input()
    print("Nhap nam hoc: ", end = ""); namhoc = input()  #(2018, 2024)
    print("Nhap xep loai: ", end = ""); xeploai = input() #Xuat sac, Gioi, Kha, Trung binh, Yeu

    # Kết nối tới cơ sở dữ liệu MySQL
    connection = mysql.connector.connect(
        host = localhost,
        user = your_username,
        password = your_password,
        database = your_database
    )
    # Tạo đối tượng cursor
    cursor = connection.cursor()

    # Tạo câu truy vấn để lấy danh sách học sinh
    query = f"""
SELECT HS.HO, HS.TEN, HS.NTNS, HOC.DIEMTB, HOC.XEPLOAI, HOC.KQUA
FROM HS
JOIN HOC ON HS.MAHS = HOC.MAHS
JOIN TRUONG ON HOC.MATR = TRUONG.MATR
WHERE TRUONG.TENTR = '{truong}' AND HOC.NAMHOC = {namhoc} AND HOC.XEPLOAI = '{xeploai}';
    """
    # Thực thi câu truy vấn và đo thời gian truy vấn
    start_time = time.time()
    cursor.execute(query)
    end_time = time.time()
    execution_time = end_time - start_time

    # Lấy kết quả truy vấn
    results = cursor.fetchall()

    # Tạo danh sách học sinh dưới dạng cây XML
    root = ET.Element("Root")  # Create a root element
    hoc_sinh_list = ET.SubElement(root, "HocSinhList")  # Create the HocSinhList element

    for result in results:
        ho, ten, ntns, diemtb, xeploai, kqua = result
        hoc_sinh = ET.SubElement(hoc_sinh_list, "HocSinh")
        ET.SubElement(hoc_sinh, "Ho").text = ho
        ET.SubElement(hoc_sinh, "Ten").text = ten
        ET.SubElement(hoc_sinh, "NTNS").text = str(ntns)
        ET.SubElement(hoc_sinh, "DiemTB").text = str(float(diemtb))
        ET.SubElement(hoc_sinh, "XepLoai").text = xeploai
        ET.SubElement(hoc_sinh, "KetQua").text = kqua

    thoigian_truy_van = ET.SubElement(root, "Thoigiantruyvan")  # Create the Thoigiantruyvan element
    thoigian_truy_van.text = f"{execution_time}"  # Set the text value for Thoigiantruyvan

    # Tạo tên file XML dựa trên thông tin đầu vào
    file_name = f"XML\{your_database}-{truong}-{namhoc}-{xeploai}.xml"
    
    # Ghi danh sách học sinh vào file XML
    xml_string = ET.tostring(root, encoding="utf-8")
    dom = xml.dom.minidom.parseString(xml_string)
    pretty_xml_string = dom.toprettyxml()

    with open(file_name, "w") as file:
        file.write(pretty_xml_string)
    
    #In ra màn hình thời gian chạy truy vấn 
    print(f"Thời gian thực hiện truy vấn: {execution_time} seconds")
    
    # Đóng kết nối
    cursor.close()
    connection.close()

#Nhập các thông tin để connect vào mysql 
print("Nhập localhost: ", end=""); localhost = input() 
print("Nhập user: ", end=""); your_username = input() 
print("Nhập password: ", end=""); your_password = input() 

while True: 
    query() 
    print(
f"""
------------------------------------------------------------------------
Ban co muon tiep tuc truy van khong? 
Nhap 'n' de thoat chuong trinh!
Nhap bat ki ki tu khac de tiep tuc!"""
) 
    signal = input() 
    if signal == 'n' : 
        print("Ket thuc!") 
        break
