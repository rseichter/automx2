-- MySQL 8.0.23 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `automx2`;
CREATE DATABASE `automx2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `automx2`;

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `alembic_version` (`version_num`) VALUES
('5334f8a8282c');

CREATE TABLE `domain` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `provider_id` int NOT NULL,
  `ldapserver_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ldapserver_id` (`ldapserver_id`),
  KEY `provider_id` (`provider_id`),
  CONSTRAINT `domain_ibfk_1` FOREIGN KEY (`ldapserver_id`) REFERENCES `ldapserver` (`id`),
  CONSTRAINT `domain_ibfk_2` FOREIGN KEY (`provider_id`) REFERENCES `provider` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `domain` (`id`, `name`, `provider_id`, `ldapserver_id`) VALUES
(2, 'example.com', 100, NULL);

CREATE TABLE `ldapserver` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `port` int NOT NULL,
  `use_ssl` tinyint(1) NOT NULL,
  `search_base` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `search_filter` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `attr_uid` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `attr_cn` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `bind_password` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `bind_user` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `ldapserver_chk_1` CHECK ((`use_ssl` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `provider` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `short_name` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `provider` (`id`, `name`, `short_name`) VALUES
(100, 'Example Inc.', 'Example');

CREATE TABLE `server` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `port` int NOT NULL,
  `type` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `socket_type` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `user_name` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `authentication` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `prio` int NOT NULL DEFAULT '10',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `server` (`id`, `name`, `port`, `type`, `socket_type`, `user_name`, `authentication`, `prio`) VALUES
(1, 'imap.example.com', 993, 'imap', 'SSL', '%EMAILADDRESS%', 'plain', 10),
(2, 'smtp.example.com', 587, 'smtp', 'STARTTLS', '%EMAILADDRESS%', 'plain', 10);

CREATE TABLE `server_domain` (
  `server_id` int NOT NULL,
  `domain_id` int NOT NULL,
  PRIMARY KEY (`server_id`,`domain_id`),
  KEY `domain_id` (`domain_id`),
  CONSTRAINT `server_domain_ibfk_1` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`),
  CONSTRAINT `server_domain_ibfk_2` FOREIGN KEY (`server_id`) REFERENCES `server` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `server_domain` (`server_id`, `domain_id`) VALUES
(1, 2),
(2, 2);
