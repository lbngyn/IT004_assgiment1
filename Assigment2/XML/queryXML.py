import lxml.etree as ET
import os
import pandas as pd
import numpy as np

def query_students_by_score(xml_file, min_score, max_score):
    # Đọc tệp tin XML 
    tree = ET.parse(f'{xml_file}')
    root = tree.getroot()

    # Xpath truy vấn danh sách học sinh có điểm trung bình nằm trong ngưỡng điểm
    xpath_query = f".//HocSinh[DiemTB >= {min_score} and DiemTB <= {max_score}]"
    students = root.xpath(xpath_query)

    # In danh sách học sinh
    for student in students:
        ho = student.find("Ho").text
        ten = student.find("Ten").text
        diem = float(student.find("DiemTB").text)
        print(f"Họ tên: {ho} {ten} -- Điểm trung bình: {diem}")

#Lấy đường dẫn đến file XML 
XML_file = input("Nhap duong dan cua file XML: ")

# Nhập min và max 
min_score = float(input("Nhap so diem thap: "))
max_score = float(input("Nhap so diem cao: "))

# Thực hiện truy vấn danh sách học sinh từ tệp tin XML đã xuất ra từ câu 4
query_students_by_score(XML_file, min_score, max_score)
