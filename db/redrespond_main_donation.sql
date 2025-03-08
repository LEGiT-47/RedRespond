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
-- Table structure for table `main_donation`
--

DROP TABLE IF EXISTS `main_donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_donation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `donated_amount` decimal(5,2) NOT NULL,
  `scheduled_datetime` datetime(6) NOT NULL,
  `request_datetime` datetime(6) NOT NULL,
  `blood_bank_id` bigint NOT NULL,
  `donor_id` bigint NOT NULL,
  `not_accepted_reason` longtext,
  `status` varchar(20) NOT NULL,
  `additional_info` longtext,
  PRIMARY KEY (`id`),
  KEY `main_donation_blood_bank_id_dbd7817e_fk_main_bloodbank_id` (`blood_bank_id`),
  KEY `main_donation_donor_id_2c222ab3_fk_main_customuser_id` (`donor_id`),
  CONSTRAINT `main_donation_blood_bank_id_dbd7817e_fk_main_bloodbank_id` FOREIGN KEY (`blood_bank_id`) REFERENCES `main_bloodbank` (`id`),
  CONSTRAINT `main_donation_donor_id_2c222ab3_fk_main_customuser_id` FOREIGN KEY (`donor_id`) REFERENCES `main_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_donation`
--

LOCK TABLES `main_donation` WRITE;
/*!40000 ALTER TABLE `main_donation` DISABLE KEYS */;
INSERT INTO `main_donation` VALUES (1,0.30,'2025-02-08 10:00:00.000000','2025-02-06 18:48:29.515828',1,1,'day not suitable','not_accepted',NULL),(2,0.30,'2025-02-08 10:00:00.000000','2025-02-06 18:48:55.428114',1,1,'','donated',NULL),(3,0.23,'2025-02-04 16:23:00.000000','2025-02-18 10:53:45.411451',1,1,'','pending',NULL),(4,1.00,'2025-04-01 18:31:00.000000','2025-03-07 13:01:48.936191',1,1,'','pending',NULL),(5,0.48,'2025-03-11 10:07:00.000000','2025-03-08 04:40:38.293321',1,1,NULL,'not_confirmed',NULL),(6,0.50,'2025-02-26 08:38:00.000000','2025-03-08 16:05:23.070670',1,1,'','donated',NULL),(9,1.50,'2025-03-26 21:00:00.000000','2025-03-08 16:21:25.841169',1,1,NULL,'not_confirmed','i am coughing'),(10,1.36,'2025-03-16 21:00:00.000000','2025-03-08 16:22:12.120800',1,1,'','pending','bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb');
/*!40000 ALTER TABLE `main_donation` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-08 23:57:22
