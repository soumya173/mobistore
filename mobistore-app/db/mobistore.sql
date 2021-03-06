CREATE TABLE `users` (
  `userid` int PRIMARY KEY AUTO_INCREMENT,
  `password` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `mobile` bigint DEFAULT null,
  `type` varchar(255) NOT NULL,
  `created` timestamp NOT NULL,
  `modified` timestamp DEFAULT now()
);

CREATE TABLE `products` (
  `productid` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `price` int NOT NULL,
  `description` text DEFAULT null,
  `instock` boolean NOT NULL,
  `created` timestamp,
  `modified` timestamp DEFAULT now(),
  `addedby` int,
  `labels` varchar(255) DEFAULT null
);

CREATE TABLE `images` (
  `imageid` int PRIMARY KEY AUTO_INCREMENT,
  `productid` int,
  `url` varchar(255) NOT NULL
);

CREATE TABLE `offers` (
  `offerid` int PRIMARY KEY AUTO_INCREMENT,
  `productid` int,
  `addedby` int,
  `discount` int DEFAULT 0,
  `description` text DEFAULT null,
  `from` timestamp NOT NULL,
  `to` timestamp NOT NULL
);

ALTER TABLE `products` ADD FOREIGN KEY (`addedby`) REFERENCES `users` (`userid`);

ALTER TABLE `images` ADD FOREIGN KEY (`productid`) REFERENCES `products` (`productid`);

ALTER TABLE `offers` ADD FOREIGN KEY (`productid`) REFERENCES `products` (`productid`);

ALTER TABLE `offers` ADD FOREIGN KEY (`addedby`) REFERENCES `users` (`userid`);

INSERT INTO `users` (`password`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified`) VALUES('admin', 'Soumyajit', 'Gorai', 'sgorai@gmail.com', '9635031710', 'admin', now(), now());
