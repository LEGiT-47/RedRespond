-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: redrespond
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-01-30 15:38:28.970935'),(2,'contenttypes','0002_remove_content_type_name','2025-01-30 15:38:29.043348'),(3,'auth','0001_initial','2025-01-30 15:38:29.376692'),(4,'auth','0002_alter_permission_name_max_length','2025-01-30 15:38:29.439595'),(5,'auth','0003_alter_user_email_max_length','2025-01-30 15:38:29.446414'),(6,'auth','0004_alter_user_username_opts','2025-01-30 15:38:29.452842'),(7,'auth','0005_alter_user_last_login_null','2025-01-30 15:38:29.459842'),(8,'auth','0006_require_contenttypes_0002','2025-01-30 15:38:29.463763'),(9,'auth','0007_alter_validators_add_error_messages','2025-01-30 15:38:29.473769'),(10,'auth','0008_alter_user_username_max_length','2025-01-30 15:38:29.497912'),(11,'auth','0009_alter_user_last_name_max_length','2025-01-30 15:38:29.504913'),(12,'auth','0010_alter_group_name_max_length','2025-01-30 15:38:29.522130'),(13,'auth','0011_update_proxy_permissions','2025-01-30 15:38:29.530302'),(14,'auth','0012_alter_user_first_name_max_length','2025-01-30 15:38:29.537386'),(15,'main','0001_initial','2025-01-30 15:38:29.885162'),(16,'admin','0001_initial','2025-01-30 15:38:30.027529'),(17,'admin','0002_logentry_remove_auto_add','2025-01-30 15:38:30.039061'),(18,'admin','0003_logentry_add_action_flag_choices','2025-01-30 15:38:30.049552'),(19,'main','0002_customuser_address_customuser_blood_group_and_more','2025-01-30 15:38:30.312337'),(20,'main','0003_remove_customuser_blood_group_and_more','2025-01-30 15:38:30.575030'),(21,'sessions','0001_initial','2025-01-30 15:38:30.614962'),(22,'main','0004_donation','2025-02-06 18:46:41.409515'),(23,'main','0005_donation_bloodgroup_donation_not_accepted_reason_and_more','2025-03-08 04:28:23.408206'),(24,'main','0006_remove_donation_bloodgroup','2025-03-08 04:32:11.301375'),(25,'main','0007_remove_donation_confirmed','2025-03-08 04:46:36.863939'),(26,'main','0008_donation_additional_info','2025-03-08 16:13:34.060903');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-08 23:57:23
