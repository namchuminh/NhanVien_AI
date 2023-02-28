-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 28, 2023 at 05:55 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nhanvien_ai`
--

-- --------------------------------------------------------

--
-- Table structure for table `chamcong`
--

CREATE TABLE `chamcong` (
  `MaChamCong` int(11) NOT NULL,
  `MaNhanVien` varchar(11) COLLATE utf8_unicode_ci NOT NULL,
  `DaChamCong` int(11) NOT NULL,
  `ThoiGian` date DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `chamcong`
--

INSERT INTO `chamcong` (`MaChamCong`, `MaNhanVien`, `DaChamCong`, `ThoiGian`) VALUES
(14, 'NV01', 1, '2023-02-28');

-- --------------------------------------------------------

--
-- Table structure for table `nhanvien`
--

CREATE TABLE `nhanvien` (
  `MaNhanVien` varchar(11) COLLATE utf8_unicode_ci NOT NULL,
  `TenNhanVien` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
  `GioiTinh` varchar(11) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'Nam',
  `ChucVu` varchar(25) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'Nhân Viên',
  `Avatar` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `nhanvien`
--

INSERT INTO `nhanvien` (`MaNhanVien`, `TenNhanVien`, `GioiTinh`, `ChucVu`, `Avatar`) VALUES
('NV01', 'Chu Minh Ngọc', 'Nam', 'Quản Lý', 'avatar.png'),
('NV02', 'Trần Ngọc Hà', 'Nữ', 'Nhân Viên', 'anh-avatar-facebook-nu-toc-dai-buoc-no.jpg'),
('NV03', 'Phùng Thái Sơn', 'Nam', 'Nhân Viên', 'anh-avatar-supreme-dep-lam-dai-dien-facebook.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `tinhluong`
--

CREATE TABLE `tinhluong` (
  `MaTinhLuong` int(11) NOT NULL,
  `MaNhanVien` varchar(11) COLLATE utf8_unicode_ci NOT NULL,
  `SoCong` int(11) NOT NULL DEFAULT 0,
  `Thuong` int(11) NOT NULL DEFAULT 0,
  `Phat` int(11) NOT NULL DEFAULT 0,
  `HeSoLuong` int(11) NOT NULL DEFAULT 0,
  `ThoiGian` date NOT NULL DEFAULT current_timestamp(),
  `TrangThai` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `tinhluong`
--

INSERT INTO `tinhluong` (`MaTinhLuong`, `MaNhanVien`, `SoCong`, `Thuong`, `Phat`, `HeSoLuong`, `ThoiGian`, `TrangThai`) VALUES
(3, 'NV02', 1, 0, 0, 300, '2023-02-21', 0),
(5, 'NV03', 0, 0, 0, 200, '2023-02-22', 0),
(11, 'NV02', 1, 100, 0, 250, '2023-01-01', 0),
(12, 'NV02', 1, 100, 0, 250, '2023-01-02', 0),
(13, 'NV02', 1, 100, 0, 250, '2023-01-03', 0),
(14, 'NV02', 1, 100, 0, 250, '2023-01-04', 0),
(15, 'NV03', 1, 50, 0, 200, '2023-01-01', 0),
(16, 'NV03', 1, 50, 0, 200, '2023-01-02', 0),
(17, 'NV03', 1, 50, 0, 200, '2023-01-03', 0),
(18, 'NV03', 1, 50, 0, 200, '2023-01-04', 0),
(35, 'NV01', 0, 0, 0, 500, '2023-02-28', 0),
(36, 'NV01', 1, 0, 0, 500, '2023-02-28', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `chamcong`
--
ALTER TABLE `chamcong`
  ADD PRIMARY KEY (`MaChamCong`),
  ADD KEY `MaNhanVien` (`MaNhanVien`);

--
-- Indexes for table `nhanvien`
--
ALTER TABLE `nhanvien`
  ADD PRIMARY KEY (`MaNhanVien`);

--
-- Indexes for table `tinhluong`
--
ALTER TABLE `tinhluong`
  ADD PRIMARY KEY (`MaTinhLuong`),
  ADD KEY `MaNhanVien` (`MaNhanVien`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `chamcong`
--
ALTER TABLE `chamcong`
  MODIFY `MaChamCong` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `tinhluong`
--
ALTER TABLE `tinhluong`
  MODIFY `MaTinhLuong` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chamcong`
--
ALTER TABLE `chamcong`
  ADD CONSTRAINT `chamcong_ibfk_1` FOREIGN KEY (`MaNhanVien`) REFERENCES `nhanvien` (`MaNhanVien`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tinhluong`
--
ALTER TABLE `tinhluong`
  ADD CONSTRAINT `tinhluong_ibfk_1` FOREIGN KEY (`MaNhanVien`) REFERENCES `nhanvien` (`MaNhanVien`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
