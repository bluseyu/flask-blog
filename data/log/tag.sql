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

-- 导出  表 flaskblog.tag 结构
CREATE TABLE IF NOT EXISTS `tag` (
  `add_date` datetime NOT NULL,
  `pub_date` datetime NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  flaskblog.tag 的数据：~34 rows (大约)
INSERT INTO `tag` (`add_date`, `pub_date`, `id`, `name`) VALUES
	('2022-10-09 16:12:27', '2022-10-09 16:12:27', 1, 'Python'),
	('2022-10-09 16:13:03', '2022-10-09 16:13:03', 2, 'Flask'),
	('2022-10-10 16:00:14', '2022-10-10 16:01:21', 3, 'CSS'),
	('2022-10-10 16:02:18', '2022-10-10 16:02:18', 4, 'HTML'),
	('2022-10-10 16:02:38', '2022-10-10 16:02:38', 5, 'JavaScript'),
	('2022-10-10 16:04:29', '2022-10-10 16:04:29', 6, 'node.js'),
	('2022-10-10 16:04:47', '2022-10-10 16:04:47', 7, 'Vue.js'),
	('2022-10-10 16:05:37', '2022-10-10 16:05:37', 8, 'Express'),
	('2022-10-10 16:06:00', '2022-10-10 16:06:00', 9, 'Django'),
	('2022-10-10 16:06:20', '2022-10-10 17:20:19', 10, 'React'),
	('2022-10-12 10:49:59', '2022-10-12 10:49:59', 11, 'Web'),
	('2022-10-12 10:50:10', '2022-10-12 10:50:10', 12, '人工智能'),
	('2022-10-12 10:50:29', '2022-10-12 10:50:29', 13, '大数据'),
	('2022-10-12 10:51:09', '2022-10-12 10:51:09', 14, '学习笔记'),
	('2022-10-12 15:26:53', '2022-10-12 15:26:53', 15, 'SQL'),
	('2022-10-12 15:28:02', '2022-10-12 15:28:02', 16, 'VSCode'),
	('2022-10-17 16:11:05', '2022-10-17 16:11:05', 17, '吐槽'),
	('2022-10-17 16:12:05', '2022-10-17 16:12:05', 18, '随笔'),
	('2022-10-17 16:13:05', '2022-10-17 16:13:05', 19, '写作'),
	('2022-10-17 16:14:05', '2022-10-17 16:14:05', 20, '脑洞'),
	('2022-10-17 16:15:05', '2022-10-17 16:15:05', 21, '灵感'),
	('2022-10-17 16:16:05', '2022-10-17 16:16:05', 22, '插画'),
	('2022-10-17 16:39:29', '2022-10-17 16:39:29', 23, '测试'),
	('2022-10-18 09:07:54', '2022-10-18 09:07:54', 24, '管理'),
	('2022-10-18 09:08:54', '2022-10-18 09:08:54', 25, '心智'),
	('2022-10-18 09:09:54', '2022-10-18 09:09:54', 26, '思维模式'),
	('2022-10-18 17:51:54', '2022-10-18 17:51:54', 27, '健康'),
	('2022-10-18 17:52:54', '2022-10-18 17:52:54', 28, '运动'),
	('2022-10-18 17:53:54', '2022-10-18 17:53:54', 29, '亲子'),
	('2022-10-18 17:54:54', '2022-10-18 17:54:54', 30, '励志'),
	('2022-10-19 08:40:23', '2022-10-19 08:40:23', 31, '美图'),
	('2022-10-19 09:46:28', '2022-10-19 09:46:28', 32, '美女'),
	('2022-10-19 14:38:23', '2022-10-19 14:38:23', 33, '认知'),
	('2022-10-19 17:07:26', '2022-10-19 17:07:26', 34, '武学');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
