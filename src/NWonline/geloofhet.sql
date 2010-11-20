-- MySQL dump 10.13  Distrib 5.1.50, for Win32 (ia32)
--
-- Host: localhost    Database: geloofhet
-- ------------------------------------------------------
-- Server version	5.1.50-community-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_425ae3c4` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add message',4,'add_message'),(11,'Can change message',4,'change_message'),(12,'Can delete message',4,'delete_message'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add site',7,'add_site'),(20,'Can change site',7,'change_site'),(21,'Can delete site',7,'delete_site'),(22,'Can add log entry',8,'add_logentry'),(23,'Can change log entry',8,'change_logentry'),(24,'Can delete log entry',8,'delete_logentry'),(25,'Can add gemeente',9,'add_gemeente'),(26,'Can change gemeente',9,'change_gemeente'),(27,'Can delete gemeente',9,'delete_gemeente'),(28,'Can add gemeente type',10,'add_gemeentetype'),(29,'Can change gemeente type',10,'change_gemeentetype'),(30,'Can delete gemeente type',10,'delete_gemeentetype'),(31,'Can add geslacht',11,'add_geslacht'),(32,'Can change geslacht',11,'change_geslacht'),(33,'Can delete geslacht',11,'delete_geslacht'),(34,'Can add land',12,'add_land'),(35,'Can change land',12,'change_land'),(36,'Can delete land',12,'delete_land'),(37,'Can add gezin',13,'add_gezin'),(38,'Can change gezin',13,'change_gezin'),(39,'Can delete gezin',13,'delete_gezin'),(40,'Can add gezins rol',14,'add_gezinsrol'),(41,'Can change gezins rol',14,'change_gezinsrol'),(42,'Can delete gezins rol',14,'delete_gezinsrol'),(43,'Can add wijk',15,'add_wijk'),(44,'Can change wijk',15,'change_wijk'),(45,'Can delete wijk',15,'delete_wijk'),(46,'Can add huiskring',16,'add_huiskring'),(47,'Can change huiskring',16,'change_huiskring'),(48,'Can delete huiskring',16,'delete_huiskring'),(49,'Can add huiskring lid rol',17,'add_huiskringlidrol'),(50,'Can change huiskring lid rol',17,'change_huiskringlidrol'),(51,'Can delete huiskring lid rol',17,'delete_huiskringlidrol'),(52,'Can add huiskring lid',18,'add_huiskringlid'),(53,'Can change huiskring lid',18,'change_huiskringlid'),(54,'Can delete huiskring lid',18,'delete_huiskringlid'),(55,'Can add lidmaatschap status',19,'add_lidmaatschapstatus'),(56,'Can change lidmaatschap status',19,'change_lidmaatschapstatus'),(57,'Can delete lidmaatschap status',19,'delete_lidmaatschapstatus'),(58,'Can add persoon',20,'add_persoon'),(59,'Can change persoon',20,'change_persoon'),(60,'Can delete persoon',20,'delete_persoon');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'admin','','','l.batteau@indieit.nl','sha1$3c2b0$f3252e9e2e716ca2264d7b509dac9c1ee997b8cd',1,1,1,'2010-11-12 10:16:11','2010-10-26 12:51:03'),(2,'kbuser','Test','Gebruiker','test@nietbestaand.nl','sha1$c0999$6f44a982128af6947e8d69ab8403bf1680732f4d',1,1,0,'2010-11-20 12:58:46','2010-10-26 13:28:04'),(3,'kbadmin','Admin','Gebruiker','admin@nietbestaand.nl','sha1$58822$0908f32b2659386dd7f101e4470144749b81b34d',1,1,1,'2010-11-20 15:04:07','2010-10-26 14:15:08');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_403f60f` (`user_id`),
  KEY `auth_user_groups_425ae3c4` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_403f60f` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM AUTO_INCREMENT=121 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_403f60f` (`user_id`),
  KEY `django_admin_log_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2010-10-26 13:28:04',1,3,'2','kbuser',1,''),(2,'2010-10-26 13:28:59',1,3,'2','kbuser',2,'first_name, last_name, email en is_staff gewijzigd.'),(3,'2010-10-26 14:10:13',1,3,'2','kbuser',2,'password gewijzigd.'),(4,'2010-10-26 14:11:53',1,3,'2','kbuser',2,'user_permissions gewijzigd.'),(5,'2010-10-26 14:14:36',1,3,'2','kbuser',2,'is_superuser gewijzigd.'),(6,'2010-10-26 14:15:08',1,3,'3','testuser',1,''),(7,'2010-10-26 14:16:39',1,3,'2','kbuser',2,'is_superuser en user_permissions gewijzigd.'),(8,'2010-10-26 14:19:04',1,3,'3','kbadmin',2,'username, first_name, last_name, email, is_staff en is_superuser gewijzigd.'),(9,'2010-10-26 14:39:25',3,20,'1348','Joep Bladiebla',2,'boolactief gewijzigd.'),(10,'2010-10-26 14:43:43',3,20,'1348','Joep Bladiebla',2,'boolactief gewijzigd.'),(11,'2010-10-26 14:44:03',3,20,'1348','Joep Bladiebla',2,'boolactief gewijzigd.'),(12,'2010-10-26 15:12:00',3,20,'1','Jorieke Aaftink',2,'boolactief gewijzigd.'),(13,'2010-11-12 10:29:43',1,20,'965','Yannick Aikema',2,'idgezin en idgezinsrol gewijzigd.'),(14,'2010-11-12 10:30:11',1,20,'1113','Liza Baas',2,'idgezin en idgezinsrol gewijzigd.'),(15,'2010-11-12 10:30:51',1,13,'894','Aikema, Y.O. (Yannick)',3,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'message','auth','message'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'site','sites','site'),(8,'log entry','admin','logentry'),(9,'gemeente','OLA','gemeente'),(10,'gemeente type','OLA','gemeentetype'),(11,'geslacht','OLA','geslacht'),(12,'land','OLA','land'),(13,'gezin','OLA','gezin'),(14,'gezins rol','OLA','gezinsrol'),(15,'wijk','OLA','wijk'),(16,'huiskring','OLA','huiskring'),(17,'huiskring lid rol','OLA','huiskringlidrol'),(18,'huiskring lid','OLA','huiskringlid'),(19,'lidmaatschap status','OLA','lidmaatschapstatus'),(20,'persoon','OLA','persoon');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3a5b31beec8679220e25a1a407da6ae3','gAJ9cQEuN2QzYjAwYzBmYWI4ZjliMmIyNjU3NzVlMWU1YWY1ODU=\n','2010-12-03 16:02:53'),('f12d7f2be2130efe0fa5f3e7ae697f03','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-26 13:20:51'),('aa9aba6fb0f314a193f0bdd385d9f963','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-09 15:17:46'),('0c7006246aefd856dcf55bfb7db538f5','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-09 14:38:31'),('778171b4160d9447e024a15a3c198320','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-09 15:17:53'),('9951581bcd347011da6004d9dae22eca','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-09 15:18:15'),('23232c2773efb6ef808fdf7fc89f8a94','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-09 15:18:44'),('435ffcf023a293ec6f977c6e8b0d2940','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-09 16:01:07'),('3cd3f00c0826ec8c722680bac609a113','gAJ9cQEuN2QzYjAwYzBmYWI4ZjliMmIyNjU3NzVlMWU1YWY1ODU=\n','2010-11-09 15:19:49'),('aa627d66988b7edde74e57d8e9266e73','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-09 15:40:33'),('6b911dc2791796388cbd8eab8fe6901f','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-09 23:26:38'),('aed7f8bbbd888cfef7b0fbbdc6a6b0d1','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-10 08:34:51'),('b2baa96f57dc72e2e855b80a494338de','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-25 18:07:00'),('eea580fe884112d381aac3eab6c37713','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-24 22:39:26'),('c9319cce5fec10f165a3c14f915de4f7','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-24 20:13:33'),('a5cb808dfc73b262bf710fee5e391224','gAJ9cQEuN2QzYjAwYzBmYWI4ZjliMmIyNjU3NzVlMWU1YWY1ODU=\n','2010-11-25 16:31:50'),('aedcf55d48f63f76f0adfc2f5d77f710','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-25 11:44:57'),('eebc855be4d3af4819e6ee2ef235ace9','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-25 11:45:07'),('c6d8814397a45091e0c0f42953245d3b','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-25 11:45:16'),('942ba9e92bed647cdbc395abbf84586b','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-25 13:12:14'),('b6a26b75f193538a243bc8e214193143','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-25 13:12:22'),('9dd8486032e30626b7f29cec54952a1f','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-25 13:12:33'),('0bf8b9b3fa34a182a35c14f52977864d','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-25 15:54:11'),('fa4b0aa9c61af2a663e3527389ac18af','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-25 15:54:22'),('e9f30b26afdbcc19e7dce892d72ccaac','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-25 18:07:07'),('4e9c7d7638a0b590edb59268167461e8','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5mNDA0ZTRiOWUzOTQwMjRkNDE2\nNjM3YmRkODEyZGZlOQ==\n','2010-11-26 10:16:11'),('3ee64e844f0fdc00da7f4d120ed31b41','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-26 10:57:46'),('c176c9030cf100c970eb1884d9dae161','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-26 21:41:01'),('c43e587520ec9d35242e9721d0b404a7','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-26 21:41:12'),('249c4caf0dabf21feacde7a04f2f6374','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-26 21:41:20'),('bcb81e6247766cf52140a54eb5fd3c93','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-27 10:40:40'),('8e22f6b43375db91f4df4f8a91c30f82','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-27 20:09:08'),('05b24f9a38c91384a55e41dc0e168117','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-27 20:09:15'),('d309b1df8872b80a99a49e930ef1d7a4','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-11-28 17:51:59'),('d74afe489b2b3ced5c3dd1297e75fcd0','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-28 17:52:06'),('7682bedf068df877df1f3dd023b4fc5a','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-11-28 17:52:15'),('6d56b802152fa69ad11906ec3b3e4e82','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEDdS40MDY3ODkwMDFiYTZlYjE4MzQy\nOGI4NDFhNGY1OWUyOA==\n','2010-12-03 09:48:05'),('2ba7b3abc6459cd8dce404bb43d7f44d','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-12-03 09:48:21'),('ef2001d43c8f247d3fb76b8ba795ed17','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-12-03 10:45:33'),('fce03f6937e4b9425bef708342365a65','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-12-03 10:46:04'),('33d5a694343a8bcd3c356cef510ffdd9','gAJ9cQEuN2QzYjAwYzBmYWI4ZjliMmIyNjU3NzVlMWU1YWY1ODU=\n','2010-12-03 11:21:28'),('28f0d277f94775a86ba40c996d7bcd98','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigECdS41ZmY0ZjgwOTY4NzExMDE2ODU1\nMWQyMzVhMWU5NjJjZQ==\n','2010-12-03 11:15:59'),('4ef7edeebf0f342b1bba1cb53d37cfcd','gAJ9cQEoVQ1fYXV0aF91c2VyX2lkcQKKAQNVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSlkamFuZ28u\nY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEEdS43Njc5MjJjYzZiNzE4OTM2ZjZk\nYmQ3MWZjMzE2YjJkZg==\n','2010-12-04 15:04:07');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_gemeenten`
