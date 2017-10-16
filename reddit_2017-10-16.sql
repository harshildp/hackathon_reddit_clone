# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.19)
# Database: reddit
# Generation Time: 2017-10-16 17:38:36 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table comment_votes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `comment_votes`;

CREATE TABLE `comment_votes` (
  `user_id` int(11) NOT NULL,
  `comment_id` int(11) NOT NULL,
  `type` smallint(6) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`comment_id`),
  KEY `fk_users_has_comments_comments1_idx` (`comment_id`),
  KEY `fk_users_has_comments_users1_idx` (`user_id`),
  CONSTRAINT `fk_users_has_comments_comments1` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_comments_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `comment_votes` WRITE;
/*!40000 ALTER TABLE `comment_votes` DISABLE KEYS */;

INSERT INTO `comment_votes` (`user_id`, `comment_id`, `type`, `created_at`, `updated_at`)
VALUES
	(4,46,1,'2017-10-16 11:59:38','2017-10-16 11:59:38'),
	(5,27,1,'2017-10-16 11:50:54','2017-10-16 11:50:54'),
	(5,28,1,'2017-10-16 11:50:57','2017-10-16 11:50:57'),
	(5,30,1,'2017-10-16 11:53:38','2017-10-16 11:53:38'),
	(5,34,1,'2017-10-16 11:51:08','2017-10-16 11:51:08'),
	(5,35,1,'2017-10-16 11:50:59','2017-10-16 11:50:59'),
	(5,38,1,'2017-10-16 11:48:28','2017-10-16 11:48:28'),
	(5,40,0,'2017-10-16 11:48:26','2017-10-16 11:48:26'),
	(5,41,0,'2017-10-16 11:48:48','2017-10-16 11:48:48'),
	(5,42,0,'2017-10-16 11:50:52','2017-10-16 11:50:52'),
	(5,43,0,'2017-10-16 11:51:05','2017-10-16 11:51:05'),
	(5,44,0,'2017-10-16 11:52:44','2017-10-16 11:52:44'),
	(5,45,0,'2017-10-16 11:53:55','2017-10-16 11:53:55'),
	(6,26,1,'2017-10-16 11:37:54','2017-10-16 11:37:54'),
	(6,27,1,'2017-10-16 11:36:27','2017-10-16 11:36:27'),
	(6,28,0,'2017-10-16 11:36:32','2017-10-16 11:36:32'),
	(6,29,0,'2017-10-16 11:36:48','2017-10-16 11:36:48'),
	(6,30,0,'2017-10-16 11:37:05','2017-10-16 11:37:05'),
	(6,31,0,'2017-10-16 11:38:02','2017-10-16 11:38:02'),
	(6,32,0,'2017-10-16 11:38:10','2017-10-16 11:38:10'),
	(6,33,0,'2017-10-16 11:39:50','2017-10-16 11:39:50'),
	(7,26,0,'2017-10-16 11:34:31','2017-10-16 11:34:31'),
	(7,27,0,'2017-10-16 11:35:03','2017-10-16 11:35:03'),
	(8,26,1,'2017-10-16 11:43:21','2017-10-16 11:43:21'),
	(8,27,1,'2017-10-16 11:42:41','2017-10-16 11:42:41'),
	(8,28,1,'2017-10-16 11:42:50','2017-10-16 11:42:50'),
	(8,29,1,'2017-10-16 11:45:45','2017-10-16 11:45:45'),
	(8,31,1,'2017-10-16 11:43:24','2017-10-16 11:43:24'),
	(8,32,1,'2017-10-16 11:43:22','2017-10-16 11:43:22'),
	(8,34,0,'2017-10-16 11:42:47','2017-10-16 11:42:47'),
	(8,35,0,'2017-10-16 11:42:56','2017-10-16 11:42:56'),
	(8,36,0,'2017-10-16 11:43:29','2017-10-16 11:43:29'),
	(8,37,0,'2017-10-16 11:43:42','2017-10-16 11:43:42'),
	(8,38,0,'2017-10-16 11:45:26','2017-10-16 11:45:26'),
	(8,39,0,'2017-10-16 11:45:48','2017-10-16 11:45:48');

