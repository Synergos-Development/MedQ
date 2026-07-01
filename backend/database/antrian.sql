-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 24, 2026 at 10:21 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbmedq`
--

-- --------------------------------------------------------

--
-- Table structure for table `antrian`
--

CREATE TABLE `antrian` (
  `id_antrian` int NOT NULL,
  `nomor_antrian` varchar(20) NOT NULL,
  `id_pasien` int NOT NULL,
  `id_poli` int NOT NULL,
  `id_dokter` int NOT NULL,
  `tanggal` date NOT NULL,
  `status` enum('Menunggu','Dipanggil','Diperiksa','Selesai','Batal') DEFAULT NULL,
  `waktu_daftar` datetime DEFAULT NULL,
  `waktu_dipanggil` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `antrian`
--

INSERT INTO `antrian` (`id_antrian`, `nomor_antrian`, `id_pasien`, `id_poli`, `id_dokter`, `tanggal`, `status`, `waktu_daftar`, `waktu_dipanggil`) VALUES
(1, 'UMUM-001', 1, 1, 1, '2026-06-23', 'Selesai', '2026-06-23 22:07:43', '2026-06-23 22:45:05'),
(2, 'UMUM-002', 2, 1, 1, '2026-06-23', 'Dipanggil', '2026-06-23 22:12:14', '2026-06-23 22:45:17'),
(4, 'UMUM-003', 4, 1, 1, '2026-06-23', 'Dipanggil', '2026-06-23 22:44:03', '2026-06-23 22:45:21'),
(5, 'MATA-001', 5, 5, 6, '2026-06-24', 'Dipanggil', '2026-06-24 15:30:17', '2026-06-24 16:59:06'),
(6, 'JANTUNG-001', 6, 3, 4, '2026-06-24', 'Dipanggil', '2026-06-24 17:13:23', '2026-06-24 17:13:55');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `antrian`
--
ALTER TABLE `antrian`
  ADD PRIMARY KEY (`id_antrian`),
  ADD UNIQUE KEY `nomor_antrian` (`nomor_antrian`),
  ADD KEY `id_pasien` (`id_pasien`),
  ADD KEY `id_poli` (`id_poli`),
  ADD KEY `id_dokter` (`id_dokter`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `antrian`
--
ALTER TABLE `antrian`
  MODIFY `id_antrian` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `antrian`
--
ALTER TABLE `antrian`
  ADD CONSTRAINT `antrian_ibfk_1` FOREIGN KEY (`id_pasien`) REFERENCES `pasien` (`id_pasien`),
  ADD CONSTRAINT `antrian_ibfk_2` FOREIGN KEY (`id_poli`) REFERENCES `poli` (`id_poli`),
  ADD CONSTRAINT `antrian_ibfk_3` FOREIGN KEY (`id_dokter`) REFERENCES `dokter` (`id_dokter`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
