DROP TABLE IF EXISTS `scales`;
CREATE TABLE `scales` (
  `batch_id` bigint unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `scale_id` tinyint(4) NOT NULL,
  `gross_kg` float NOT NULL,
  `gross_lb` float NOT NULL,
  `net_kg` float NOT NULL,
  `net_lb` float NOT NULL,
  `tare_kg` float NOT NULL,
  `tare_lb` float NOT NULL,
  `TS` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`batch_id`)
);