/*!40000 ALTER TABLE `comment_votes` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table comments
# ------------------------------------------------------------

DROP TABLE IF EXISTS `comments`;

CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` text,
  `user_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `comment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comments_users1_idx` (`user_id`),
  KEY `fk_comments_posts1_idx` (`post_id`),
  CONSTRAINT `fk_comments_posts1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_comments_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;

INSERT INTO `comments` (`id`, `text`, `user_id`, `post_id`, `created_at`, `updated_at`, `comment_id`)
VALUES
	(26,'that\'s a dope meme',7,7,'2017-10-16 11:34:31','2017-10-16 11:34:31',NULL),
	(27,'pretty dope gif',7,8,'2017-10-16 11:35:03','2017-10-16 11:35:03',NULL),
	(28,'I agree',6,8,'2017-10-16 11:36:32','2017-10-16 11:36:32',27),
	(29,'no shaq shimmy but its dece',6,9,'2017-10-16 11:36:48','2017-10-16 11:36:48',NULL),
	(30,'yeah dude so pumped',6,6,'2017-10-16 11:37:05','2017-10-16 11:37:05',NULL),
	(31,'I\'m amused AF',6,7,'2017-10-16 11:38:02','2017-10-16 11:38:02',NULL),
	(32,'word',6,7,'2017-10-16 11:38:10','2017-10-16 11:38:10',26),
	(33,'fuck that guy',6,5,'2017-10-16 11:39:50','2017-10-16 11:39:50',NULL),
	(34,'this GIF rocks',8,8,'2017-10-16 11:42:47','2017-10-16 11:42:47',NULL),
	(35,'you have good taste',8,8,'2017-10-16 11:42:56','2017-10-16 11:42:56',28),
	(36,'me too',8,7,'2017-10-16 11:43:29','2017-10-16 11:43:29',31),
	(37,'this meme for lyfe',8,7,'2017-10-16 11:43:42','2017-10-16 11:43:42',32),
	(38,'You\'re an asshole',8,10,'2017-10-16 11:45:26','2017-10-16 11:45:26',NULL),
	(39,'RT',8,9,'2017-10-16 11:45:48','2017-10-16 11:45:48',29),
	(40,'seriously what the fuck?',5,10,'2017-10-16 11:48:26','2017-10-16 11:48:26',NULL),
	(41,'Season 7 just ended jeeeeez',5,11,'2017-10-16 11:48:48','2017-10-16 11:48:48',NULL),
	(42,'best GIF on the internet ',5,8,'2017-10-16 11:50:52','2017-10-16 11:50:52',NULL),
	(43,'You all do!',5,8,'2017-10-16 11:51:05','2017-10-16 11:51:05',35),
	(44,'I got a few',5,12,'2017-10-16 11:52:44','2017-10-16 11:52:44',NULL),
	(45,'don\'t be a dick',5,5,'2017-10-16 11:53:55','2017-10-16 11:53:55',NULL),
	(46,'hello',4,17,'2017-10-16 11:59:38','2017-10-16 11:59:38',NULL);

/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table messages
# ------------------------------------------------------------

DROP TABLE IF EXISTS `messages`;

CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `recipient_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_messages_users1_idx` (`recipient_id`),
  KEY `fk_messages_users2_idx` (`author_id`),
  CONSTRAINT `fk_messages_users1` FOREIGN KEY (`recipient_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_users2` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;

INSERT INTO `messages` (`id`, `text`, `created_at`, `updated_at`, `recipient_id`, `author_id`)
VALUES
	(3,'How\'s it hanging?','2017-10-16 11:27:34','2017-10-16 11:27:34',7,1),
	(4,'Isn\'t this dope?','2017-10-16 11:27:41','2017-10-16 11:27:41',5,1),
	(5,'Pretty good mayne','2017-10-16 11:29:53','2017-10-16 11:29:53',1,7),
	(6,'How\'s that side of the desk?','2017-10-16 11:30:09','2017-10-16 11:30:09',6,7),
	(7,'hello','2017-10-16 11:30:17','2017-10-16 11:30:17',5,7),
	(8,'it\'s pretty good','2017-10-16 11:37:21','2017-10-16 11:37:21',7,6),
	(9,'ayyyyyy','2017-10-16 11:37:36','2017-10-16 11:37:36',5,6),
	(10,'it\'s solid','2017-10-16 11:53:15','2017-10-16 11:53:15',1,5),
	(11,'ayyyyyyyyy','2017-10-16 11:53:23','2017-10-16 11:53:23',6,5),
	(12,'hello\r\n','2017-10-16 11:56:43','2017-10-16 11:56:43',1,4),
	(13,'whatsup teach\r\n','2017-10-16 12:01:26','2017-10-16 12:01:26',3,5);

/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table post_votes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `post_votes`;

CREATE TABLE `post_votes` (
  `post_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `type` smallint(6) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`post_id`,`user_id`),
  KEY `fk_posts_has_users_users1_idx` (`user_id`),
  KEY `fk_posts_has_users_posts1_idx` (`post_id`),
  CONSTRAINT `fk_posts_has_users_posts1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_posts_has_users_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `post_votes` WRITE;
/*!40000 ALTER TABLE `post_votes` DISABLE KEYS */;

