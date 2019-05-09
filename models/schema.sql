CREATE TABLE `searchhash` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info_hash` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `data_hash` varchar(50) DEFAULT NULL,
  `name` varchar(500) DEFAULT NULL,
  `extension` varchar(100) DEFAULT NULL,
  `classified` tinyint(1) DEFAULT NULL,
  `source_ip` varchar(50) DEFAULT NULL,
  `tagged` tinyint(1) DEFAULT NULL,
  `length` bigint(64) DEFAULT NULL,
  `files` varchar(500) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `last_seen` datetime(6) DEFAULT NULL,
  `requests` int(11) DEFAULT NULL,
  `filescount` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FULLTEXT KEY `FIDX_NAME` (`name`) /*!50100 WITH PARSER `ngram` */
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE `searchhash` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info_hash` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `data_hash` varchar(50) DEFAULT NULL,
  `name` varchar(500) DEFAULT NULL,
  `extension` varchar(100) DEFAULT NULL,
  `classified` tinyint(1) DEFAULT NULL,
  `source_ip` varchar(50) DEFAULT NULL,
  `tagged` tinyint(1) DEFAULT NULL,
  `length` bigint(64) DEFAULT NULL,
  `files` varchar(500) DEFAULT NULL,
  `create_time` TIMESTAMP  NULL,
  `last_seen` TIMESTAMP NULL,
  `requests` int(11) DEFAULT NULL,
  `filescount` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE `torfiles` (
  `TFID` int(11) NOT NULL AUTO_INCREMENT,
  `INFOHASH` varchar(50) DEFAULT NULL,
  `FILENAME` varchar(260) DEFAULT NULL,
  `FILESIZE` bigint(64) DEFAULT NULL,
  `EXTENSION` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`TFID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
;

alter table searchhash add fulltext index FIDX_NAME(name) with parser ngram;

drop index FIDX_NAME on searchhash;

show variables like "%character%";

alter table torfiles modify column FILESIZE bigint(64);

-- alter table for searchhash

  -- s1
  select count(*) from searchhash; 
  create table searchhash_bak as select * from searchhash where 1=0;
  
  alter table searchhash_bak ADD PRIMARY KEY(id);
  select count(*) from searchhash_bak; 

  insert into searchhash_bak(id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length,  create_time, last_seen,  requests, filescount) 
  select id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length, create_time, last_seen,  requests, filescount 
    from searchhash b limit 0,500000; 

  insert into searchhash_bak(id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length,  create_time, last_seen,  requests, filescount) 
  select id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length, create_time, last_seen,  requests, filescount 
    from searchhash b limit 500000,500000;

  insert into searchhash_bak(id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length,  create_time, last_seen,  requests, filescount) 
  select id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length, create_time, last_seen,  requests, filescount 
    from searchhash b limit 1000000,500000;

  insert into searchhash_bak(id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length,  create_time, last_seen,  requests, filescount) 
  select id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length, create_time, last_seen,  requests, filescount 
    from searchhash b limit 1500000,500000;
  
  insert into searchhash_bak(id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length,  create_time, last_seen,  requests, filescount) 
  select id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length, create_time, last_seen,  requests, filescount 
    from searchhash b limit 2000000,500000;

  --s2
  TRUNCATE table searchhash;

  --s3
  alter table searchhash add column sensi BOOLEAN DEFAULT 0;

  --s4 loop insert
  insert into searchhash(id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length, 
    create_time, last_seen,  requests, filescount) 
  select id,  info_hash,  category,  data_hash,  name,
    extension,  classified, source_ip,  tagged,  length, 
    create_time, last_seen,  requests, filescount from searchhash_bak b limit 0,500000;

  --s5
  TRUNCATE table searchhash_bak;
  DROP table searchhash_bak; 