--

DROP TABLE IF EXISTS `ledendb_gemeenten`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_gemeenten` (
  `idGemeente` int(11) NOT NULL AUTO_INCREMENT,
  `txtGemeenteNaam` varchar(50) DEFAULT NULL,
  `idGemeenteType` int(11) DEFAULT NULL,
  `txtOpmerking` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idGemeente`)
) ENGINE=InnoDB AUTO_INCREMENT=467 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_gemeenten`
--

LOCK TABLES `ledendb_gemeenten` WRITE;
/*!40000 ALTER TABLE `ledendb_gemeenten` DISABLE KEYS */;
INSERT INTO `ledendb_gemeenten` VALUES (1,'geref. kerk Test',NULL,NULL),(2,'Dopperkerk Heilbron',NULL,NULL),(3,'geref. Huisgemeente Paramaribo',NULL,NULL),(4,'geref. kerk \'t Harde',NULL,NULL),(5,'geref. kerk (syn.) \'s Gravenzande',NULL,NULL),(6,'geref. kerk (syn.) Nieuwegein',NULL,NULL),(7,'geref. kerk (syn.) Weesp',NULL,NULL),(8,'geref. kerk Almkerk',NULL,NULL),(9,'geref. kerk Almkerk-Werkendam',NULL,NULL),(10,'geref. kerk Amersfoort',NULL,NULL),(11,'geref. kerk Amersfoort-West',NULL,NULL),(12,'[onbekend]',NULL,NULL),(13,'geref. kerk Amsterdam',NULL,NULL),(14,'geref. kerk Amsterdam-Centrum',NULL,NULL),(15,'geref. kerk Arnhem',NULL,NULL),(16,'geref. kerk Assen',NULL,NULL),(17,'geref. kerk Bedum',NULL,NULL),(18,'geref. kerk Beetsterzwaag',NULL,NULL),(19,'geref. kerk Bergschenhoek',NULL,NULL),(20,'geref. kerk Bilthoven',NULL,NULL),(21,'geref. kerk Bodegraven-Woerden',NULL,NULL),(22,'geref. kerk Breukelen',NULL,NULL),(23,'geref. kerk Bunschoten',NULL,NULL),(24,'geref. kerk Bunschoten-Oost',NULL,NULL),(25,'geref. kerk Bussum',NULL,NULL),(26,'geref. kerk Culemborg',NULL,NULL),(27,'geref. kerk De Bilt-Bilthoven',NULL,NULL),(28,'geref. kerk Den Helder',NULL,NULL),(29,'geref. kerk Deventer',NULL,NULL),(30,'geref. kerk Doesburg',NULL,NULL),(31,'geref. kerk Dokkum',NULL,NULL),(32,'geref. kerk Eindhoven',NULL,NULL),(33,'geref. kerk Emmeloord',NULL,NULL),(34,'geref. kerk Ermelo',NULL,NULL),(35,'geref. kerk Gees',NULL,NULL),(36,'geref. kerk Glanerbrug',NULL,NULL),(37,'geref. kerk Goes',NULL,NULL),(38,'geref. kerk Gouda',NULL,NULL),(39,'geref. kerk Groningen',NULL,NULL),(40,'geref. kerk Groningen-Noord',NULL,NULL),(41,'geref. kerk Groningen-Oost',NULL,NULL),(42,'geref. kerk Groningen-Zuid',NULL,NULL),(43,'geref. kerk Hardenberg',NULL,NULL),(44,'geref. kerk Harderwijk',NULL,NULL),(45,'geref. kerk Haulerwijk',NULL,NULL),(46,'geref. kerk Heerde',NULL,NULL),(47,'geref. kerk Heereveen',NULL,NULL),(48,'geref. kerk Hoogkerk',NULL,NULL),(49,'geref. kerk Hoogvliet-Spijkenisse',NULL,NULL),(51,'geref. kerk Leek/Roden',NULL,NULL),(52,'geref. kerk Leerdam',NULL,NULL),(53,'geref. kerk Leusden',NULL,NULL),(54,'geref. kerk Maartensdijk',NULL,NULL),(55,'geref. kerk Maassluis',NULL,NULL),(56,'geref. kerk Mariënberg',NULL,NULL),(57,'geref. kerk Marknesse',NULL,NULL),(58,'geref. kerk Middelstum',NULL,NULL),(59,'geref. kerk Monster',NULL,NULL),(60,'geref. kerk Mussel',NULL,NULL),(61,'geref. kerk New Westminster',NULL,NULL),(62,'geref. kerk Nieuwleusen',NULL,NULL),(63,'geref. kerk Ommen',NULL,NULL),(64,'geref. kerk Oostburg',NULL,NULL),(65,'geref. kerk Oostelijk Flevoland',NULL,NULL),(66,'geref. kerk Pieterburen',NULL,NULL),(68,'geref. kerk Rotterdam-Centrum',NULL,NULL),(69,'geref. kerk Rotterdam-Hilligersberg',NULL,NULL),(70,'geref. kerk Rotterdam-Kralingen',NULL,NULL),(71,'geref. kerk Rotterdam-Noord',NULL,NULL),(72,'geref. kerk Rotterdam-Zuid',NULL,NULL),(73,'geref. kerk Schermerborn',NULL,NULL),(74,'geref. kerk Sneek',NULL,NULL),(75,'geref. kerk Souburg-Vlissingen',NULL,NULL),(76,'geref. kerk Spakenburg-Noord',NULL,NULL),(77,'geref. kerk Spakenburg-Zuid',NULL,NULL),(78,'geref. kerk Stadskanaal',NULL,NULL),(79,'geref. kerk Tiel',NULL,NULL),(80,'geref. kerk Uithuizermeden',NULL,NULL),(81,'geref. kerk Ulrum',NULL,NULL),(82,'geref. kerk Vlaardingen',NULL,NULL),(83,'geref. kerk Vleuten-De Meern',NULL,NULL),(84,'geref. kerk Wageningen',NULL,NULL),(86,'geref. kerk Wezep',NULL,NULL),(87,'geref. kerk Zaandam',NULL,NULL),(88,'geref. kerk Zevenbergen',NULL,NULL),(89,'geref. kerk Zuidhorn',NULL,NULL),(90,'geref. kerk Zutphen',NULL,NULL),(91,'geref. kerk Zwolle',NULL,NULL),(92,'Gereformeerde kerk Curitiba',NULL,NULL),(94,'Herv. kerk Veenendaal',NULL,NULL),(95,'Herv. kerk Zuilen',NULL,NULL),(96,'Huisgemeente Boma',NULL,NULL),(97,'Huisgemeente Veenhuizen',NULL,NULL),(98,'Monte Alegre, Brazil',NULL,NULL),(99,'Ned. geref. kerk Zwartsluis',NULL,NULL),(100,'Oud Geref. Gemeente Utrecht',NULL,NULL),(101,'R.K. kerk Bonaire',NULL,NULL),(102,'R.K. kerk Colombia',NULL,NULL),(103,'R.K. kerk Etten-Leur',NULL,NULL),(104,'R.K. kerk Laren',NULL,NULL),(105,'R.K.H. Bonaventurakerk Woerden',NULL,NULL),(106,'Roomse kerk Utrecht',NULL,NULL),(107,'Cloverdale, Canada',NULL,NULL),(108,'geref. kerk \'s-Hertogenbosch',NULL,NULL),(109,'geref. kerk (syn.) Nieuwegein',NULL,NULL),(112,'geref. kerk Almelo',NULL,NULL),(113,'geref. kerk Alphen a/d Rijn',NULL,NULL),(114,'geref. kerk Amersfoort-Centrum',NULL,NULL),(115,'geref. kerk Amersfoort-Noord',NULL,NULL),(118,'geref. kerk Apeldoorn',NULL,NULL),(119,'geref. kerk Avereest-Dedemsvaart',NULL,NULL),(120,'geref. kerk Barendrecht',NULL,NULL),(123,'geref. kerk Beverwijk',NULL,NULL),(125,'geref. kerk Capelle a/d IJssel',NULL,NULL),(126,'geref. kerk Creil',NULL,NULL),(127,'geref. kerk Daarleveen',NULL,NULL),(128,'geref. kerk Dalfsen',NULL,NULL),(130,'geref. kerk Driebergen-Rijsenburg',NULL,NULL),(131,'geref. kerk Dronten',NULL,NULL),(132,'geref. kerk Enschede-Noord',NULL,NULL),(133,'geref. kerk Enschede-Oost',NULL,NULL),(134,'geref. kerk Groningen-West',NULL,NULL),(135,'geref. kerk Hardenberg-Centrum',NULL,NULL),(136,'geref. kerk Hardinxveld-Giessendam',NULL,NULL),(137,'geref. kerk Haren',NULL,NULL),(138,'geref. kerk Hattem',NULL,NULL),(139,'geref. kerk Helpman',NULL,NULL),(140,'geref. kerk Hengelo',NULL,NULL),(141,'geref. kerk Hilversum',NULL,NULL),(142,'geref. kerk Hoogeveen',NULL,NULL),(143,'geref. kerk Loenen a/d Vecht',NULL,NULL),(144,'geref. kerk Middelburg',NULL,NULL),(146,'geref. kerk Nijmegen',NULL,NULL),(147,'geref. kerk Ontario',NULL,NULL),(149,'geref. kerk Rijswijk',NULL,NULL),(150,'geref. kerk Rotterdam-Oost',NULL,NULL),(151,'geref. kerk Santa Rosa/Curacao',NULL,NULL),(152,'geref. kerk Spakenburg',NULL,NULL),(153,'geref. kerk Steenwijk',NULL,NULL),(154,'geref. kerk Ten Boer',NULL,NULL),(155,'geref. kerk Terneuzen',NULL,NULL),(156,'geref. kerk Ureterp',NULL,NULL),(157,'geref. kerk Utrecht-Noord/West',NULL,NULL),(159,'geref. kerk Velp',NULL,NULL),(160,'geref. kerk Vlissingen',NULL,NULL),(161,'geref. kerk Voorburg',NULL,NULL),(163,'geref. kerk Waddinxveen',NULL,NULL),(165,'geref. kerk Westeremden',NULL,NULL),(166,'geref. kerk Zeewolde',NULL,NULL),(167,'geref. kerk Zoetermeer',NULL,NULL),(168,'geref. kerk Zuidlaren',NULL,NULL),(169,'geref. kerk Zuilen',NULL,NULL),(170,'geref. kerk Zwijndrecht',NULL,NULL),(171,'geref. kerk Zwijndrecht Groote Lindt',NULL,NULL),(172,'Herv. Gemeente IJsselmuiden en Grafhorst',NULL,NULL),(173,'Herv. Gemeente Utrecht',NULL,NULL),(174,'Herv. kerk Zegveld',NULL,NULL),(176,'Ned. geref. kerk Utrecht',NULL,NULL),(177,'Ned. geref. kerk Zwolle',NULL,NULL),(178,'geref. kerk \'s Hertogenbosch',NULL,NULL),(179,'geref. kerk Aduard',NULL,NULL),(180,'geref. kerk Alkmaar',NULL,NULL),(188,'geref. kerk Axel',NULL,NULL),(189,'geref. kerk Baarn',NULL,NULL),(192,'geref. kerk Berkel en Rodenrijs',NULL,NULL),(194,'geref. kerk Brunsum-Treebeek',NULL,NULL),(196,'geref. kerk Buschoten/Spakenburg',NULL,NULL),(197,'geref. kerk Bussum-Huizen',NULL,NULL),(198,'Canada',NULL,NULL),(200,'geref. kerk Curaçao',NULL,NULL),(205,'geref. kerk Den Bosch',NULL,NULL),(208,'geref. kerk Dordrecht',NULL,NULL),(209,'geref. kerk Drachten',NULL,NULL),(211,'geref. kerk Ede-Noord',NULL,NULL),(213,'geref. kerk Emmen',NULL,NULL),(216,'geref. kerk Anna-Paulowna',NULL,NULL),(217,'geref. kerk Bunschoten-West',NULL,NULL),(218,'geref. kerk Capelle a/d IJssel-Zuid/West',NULL,NULL),(220,'geref. kerk Kampen',NULL,NULL),(221,'geref. kerk Leiden',NULL,NULL),(222,'geref. kerk Rotterdam-Stad',NULL,NULL),(223,'geref. kerk Utrecht-Centrum',NULL,NULL),(224,'geref. kerk Zwolle-Zuid',NULL,NULL),(225,'geref. kerk Giessen-Rijswijk  (NBR)',NULL,NULL),(231,'geref. kerk Haarlem',NULL,NULL),(232,'geref. kerk Hardenberg Oost',NULL,NULL),(236,'Herv. Gemeente Zegveld',NULL,NULL),(239,'geref. kerk Idskenhuizen (syn.)',NULL,NULL),(240,'geref. kerk Kadoelen',NULL,NULL),(247,'geref. kerk Neede',NULL,NULL),(248,'geref. kerk Nieuwegein',NULL,NULL),(249,'geref. kerk Nijkerk',NULL,NULL),(251,'nvt/Colombia',NULL,NULL),(253,'geref. kerk Pijnacker-Nootdorp',NULL,NULL),(254,'geref. kerk Roden',NULL,NULL),(256,'geref. kerk Rotterdam-Delfshaven',NULL,NULL),(267,'geref. kerk Veenendaal',NULL,NULL),(271,'geref. kerk Voorthuizen-Barneveld',NULL,NULL),(275,'geref. kerk Weesp-Nigtevecht',NULL,NULL),(276,'geref. kerk Zeist',NULL,NULL),(283,'geref. kerk Assen-Noord',NULL,NULL),(284,'geref. kerk Drachten Zuid/Oost',NULL,NULL),(285,'geref. kerk Utrecht',NULL,NULL),(287,'geref. kerk Winsum-Obergum',NULL,NULL),(289,'geref. kerk Zuidwolde',NULL,NULL),(290,'Canadian Reformed Church Londen Ontario',NULL,NULL),(291,'geref. kerk Amersfoort-Oost',NULL,NULL),(292,'geref. kerk Broek op Langedijk',NULL,NULL),(294,'geref. kerk Maarssen-Breukelen',NULL,NULL),(297,'geref. kerk Rozenburg',NULL,NULL),(298,'geref. kerk Veendam',NULL,NULL),(299,'geref. kerk Zwolle-Centrum',NULL,NULL),(310,'geref. kerk Hasselt',NULL,NULL),(311,'geref. kerk Hoofddorp',NULL,NULL),(312,'geref. kerk Doetinchem',NULL,NULL),(313,'Ned. herv. kerk De Bilt',NULL,NULL),(315,'geref. kerk Vrouwenpolder',NULL,NULL),(316,'geref. kerk Assen-Zuid',NULL,NULL),(317,'geref. kerk Amsterdam-Zuid/West',NULL,NULL),(318,'geref. kerk Soest',NULL,NULL),(319,'geref. kerk Barneveld-Voorthuizen',NULL,NULL),(320,'geref. kerk Langerak',NULL,NULL),(321,'geref. kerk Lemele-Lemelerveld',NULL,NULL),(322,'geref. kerk Meppel',NULL,NULL),(323,'geref. kerk Eindhoven-Best',NULL,NULL),(324,'R.K. kerk Utrecht',NULL,NULL),(325,'geref. kerk Delfzijl',NULL,NULL),(326,'Christian Reformed Church of Peterborough, ON',NULL,NULL),(327,'geref. kerk Den Haag-Zuid/Rijswijk',NULL,NULL),(328,'American Reformed Church of Lynden (Wash.)',NULL,NULL),(329,'Ned. geref. kerk Glanerbrug',NULL,NULL),(330,'geref. kerk Mijdrecht',NULL,NULL),(331,'R.K. Zuilen Jacubus Ludgerus',NULL,NULL),(332,'Remonstrantse Gemeente te Dordrecht',NULL,NULL),(333,'geref. kerk Tilburg',NULL,NULL),(334,'geref. kerk Lutten',NULL,NULL),(335,'geref. kerk Voorschoten',NULL,NULL),(336,'geref. kerk Hoek',NULL,NULL),(337,'Alt reformierte Kirche Campen (D)',NULL,NULL),(338,'onttrokken',NULL,NULL),(339,'overleden',NULL,NULL),(340,'geboren',NULL,NULL),(341,'Victory Outreach Utrecht',NULL,NULL),(342,'geref. kerk Breezand',NULL,NULL),(343,'geref. kerk Buitenpost',NULL,NULL),(344,'geref. kerk Nieuw-Lekkerland',NULL,NULL),(345,'geref. kerk Frieschepalen',NULL,NULL),(346,'geref. kerk Hardenberg-Baalderveld',NULL,NULL),(347,'geref. kerk Noordbergum',NULL,NULL),(348,'S.O.W. gemeente Utrecht',NULL,NULL),(349,'Hervormde kerk',NULL,NULL),(350,'Ned. herv. kerk Zwolle',NULL,NULL),(351,'geref. kerk Rouveen',NULL,NULL),(352,'geref. kerk enschede-west',NULL,NULL),(353,'geref. kerk Amersfoort-Nieuwland',NULL,NULL),(354,'geref. kerk Apeldoorn-Centrum',NULL,NULL),(355,'geref. kerk Kampen-zuid',NULL,NULL),(356,'geref. kerk Kampen-noord',NULL,NULL),(357,'geref. kerk Oegstgeest',NULL,NULL),(358,'geref. kerk Amersfoort-Emiclaer',NULL,NULL),(359,'geref. kerk (syn.) Westbroek',NULL,NULL),(360,'Assemblé de Dieu, Kigali, Rwanda',NULL,NULL),(361,'St. John\'s Bega. Australia',NULL,NULL),(362,'Chris. Church Pambula, Australia',NULL,NULL),(363,'Anglican Church Sydney, Australia',NULL,NULL),(364,'geref. kerk Oldenhove',NULL,NULL),(365,'geref. kerk Garrelsweer',NULL,NULL),(366,'geref. kerk Breda',NULL,NULL),(367,'geref. kerk Berkum',NULL,NULL),(368,'geref. kerk Krimpen a/d IJssel',NULL,NULL),(369,'Ned. herv. kerk Amersfoort',NULL,NULL),(370,'Leger des heils Amersfoort',NULL,NULL),(371,'geref. kerk Gorinchem',NULL,NULL),(372,'geref. kerk Zaltbommel',NULL,NULL),(373,'Uitgesloten uit de gemeenschap van de kerk',NULL,NULL),(374,'Vrij evangelische gemeente Zwolle',NULL,NULL),(375,'geref. kerk \'s-Gravenhage-Centrum/Scheveningen',NULL,NULL),(376,'geref. kerk Drachten-oost',NULL,NULL),(377,'geref. kerk Grootegast',NULL,NULL),(378,'geref. kerk Delft',NULL,NULL),(379,'Gereja Reformasi, Bomakia (Irian Jaya)',NULL,NULL),(380,'geref. kerk Leidsche Rijn',NULL,NULL),(381,'geref. kerk Mechelen (België)',NULL,NULL),(382,'geref. kerk Houten',NULL,NULL),(383,'Anglicaanse kerk van Merimbula, New South Wales',NULL,NULL),(384,'CGK Arnhem',NULL,NULL),(385,'geref. Kerk Soest-Baarn',NULL,NULL),(386,'geref. kerk Lelystad',NULL,NULL),(387,'geref. kerk Assen-Kloosterveen',NULL,NULL),(388,'geref. kerk Amersfoort-De Horsten',NULL,NULL),(389,'geref. kerk Hattem-Noord',NULL,NULL),(390,'geref. kerk Hardenberg-Baalder',NULL,NULL),(391,'geref. kerk Almere',NULL,NULL),(392,'Ned. geref. kerk Houten',NULL,NULL),(393,'geref. kerk Balkbrug',NULL,NULL),(394,'geref. kerk Assen-Marsdijk',NULL,NULL),(395,'Evangelische Gemeente Zuilen',NULL,NULL),(396,'Presbyterian Church Korea',NULL,NULL),(397,'Baptisten gemeente Utrecht',NULL,NULL),(398,'gedoopt',NULL,NULL),(399,'Canadian Reformed Church Edmonton',NULL,NULL),(401,'geref. kerk Ten Post',NULL,NULL),(402,'Ned. geref. kerk Ten Post',NULL,NULL),(403,'Geref. gemeente \'s-Gravenhage Zuid',NULL,NULL),(404,'geref. kerk Middelharnis',NULL,NULL),(405,'Geref. gemeente Soest',NULL,NULL),(406,'CGK Soest',NULL,NULL),(407,'geref. kerk Zwolle-Berkum',NULL,NULL),(408,'geref. kerk Amersfoort-Hoogland',NULL,NULL),(409,'geref. kerk Loppersum',NULL,NULL),(410,'Herv. Gemeente Waddinxveen',NULL,NULL),(411,'geref. kerk Damwoude',NULL,NULL),(412,'R.K. te Musaga (Burundi)',NULL,NULL),(413,'geref. kerk Enumatil',NULL,NULL),(415,'geref. kerk Ede',NULL,NULL),(416,'Baptisten gemeente Amersfoort',NULL,NULL),(417,'geref. kerk Amersfoort-Vathorst',NULL,NULL),(418,'geref. kerk Bergentheim',NULL,NULL),(419,'geref. kerk Zwolle-Noord',NULL,NULL),(420,'geref. kerk Rijnsburg',NULL,NULL),(421,'toegelaten',NULL,NULL),(422,'CGK Utrecht-Noord',NULL,NULL),(423,'CGK Utrecht-West',NULL,NULL),(424,'geref. kerk Putten',NULL,NULL),(425,'Free Church of Scotland in Londen - UK',NULL,NULL),(426,'Ned. geref. kerk Breukelen',NULL,NULL),(427,'geref. kerk Overschie',NULL,NULL),(428,'geref. kerk Leeuwarden',NULL,NULL),(429,'geref. kerk Den Haag-Centrum/Scheveningen',NULL,NULL),(430,'geref. kerk Amersfoort-Zuid',NULL,NULL),(431,'geref. kerk spakenburg-Zuid',NULL,NULL),(432,'geref. kerk Zwolle-West',NULL,NULL),(434,'geref. kerk Lisse',NULL,NULL),(435,'Geref. gemeente \'s Gravenpolder',NULL,NULL),(436,'geref. gemeente Utrecht',NULL,NULL),(437,'Herv. gemeente Woerden',NULL,NULL),(438,'geref. kerk (syn.) Woerden',NULL,NULL),(439,'geref. kerk Leek',NULL,NULL),(440,'Orthodox Presbyterian Church Birmingham',NULL,NULL),(441,'American Reformed Church Grand Rapids (VS)',NULL,NULL),(442,'geref. kerk Capelle a/d IJssel-Noord',NULL,NULL),(443,'CGK Amsterdam',NULL,NULL),(444,'PKN Nieuwe Kerk te Utrecht',NULL,NULL),(445,'Crossroad International Church te Amstelveen',NULL,NULL),(446,'geref. kerk Pernis',NULL,NULL),(447,'geref. kerk Pernis-Albrandswaard',NULL,NULL),(448,'CGK Zwolle',NULL,NULL),(450,'geref. kerk Veenendaal-Oost',NULL,NULL),(451,'geref. kerk Veenendaal-West',NULL,NULL),(452,'Ned. geref. kerk Deventer',NULL,NULL),(453,'geref. kerk Ede-Zuid',NULL,NULL),(454,'geref. kerk Waardhuizen',NULL,NULL),(455,'geref. kerk Enschede-Zuid',NULL,NULL),(456,'geref. kerk Nieuwerkerk a/d IJssel',NULL,NULL),(457,'geref. kerk Woerden/Bodegraven',NULL,NULL),(458,'CGK Biezelinge',NULL,NULL),(459,'CGK Biezelinge',NULL,NULL),(460,'PKN Dordrecht',NULL,NULL),(461,'Nieuw vrijgemaakte kerk Utrecht',NULL,NULL),(462,'CGK IJmuiden',NULL,NULL),(463,'geref. kerk Amstelveen',NULL,NULL),(464,'geref. kerk Roodeschool',NULL,NULL),(465,'geref. kerk Langeslag',NULL,NULL),(466,'Ned. geref. kerk Assen',NULL,NULL);
/*!40000 ALTER TABLE `ledendb_gemeenten` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_gemeentetypes`
--

