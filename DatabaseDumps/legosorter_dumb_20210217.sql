CREATE DATABASE  IF NOT EXISTS `LegoSorterDB` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `LegoSorterDB`;
-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: LegoSorterDB
-- ------------------------------------------------------
-- Server version	8.0.23-0ubuntu0.20.04.1

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
-- Table structure for table `Categories`
--

DROP TABLE IF EXISTS `Categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Categories` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `category_id` int unsigned NOT NULL,
  `category_name` varchar(500) NOT NULL,
  `parent_id` int unsigned NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_id` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=500 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Collections`
--

DROP TABLE IF EXISTS `Collections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Collections` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(300) DEFAULT NULL,
  `weight_kg` decimal(18,0) unsigned DEFAULT NULL,
  `origin` varchar(300) DEFAULT NULL,
  `origin_url` varchar(300) DEFAULT NULL,
  `seller` varchar(300) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `cost` decimal(18,0) unsigned DEFAULT NULL,
  `porto` decimal(18,0) unsigned DEFAULT NULL,
  `thumbnail_url` varchar(500) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Colors`
--

DROP TABLE IF EXISTS `Colors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Colors` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `color_id` int unsigned NOT NULL,
  `color_name` varchar(500) NOT NULL,
  `color_code` varchar(20) NOT NULL,
  `color_type` varchar(20) NOT NULL,
  `parts_count` int unsigned DEFAULT NULL,
  `year_from` int unsigned DEFAULT NULL,
  `year_to` int unsigned DEFAULT NULL,
  `lower_treshold` varchar(15) DEFAULT NULL,
  `upper_treshold` varchar(15) DEFAULT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `color_id` (`color_id`)
) ENGINE=InnoDB AUTO_INCREMENT=179 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Partimages`
--

DROP TABLE IF EXISTS `Partimages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Partimages` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `run_id` int unsigned NOT NULL,
  `path` varchar(300) NOT NULL,
  `size_kb` int unsigned DEFAULT NULL,
  `x` int unsigned DEFAULT NULL,
  `y` int unsigned DEFAULT NULL,
  `w` int unsigned DEFAULT NULL,
  `h` int unsigned DEFAULT NULL,
  `blue` int unsigned DEFAULT NULL,
  `green` int unsigned DEFAULT NULL,
  `red` int unsigned DEFAULT NULL,
  `color` varchar(45) DEFAULT NULL,
  `camera` varchar(45) DEFAULT NULL,
  `created` datetime NOT NULL,
  `imported` datetime NOT NULL,
  `deleted` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path` (`path`)
) ENGINE=InnoDB AUTO_INCREMENT=53258 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Parts`
--

DROP TABLE IF EXISTS `Parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Parts` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `no` varchar(100) NOT NULL,
  `name` varchar(200) NOT NULL,
  `type` varchar(50) NOT NULL,
  `category_id` int unsigned NOT NULL,
  `color_id` int unsigned NOT NULL,
  `year` varchar(100) DEFAULT NULL,
  `weight_g` int DEFAULT NULL,
  `size` varchar(200) DEFAULT NULL,
  `is_obsolete` tinyint(1) DEFAULT NULL,
  `qty_avg_price_stock` double unsigned DEFAULT NULL,
  `qty_avg_price_sold` double unsigned DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `thumbnail_url` varchar(500) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `part` (`no`,`color_id`,`type`)
) ENGINE=InnoDB AUTO_INCREMENT=24416 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Prices`
--

DROP TABLE IF EXISTS `Prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Prices` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `no` varchar(100) NOT NULL,
  `type` varchar(50) NOT NULL,
  `new_or_used` varchar(1) NOT NULL,
  `color_id` int unsigned NOT NULL,
  `region` varchar(10) NOT NULL,
  `guide_type` varchar(10) NOT NULL,
  `currency_code` varchar(10) NOT NULL,
  `min_price` double unsigned NOT NULL,
  `max_price` double unsigned NOT NULL,
  `avg_price` double unsigned NOT NULL,
  `qty_avg_price` double unsigned NOT NULL,
  `unit_quantity` int unsigned NOT NULL,
  `total_quantity` int unsigned NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `price` (`no`,`type`,`new_or_used`,`color_id`,`region`,`guide_type`,`currency_code`)
) ENGINE=InnoDB AUTO_INCREMENT=48853 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Recognisedimages`
--

