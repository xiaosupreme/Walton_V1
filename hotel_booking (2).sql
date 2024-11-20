-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 20, 2024 at 06:47 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel_booking`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `room_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` enum('Ongoing','Completed') DEFAULT 'Ongoing',
  `final_price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `username`, `room_id`, `start_date`, `end_date`, `status`, `final_price`) VALUES
(1, 'user', 1, '2024-11-18', '2024-11-18', 'Completed', '0.00'),
(2, 'user', 3, '2024-11-18', '2024-11-18', 'Completed', '0.00'),
(3, 'user2', 3, '2024-11-18', '2024-11-18', 'Completed', '0.00'),
(4, 'user', 2, '2024-11-18', '2024-11-18', 'Completed', '0.00'),
(5, 'user2', 2, '2024-11-18', '2024-11-18', 'Completed', '0.00'),
(6, 'user', 5, '2024-11-18', '2024-11-18', 'Completed', '0.00'),
(7, 'user2', 5, '2024-11-18', '2024-11-19', 'Completed', '0.00'),
(8, 'user', 5, '2024-11-21', '2024-11-19', 'Completed', '0.00'),
(9, 'user', 11, '2024-11-22', '2024-11-23', 'Ongoing', '0.00'),
(10, 'user2', 7, '2024-11-18', '2024-11-19', 'Ongoing', '0.00'),
(11, 'user', 23, '2024-11-20', '2024-11-21', 'Ongoing', '0.00'),
(12, 'user', 12, '2024-11-19', '2024-11-19', 'Ongoing', '0.00'),
(13, 'user', 13, '2024-11-19', '2024-11-26', 'Ongoing', '11760.00'),
(14, 'user', 50, '2024-12-28', '2024-12-31', 'Ongoing', '28125.00'),
(15, 'user', 46, '2024-12-28', '2024-12-31', 'Ongoing', '28125.00'),
(16, 'user2', 41, '2024-11-19', '2024-11-19', 'Ongoing', '0.00'),
(17, 'user2', 12, '2024-12-20', '2024-12-26', 'Ongoing', '9120.00'),
(18, 'user', 11, '2024-11-19', '2024-11-19', 'Ongoing', '0.00'),
(19, 'user2', 1, '2024-11-19', '2024-11-19', 'Ongoing', '0.00'),
(20, 'user2', 24, '2024-11-19', '2024-11-19', 'Ongoing', '0.00'),
(21, 'user', 1, '2024-11-20', '2024-11-20', 'Ongoing', '0.00'),
(22, 'user', 22, '2024-11-20', '2024-11-21', 'Ongoing', '2500.00'),
(23, 'user', 21, '2024-11-19', '2024-11-19', 'Ongoing', '0.00'),
(24, 'user2', 11, '2024-11-20', '2024-11-21', 'Ongoing', '1520.00'),
(25, 'user2', 12, '2024-11-20', '2024-11-21', 'Ongoing', '1520.00'),
(26, 'user2', 17, '2024-11-21', '2024-11-22', 'Ongoing', '1520.00'),
(27, 'user', 5, '2024-11-19', '2024-11-20', 'Ongoing', '760.00'),
(28, 'user', 9, '2024-11-19', '2024-11-20', 'Ongoing', '760.00'),
(29, 'user', 2, '2024-11-22', '2024-11-23', 'Ongoing', '760.00'),
(30, 'user', 1, '2024-12-02', '2025-01-07', 'Ongoing', '27360.00'),
(31, 'user', 31, '2024-11-19', '2024-11-20', 'Ongoing', '4750.00'),
(32, 'user2', 31, '2024-11-21', '2024-11-23', 'Ongoing', '10000.00'),
(33, 'user2', 47, '2024-11-29', '2024-11-30', 'Ongoing', '7500.00'),
(34, 'user', 41, '2024-12-19', '2025-01-20', 'Ongoing', '300000.00');

-- --------------------------------------------------------

--
-- Table structure for table `booking_requests`
--

