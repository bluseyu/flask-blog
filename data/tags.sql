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

-- 导出  表 flaskblog.tags 结构
CREATE TABLE IF NOT EXISTS `tags` (
  `tag_id` int NOT NULL,
  `post_id` int NOT NULL,
  PRIMARY KEY (`tag_id`,`post_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `tags_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`),
  CONSTRAINT `tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  flaskblog.tags 的数据：~51 rows (大约)
INSERT INTO `tags` (`tag_id`, `post_id`) VALUES
	(1, 1),
	(2, 1),
	(6, 2),
	(15, 3),
	(1, 4),
	(3, 6),
	(2, 7),
	(11, 7),
	(3, 8),
	(3, 9),
	(1, 10),
	(2, 10),
	(14, 10),
	(3, 11),
	(15, 12),
	(19, 13),
	(6, 14),
	(23, 15),
	(19, 16),
	(19, 17),
	(19, 18),
	(19, 19),
	(3, 20),
	(22, 21),
	(23, 24),
	(1, 25),
	(25, 26),
	(1, 27),
	(25, 28),
	(26, 28),
	(31, 29),
	(32, 29),
	(31, 30),
	(32, 30),
	(31, 31),
	(32, 31),
	(25, 32),
	(33, 32),
	(33, 33),
	(18, 34),
	(34, 34),
	(18, 35),
	(34, 35),
	(25, 37),
	(33, 37),
	(18, 38),
	(36, 39),
	(37, 39),
	(38, 40),
	(29, 41),
	(33, 41);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
