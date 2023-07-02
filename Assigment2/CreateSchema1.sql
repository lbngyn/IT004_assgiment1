DROP DATABASE IF EXISTS TRUONGHOC1; 
CREATE DATABASE TRUONGHOC1;
USE TRUONGHOC1;
SET NAMES utf8;

DROP TABLE IF EXISTS TRUONG ;
CREATE TABLE TRUONG(
    MATR VARCHAR(20) PRIMARY KEY,
	TENTR VARCHAR(100) NOT NULL,
    DCHITR VARCHAR(255) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE INDEX IX_TRUONG_MATR ON TRUONG (MATR);

DROP TABLE IF EXISTS HS;
CREATE TABLE HS(
    MAHS VARCHAR(20) PRIMARY KEY,
    HO VARCHAR(50) NOT NULL,
    TEN VARCHAR(10) NOT NULL,
    CCCD VARCHAR(20),
    NTNS DATE NOT NULL,
    DCHI_HS VARCHAR(100) NOT NULL,
    CONSTRAINT UQ_HS_CCCD UNIQUE (CCCD)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE INDEX IX_HS_MAHS ON HS (MAHS);

DROP TABLE IF EXISTS HOC;
CREATE TABLE HOC(
    MATR VARCHAR(20),
    MAHS VARCHAR(20),
    NAMHOC INT,
    DIEMTB DECIMAL(3, 1) NOT NULL,
    XEPLOAI VARCHAR(20) NOT NULL,
    KQUA VARCHAR(20) NOT NULL,
    PRIMARY KEY (MATR, MAHS, NAMHOC),
    CONSTRAINT FK_HOC_MATR FOREIGN KEY (MATR) REFERENCES TRUONG(MATR),
    CONSTRAINT FK_HOC_MAHS FOREIGN KEY (MAHS) REFERENCES HS(MAHS)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE INDEX IX_HOC_MATR_MAHS_NAMHOC ON HOC (MATR, MAHS, NAMHOC);