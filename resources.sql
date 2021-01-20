-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.7.31-log - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for resources
CREATE DATABASE IF NOT EXISTS `resources` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `resources`;

-- Dumping structure for table resources.accounts
CREATE TABLE IF NOT EXISTS `accounts` (
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `PASSWORD` varchar(255) NOT NULL,
  `accountType` enum('renter','owner') NOT NULL,
  PRIMARY KEY (`username`,`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.facilities
CREATE TABLE IF NOT EXISTS `facilities` (
  `unitID` varchar(16) NOT NULL,
  `facility` varchar(255) NOT NULL,
  KEY `unitID` (`unitID`),
  CONSTRAINT `facilities_ibfk_1` FOREIGN KEY (`unitID`) REFERENCES `units` (`unitID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.feedbacks
CREATE TABLE IF NOT EXISTS `feedbacks` (
  `username` varchar(255) NOT NULL,
  `RBID` varchar(16) NOT NULL,
  `feedbackNo` int(11) NOT NULL AUTO_INCREMENT,
  `feedback` varchar(255) NOT NULL,
  `starRating` int(11) NOT NULL,
  `feedbackDate` date NOT NULL,
  PRIMARY KEY (`feedbackNo`),
  KEY `RBID` (`RBID`),
  KEY `username` (`username`),
  CONSTRAINT `feedbacks_ibfk_1` FOREIGN KEY (`RBID`) REFERENCES `rentalbusiness` (`RBID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `feedbacks_ibfk_2` FOREIGN KEY (`username`) REFERENCES `accounts` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.images
CREATE TABLE IF NOT EXISTS `images` (
  `imageID` varchar(16) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `datum` longblob NOT NULL,
  PRIMARY KEY (`imageID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.locations
CREATE TABLE IF NOT EXISTS `locations` (
  `unitID` varchar(16) NOT NULL,
  `locationID` varchar(16) NOT NULL,
  `latitude` decimal(10,8) NOT NULL,
  `longitude` decimal(11,8) NOT NULL,
  `street` varchar(255) NOT NULL,
  `barangay` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `zipcode` varchar(4) NOT NULL,
  PRIMARY KEY (`locationID`),
  KEY `unitID` (`unitID`),
  CONSTRAINT `locations_ibfk_1` FOREIGN KEY (`unitID`) REFERENCES `units` (`unitID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.payments
CREATE TABLE IF NOT EXISTS `payments` (
  `username` varchar(255) NOT NULL,
  `RBID` varchar(16) NOT NULL,
  `paymentNo` int(11) NOT NULL AUTO_INCREMENT,
  `amount` int(11) NOT NULL,
  `paymentDate` date NOT NULL,
  `unitRented` varchar(16) NOT NULL,
  PRIMARY KEY (`paymentNo`),
  KEY `RBID` (`RBID`),
  KEY `username` (`username`),
  KEY `unitRented` (`unitRented`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`RBID`) REFERENCES `rentalbusiness` (`RBID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`username`) REFERENCES `accounts` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `payments_ibfk_3` FOREIGN KEY (`unitRented`) REFERENCES `units` (`unitID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;


-- Data exporting was unselected.

-- Dumping structure for table resources.profilephonenumber
CREATE TABLE IF NOT EXISTS `profilephonenumber` (
  `profileID` varchar(16) NOT NULL,
  `phoneNumber` varchar(20) NOT NULL,
  KEY `profileID` (`profileID`),
  CONSTRAINT `profilephonenumber_ibfk_1` FOREIGN KEY (`profileID`) REFERENCES `profiles` (`profileID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table resources.profilepictures
CREATE TABLE IF NOT EXISTS `profilepictures` (
  `profileID` varchar(255) NOT NULL,
  `imageID` varchar(255) NOT NULL,
  KEY `profileID` (`profileID`),
  KEY `imageID` (`imageID`),
  CONSTRAINT `profilepictures_ibfk_1` FOREIGN KEY (`profileID`) REFERENCES `profiles` (`profileID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `profilepictures_ibfk_2` FOREIGN KEY (`imageID`) REFERENCES `images` (`imageID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.profiles
CREATE TABLE IF NOT EXISTS `profiles` (
  `username` varchar(255) NOT NULL,
  `profileID` varchar(16) NOT NULL,
  `firstName` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `birthdate` date NOT NULL,
  `sex` enum('Male','Female') DEFAULT NULL,
  PRIMARY KEY (`profileID`),
  KEY `username` (`username`),
  CONSTRAINT `profiles_ibfk_1` FOREIGN KEY (`username`) REFERENCES `accounts` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.protocols
CREATE TABLE IF NOT EXISTS `protocols` (
  `RBID` varchar(16) NOT NULL,
  `protocol` varchar(255) NOT NULL,
  KEY `RBID` (`RBID`),
  CONSTRAINT `protocols_ibfk_1` FOREIGN KEY (`RBID`) REFERENCES `rentalbusiness` (`RBID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.rentalbusiness
CREATE TABLE IF NOT EXISTS `rentalbusiness` (
  `ownersUserName` varchar(255) NOT NULL,
  `rbName` varchar(255) NOT NULL,
  `RBID` varchar(16) NOT NULL,
  `description` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`RBID`),
  KEY `ownersUserName` (`ownersUserName`),
  CONSTRAINT `rentalbusiness_ibfk_1` FOREIGN KEY (`ownersUserName`) REFERENCES `accounts` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.rentalbusinessphonenumber
CREATE TABLE IF NOT EXISTS `rentalbusinessphonenumber` (
  `RBID` varchar(16) NOT NULL,
  `phoneNumber` varchar(255) NOT NULL,
  KEY `RBID` (`RBID`),
  CONSTRAINT `rentalbusinessphonenumber_ibfk_1` FOREIGN KEY (`RBID`) REFERENCES `rentalbusiness` (`RBID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.renters
CREATE TABLE IF NOT EXISTS `renters` (
  `username` varchar(255) NOT NULL,
  `unitID` varchar(16) NOT NULL,
  `checkinDate` date NOT NULL,
  `checkoutDate` date DEFAULT NULL,
  KEY `username` (`username`),
  CONSTRAINT `renters_ibfk_1` FOREIGN KEY (`username`) REFERENCES `accounts` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table resources.reservation
CREATE TABLE IF NOT EXISTS `reservation` (
  `username` varchar(255) NOT NULL,
  `unitID` varchar(16) NOT NULL,
  `reservationNo` int(11) NOT NULL AUTO_INCREMENT,
  `reservationDate` date NOT NULL,
  PRIMARY KEY (`reservationNo`),
  KEY `username` (`username`),
  KEY `unitID` (`unitID`),
  CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`username`) REFERENCES `accounts` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reservation_ibfk_2` FOREIGN KEY (`unitID`) REFERENCES `units` (`unitID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table resources.services
CREATE TABLE IF NOT EXISTS `services` (
  `RBID` varchar(16) NOT NULL,
  `service` varchar(255) NOT NULL,
  KEY `RBID` (`RBID`),
  CONSTRAINT `services_ibfk_1` FOREIGN KEY (`RBID`) REFERENCES `rentalbusiness` (`RBID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.unitimages
CREATE TABLE IF NOT EXISTS `unitimages` (
  `unitID` varchar(16) NOT NULL,
  `imageID` varchar(16) NOT NULL,
  KEY `unitID` (`unitID`),
  KEY `imageID` (`imageID`),
  CONSTRAINT `unitimages_ibfk_1` FOREIGN KEY (`unitID`) REFERENCES `units` (`unitID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `unitimages_ibfk_2` FOREIGN KEY (`imageID`) REFERENCES `images` (`imageID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table resources.units
CREATE TABLE IF NOT EXISTS `units` (
  `RBID` varchar(255) NOT NULL,
  `unitID` varchar(16) NOT NULL,
  `capacity` int(11) NOT NULL,
  `rate` varchar(255) NOT NULL,
  `unitType` varchar(255) NOT NULL,
  `genderAccommodation` enum('Female','Male','Unisex') NOT NULL,

  PRIMARY KEY (`unitID`),
  KEY `RBID` (`RBID`),
  CONSTRAINT `units_ibfk_1` FOREIGN KEY (`RBID`) REFERENCES `rentalbusiness` (`RBID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
