-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS dispensadorBD;

-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: dispensadorBD
-- ------------------------------------------------------
-- Server version	8.2.0

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
-- Table structure for table `componentes`
--

DROP TABLE IF EXISTS `componentes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `componentes` (
  `idComponente` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(50) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idComponente`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `componentes`
--

LOCK TABLES `componentes` WRITE;
/*!40000 ALTER TABLE `componentes` DISABLE KEYS */;
INSERT INTO `componentes` VALUES (1,'actuador','dispensador agua','dispensador'),(2,'actuador','dispensador alimento','dispensador');
/*!40000 ALTER TABLE `componentes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registros`
--

DROP TABLE IF EXISTS `registros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registros` (
  `idRegistro` int NOT NULL AUTO_INCREMENT,
  `idComponente` int unsigned DEFAULT NULL,
  `estado` varchar(10) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  PRIMARY KEY (`idRegistro`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registros`
--

LOCK TABLES `registros` WRITE;
/*!40000 ALTER TABLE `registros` DISABLE KEYS */;
INSERT INTO `registros` VALUES (45,1,'CERRADO','2024-03-10','10:05:54'),(46,1,'ABIERTO','2024-03-10','10:09:31'),(47,2,'ABIERTO','2024-03-10','10:11:04'),(48,1,'CERRADO','2024-03-10','10:11:21'),(49,2,'CERRADO','2024-03-10','10:12:50'),(50,1,'ABIERTO','2024-03-10','10:21:02'),(51,1,'CERRADO','2024-03-10','10:21:28'),(52,1,'ABIERTO','2024-03-10','10:22:44'),(53,2,'CERRADO','2024-03-10','10:25:04'),(54,2,'ABIERTO','2024-03-10','10:26:54'),(55,2,'CERRADO','2024-03-10','10:27:00'),(56,1,'CERRADO','2024-03-10','10:27:16'),(57,2,'ABIERTO','2024-03-10','10:28:13'),(58,1,'ABIERTO','2024-03-10','10:28:41'),(59,2,'CERRADO','2024-03-10','10:30:17'),(60,1,'CERRADO','2024-03-10','10:30:34'),(61,1,'ABIERTO','2024-03-10','10:35:05'),(62,1,'CERRADO','2024-03-10','10:35:48'),(63,1,'ABIERTO','2024-03-10','10:36:07'),(64,2,'ABIERTO','2024-03-10','10:36:57'),(65,2,'CERRADO','2024-03-10','10:38:09'),(66,1,'CERRADO','2024-03-10','10:38:14'),(67,2,'ABIERTO','2024-03-10','11:04:23'),(68,1,'ABIERTO','2024-03-10','11:04:33'),(69,2,'CERRADO','2024-03-10','11:05:50'),(70,1,'CERRADO','2024-03-10','11:05:52'),(71,2,'ABIERTO','2024-03-10','11:06:07'),(72,1,'ABIERTO','2024-03-10','11:06:07'),(73,1,'CERRADO','2024-03-10','11:06:10'),(74,2,'CERRADO','2024-03-10','11:06:25'),(75,1,'ABIERTO','2024-03-10','11:06:33'),(76,2,'ABIERTO','2024-03-10','11:06:35'),(77,2,'CERRADO','2024-03-10','11:06:38'),(78,1,'CERRADO','2024-03-10','11:06:40'),(79,1,'ABIERTO','2024-03-10','11:07:09'),(80,1,'CERRADO','2024-03-10','11:10:05'),(81,2,'ABIERTO','2024-03-10','11:10:07'),(82,1,'ABIERTO','2024-03-10','11:10:15'),(83,2,'CERRADO','2024-03-10','11:18:17'),(84,1,'CERRADO','2024-03-10','11:18:18'),(85,1,'ABIERTO','2024-03-10','11:18:24'),(86,1,'CERRADO','2024-03-10','11:19:09'),(87,1,'ABIERTO','2024-03-10','11:19:33'),(88,2,'ABIERTO','2024-03-10','11:26:57'),(89,1,'CERRADO','2024-03-10','11:27:01'),(90,1,'ABIERTO','2024-03-10','11:27:12'),(91,2,'CERRADO','2024-03-10','12:02:01'),(92,2,'ABIERTO','2024-03-10','12:02:02'),(93,2,'CERRADO','2024-03-10','12:02:03'),(94,2,'ABIERTO','2024-03-10','12:02:05'),(95,2,'CERRADO','2024-03-10','12:02:08'),(96,1,'CERRADO','2024-03-10','12:02:51'),(97,1,'ABIERTO','2024-03-10','12:03:18'),(98,1,'CERRADO','2024-03-10','12:03:25');
/*!40000 ALTER TABLE `registros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'dispensadorBD'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-10 14:51:27