DROP TABLE IF EXISTS `Recognisedimages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Recognisedimages` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `image_id` int unsigned NOT NULL,
  `part_id` int unsigned NOT NULL,
  `score` double unsigned DEFAULT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `image_id` (`image_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53258 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Recognisedparts`
--

DROP TABLE IF EXISTS `Recognisedparts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Recognisedparts` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `run_id` int unsigned NOT NULL,
  `no` varchar(100) DEFAULT NULL,
  `color_id` int unsigned DEFAULT NULL,
  `score` double unsigned DEFAULT NULL,
  `identifier` varchar(300) DEFAULT NULL,
  `created` datetime NOT NULL,
  `deleted` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6231 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Recognisedsets`
--

DROP TABLE IF EXISTS `Recognisedsets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Recognisedsets` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `collection_id` int unsigned NOT NULL,
  `setNo` varchar(300) NOT NULL,
  `comments` varchar(500) DEFAULT NULL,
  `instructions` varchar(45) DEFAULT NULL,
  `condition` varchar(500) DEFAULT NULL,
  `status` int NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RunStatus`
--

DROP TABLE IF EXISTS `RunStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RunStatus` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `run_id` int unsigned NOT NULL,
  `status` int unsigned NOT NULL,
  `reason` varchar(1000) DEFAULT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Runs`
--

DROP TABLE IF EXISTS `Runs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Runs` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `no` int unsigned NOT NULL,
  `collection_id` int unsigned NOT NULL,
  `sorter_id` int unsigned NOT NULL,
  `imagefolder` varchar(500) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Sets`
--

DROP TABLE IF EXISTS `Sets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sets` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `no` varchar(300) NOT NULL,
  `name` varchar(500) DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `year` varchar(100) DEFAULT NULL,
  `weight_g` int DEFAULT NULL,
  `size` varchar(200) DEFAULT NULL,
  `complete_part_count` int unsigned DEFAULT NULL,
  `complete_minifigs_count` int DEFAULT NULL,
  `min_price` decimal(11,0) DEFAULT NULL,
  `max_price` decimal(11,0) DEFAULT NULL,
  `avg_price` decimal(11,0) DEFAULT NULL,
  `qty_avg_price` decimal(11,0) DEFAULT NULL,
  `unit_quantity` int DEFAULT NULL,
  `total_quantity` int DEFAULT NULL,
  `thumbnail_url` varchar(500) DEFAULT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=140 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Sorters`
--

DROP TABLE IF EXISTS `Sorters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sorters` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `lifter_status_url` varchar(200) DEFAULT NULL,
  `lifter_update_url` varchar(200) DEFAULT NULL,
  `lifter_alterspeed_url` varchar(200) DEFAULT NULL,
  `vfeeder_status_url` varchar(200) DEFAULT NULL,
  `vfeeder_update_url` varchar(200) DEFAULT NULL,
  `vfeeder_alterspeed_url` varchar(200) DEFAULT NULL,
  `conveyor_status_url` varchar(200) DEFAULT NULL,
  `conveyor_update_url` varchar(200) DEFAULT NULL,
  `conveyor_alterspeed_url` varchar(200) DEFAULT NULL,
  `pusher_count` int DEFAULT NULL,
  `pusher_status_baseurl` varchar(200) DEFAULT NULL,
  `pusher_mode_baseurl` varchar(200) DEFAULT NULL,
  `created` datetime NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Status`
--

DROP TABLE IF EXISTS `Status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Status` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` varchar(20) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  UNIQUE KEY `status_id` (`id`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Subsets`
--

DROP TABLE IF EXISTS `Subsets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Subsets` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `setNo` int NOT NULL,
  `match_no` int unsigned NOT NULL,
  `no` varchar(100) NOT NULL,
  `name` varchar(200) NOT NULL,
  `type` varchar(50) NOT NULL,
  `category_id` int unsigned NOT NULL,
  `color_id` int unsigned DEFAULT NULL,
  `quantity` int unsigned NOT NULL,
  `extra_quantity` int unsigned NOT NULL,
  `is_alternate` tinyint(1) NOT NULL,
  `is_counterpart` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subset` (`setNo`,`no`,`color_id`,`is_counterpart`)
) ENGINE=InnoDB AUTO_INCREMENT=24874 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `SuperSets`
--

DROP TABLE IF EXISTS `SuperSets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SuperSets` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `partNo` varchar(100) NOT NULL,
  `setNo` varchar(100) NOT NULL,
  `name` varchar(200) NOT NULL,
  `type` varchar(50) NOT NULL,
  `category_id` int unsigned NOT NULL,
  `color_id` int unsigned DEFAULT NULL,
  `quantity` int unsigned NOT NULL,
  `appears_as` varchar(10) DEFAULT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `superset` (`partNo`,`setNo`,`color_id`)
) ENGINE=InnoDB AUTO_INCREMENT=83578 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(16) NOT NULL,
  `password` varchar(60) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `max_recognisedparts_in_a_run_view`
--

DROP TABLE IF EXISTS `max_recognisedparts_in_a_run_view`;
/*!50001 DROP VIEW IF EXISTS `max_recognisedparts_in_a_run_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `max_recognisedparts_in_a_run_view` AS SELECT 
 1 AS `collection_id`,
 1 AS `partno`,
 1 AS `color_id`,
 1 AS `max_count`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `parts_overview`
--

DROP TABLE IF EXISTS `parts_overview`;
/*!50001 DROP VIEW IF EXISTS `parts_overview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `parts_overview` AS SELECT 
 1 AS `collection_id`,
 1 AS `setIds`,
 1 AS `match_no`,
 1 AS `thumbnail_url`,
 1 AS `part_no`,
 1 AS `setNos`,
 1 AS `name`,
 1 AS `type`,
 1 AS `category_id`,
 1 AS `color_id`,
 1 AS `color_name`,
 1 AS `quantities`,
 1 AS `total_quantity`,
 1 AS `qty_avg_price_stock`,
 1 AS `qty_avg_price_sold`,
 1 AS `extra_quantities`,
 1 AS `is_alternates`,
 1 AS `is_counterparts`,
 1 AS `status_name`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `recognisedparts_deltaparts_view`
--

DROP TABLE IF EXISTS `recognisedparts_deltaparts_view`;
/*!50001 DROP VIEW IF EXISTS `recognisedparts_deltaparts_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `recognisedparts_deltaparts_view` AS SELECT 
 1 AS `collection_id`,
 1 AS `setNo`,
 1 AS `partno`,
 1 AS `color_id`,
 1 AS `expecting`,
 1 AS `existing`,
 1 AS `missing`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `recognisedparts_existingpartsperset_view`
--

DROP TABLE IF EXISTS `recognisedparts_existingpartsperset_view`;
/*!50001 DROP VIEW IF EXISTS `recognisedparts_existingpartsperset_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `recognisedparts_existingpartsperset_view` AS SELECT 
 1 AS `collection_id`,
 1 AS `setNo`,
 1 AS `parts_existing`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `recognisedparts_per_run_view`
--

DROP TABLE IF EXISTS `recognisedparts_per_run_view`;
/*!50001 DROP VIEW IF EXISTS `recognisedparts_per_run_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `recognisedparts_per_run_view` AS SELECT 
 1 AS `collection_id`,
 1 AS `run_id`,
 1 AS `partno`,
 1 AS `color_id`,
 1 AS `count`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `recognisedparts_usage_view`
--

DROP TABLE IF EXISTS `recognisedparts_usage_view`;
/*!50001 DROP VIEW IF EXISTS `recognisedparts_usage_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `recognisedparts_usage_view` AS SELECT 
 1 AS `run_collection_id`,
 1 AS `partNo`,
 1 AS `color_id`,
 1 AS `downloaded_sets`,
 1 AS `part_in_sets_of_collection`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `recognisedparts_usage_with_supersets_view`
--

DROP TABLE IF EXISTS `recognisedparts_usage_with_supersets_view`;
/*!50001 DROP VIEW IF EXISTS `recognisedparts_usage_with_supersets_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `recognisedparts_usage_with_supersets_view` AS SELECT 
 1 AS `run_collection_id`,
 1 AS `partNo`,
 1 AS `color_id`,
 1 AS `downloaded_sets`,
 1 AS `part_in_sets_of_collection`,
 1 AS `super_setnos`,
 1 AS `super_set_count`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `sets_overview`
--

DROP TABLE IF EXISTS `sets_overview`;
/*!50001 DROP VIEW IF EXISTS `sets_overview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `sets_overview` AS SELECT 
 1 AS `rs_id`,
 1 AS `collection_id`,
 1 AS `comments`,
 1 AS `instructions`,
 1 AS `condition`,
 1 AS `s_id`,
 1 AS `no`,
 1 AS `name`,
 1 AS `category_id`,
 1 AS `year`,
 1 AS `weight_g`,
 1 AS `size`,
 1 AS `complete_part_count`,
 1 AS `complete_minifigs_count`,
 1 AS `min_price`,
 1 AS `max_price`,
 1 AS `avg_price`,
 1 AS `qty_avg_price`,
 1 AS `unit_quantity`,
 1 AS `total_quantity`,
 1 AS `thumbnail_url`,
 1 AS `image_url`,
 1 AS `created`,
 1 AS `parts_existing`,
 1 AS `complete_percentage`,
 1 AS `category_name`,
 1 AS `status_name`,
 1 AS `status_description`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `sets_view`
--

DROP TABLE IF EXISTS `sets_view`;
/*!50001 DROP VIEW IF EXISTS `sets_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `sets_view` AS SELECT 
 1 AS `id`,
 1 AS `no`,
 1 AS `name`,
 1 AS `year`,
 1 AS `weight_g`,
 1 AS `size`,
 1 AS `complete_part_count`,
 1 AS `complete_minifigs_count`,
 1 AS `min_price`,
 1 AS `max_price`,
 1 AS `avg_price`,
 1 AS `qty_avg_price`,
 1 AS `unit_quantity`,
 1 AS `total_quantity`,
 1 AS `thumbnail_url`,
 1 AS `image_url`,
 1 AS `created`,
 1 AS `category_name`,
 1 AS `rs_ids`,
 1 AS `rs_collection_ids`,
 1 AS `rs_comments`,
 1 AS `rs_instructions`,
 1 AS `rs_conditions`,
 1 AS `rs_status_names`,
 1 AS `rs_status_descriptions`,
 1 AS `rs_created`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `suggested_sets`
--

DROP TABLE IF EXISTS `suggested_sets`;
/*!50001 DROP VIEW IF EXISTS `suggested_sets`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `suggested_sets` AS SELECT 
 1 AS `collection_id`,
 1 AS `partNos`,
 1 AS `color_ids`,
 1 AS `setNo`,
 1 AS `count`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `suggested_sets_detail_view`
--

DROP TABLE IF EXISTS `suggested_sets_detail_view`;
/*!50001 DROP VIEW IF EXISTS `suggested_sets_detail_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `suggested_sets_detail_view` AS SELECT 
 1 AS `collection_id`,
 1 AS `partNos`,
 1 AS `color_ids`,
 1 AS `setNo`,
 1 AS `count`,
 1 AS `s_id`,
 1 AS `no`,
 1 AS `name`,
 1 AS `category_id`,
 1 AS `year`,
 1 AS `weight_g`,
 1 AS `size`,
 1 AS `complete_part_count`,
 1 AS `complete_minifigs_count`,
 1 AS `min_price`,
 1 AS `max_price`,
 1 AS `avg_price`,
 1 AS `qty_avg_price`,
 1 AS `unit_quantity`,
 1 AS `total_quantity`,
 1 AS `thumbnail_url`,
 1 AS `image_url`,
 1 AS `created`,
 1 AS `parts_existing`,
 1 AS `complete_percentage`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `unsetted_parts`
--

DROP TABLE IF EXISTS `unsetted_parts`;
/*!50001 DROP VIEW IF EXISTS `unsetted_parts`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `unsetted_parts` AS SELECT 
 1 AS `collection_id`,
 1 AS `partNo`,
 1 AS `color_id`,
 1 AS `downloaded_sets`,
 1 AS `part_in_sets_of_collection`,
 1 AS `super_setnos`,
 1 AS `super_set_count`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'LegoSorterDB'
--

--
-- Dumping routines for database 'LegoSorterDB'
--

--
-- Final view structure for view `max_recognisedparts_in_a_run_view`
--

/*!50001 DROP VIEW IF EXISTS `max_recognisedparts_in_a_run_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `max_recognisedparts_in_a_run_view` AS select `recognisedparts_per_run_view`.`collection_id` AS `collection_id`,`recognisedparts_per_run_view`.`partno` AS `partno`,`recognisedparts_per_run_view`.`color_id` AS `color_id`,max(`recognisedparts_per_run_view`.`count`) AS `max_count` from `recognisedparts_per_run_view` group by `recognisedparts_per_run_view`.`collection_id`,`recognisedparts_per_run_view`.`partno`,`recognisedparts_per_run_view`.`color_id` order by `recognisedparts_per_run_view`.`partno` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `parts_overview`
--

/*!50001 DROP VIEW IF EXISTS `parts_overview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `parts_overview` AS select `rs`.`collection_id` AS `collection_id`,group_concat(`sets`.`id` separator ',') AS `setIds`,`Subsets`.`match_no` AS `match_no`,`p`.`thumbnail_url` AS `thumbnail_url`,`p`.`no` AS `part_no`,group_concat(`Subsets`.`setNo` separator ',') AS `setNos`,`Subsets`.`name` AS `name`,`Subsets`.`type` AS `type`,`Subsets`.`category_id` AS `category_id`,`Subsets`.`color_id` AS `color_id`,`c`.`color_name` AS `color_name`,group_concat(`Subsets`.`quantity` separator ',') AS `quantities`,sum(`Subsets`.`quantity`) AS `total_quantity`,`p`.`qty_avg_price_stock` AS `qty_avg_price_stock`,`p`.`qty_avg_price_sold` AS `qty_avg_price_sold`,group_concat(`Subsets`.`extra_quantity` separator ',') AS `extra_quantities`,group_concat(`Subsets`.`is_alternate` separator ',') AS `is_alternates`,group_concat(`Subsets`.`is_counterpart` separator ',') AS `is_counterparts`,`st`.`name` AS `status_name` from (((((`Subsets` left join `Sets` `sets` on((`sets`.`no` = `Subsets`.`setNo`))) left join `Recognisedsets` `rs` on((`rs`.`setNo` = convert(`sets`.`no` using utf8mb4)))) left join `Colors` `c` on((`c`.`color_id` = `Subsets`.`color_id`))) left join `Parts` `p` on(((`Subsets`.`no` = `p`.`no`) and (`Subsets`.`color_id` = `p`.`color_id`)))) left join `Status` `st` on(((`p`.`status` = `st`.`id`) and (`st`.`type` = `Subsets`.`type`)))) group by `rs`.`collection_id`,`Subsets`.`match_no`,`p`.`thumbnail_url`,`p`.`no`,`Subsets`.`name`,`Subsets`.`type`,`Subsets`.`category_id`,`Subsets`.`color_id`,`c`.`color_name`,`p`.`qty_avg_price_stock`,`p`.`qty_avg_price_sold`,`st`.`name` order by concat(`c`.`color_name`,' ',`Subsets`.`name`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `recognisedparts_deltaparts_view`
--

/*!50001 DROP VIEW IF EXISTS `recognisedparts_deltaparts_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `recognisedparts_deltaparts_view` AS select `mp`.`collection_id` AS `collection_id`,`sub`.`setNo` AS `setNo`,`sub`.`no` AS `partno`,`sub`.`color_id` AS `color_id`,`sub`.`quantity` AS `expecting`,if((`mp`.`max_count` is null),0,`mp`.`max_count`) AS `existing`,if((if((`mp`.`max_count` is null),0,`mp`.`max_count`) > `sub`.`quantity`),0,(`sub`.`quantity` - if((`mp`.`max_count` is null),0,`mp`.`max_count`))) AS `missing` from (`Subsets` `sub` left join `max_recognisedparts_in_a_run_view` `mp` on(((`sub`.`no` = `mp`.`partno`) and (`sub`.`color_id` = `mp`.`color_id`)))) where (`sub`.`type` = 'PART') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `recognisedparts_existingpartsperset_view`
--

/*!50001 DROP VIEW IF EXISTS `recognisedparts_existingpartsperset_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `recognisedparts_existingpartsperset_view` AS select `recognisedparts_deltaparts_view`.`collection_id` AS `collection_id`,`recognisedparts_deltaparts_view`.`setNo` AS `setNo`,(sum(`recognisedparts_deltaparts_view`.`expecting`) - sum(`recognisedparts_deltaparts_view`.`missing`)) AS `parts_existing` from `recognisedparts_deltaparts_view` where (`recognisedparts_deltaparts_view`.`collection_id` is not null) group by `recognisedparts_deltaparts_view`.`setNo`,`recognisedparts_deltaparts_view`.`collection_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `recognisedparts_per_run_view`
--

/*!50001 DROP VIEW IF EXISTS `recognisedparts_per_run_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `recognisedparts_per_run_view` AS select `Runs`.`collection_id` AS `collection_id`,`rp`.`run_id` AS `run_id`,`rp`.`no` AS `partno`,`rp`.`color_id` AS `color_id`,count(0) AS `count` from (`Recognisedparts` `rp` left join `Runs` on((`Runs`.`id` = `rp`.`run_id`))) where (`rp`.`color_id` > 0) group by `Runs`.`collection_id`,`rp`.`run_id`,`rp`.`no`,`rp`.`color_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `recognisedparts_usage_view`
--

/*!50001 DROP VIEW IF EXISTS `recognisedparts_usage_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `recognisedparts_usage_view` AS select `r`.`collection_id` AS `run_collection_id`,`rp`.`no` AS `partNo`,`rp`.`color_id` AS `color_id`,group_concat(`sub`.`setNo` separator ',') AS `downloaded_sets`,sum(if((`rs`.`collection_id` > 0),1,0)) AS `part_in_sets_of_collection` from (((`Recognisedparts` `rp` left join `Runs` `r` on((`r`.`id` = `rp`.`run_id`))) left join `Subsets` `sub` on(((`rp`.`no` = `sub`.`no`) and (`rp`.`color_id` = `sub`.`color_id`)))) left join `Recognisedsets` `rs` on(((`rs`.`setNo` = `sub`.`setNo`) and (`rs`.`collection_id` = `r`.`collection_id`)))) where (`rp`.`color_id` > 0) group by `rp`.`no`,`rp`.`color_id`,`r`.`collection_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `recognisedparts_usage_with_supersets_view`
--

/*!50001 DROP VIEW IF EXISTS `recognisedparts_usage_with_supersets_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `recognisedparts_usage_with_supersets_view` AS select `pu`.`run_collection_id` AS `run_collection_id`,`pu`.`partNo` AS `partNo`,`pu`.`color_id` AS `color_id`,`pu`.`downloaded_sets` AS `downloaded_sets`,`pu`.`part_in_sets_of_collection` AS `part_in_sets_of_collection`,group_concat(`super`.`setNo` separator ',') AS `super_setnos`,sum(if((`super`.`setNo` is not null),1,0)) AS `super_set_count` from (`recognisedparts_usage_view` `pu` left join `SuperSets` `super` on((`super`.`partNo` = `pu`.`partNo`))) group by `pu`.`run_collection_id`,`pu`.`partNo`,`pu`.`color_id`,`pu`.`downloaded_sets`,`pu`.`part_in_sets_of_collection` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `sets_overview`
--

/*!50001 DROP VIEW IF EXISTS `sets_overview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `sets_overview` AS select `rs`.`id` AS `rs_id`,`rs`.`collection_id` AS `collection_id`,`rs`.`comments` AS `comments`,`rs`.`instructions` AS `instructions`,`rs`.`condition` AS `condition`,`s`.`id` AS `s_id`,`s`.`no` AS `no`,`s`.`name` AS `name`,`s`.`category_id` AS `category_id`,`s`.`year` AS `year`,`s`.`weight_g` AS `weight_g`,`s`.`size` AS `size`,`s`.`complete_part_count` AS `complete_part_count`,`s`.`complete_minifigs_count` AS `complete_minifigs_count`,`s`.`min_price` AS `min_price`,`s`.`max_price` AS `max_price`,`s`.`avg_price` AS `avg_price`,`s`.`qty_avg_price` AS `qty_avg_price`,`s`.`unit_quantity` AS `unit_quantity`,`s`.`total_quantity` AS `total_quantity`,`s`.`thumbnail_url` AS `thumbnail_url`,`s`.`image_url` AS `image_url`,`s`.`created` AS `created`,`ep`.`parts_existing` AS `parts_existing`,round(((`ep`.`parts_existing` / `s`.`complete_part_count`) * 100),2) AS `complete_percentage`,`c`.`category_name` AS `category_name`,`st`.`name` AS `status_name`,`st`.`description` AS `status_description` from ((((`Recognisedsets` `rs` left join `Sets` `s` on((convert(`s`.`no` using utf8mb4) = `rs`.`setNo`))) left join `Categories` `c` on((`c`.`category_id` = `s`.`category_id`))) left join `Status` `st` on(((`rs`.`status` = `st`.`id`) and (`st`.`type` = 'SET')))) left join `recognisedparts_existingpartsperset_view` `ep` on(((`ep`.`setNo` = `s`.`no`) and (`ep`.`collection_id` = `rs`.`collection_id`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `sets_view`
--

/*!50001 DROP VIEW IF EXISTS `sets_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `sets_view` AS select `Sets`.`id` AS `id`,`Sets`.`no` AS `no`,`Sets`.`name` AS `name`,`Sets`.`year` AS `year`,`Sets`.`weight_g` AS `weight_g`,`Sets`.`size` AS `size`,`Sets`.`complete_part_count` AS `complete_part_count`,`Sets`.`complete_minifigs_count` AS `complete_minifigs_count`,`Sets`.`min_price` AS `min_price`,`Sets`.`max_price` AS `max_price`,`Sets`.`avg_price` AS `avg_price`,`Sets`.`qty_avg_price` AS `qty_avg_price`,`Sets`.`unit_quantity` AS `unit_quantity`,`Sets`.`total_quantity` AS `total_quantity`,`Sets`.`thumbnail_url` AS `thumbnail_url`,`Sets`.`image_url` AS `image_url`,`Sets`.`created` AS `created`,`c`.`category_name` AS `category_name`,group_concat(`rs`.`id` separator '|') AS `rs_ids`,group_concat(`rs`.`collection_id` separator '|') AS `rs_collection_ids`,group_concat(`rs`.`comments` separator '|') AS `rs_comments`,group_concat(`rs`.`instructions` separator '|') AS `rs_instructions`,group_concat(`rs`.`condition` separator '|') AS `rs_conditions`,group_concat(`st`.`name` separator '|') AS `rs_status_names`,group_concat(`st`.`description` separator '|') AS `rs_status_descriptions`,group_concat(`rs`.`created` separator '|') AS `rs_created` from (((`Sets` left join `Recognisedsets` `rs` on((convert(`Sets`.`no` using utf8mb4) = `rs`.`setNo`))) left join `Categories` `c` on((`c`.`category_id` = `Sets`.`category_id`))) left join `Status` `st` on(((`rs`.`status` = `st`.`id`) and (`st`.`type` = 'set')))) group by `Sets`.`id`,`Sets`.`no`,`Sets`.`name`,`Sets`.`year`,`Sets`.`weight_g`,`Sets`.`size`,`Sets`.`complete_part_count`,`Sets`.`complete_minifigs_count`,`Sets`.`min_price`,`Sets`.`max_price`,`Sets`.`avg_price`,`Sets`.`qty_avg_price`,`Sets`.`unit_quantity`,`Sets`.`total_quantity`,`Sets`.`thumbnail_url`,`Sets`.`image_url`,`Sets`.`created`,`c`.`category_name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `suggested_sets`
--

/*!50001 DROP VIEW IF EXISTS `suggested_sets`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `suggested_sets` AS select `up`.`collection_id` AS `collection_id`,group_concat(`up`.`partNo` separator ',') AS `partNos`,group_concat(`up`.`color_id` separator ',') AS `color_ids`,`ss`.`setNo` AS `setNo`,count(0) AS `count` from (`unsetted_parts` `up` left join `SuperSets` `ss` on(((`ss`.`partNo` = `up`.`partNo`) and (`ss`.`color_id` = `up`.`color_id`)))) where (`ss`.`setNo` is not null) group by `up`.`collection_id`,`ss`.`setNo` order by count(0) desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `suggested_sets_detail_view`
--

/*!50001 DROP VIEW IF EXISTS `suggested_sets_detail_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `suggested_sets_detail_view` AS select `ss`.`collection_id` AS `collection_id`,`ss`.`partNos` AS `partNos`,`ss`.`color_ids` AS `color_ids`,`ss`.`setNo` AS `setNo`,`ss`.`count` AS `count`,`s`.`id` AS `s_id`,`s`.`no` AS `no`,`s`.`name` AS `name`,`s`.`category_id` AS `category_id`,`s`.`year` AS `year`,`s`.`weight_g` AS `weight_g`,`s`.`size` AS `size`,`s`.`complete_part_count` AS `complete_part_count`,`s`.`complete_minifigs_count` AS `complete_minifigs_count`,`s`.`min_price` AS `min_price`,`s`.`max_price` AS `max_price`,`s`.`avg_price` AS `avg_price`,`s`.`qty_avg_price` AS `qty_avg_price`,`s`.`unit_quantity` AS `unit_quantity`,`s`.`total_quantity` AS `total_quantity`,`s`.`thumbnail_url` AS `thumbnail_url`,`s`.`image_url` AS `image_url`,`s`.`created` AS `created`,`ep`.`parts_existing` AS `parts_existing`,round(((`ep`.`parts_existing` / `s`.`complete_part_count`) * 100),2) AS `complete_percentage` from ((`suggested_sets` `ss` left join `Sets` `s` on((replace(`ss`.`setNo`,'-1','') = `s`.`no`))) left join `recognisedparts_existingpartsperset_view` `ep` on(((`ep`.`setNo` = `s`.`no`) and (`ep`.`collection_id` = `ss`.`collection_id`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `unsetted_parts`
--

/*!50001 DROP VIEW IF EXISTS `unsetted_parts`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `unsetted_parts` AS select `recognisedparts_usage_with_supersets_view`.`run_collection_id` AS `collection_id`,`recognisedparts_usage_with_supersets_view`.`partNo` AS `partNo`,`recognisedparts_usage_with_supersets_view`.`color_id` AS `color_id`,`recognisedparts_usage_with_supersets_view`.`downloaded_sets` AS `downloaded_sets`,`recognisedparts_usage_with_supersets_view`.`part_in_sets_of_collection` AS `part_in_sets_of_collection`,`recognisedparts_usage_with_supersets_view`.`super_setnos` AS `super_setnos`,`recognisedparts_usage_with_supersets_view`.`super_set_count` AS `super_set_count` from `recognisedparts_usage_with_supersets_view` where (`recognisedparts_usage_with_supersets_view`.`part_in_sets_of_collection` = 0) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-17 13:10:05
