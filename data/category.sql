-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        8.0.30 - MySQL Community Server - GPL
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 导出 flaskblog 的数据库结构
CREATE DATABASE IF NOT EXISTS `flaskblog` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `flaskblog`;

-- 导出  表 flaskblog.category 结构
CREATE TABLE IF NOT EXISTS `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `icon` varchar(128) DEFAULT NULL,
  `add_date` datetime NOT NULL,
  `pub_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  flaskblog.category 的数据：~7 rows (大约)
INSERT INTO `category` (`id`, `name`, `icon`, `add_date`, `pub_date`) VALUES
	(1, '程序开发', '', '2022-10-09 10:21:37', '2022-10-17 16:11:05'),
	(2, '项目与产品', '', '2022-10-09 10:21:54', '2022-10-17 16:12:24'),
	(3, '创业邦', '', '2022-10-09 10:23:23', '2022-10-17 16:14:15'),
	(4, '读书与思考', '', '2022-10-09 10:23:39', '2022-10-17 16:15:48'),
	(7, '随笔与写作', '', '2022-10-11 16:57:02', '2022-10-17 16:18:37'),
	(8, '摸鱼儿', '', '2022-10-11 16:57:11', '2022-10-17 16:45:50'),
	(9, '涨姿势', '', '2022-10-17 16:16:35', '2022-10-17 16:17:23');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