INSERT INTO `post_votes` (`post_id`, `user_id`, `type`, `created_at`, `updated_at`)
VALUES
	(5,1,0,'2017-10-16 11:01:24','2017-10-16 11:01:24'),
	(5,5,-1,'2017-10-16 11:53:50','2017-10-16 11:53:50'),
	(5,6,-1,'2017-10-16 11:39:52','2017-10-16 11:39:52'),
	(6,1,0,'2017-10-16 11:01:46','2017-10-16 11:01:46'),
	(6,5,1,'2017-10-16 11:53:36','2017-10-16 11:53:36'),
	(6,6,1,'2017-10-16 11:37:07','2017-10-16 11:37:07'),
	(7,1,1,'2017-10-16 11:03:00','2017-10-16 11:03:00'),
	(7,6,1,'2017-10-16 11:37:52','2017-10-16 11:37:52'),
	(7,7,1,'2017-10-16 11:28:35','2017-10-16 11:28:35'),
	(7,8,1,'2017-10-16 11:43:15','2017-10-16 11:43:15'),
	(8,1,1,'2017-10-16 11:03:47','2017-10-16 11:03:47'),
	(8,5,1,'2017-10-16 11:50:45','2017-10-16 11:50:45'),
	(8,6,1,'2017-10-16 11:36:25','2017-10-16 11:36:25'),
	(8,7,1,'2017-10-16 11:28:27','2017-10-16 11:28:27'),
	(8,8,1,'2017-10-16 11:40:08','2017-10-16 11:40:08'),
	(9,6,1,'2017-10-16 11:36:51','2017-10-16 11:36:51'),
	(9,7,1,'2017-10-16 11:36:02','2017-10-16 11:36:02'),
	(9,8,1,'2017-10-16 11:45:43','2017-10-16 11:45:43'),
	(10,5,-1,'2017-10-16 11:48:18','2017-10-16 11:48:18'),
	(10,6,0,'2017-10-16 11:39:37','2017-10-16 11:39:37'),
	(10,8,-1,'2017-10-16 11:45:20','2017-10-16 11:45:20'),
	(11,5,1,'2017-10-16 11:48:39','2017-10-16 11:48:39'),
	(11,8,0,'2017-10-16 11:44:26','2017-10-16 11:44:26'),
	(12,5,1,'2017-10-16 11:52:17','2017-10-16 11:52:17'),
	(12,8,0,'2017-10-16 11:46:14','2017-10-16 11:46:14'),
	(13,5,1,'2017-10-16 11:52:53','2017-10-16 11:52:53'),
	(13,8,0,'2017-10-16 11:47:58','2017-10-16 11:47:58'),
	(14,5,0,'2017-10-16 11:50:36','2017-10-16 11:50:36'),
	(15,5,0,'2017-10-16 11:52:06','2017-10-16 11:52:06'),
	(16,5,0,'2017-10-16 11:54:39','2017-10-16 11:54:39'),
	(17,4,1,'2017-10-16 11:58:59','2017-10-16 11:58:59');

