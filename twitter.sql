-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 16, 2018 alle 13:27
-- Versione del server: 5.5.59-0+deb8u1-log
-- PHP Version: 5.6.33-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `twitter`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `tweet`
--

CREATE TABLE IF NOT EXISTS `tweet` (
  `id_user` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_tweet` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `text` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` date NOT NULL,
  `favorite_count` int(11) DEFAULT NULL,
  `sensitive` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lan` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` varchar(30) NOT NULL DEFAULT '0',
  `screen_name` varchar(100) DEFAULT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL,
  `created_at` varchar(50) NOT NULL,
  `description` varchar(300) CHARACTER SET utf8mb4 NOT NULL,
  `lang` varchar(10) NOT NULL,
  `location` varchar(20) NOT NULL,
  `time_zone` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `user_ff`
--

CREATE TABLE IF NOT EXISTS `user_ff` (
  `id` varchar(30) NOT NULL DEFAULT '0',
  `tw_user_id` varchar(100) NOT NULL COMMENT 'Twitter user id (table: user > id)',
  `type` varchar(10) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL,
  `screen_name` varchar(100) DEFAULT NULL,
  `created_at` varchar(50) NOT NULL,
  `description` varchar(300) CHARACTER SET utf8mb4 NOT NULL,
  `lang` varchar(10) NOT NULL,
  `location` varchar(100) NOT NULL,
  `time_zone` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tweet`
--
ALTER TABLE `tweet`
 ADD PRIMARY KEY (`id_tweet`), ADD KEY `id_user` (`id_user`), ADD KEY `id_user_2` (`id_user`), ADD KEY `created_at` (`created_at`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_ff`
--
ALTER TABLE `user_ff`
 ADD PRIMARY KEY (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
