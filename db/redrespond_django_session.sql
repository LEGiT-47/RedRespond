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
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('23a8ansxhs52fxjde3gdvppuw78rz6zm','.eJxVjDkOwjAUBe_iGlnxEi-U9JzBel4-DiBbylIh7g6RUkD7Zua9WMC21rAtZQ5TZmcm2Ol3i0iP0naQ72i3zlNv6zxFviv8oAu_9lyel8P9O6hY6rd2eowyOZCxKjpLA0jEQRZFRnhE70HSkgGK1QTlR-HJqVErDVDRjr0_8RQ4RA:1tkKNx:GpwmCxmZ1XvUqXFEodvV4JFchpkaUsY3G_yhR1fnsUc','2025-03-04 09:59:25.404441'),('2y3deo261eficydizer602hfyg8i67os','.eJxVjDkOwjAUBe_iGlnxEi-U9JzBel4-DiBbylIh7g6RUkD7Zua9WMC21rAtZQ5TZmcm2Ol3i0iP0naQ72i3zlNv6zxFviv8oAu_9lyel8P9O6hY6rd2eowyOZCxKjpLA0jEQRZFRnhE70HSkgGK1QTlR-HJqVErDVDRjr0_8RQ4RA:1tkKNx:GpwmCxmZ1XvUqXFEodvV4JFchpkaUsY3G_yhR1fnsUc','2025-03-04 09:59:25.836591'),('5orddmung6xqzxowxwe4qxd0hp9nxj9d','.eJxVjDkOwjAUBe_iGlnxEi-U9JzBel4-DiBbylIh7g6RUkD7Zua9WMC21rAtZQ5TZmcm2Ol3i0iP0naQ72i3zlNv6zxFviv8oAu_9lyel8P9O6hY6rd2eowyOZCxKjpLA0jEQRZFRnhE70HSkgGK1QTlR-HJqVErDVDRjr0_8RQ4RA:1tg6yq:m-sDFL29nKpDk5imW9FxS5wWTTJz9lZWqmE3GBR2H-4','2025-02-20 18:52:04.650264'),('63yst476o2i80vfq04qax9dd4sh8f2qg','.eJxVjDkOwjAUBe_iGlnxEi-U9JzBel4-DiBbylIh7g6RUkD7Zua9WMC21rAtZQ5TZmcm2Ol3i0iP0naQ72i3zlNv6zxFviv8oAu_9lyel8P9O6hY6rd2eowyOZCxKjpLA0jEQRZFRnhE70HSkgGK1QTlR-HJqVErDVDRjr0_8RQ4RA:1tms5W:MK3yBEoYJd1pogj27nU_D_3ALf940qLmQkieXzWMHyY','2025-03-11 10:22:54.677397'),('8ypqo4i1i12syyhqpo92fcj0fyiocp7w','.eJxVjDkOwjAUBe_iGlnxEi-U9JzBel4-DiBbylIh7g6RUkD7Zua9WMC21rAtZQ5TZmcm2Ol3i0iP0naQ72i3zlNv6zxFviv8oAu_9lyel8P9O6hY6rd2eowyOZCxKjpLA0jEQRZFRnhE70HSkgGK1QTlR-HJqVErDVDRjr0_8RQ4RA:1tqwEO:VnIHqTXLzZAt-rs1l-W1tc9yJqkMKCqwXfSrpSmSgJ4','2025-03-22 15:36:52.034751'),('9h6swbukhw403bshwljdgimzebrmxevu','.eJxVjDkOwjAUBe_iGlnxEi-U9JzBel4-DiBbylIh7g6RUkD7Zua9WMC21rAtZQ5TZmcm2Ol3i0iP0naQ72i3zlNv6zxFviv8oAu_9lyel8P9O6hY6rd2eowyOZCxKjpLA0jEQRZFRnhE70HSkgGK1QTlR-HJqVErDVDRjr0_8RQ4RA:1tho9S:Nfvdfw1zzme_n0Wq__R_aUoaUVBwCtUZX_7n0B_55JE','2025-02-25 11:10:02.184624'),('m00ca1s3wmtaaxl1hpc8ji43at0b0bl5','.eJxVjEEOgjAQRe_StWlombajS_ecoZnpDIIaSCisjHdXEha6_e-9_zKZtnXIW9Ulj2IuxpvT78ZUHjrtQO403WZb5mldRra7Yg9abTeLPq-H-3cwUB2-9RmDxFaRXAAsrUT2jAINA4AUjqUP0SmIRvShgdRHbENymDyRMjrz_gDaNzeC:1tdZvU:sT5NEjIlOMaDFZkTM_Sc8wnq9rwVLJTp6tKySjem3jo','2025-02-13 19:10:08.976101'),('r9l4k5hlbahqrn417hyke66xlrtxcm6w','.eJxVjEEOgjAQRe_StWlombajS_ecoZnpDIIaSCisjHdXEha6_e-9_zKZtnXIW9Ulj2IuxpvT78ZUHjrtQO403WZb5mldRra7Yg9abTeLPq-H-3cwUB2-9RmDxFaRXAAsrUT2jAINA4AUjqUP0SmIRvShgdRHbENymDyRMjrz_gDaNzeC:1tqwGv:N7kDHgilWDZk9iPmhQSQA51AsZP-P7DOFHbmdIQRmfk','2025-03-22 15:39:29.243122');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
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