CREATE TABLE `booking_requests` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `room_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  `final_price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking_requests`
--

INSERT INTO `booking_requests` (`id`, `username`, `room_id`, `start_date`, `end_date`, `status`, `final_price`) VALUES
(13, 'user', 6, '2024-11-18', '2024-11-18', 'Pending', '0.00'),
(14, 'user', 13, '2024-11-18', '2024-11-18', 'Pending', '0.00'),
(15, 'user', 8, '2024-11-18', '2024-11-19', 'Pending', '0.00'),
(16, 'user', 14, '2024-11-18', '2024-11-19', 'Pending', '0.00'),
(17, 'user', 9, '2024-11-18', '2024-11-19', 'Pending', '0.00'),
(18, 'user', 41, '2024-11-19', '2024-11-19', 'Pending', '0.00'),
(23, 'user', 50, '2024-12-28', '2024-12-31', 'Rejected', '28125.00'),
(24, 'user', 50, '2024-12-28', '2024-12-31', 'Rejected', '28125.00'),
(26, 'user', 46, '2024-12-28', '2024-12-31', 'Rejected', '28125.00'),
(27, 'walton', 41, '2024-11-19', '2024-11-19', 'Pending', '0.00'),
(28, 'walton', 2, '2024-11-19', '2024-11-19', 'Pending', '0.00'),
(29, 'walton', 2, '2024-11-19', '2024-11-19', 'Pending', '0.00'),
(30, 'walton', 14, '2024-11-19', '2024-11-19', 'Pending', '0.00'),
(31, 'walton', 2, '2024-11-21', '2024-11-23', 'Pending', '2000.00'),
(32, 'walton', 10, '2024-11-19', '2024-11-19', 'Pending', '0.00'),
(33, 'walton', 10, '2024-11-19', '2024-11-20', 'Pending', '950.00'),
(34, 'walton', 42, '2025-02-27', '2025-02-28', 'Pending', '7500.00'),
(35, 'walton', 3, '2024-11-19', '2024-11-20', 'Pending', '950.00');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `id` int(11) NOT NULL,
  `room_type` enum('Single','Double','Family','Deluxe','Suite') NOT NULL,
  `room_number` varchar(10) NOT NULL,
  `is_available` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`id`, `room_type`, `room_number`, `is_available`) VALUES
(1, 'Single', 'S101', 1),
(2, 'Single', 'S102', 1),
(3, 'Single', 'S103', 1),
(4, 'Single', 'S104', 1),
(5, 'Single', 'S105', 1),
(6, 'Single', 'S106', 1),
(7, 'Single', 'S107', 1),
(8, 'Single', 'S108', 1),
(9, 'Single', 'S109', 1),
(10, 'Single', 'S110', 1),
(11, 'Double', 'D201', 1),
(12, 'Double', 'D202', 1),
(13, 'Double', 'D203', 1),
(14, 'Double', 'D204', 1),
(15, 'Double', 'D205', 1),
(16, 'Double', 'D206', 1),
(17, 'Double', 'D207', 1),
(18, 'Double', 'D208', 1),
(19, 'Double', 'D209', 1),
(20, 'Double', 'D210', 1),
(21, 'Family', 'F301', 1),
(22, 'Family', 'F302', 1),
(23, 'Family', 'F303', 1),
(24, 'Family', 'F304', 1),
(25, 'Family', 'F305', 1),
(26, 'Family', 'F306', 1),
(27, 'Family', 'F307', 1),
(28, 'Family', 'F308', 1),
(29, 'Family', 'F309', 1),
(30, 'Family', 'F310', 1),
(31, 'Deluxe', 'DL401', 1),
(32, 'Deluxe', 'DL402', 1),
(33, 'Deluxe', 'DL403', 1),
(34, 'Deluxe', 'DL404', 1),
(35, 'Deluxe', 'DL405', 1),
(36, 'Deluxe', 'DL406', 1),
(37, 'Deluxe', 'DL407', 1),
(38, 'Deluxe', 'DL408', 1),
(39, 'Deluxe', 'DL409', 1),
(40, 'Deluxe', 'DL410', 1),
(41, 'Suite', 'SU501', 1),
(42, 'Suite', 'SU502', 1),
(43, 'Suite', 'SU503', 1),
(44, 'Suite', 'SU504', 1),
(45, 'Suite', 'SU505', 1),
(46, 'Suite', 'SU506', 1),
(47, 'Suite', 'SU507', 1),
(48, 'Suite', 'SU508', 1),
(49, 'Suite', 'SU509', 1),
(50, 'Suite', 'SU510', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(1, 'walton', 'scrypt:32768:8:1$wdNR6XnKeBPGBGRp$56acf1840cd9febf351a3864ad18102ba6d086794bc212ec71ef81470702ef606ffe28c65d8b4ebfe7eb9501c95d6c94369fdb00e6ae3245aa2b1b7973e2aa57', 'admin'),
(2, 'user', 'scrypt:32768:8:1$sgWy1tSBgDHgZBDM$483f5f880038a925323aea850a7c51ba4b658e031b34721eaef6b99bb7dc7e80c25f326b17b1ed4616ecfe545950a6e3c3667b0d830cebe4faeb64a206911d9f', 'user'),
(3, 'user2', 'scrypt:32768:8:1$ZOKq2Lx8McF5CTsw$b012a648031f8dbaa9675627271acc0fdb79f79370007be47c124bb02f1b99f047b08a05dbea86addd7a16924728029ff3a9356e08f04b38743a68d75b0dfd57', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `booking_requests`
--
ALTER TABLE `booking_requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `room_number` (`room_number`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `booking_requests`
--
ALTER TABLE `booking_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `booking_requests`
--
ALTER TABLE `booking_requests`
  ADD CONSTRAINT `booking_requests_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
