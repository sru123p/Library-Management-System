-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: library_management
-- ------------------------------------------------------
-- Server version	8.0.21

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
-- Table structure for table `authors`
--

DROP TABLE IF EXISTS `authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authors` (
  `authorID` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `details` varchar(45) NOT NULL DEFAULT '"nicee"',
  PRIMARY KEY (`authorID`),
  UNIQUE KEY `authorID_UNIQUE` (`authorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authors`
--

LOCK TABLES `authors` WRITE;
/*!40000 ALTER TABLE `authors` DISABLE KEYS */;
/*!40000 ALTER TABLE `authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_authors`
--

DROP TABLE IF EXISTS `book_authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_authors` (
  `bookID` int NOT NULL,
  `authorName` varchar(100) NOT NULL,
  PRIMARY KEY (`authorName`,`bookID`),
  KEY `bookID_idx` (`bookID`),
  CONSTRAINT `bookID` FOREIGN KEY (`bookID`) REFERENCES `books` (`ISBNnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_authors`
--

LOCK TABLES `book_authors` WRITE;
/*!40000 ALTER TABLE `book_authors` DISABLE KEYS */;
INSERT INTO `book_authors` VALUES (21,'ramez_elmasri'),(22,'d_samanta'),(23,'Calre_desouse'),(24,'Hari Narayan'),(25,'Irodov'),(26,'B.M.Sharma'),(27,'Atli sampath'),(28,'Raghu Nandha'),(30,'ponugoti'),(30,'Sruthi');
/*!40000 ALTER TABLE `book_authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `ISBNnumber` int NOT NULL,
  `copyNo` int NOT NULL,
  `title` varchar(45) NOT NULL,
  `publication_year` date DEFAULT NULL,
  `shelfID` int NOT NULL,
  `current_status` varchar(45) DEFAULT 'onshelf',
  `present` varchar(45) DEFAULT 'yes',
  PRIMARY KEY (`ISBNnumber`,`copyNo`),
  UNIQUE KEY `ISBNnumber_UNIQUE` (`ISBNnumber`),
  KEY `shelfID_idx` (`shelfID`),
  CONSTRAINT `shelfID` FOREIGN KEY (`shelfID`) REFERENCES `shelf` (`shelfID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (21,5,'Quantum Mechanics','1997-02-08',2,'not_available','yes'),(22,1,'Light and its effects','1997-02-08',2,'onshelf','no'),(23,3,'datastructures','1999-06-04',1,'available','yes'),(24,1,'powers','2007-04-10',3,'available','yes'),(25,1,'construct','1973-10-21',4,'available','yes'),(26,3,'communism','2002-08-15',3,'not_available','yes'),(27,1,'database_and_information_systems','1985-12-24',1,'available','no'),(28,2,'Linear Algebra','1985-04-10',4,'available','yes'),(30,1,'Green house gases',NULL,3,'onshelf','no'),(60,1,'mechanics',NULL,3,'onshelf','yes'),(64,1,'mechanics',NULL,3,'onshelf','yes');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `borrowed_books`
--

DROP TABLE IF EXISTS `borrowed_books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `borrowed_books` (
  `ISBN_book` int NOT NULL,
  `copy_num` int NOT NULL,
  `id_user` int NOT NULL,
  `issued_date` date NOT NULL,
  `due_id` int NOT NULL,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`copy_num`,`ISBN_book`,`id_user`,`due_id`),
  KEY `ISBN_book_idx` (`ISBN_book`),
  KEY `id_user_idx` (`id_user`),
  KEY `copy_number_idx` (`copy_num`),
  KEY `due_id_idx` (`due_id`),
  CONSTRAINT `due_id` FOREIGN KEY (`due_id`) REFERENCES `dues` (`due_ID`),
  CONSTRAINT `id_user` FOREIGN KEY (`id_user`) REFERENCES `users` (`userID`),
  CONSTRAINT `ISBN_book` FOREIGN KEY (`ISBN_book`) REFERENCES `books` (`ISBNnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `borrowed_books`
--

LOCK TABLES `borrowed_books` WRITE;
/*!40000 ALTER TABLE `borrowed_books` DISABLE KEYS */;
INSERT INTO `borrowed_books` VALUES (22,1,1,'2020-02-08',1,'returned'),(24,1,2,'1997-02-08',2,'borrowed'),(24,1,2,'2021-04-22',6,'borrowed'),(25,1,1,'2020-02-08',4,'borrowed'),(23,3,2,'2020-02-08',2,'borrowed'),(26,3,2,'2020-02-08',5,'borrowed');
/*!40000 ALTER TABLE `borrowed_books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `bookISBN` int NOT NULL,
  `Category_name` varchar(45) NOT NULL,
  PRIMARY KEY (`bookISBN`,`Category_name`),
  KEY `bookISBN_idx` (`bookISBN`),
  CONSTRAINT `bookISBN` FOREIGN KEY (`bookISBN`) REFERENCES `books` (`ISBNnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (21,'Physics'),(22,'Physics'),(23,'Computer Science'),(24,'Civil Engineering'),(25,'Civil Engineering'),(26,'Economics'),(27,'Computer Science'),(28,'Maths');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'sessions','0001_initial','2021-04-22 06:14:25.954429');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

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
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dues`
--

DROP TABLE IF EXISTS `dues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dues` (
  `due_ID` int NOT NULL AUTO_INCREMENT,
  `due_date` date NOT NULL,
  `fine_amount` int DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `payment_method` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`due_ID`),
  UNIQUE KEY `due_ID_UNIQUE` (`due_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dues`
--

LOCK TABLES `dues` WRITE;
/*!40000 ALTER TABLE `dues` DISABLE KEYS */;
INSERT INTO `dues` VALUES (1,'2020-02-08',2195,'2021-04-22','cash'),(2,'2021-02-08',NULL,NULL,NULL),(3,'2021-05-08',NULL,NULL,NULL),(4,'2021-05-08',NULL,NULL,NULL),(5,'2021-05-08',NULL,NULL,NULL),(6,'2021-05-22',NULL,NULL,NULL);
/*!40000 ALTER TABLE `dues` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `friends`
--

DROP TABLE IF EXISTS `friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `friends` (
  `f1ID` int NOT NULL,
  `f2ID` int NOT NULL,
  PRIMARY KEY (`f1ID`,`f2ID`),
  KEY `f2ID_idx` (`f2ID`),
  CONSTRAINT `f1ID` FOREIGN KEY (`f1ID`) REFERENCES `users` (`userID`),
  CONSTRAINT `f2ID` FOREIGN KEY (`f2ID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friends`
--

LOCK TABLES `friends` WRITE;
/*!40000 ALTER TABLE `friends` DISABLE KEYS */;
/*!40000 ALTER TABLE `friends` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `librarians`
--

DROP TABLE IF EXISTS `librarians`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `librarians` (
  `librarianID` int NOT NULL,
  `Name` varchar(45) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `address` varchar(45) NOT NULL,
  PRIMARY KEY (`librarianID`),
  UNIQUE KEY `librarianID_UNIQUE` (`librarianID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `librarians`
--

LOCK TABLES `librarians` WRITE;
/*!40000 ALTER TABLE `librarians` DISABLE KEYS */;
INSERT INTO `librarians` VALUES (1,'sruthi','cse190001047@iiti.ac.in','$2b$12$kV3CmY1.sSVqI85iLLBgjOxAMskyDlmhXEkL6YOtcFwIQ0F.Y6zm.','jc_bose');
/*!40000 ALTER TABLE `librarians` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personal_bookshelf`
--

DROP TABLE IF EXISTS `personal_bookshelf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personal_bookshelf` (
  `iduser` int NOT NULL,
  `ISBNbook` int NOT NULL,
  PRIMARY KEY (`iduser`,`ISBNbook`),
  KEY `iduser_idx` (`iduser`),
  KEY `ISBNbook_idx` (`ISBNbook`),
  CONSTRAINT `iduser` FOREIGN KEY (`iduser`) REFERENCES `users` (`userID`),
  CONSTRAINT `ISBNbook` FOREIGN KEY (`ISBNbook`) REFERENCES `books` (`ISBNnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal_bookshelf`
--

LOCK TABLES `personal_bookshelf` WRITE;
/*!40000 ALTER TABLE `personal_bookshelf` DISABLE KEYS */;
/*!40000 ALTER TABLE `personal_bookshelf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ratings&reviews`
--

DROP TABLE IF EXISTS `ratings&reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ratings&reviews` (
  `user_ID` int NOT NULL,
  `book_ID` int NOT NULL,
  `rating` int NOT NULL,
  `review` varchar(45) NOT NULL,
  PRIMARY KEY (`user_ID`,`book_ID`),
  KEY `user_ID_idx` (`user_ID`),
  KEY `book_ID_idx` (`book_ID`),
  CONSTRAINT `book_ID` FOREIGN KEY (`book_ID`) REFERENCES `books` (`ISBNnumber`),
  CONSTRAINT `user_ID` FOREIGN KEY (`user_ID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings&reviews`
--

LOCK TABLES `ratings&reviews` WRITE;
/*!40000 ALTER TABLE `ratings&reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `ratings&reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shelf`
--

DROP TABLE IF EXISTS `shelf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shelf` (
  `shelfID` int NOT NULL,
  `capacity` varchar(45) NOT NULL,
  PRIMARY KEY (`shelfID`),
  UNIQUE KEY `shelfID_UNIQUE` (`shelfID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shelf`
--

LOCK TABLES `shelf` WRITE;
/*!40000 ALTER TABLE `shelf` DISABLE KEYS */;
INSERT INTO `shelf` VALUES (1,'25'),(2,'20'),(3,'30'),(4,'15'),(5,'25');
/*!40000 ALTER TABLE `shelf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temp_request`
--

DROP TABLE IF EXISTS `temp_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_request` (
  `user1ID` int NOT NULL,
  `user2ID` int NOT NULL,
  PRIMARY KEY (`user1ID`,`user2ID`),
  KEY `user2ID_idx` (`user2ID`),
  CONSTRAINT `user1ID` FOREIGN KEY (`user1ID`) REFERENCES `users` (`userID`),
  CONSTRAINT `user2ID` FOREIGN KEY (`user2ID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temp_request`
--

LOCK TABLES `temp_request` WRITE;
/*!40000 ALTER TABLE `temp_request` DISABLE KEYS */;
/*!40000 ALTER TABLE `temp_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userID` int NOT NULL,
  `Name` varchar(45) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `address` varchar(45) NOT NULL,
  `role` varchar(45) NOT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `idUsers_UNIQUE` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'sruthi','cse190001047@iiti.ac.in','$2b$12$LyMgUFzi31bsCbmBGZFekeNSO1U9M5QIWXuq6./L6MXMxl8xgHlfy','xyz','student'),(2,'Ponugoti Sruthi','ponugotisruthi307@gmail.com','$2b$12$I3u6UBh0sZqz.ND2rgMXYenQmqDOJAX/r0MY90xuM6CA0bkZGhhdS','H.no.8-6-453,christians colony,hasthinapauram','student'),(3,'Yashu','sruthiponugoti25@gmail.com','$2b$12$LyMgUFzi31bsCbmBGZFekeNSO1U9M5QIWXuq6./L6MXMxl8xgHlfy','H.no.8-6-453,christians colony,hasthinapauram','student');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-22 12:31:23
