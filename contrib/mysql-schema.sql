-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `davserver`
--

DROP TABLE IF EXISTS `davserver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `davserver` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(128) NOT NULL,
  `port` int NOT NULL,
  `type` varchar(32) NOT NULL,
  `use_ssl` tinyint(1) NOT NULL,
  `domain_required` tinyint(1) NOT NULL,
  `user_name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `davserver_chk_1` CHECK ((`use_ssl` in (0,1))),
  CONSTRAINT `davserver_chk_2` CHECK ((`domain_required` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=4102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `davserver_domain`
--

DROP TABLE IF EXISTS `davserver_domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `davserver_domain` (
  `davserver_id` int NOT NULL,
  `domain_id` int NOT NULL,
  PRIMARY KEY (`davserver_id`,`domain_id`),
  KEY `domain_id` (`domain_id`),
  CONSTRAINT `davserver_domain_ibfk_1` FOREIGN KEY (`davserver_id`) REFERENCES `davserver` (`id`),
  CONSTRAINT `davserver_domain_ibfk_2` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `domain`
--

DROP TABLE IF EXISTS `domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `domain` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `provider_id` int NOT NULL,
  `ldapserver_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `provider_id` (`provider_id`),
  KEY `ldapserver_id` (`ldapserver_id`),
  CONSTRAINT `domain_ibfk_1` FOREIGN KEY (`provider_id`) REFERENCES `provider` (`id`),
  CONSTRAINT `domain_ibfk_2` FOREIGN KEY (`ldapserver_id`) REFERENCES `ldapserver` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3005 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ldapserver`
--

DROP TABLE IF EXISTS `ldapserver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ldapserver` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `port` int NOT NULL,
  `use_ssl` tinyint(1) NOT NULL,
  `search_base` varchar(128) NOT NULL,
  `search_filter` varchar(128) NOT NULL,
  `attr_uid` varchar(32) NOT NULL,
  `attr_cn` varchar(32) DEFAULT NULL,
  `bind_password` varchar(128) DEFAULT NULL,
  `bind_user` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `ldapserver_chk_1` CHECK ((`use_ssl` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `provider`
--

DROP TABLE IF EXISTS `provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `provider` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `short_name` varchar(32) NOT NULL,
  `sign` tinyint(1) DEFAULT 0 NOT NULL,
  `sign_cert` text NULL,
  `sign_key` text NULL
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1003 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `server`
--

DROP TABLE IF EXISTS `server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `server` (
  `id` int NOT NULL AUTO_INCREMENT,
  `prio` int NOT NULL DEFAULT '10',
  `name` varchar(128) NOT NULL,
  `port` int NOT NULL,
  `type` varchar(32) NOT NULL,
  `socket_type` varchar(32) NOT NULL,
  `user_name` varchar(64) NOT NULL,
  `authentication` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4006 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `server_domain`
--

DROP TABLE IF EXISTS `server_domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `server_domain` (
  `server_id` int NOT NULL,
  `domain_id` int NOT NULL,
  PRIMARY KEY (`server_id`,`domain_id`),
  KEY `domain_id` (`domain_id`),
  CONSTRAINT `server_domain_ibfk_1` FOREIGN KEY (`server_id`) REFERENCES `server` (`id`),
  CONSTRAINT `server_domain_ibfk_2` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-04 15:35:19