/*!40000 ALTER TABLE `post_votes` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table posts
# ------------------------------------------------------------

DROP TABLE IF EXISTS `posts`;

CREATE TABLE `posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` text,
  `user_id` int(11) NOT NULL,
  `subreddit_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `title` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_posts_users1_idx` (`user_id`),
  KEY `fk_posts_subreddits1_idx` (`subreddit_id`),
  CONSTRAINT `fk_posts_subreddits1` FOREIGN KEY (`subreddit_id`) REFERENCES `subreddits` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_posts_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;

INSERT INTO `posts` (`id`, `text`, `user_id`, `subreddit_id`, `created_at`, `updated_at`, `title`)
VALUES
	(5,'Rough for the Packers!',1,1,'2017-10-16 11:01:24','2017-10-16 11:01:24','How about that Aaron Rodgers injury?'),
	(6,'Finally we\'re done with these garbage pre-season games!',1,1,'2017-10-16 11:01:46','2017-10-16 11:01:46','NBA season hype!'),
	(7,'http://i.imgur.com/LPtmwpd.gif',1,3,'2017-10-16 11:03:00','2017-10-16 11:03:00','Click here to be amused!'),
	(8,'http://i.imgur.com/LPtmwpd.gif',1,4,'2017-10-16 11:03:47','2017-10-16 11:03:47','Shaq Shimmy Baby!'),
	(9,'https://i.ytimg.com/vi/tYBk4kLHPkk/maxresdefault.jpg',7,4,'2017-10-16 11:36:02','2017-10-16 11:36:02','This other meme is pretty legit'),
	(10,'Are they even Americans?',6,6,'2017-10-16 11:39:37','2017-10-16 11:39:37','Fuck Puerto Rico'),
	(11,'Seriously WTF guys',8,7,'2017-10-16 11:44:26','2017-10-16 11:44:26','Is Season 8 here yet?'),
	(12,'http://i0.kym-cdn.com/photos/images/newsfeed/001/144/795/b08.jpg',8,4,'2017-10-16 11:46:14','2017-10-16 11:46:14','I got meme withdrawal'),
	(13,'https://i.pinimg.com/originals/8d/3e/fa/8d3efa994c2a025c285a2cc7b06fc2aa.gif',8,4,'2017-10-16 11:47:58','2017-10-16 11:47:58','Meme\'s make me feel like'),
	(14,'Got that Lovecraft Zenyatta yet?',5,8,'2017-10-16 11:50:36','2017-10-16 11:50:36','How bout that Overwatch Halloween event?'),
	(15,'https://i0.wp.com/blogs.techsmith.com/wp-content/uploads/2016/09/what-is-a-meme.jpg?resize=640%2C480',5,4,'2017-10-16 11:52:06','2017-10-16 11:52:06','Meme-ception'),
	(16,'https://media.tenor.com/images/4082f8a8dd612a9728a49c28724d9a4a/tenor.gif',5,1,'2017-10-16 11:54:39','2017-10-16 11:54:39','Check out this dope shimmy'),
	(17,'balahbalaha',4,9,'2017-10-16 11:58:59','2017-10-16 11:58:59','Yummy');

/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table subreddits
# ------------------------------------------------------------

DROP TABLE IF EXISTS `subreddits`;

CREATE TABLE `subreddits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

LOCK TABLES `subreddits` WRITE;
/*!40000 ALTER TABLE `subreddits` DISABLE KEYS */;

INSERT INTO `subreddits` (`id`, `url`, `created_at`, `updated_at`, `description`)
VALUES
	(1,'r/sports','2017-10-15 17:13:02','2017-10-15 17:13:02','A place to talk about sports'),
	(2,'r/politics','2017-10-15 17:16:14','2017-10-15 17:16:14','a place to talk about politics'),
	(3,'r/shaq_shimmy','2017-10-16 09:43:08','2017-10-16 09:43:08','Only for posting the Shaq shimmy GIF'),
	(4,'r/memes_for_life','2017-10-16 11:03:30','2017-10-16 11:03:30','This community is for people who live and breathe memes. '),
	(5,'r/world_politics','2017-10-16 11:33:10','2017-10-16 11:33:10','I\'m not retyping all that. '),
	(6,'r/The_Donald','2017-10-16 11:39:12','2017-10-16 11:39:12','A community for fucking assholes.'),
	(7,'r/TV','2017-10-16 11:44:02','2017-10-16 11:44:02','Just a place to ignore reality.'),
	(8,'r/video_games','2017-10-16 11:49:34','2017-10-16 11:49:34','Because real life sucks'),
	(9,'r/Food','2017-10-16 11:58:39','2017-10-16 11:58:39','Hangry....');

