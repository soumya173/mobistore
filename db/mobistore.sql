CREATE TABLE `users` (
  `userid` int PRIMARY KEY AUTO_INCREMENT,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `mobile` bigint,
  `type` varchar(255) NOT NULL,
  `created` timestamp,
  `modified` timestamp DEFAULT (now())
);

CREATE TABLE `products` (
  `productid` int PRIMARY KEY AUTO_INCREMENT,
  `offerid` int,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `price` int NOT NULL,
  `description` text,
  `instock` boolean NOT NULL,
  `created` timestamp,
  `modified` timestamp DEFAULT (now()),
  `addedby` int
);

CREATE TABLE `offers` (
  `offerid` int PRIMARY KEY AUTO_INCREMENT,
  `productid` int,
  `addedby` int,
  `discount` int,
  `description` text NOT NULL,
  `from` timestamp NOT NULL,
  `to` timestamp NOT NULL
);

ALTER TABLE `products` ADD FOREIGN KEY (`addedby`) REFERENCES `users` (`userid`);

ALTER TABLE `offers` ADD FOREIGN KEY (`productid`) REFERENCES `products` (`productid`);

ALTER TABLE `offers` ADD FOREIGN KEY (`addedby`) REFERENCES `users` (`userid`);
