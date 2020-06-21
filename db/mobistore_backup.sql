CREATE TABLE `users` (
  `userid` int PRIMARY KEY AUTO_INCREMENT,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `mobile` bigint DEFAULT null,
  `type` varchar(255) NOT NULL,
  `created` timestamp NOT NULL,
  `modified` timestamp DEFAULT (now())
  CONSTRAINT email_unique UNIQUE (email)
);

CREATE TABLE `products` (
  `productid` int PRIMARY KEY AUTO_INCREMENT,
  `offerid` int DEFAULT null,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `price` int NOT NULL,
  `description` text DEFAULT null,
  `instock` boolean NOT NULL,
  `created` timestamp,
  `modified` timestamp DEFAULT (now()),
  `addedby` int
);

CREATE TABLE `offers` (
  `offerid` int PRIMARY KEY AUTO_INCREMENT,
  `productid` int,
  `addedby` int,
  `discount` int DEFAULT 0,
  `description` text NOT NULL,
  `from` timestamp NOT NULL,
  `to` timestamp NOT NULL
);

ALTER TABLE `products` ADD FOREIGN KEY (`addedby`) REFERENCES `users` (`userid`);

ALTER TABLE `offers` ADD FOREIGN KEY (`productid`) REFERENCES `products` (`productid`);

ALTER TABLE `offers` ADD FOREIGN KEY (`addedby`) REFERENCES `users` (`userid`);
