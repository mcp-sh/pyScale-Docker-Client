CREATE TABLE `scales` (
  `batch` bigint unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `timestamp` varchar(255) NOT NULL,
  `scale_id` tinyint NOT NULL,
  `gross_kg` float NOT NULL,
  `gross_lb` float NOT NULL,
  `net_kg` float NOT NULL,
  `net_lb` float NOT NULL,
  `tare_kg` float NOT NULL,
  `tare_lb` float NOT NULL,
  `TS` timestamp NOT NULL
);