DROP TABLE IF EXISTS `ledendb_gemeentetypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_gemeentetypes` (
  `idGemeenteType` int(11) NOT NULL AUTO_INCREMENT,
  `txtGemeenteType` varchar(50) NOT NULL,
  PRIMARY KEY (`idGemeenteType`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_gemeentetypes`
--

LOCK TABLES `ledendb_gemeentetypes` WRITE;
/*!40000 ALTER TABLE `ledendb_gemeentetypes` DISABLE KEYS */;
INSERT INTO `ledendb_gemeentetypes` VALUES (1,'GKV'),(2,'NGK'),(3,'CGK'),(4,'PKN'),(5,'RK'),(6,'Evangelisch'),(7,'Zusterkerk buitenland');
/*!40000 ALTER TABLE `ledendb_gemeentetypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_geslachten`
--

DROP TABLE IF EXISTS `ledendb_geslachten`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_geslachten` (
  `idGeslacht` int(11) NOT NULL AUTO_INCREMENT,
  `txtGeslacht` varchar(1) DEFAULT NULL,
  `txtGeslachtLang` varchar(50) DEFAULT NULL,
  `txtAanhef` varchar(50) DEFAULT NULL,
  `txtAanhefKort` varchar(50) DEFAULT NULL,
  `txtAanhefKerk` varchar(45) DEFAULT NULL,
  `txtAanhefKerkKort` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idGeslacht`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_geslachten`
--

LOCK TABLES `ledendb_geslachten` WRITE;
/*!40000 ALTER TABLE `ledendb_geslachten` DISABLE KEYS */;
INSERT INTO `ledendb_geslachten` VALUES (1,'M','man','de heer','dhr.','broeder','br.'),(2,'V','vrouw','mevrouw','mw.','zuster','zr.');
/*!40000 ALTER TABLE `ledendb_geslachten` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_gezinnen`
--

DROP TABLE IF EXISTS `ledendb_gezinnen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_gezinnen` (
  `idGezin` int(11) NOT NULL AUTO_INCREMENT,
  `txtGezinsnaam` varchar(50) NOT NULL,
  `txtStraatnaam` varchar(50) DEFAULT NULL,
  `intHuisnummer` int(11) DEFAULT NULL,
  `txtHuisnummerToevoeging` varchar(20) DEFAULT NULL,
  `txtPostcode` varchar(20) DEFAULT NULL,
  `txtPlaats` varchar(50) DEFAULT NULL,
  `idLand` int(11) DEFAULT NULL,
  `txtTelefoon` varchar(25) DEFAULT NULL,
  `txtOpmerking` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idGezin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_gezinnen`
--

LOCK TABLES `ledendb_gezinnen` WRITE;
/*!40000 ALTER TABLE `ledendb_gezinnen` DISABLE KEYS */;
/*!40000 ALTER TABLE `ledendb_gezinnen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_gezinsrollen`
--

DROP TABLE IF EXISTS `ledendb_gezinsrollen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_gezinsrollen` (
  `idGezinsrol` int(11) NOT NULL AUTO_INCREMENT,
  `txtGezinsrol` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idGezinsrol`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_gezinsrollen`
--

LOCK TABLES `ledendb_gezinsrollen` WRITE;
/*!40000 ALTER TABLE `ledendb_gezinsrollen` DISABLE KEYS */;
INSERT INTO `ledendb_gezinsrollen` VALUES (1,'Gezinshoofd'),(2,'Partner'),(3,'Kind (inwonend)');
/*!40000 ALTER TABLE `ledendb_gezinsrollen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_huiskringen`
--

DROP TABLE IF EXISTS `ledendb_huiskringen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_huiskringen` (
  `idHuiskring` int(11) NOT NULL AUTO_INCREMENT,
  `txtHuiskringNaam` varchar(50) NOT NULL,
  `idWijk` int(11) NOT NULL,
  `txtOpmerking` varchar(255) DEFAULT NULL,
  `txtVolgnummer` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`idHuiskring`),
  KEY `FK_LedenDB_Huiskringen_Wijken` (`idWijk`),
  CONSTRAINT `FK_LedenDB_Huiskringen_Wijken` FOREIGN KEY (`idWijk`) REFERENCES `ledendb_wijken` (`idWijk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_huiskringen`
--

LOCK TABLES `ledendb_huiskringen` WRITE;
/*!40000 ALTER TABLE `ledendb_huiskringen` DISABLE KEYS */;
/*!40000 ALTER TABLE `ledendb_huiskringen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_huiskringleden`
--

DROP TABLE IF EXISTS `ledendb_huiskringleden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_huiskringleden` (
  `idPersoon` int(11) NOT NULL DEFAULT '0',
  `idHuiskring` int(11) NOT NULL,
  `idHuiskringRol` int(11) NOT NULL,
  `idHuiskringLid` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idHuiskringLid`),
  KEY `FK_LedenDB_Huiskringleden_Huiskringen` (`idHuiskring`),
  KEY `FK_LedenDB_Huiskringleden_HuiskringLidRol` (`idHuiskringRol`),
  CONSTRAINT `FK_LedenDB_Huiskringleden_Huiskringen` FOREIGN KEY (`idHuiskring`) REFERENCES `ledendb_huiskringen` (`idHuiskring`),
  CONSTRAINT `FK_LedenDB_Huiskringleden_HuiskringLidRol` FOREIGN KEY (`idHuiskringRol`) REFERENCES `ledendb_huiskringlidrollen` (`idHuiskringrol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_huiskringleden`
--

LOCK TABLES `ledendb_huiskringleden` WRITE;
/*!40000 ALTER TABLE `ledendb_huiskringleden` DISABLE KEYS */;
/*!40000 ALTER TABLE `ledendb_huiskringleden` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_huiskringlidrollen`
--

DROP TABLE IF EXISTS `ledendb_huiskringlidrollen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_huiskringlidrollen` (
  `idHuiskringrol` int(11) NOT NULL AUTO_INCREMENT,
  `txtHuiskringrol` varchar(50) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`idHuiskringrol`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_huiskringlidrollen`
--

LOCK TABLES `ledendb_huiskringlidrollen` WRITE;
/*!40000 ALTER TABLE `ledendb_huiskringlidrollen` DISABLE KEYS */;
INSERT INTO `ledendb_huiskringlidrollen` VALUES (1,'Huiskringleider'),(2,'Huiskringlid'),(3,'Huiskringlid kind'),(4,'Wijklid'),(5,'Wijklid kind');
/*!40000 ALTER TABLE `ledendb_huiskringlidrollen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_landen`
--

DROP TABLE IF EXISTS `ledendb_landen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_landen` (
  `idLand` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `txtLandnaam` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idLand`)
) ENGINE=InnoDB AUTO_INCREMENT=245 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_landen`
--

LOCK TABLES `ledendb_landen` WRITE;
/*!40000 ALTER TABLE `ledendb_landen` DISABLE KEYS */;
INSERT INTO `ledendb_landen` VALUES (1,'NEDERLAND'),(2,'ANDORRA'),(3,'VERENIGDE ARABISCHE EMIRATEN'),(4,'AFGHANISTAN'),(5,'ANTIGUA EN BARBUDA'),(6,'ANGUILLA'),(7,'ALBANIE'),(8,'ARMENIE'),(9,'NEDERLANDSE ANTILLEN'),(10,'ANGOLA'),(11,'ANTARCTICA'),(12,'ARGENTINIE'),(13,'AMERIKAANS-SAMOA'),(14,'OOSTENRIJK'),(15,'AUSTRALIE'),(16,'ARUBA'),(17,'AZERBEIDZJAN'),(18,'BOSNIE-HERZEGOVINA'),(19,'BARBADOS'),(20,'BANGLADESH'),(21,'BELGIE'),(22,'BURKINA FASO'),(23,'BULGARIJE'),(24,'BAHREIN'),(25,'BOEROENDI'),(26,'BENIN'),(27,'BERMUDA'),(28,'BRUNEI DARUSSALAM'),(29,'BOLIVIA'),(30,'BAHAMA\'S'),(31,'BHUTAN'),(32,'BOUVETEILAND'),(33,'BOTSWANA'),(34,'BELARUS'),(35,'BELIZE'),(36,'CANADA'),(37,'COCOSEILANDEN (OF KEELINGEILANDEN)'),(38,'CONGO, DEMOCRATISCHE REPUBLIEK'),(39,'CENTRAAL-AFRIKAANSE REPUBLIEK'),(40,'CONGO'),(41,'ZWITSERLAND'),(42,'IVOORKUST'),(43,'COOKEILANDEN'),(44,'CHILI'),(45,'KAMEROEN'),(46,'CHINA'),(47,'COLOMBIA'),(48,'COSTA RICA'),(49,'CUBA'),(50,'KAAPVERDIE'),(51,'CHRISTMASEILAND'),(52,'CYPRUS'),(53,'TSJECHIE'),(54,'DUITSLAND'),(55,'DIJBOUTI'),(56,'DENEMARKEN'),(57,'DOMINICA'),(58,'DOMINICAANSE REPUBLIEK'),(59,'ALGERIJE'),(60,'ECUADOR'),(61,'ESTLAND'),(62,'EGYPTE'),(63,'ERITREA'),(64,'SPANJE'),(65,'ETHIOPIE'),(66,'EUROPESE GEMEENSCHAP'),(67,'FINLAND'),(68,'FIJI'),(69,'FALKLANDEILANDEN'),(70,'MICRONESIA'),(71,'FAEROER'),(72,'FRANKRIJK'),(73,'GABON'),(74,'VERENIGD KONINKRIJK'),(75,'GRENADA'),(76,'GEORGIE'),(77,'GHANA'),(78,'GIBRALTAR'),(79,'GROENLAND'),(80,'GAMBIA'),(81,'GUINEE'),(82,'EQUATORIAAL-GUINEA'),(83,'GRIEKENLAND'),(84,'ZUID-GEORGIE EN DE ZUID-SANDWICHEILANDEN'),(85,'GUATEMALA'),(86,'GUAM'),(87,'GUINEE-BISSAU'),(88,'GUYANA'),(89,'HONGKONG'),(90,'HEARD-EN MCDONALDEILANDEN'),(91,'HONDURAS'),(92,'KROATIE'),(93,'HAITI'),(94,'HONGARIJE'),(95,'INDONESIE'),(96,'IERLAND'),(97,'ISRAEL'),(98,'INDIA'),(99,'BRITS GEBIED IN INDISCHE OCEAAN'),(100,'IRAK'),(101,'IRAN'),(102,'IJSLAND'),(103,'ITALIE'),(104,'JAMAICA'),(105,'JORDANIE'),(106,'JAPAN'),(107,'KENIA'),(108,'KIRGIZIE'),(109,'CAMBODJA'),(110,'KIRIBATI'),(111,'COMOREN'),(112,'SAINT KITTS EN NEVIS'),(113,'NOORD-KOREA'),(114,'ZUID-KOREA'),(115,'KOEWEIT'),(116,'CAYMANEILANDEN'),(117,'KAZACHSTAN'),(118,'LAOS'),(119,'LIBANON'),(120,'SAINT LUCIA'),(121,'LIECHTENSTEIN'),(122,'SRI LANKA'),(123,'LIBERIA'),(124,'LESOTHO'),(125,'LITOUWEN'),(126,'LUXEMBURG'),(127,'LETLAND'),(128,'LYBIE'),(129,'MAROKKO'),(130,'MOLDAVIE'),(131,'MONTENEGRO'),(132,'MADAGASKAR'),(133,'MARSHALLEILANDEN'),(134,'VOORMALIGE JOEGOSLAVISCHE REPUBLIEK MACEDONIE'),(135,'MALI'),(136,'MYANMAR'),(137,'MONGOLIE'),(138,'MACAU'),(139,'NOORDELIJKE MARIANEN'),(140,'MAURITANIE'),(141,'MONTSERRAT'),(142,'MALTA'),(143,'MAURITIUS'),(144,'MALDIVEN'),(145,'MALAWI'),(146,'MEXICO'),(147,'MALEISIE'),(148,'MOZAMBIQUE'),(149,'NAMIBIE'),(150,'NIEUW-CALEDONIE'),(151,'NIGER'),(152,'NORFOLK'),(153,'NIGERIA'),(154,'NICARAGUA'),(155,'NOORWEGEN'),(156,'NEPAL'),(157,'NAURU'),(158,'NIUE'),(159,'NIEUW-ZEELAND'),(160,'OMAN'),(161,'PANAMA'),(162,'PERU'),(163,'FRANS-POLYNESIE'),(164,'PAPOEA-NIEUW-GUINEA'),(165,'FILIPIJNEN'),(166,'PAKISTAN'),(167,'POLEN'),(168,'SAINT-PIERRE EN MIQUELON'),(169,'PITCAIRNEILANDEN'),(170,'BEZETTE PALESTIJNSE GEBIEDEN'),(171,'PORTUGAL'),(172,'PALAU'),(173,'PARAGUAY'),(174,'QATAR'),(175,'BOORDPROVISIE EN BENODIGHEDEN, ALSMEDE BUNKERMATERIAAL'),(176,'BOORDPROV. EN BUNKERMAT. IHK INTRACOMM. HANDELSVERKEER'),(177,'BOORDPROV. EN BUNKERMAT. IHK HANDELSVERKEER 3E LANDEN'),(178,'NIET NADER BEPAALDE LANDEN EN GEBIEDEN'),(179,'NIET NADER BEP. LANDEN IHK INTRACOMM. HANDELSVERKEER'),(180,'NIET NADER BEP. LANDEN IHK HANDELSVERKEER 3E LANDEN'),(181,'OM COMMERCIELE OF MILITAIRE REDENEN NT NADER AANG LANDEN/GEB'),(182,'MILITAIRE LEVERING NNB IHK INTRACOMM. HANDELSVERKEER'),(183,'MILITAIRE LEVERING NNB IHK HANDELSVERKEER 3E LANDEN'),(184,'ROEMENIE'),(185,'RUSLAND'),(186,'RWANDA'),(187,'SAOEDI-ARABIE'),(188,'SALOMONSEILANDEN'),(189,'SEYCHELLEN'),(190,'SOEDAN'),(191,'ZWEDEN'),(192,'SINGAPORE'),(193,'ST. HELENA'),(194,'SLOVENIE'),(195,'SLOWAKIJE'),(196,'SIERRA LEONE'),(197,'SAN MARINO'),(198,'SENEGAL'),(199,'SOMALIE'),(200,'SURINAME'),(201,'SAO TOME EN PRINCIPE'),(202,'EL SALVADOR'),(203,'SYRIE'),(204,'SWAZILAND'),(205,'TURKS-EN CAICOSEILANDEN'),(206,'TSJAAD'),(207,'FRANSE ZUIDELIJKE GEBIEDEN'),(208,'TOGO'),(209,'THAILAND'),(210,'TADZJIKISTAN'),(211,'TOKELAU-EILANDEN'),(212,'TIMOR-LESTE'),(213,'TURKMENISTAN'),(214,'TUNESIE'),(215,'TONGA'),(216,'TURKIJE'),(217,'TRINIDAD EN TOBAGO'),(218,'TUVALU'),(219,'TAIWAN'),(220,'TANZANIA'),(221,'OEKRAINE'),(222,'OEGANDA'),(223,'VERAFGELEGEN EILANDJES VAN DE VERENIGDE STATEN'),(224,'VERENIGDE STATEN'),(225,'URUGUAY'),(226,'OEZBEKISTAN'),(227,'HEILIGE STOEL (VATICAANSTAD)'),(228,'SAINT VINCENT EN DE GRENADINES'),(229,'VENEZUELA'),(230,'BRITSE MAAGDENEILANDEN'),(231,'AMERIKAANSE MAAGDENEILANDEN'),(232,'VIETNAM'),(233,'VANUATU'),(234,'WALLIS EN FUTUNA'),(235,'SAMOA'),(236,'CEUTA'),(237,'KOSOVO'),(238,'MELILLA'),(239,'SERVIE'),(240,'JEMEN'),(241,'MAYOTTE'),(242,'ZUID-AFRIKA'),(243,'ZAMBIA'),(244,'ZIMBABWE');
/*!40000 ALTER TABLE `ledendb_landen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_lidmaatschapstatussen`
--

DROP TABLE IF EXISTS `ledendb_lidmaatschapstatussen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_lidmaatschapstatussen` (
  `idLidmaatschapstatus` int(11) NOT NULL AUTO_INCREMENT,
  `txtLidmaatschapstatus` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `boolVoorQuotum` bit(1) NOT NULL,
  `txtLidmaatschapstatusKort` varchar(50) DEFAULT NULL,
  `txtAttestatie` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idLidmaatschapstatus`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_lidmaatschapstatussen`
--

LOCK TABLES `ledendb_lidmaatschapstatussen` WRITE;
/*!40000 ALTER TABLE `ledendb_lidmaatschapstatussen` DISABLE KEYS */;
INSERT INTO `ledendb_lidmaatschapstatussen` VALUES (1,'Dooplid','','D','doopattestatie'),(2,'Belijdend lid','','B','belijdenisattestatie'),(3,'Catechumeen','\0','C',NULL),(4,'Overig','\0','-',NULL),(5,'Gastlid (belijdend)','\0','B(g)','belijdenisattestatie als gastlid'),(6,'Gastlid (dooplid)','\0','D(g)','doopattestatie als gastlid'),(7,'Gast','\0','G',NULL);
/*!40000 ALTER TABLE `ledendb_lidmaatschapstatussen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_personen`
--

DROP TABLE IF EXISTS `ledendb_personen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_personen` (
  `idPersoon` int(11) NOT NULL AUTO_INCREMENT,
  `idLidmaatschapStatus` int(11) DEFAULT NULL,
  `idGezin` int(11) NOT NULL,
  `idGezinsRol` int(11) NOT NULL,
  `txtAchternaam` varchar(50) NOT NULL,
  `txtTussenvoegsels` varchar(50) DEFAULT NULL,
  `txtVoorletters` varchar(50) DEFAULT NULL,
  `txtDoopnaam` varchar(50) DEFAULT NULL,
  `txtRoepnaam` varchar(50) DEFAULT NULL,
  `boolAansprekenMetRoepnaam` bit(1) DEFAULT NULL,
  `dtmGeboortedatum` datetime DEFAULT NULL,
  `txtGeboorteplaats` varchar(50) DEFAULT NULL,
  `idGeslacht` int(11) DEFAULT NULL,
  `dtmDatumDoop` datetime DEFAULT NULL,
  `idDoopgemeente` int(11) DEFAULT NULL,
  `dtmDatumBelijdenis` datetime DEFAULT NULL,
  `idBelijdenisgemeente` int(11) DEFAULT NULL,
  `dtmHuwelijksDatum` datetime DEFAULT NULL,
  `idHuwelijksGemeente` int(11) DEFAULT NULL,
  `dtmDatumBinnenkomst` datetime DEFAULT NULL,
  `idBinnengekomenUitGemeente` int(11) DEFAULT NULL,
  `dtmDatumVertrek` datetime DEFAULT NULL,
  `idVertrokkenNaarGemeente` int(11) DEFAULT NULL,
  `txtTelefoonNummer` varchar(25) DEFAULT NULL,
  `txtEmailAdres` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `dtmDatumHuwelijksbevestiging` datetime DEFAULT NULL,
  `txtOpmerking` varchar(255) DEFAULT NULL,
  `dtmOverlijdensdatum` datetime DEFAULT NULL,
  `dtmDatumOnttrokken` datetime DEFAULT NULL,
  `boolActief` bit(1) NOT NULL,
  `idWijk` int(11) DEFAULT NULL,
  `idGastGemeente` int(11) DEFAULT NULL,
  `idGastHoofdGemeente` int(11) DEFAULT NULL,
  `boolGastlidNW` bit(1) NOT NULL,
  `boolGeborenNW` bit(1) NOT NULL,
  PRIMARY KEY (`idPersoon`),
  KEY `FK_LedenDB_Personen_LidmaatschapStatus` (`idLidmaatschapStatus`),
  KEY `FK_LedenDB_Personen_Gezinsrollen` (`idGezin`),
  KEY `FK_LedenDB_Personen_Doopgemeente` (`idDoopgemeente`),
  KEY `FK_LedenDB_Personen_Belijdenisgemeente` (`idBelijdenisgemeente`),
  KEY `FK_LedenDB_Personen_Huwelijksgemeente` (`idHuwelijksGemeente`),
  KEY `FK_LedenDB_Personen_BinnengekomenUitGemeente` (`idBinnengekomenUitGemeente`),
  KEY `FK_LedenDB_Personen_VertrokkenNaarGemeente` (`idVertrokkenNaarGemeente`),
  CONSTRAINT `FK_LedenDB_Personen_Belijdenisgemeente` FOREIGN KEY (`idBelijdenisgemeente`) REFERENCES `ledendb_gemeenten` (`idGemeente`),
  CONSTRAINT `FK_LedenDB_Personen_BinnengekomenUitGemeente` FOREIGN KEY (`idBinnengekomenUitGemeente`) REFERENCES `ledendb_gemeenten` (`idGemeente`),
  CONSTRAINT `FK_LedenDB_Personen_Doopgemeente` FOREIGN KEY (`idDoopgemeente`) REFERENCES `ledendb_gemeenten` (`idGemeente`),
  CONSTRAINT `FK_LedenDB_Personen_Gezinnen` FOREIGN KEY (`idGezin`) REFERENCES `ledendb_gezinnen` (`idGezin`),
  CONSTRAINT `FK_LedenDB_Personen_Gezinsrollen` FOREIGN KEY (`idGezin`) REFERENCES `ledendb_gezinnen` (`idGezin`),
  CONSTRAINT `FK_LedenDB_Personen_Huwelijksgemeente` FOREIGN KEY (`idHuwelijksGemeente`) REFERENCES `ledendb_gemeenten` (`idGemeente`),
  CONSTRAINT `FK_LedenDB_Personen_VertrokkenNaarGemeente` FOREIGN KEY (`idVertrokkenNaarGemeente`) REFERENCES `ledendb_gemeenten` (`idGemeente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_personen`
--

LOCK TABLES `ledendb_personen` WRITE;
/*!40000 ALTER TABLE `ledendb_personen` DISABLE KEYS */;
/*!40000 ALTER TABLE `ledendb_personen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ledendb_wijken`
--

DROP TABLE IF EXISTS `ledendb_wijken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ledendb_wijken` (
  `idWijk` int(11) NOT NULL AUTO_INCREMENT,
  `txtWijkNaam` varchar(50) CHARACTER SET latin1 NOT NULL,
  `txtWijkNaamKort` varchar(3) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`idWijk`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ledendb_wijken`
--

LOCK TABLES `ledendb_wijken` WRITE;
/*!40000 ALTER TABLE `ledendb_wijken` DISABLE KEYS */;
INSERT INTO `ledendb_wijken` VALUES (1,'Kop van Lombok, Pijlsweerd',NULL),(2,'Lombok',NULL),(3,'Oog in Al, Lombok-West, Schepenbuurt',NULL),(4,'Leidsche Rijn',NULL),(5,'Ondiep',NULL),(6,'Zuilen-Zuid',NULL),(7,'Zuilen-Noord',NULL),(8,'Overvecht-Zuid',NULL),(9,'Overvecht-Noord',NULL),(10,'Buitenland',NULL);
/*!40000 ALTER TABLE `ledendb_wijken` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-11-20 15:04:53
