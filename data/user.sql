-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        8.0.30 - MySQL Community Server - GPL
-- 服务器操作系统:                      Win64
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

-- 导出  表 flaskblog.user 结构
CREATE TABLE IF NOT EXISTS `user` (
  `add_date` datetime NOT NULL,
  `pub_date` datetime NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password` varchar(320) NOT NULL,
  `avatar` varchar(200) DEFAULT NULL,
  `is_super_user` tinyint(1) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `is_staff` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  flaskblog.user 的数据：~3 rows (大约)
INSERT INTO `user` (`add_date`, `pub_date`, `id`, `username`, `password`, `avatar`, `is_super_user`, `is_active`, `is_staff`) VALUES
	('2022-09-28 07:28:13', '2022-10-13 06:49:37', 1, 'ceshi', 'pbkdf2:sha256:260000$Pq43VcioW9WX2YMw$7da1ac3799d7f4d52408b20baa9ffd290abd40ef420604f446808cc7abb8e932', 'avatar/cf6f64be73f145ac84046d6531d2ee24.jpg', 1, 1, 0),
	('2022-10-11 02:06:25', '2022-10-11 08:27:54', 2, 'admin', 'pbkdf2:sha256:260000$BLfP7DA2V6iP8fpN$6912ece1bb49e8b61f9b6e3cf6db4ce92a634d442d59668dee40330002b0b3c9', 'avatar/d0690074e80e4fd9a34e99ea8165ea11.jpg', 1, 1, 1),
	('2022-10-11 08:28:57', '2022-10-13 06:49:44', 4, 'test', 'pbkdf2:sha256:260000$0tiK9Dizt40C7QYE$a916dc98b7c091d1dd963589ed2f1a9176fa1397e1a3e6d3a5fce98bf3c1771a', 'avatar/b8b46e87e6b04fbfb990b3fe758cc16f.gif', 0, 1, 0);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