/*!40000 ALTER TABLE `subreddits` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table subscriptions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `subscriptions`;

CREATE TABLE `subscriptions` (
  `user_id` int(11) NOT NULL,
  `subreddit_id` int(11) NOT NULL,
  `moderator` tinyint(4) DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`subreddit_id`),
  KEY `fk_users_has_subreddits_subreddits1_idx` (`subreddit_id`),
  KEY `fk_users_has_subreddits_users_idx` (`user_id`),
  CONSTRAINT `fk_users_has_subreddits_subreddits1` FOREIGN KEY (`subreddit_id`) REFERENCES `subreddits` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_subreddits_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `subscriptions` WRITE;
/*!40000 ALTER TABLE `subscriptions` DISABLE KEYS */;

INSERT INTO `subscriptions` (`user_id`, `subreddit_id`, `moderator`, `created_at`, `updated_at`)
VALUES
	(1,1,1,'2017-10-15 17:16:45','2017-10-15 17:16:48'),
	(1,3,1,'2017-10-16 09:43:08','2017-10-16 09:43:08'),
	(1,4,1,'2017-10-16 11:03:30','2017-10-16 11:03:30'),
	(4,3,0,'2017-10-16 11:57:13','2017-10-16 11:57:13'),
	(4,9,1,'2017-10-16 11:58:39','2017-10-16 11:58:39'),
	(5,1,0,'2017-10-16 11:53:33','2017-10-16 11:53:33'),
	(5,4,0,'2017-10-16 11:51:12','2017-10-16 11:51:12'),
	(5,7,0,'2017-10-16 11:48:50','2017-10-16 11:48:50'),
	(5,8,1,'2017-10-16 11:49:34','2017-10-16 11:49:34'),
	(6,1,0,'2017-10-16 11:37:09','2017-10-16 11:37:09'),
	(6,3,0,'2017-10-16 11:37:48','2017-10-16 11:37:48'),
	(6,4,0,'2017-10-16 11:36:37','2017-10-16 11:36:37'),
	(6,6,1,'2017-10-16 11:39:12','2017-10-16 11:39:12'),
	(7,3,0,'2017-10-16 11:28:38','2017-10-16 11:28:38'),
	(7,4,0,'2017-10-16 11:29:24','2017-10-16 11:29:24'),
	(7,5,1,'2017-10-16 11:33:10','2017-10-16 11:33:10'),
	(8,3,0,'2017-10-16 11:43:11','2017-10-16 11:43:11'),
	(8,4,0,'2017-10-16 11:40:11','2017-10-16 11:40:11'),
	(8,7,1,'2017-10-16 11:44:02','2017-10-16 11:44:02');

/*!40000 ALTER TABLE `subscriptions` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `salt` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`id`, `username`, `email`, `salt`, `password`, `created_at`, `updated_at`)
VALUES
	(1,'sjweil','stephen.weil@fake.com','fb6bbcfe02984810d02882bc38c06f','96d9715f0ccad52ed95226b8e30eb184','2017-10-15 17:15:56','2017-10-15 17:15:56'),
	(2,'newuser','new@email.com','b93845251317c68294a8629aa59acc','b025bacb789a319a2d5deaa8e8357309','2017-10-16 09:42:01','2017-10-16 09:42:01'),
	(3,'elibyers','elibyers@codingdojo.com','ded7fd5efce80fa7f641f1ad969aa1','4c8a2d4f77ac1ed0b4447a17a82d98bc','2017-10-16 10:57:15','2017-10-16 10:57:15'),
	(4,'aadilmoosa','aadilmoosa@fake.com','2aa1609343ba0bf6ff8f3a708677d1','17ee8682022abf50016a4fa882739e8d','2017-10-16 10:57:44','2017-10-16 10:57:44'),
	(5,'harshilp','harshilp@fake.com','e817d64237babba01321e4b43fbf2a','5c516a7d476bce805a695deca1401777','2017-10-16 10:58:40','2017-10-16 10:58:40'),
	(6,'cooper','cooper@fake.com','ce4e921a1ddf0fd0ed8439a7bfb674','a2afb9a9c825980df311ddb46993b8d8','2017-10-16 10:58:53','2017-10-16 10:58:53'),
	(7,'shiv','shiv@fake.com','1173c6fbb06865c976ad85a094fdec','0014be17f94f4ecbcb6ba09d2f7a21d4','2017-10-16 10:59:22','2017-10-16 10:59:22'),
	(8,'remy','remy@fake.com','86b6155b985eb22ac1c35a2b77a9b3','9e7e730f37a84408df7292474dbfd73e','2017-10-16 10:59:52','2017-10-16 10:59:52');

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
