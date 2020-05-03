BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "article_tags" (
	"article_id"	INTEGER NOT NULL,
	"tag_id"	INTEGER NOT NULL,
	FOREIGN KEY("article_id") REFERENCES "articles"("id"),
	PRIMARY KEY("article_id","tag_id"),
	FOREIGN KEY("tag_id") REFERENCES "tags"("id")
);
CREATE TABLE IF NOT EXISTS "tags" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	"tmdb_id"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "articles" (
	"id"	INTEGER NOT NULL,
	"article_type_id"	INTEGER,
	"image"	VARCHAR(128),
	"title"	VARCHAR(128),
	"title_slug"	VARCHAR(64),
	"draft_title"	VARCHAR(64),
	"body_html"	TEXT,
	"body"	TEXT,
	"draft"	TEXT,
	"blurb"	VARCHAR(256),
	"youtube"	VARCHAR(64),
	"final_verdict"	VARCHAR(256),
	"rating"	INTEGER,
	"created"	DATETIME,
	"last_edit"	DATETIME,
	"publish_date"	DATETIME,
	"author_id"	INTEGER,
	"subject_id"	INTEGER,
	"request_to_publish"	BOOLEAN,
	"is_published"	BOOLEAN,
	"letter_rating"	VARCHAR(3),
	PRIMARY KEY("id"),
	FOREIGN KEY("article_type_id") REFERENCES "article_type"("id"),
	FOREIGN KEY("author_id") REFERENCES "users"("id"),
	CHECK(request_to_publish IN (0,1)),
	CHECK(is_published IN (0,1)),
	FOREIGN KEY("subject_id") REFERENCES "creative_works"("id")
);
CREATE TABLE IF NOT EXISTS "follows" (
	"follower_id"	INTEGER NOT NULL,
	"followed_id"	INTEGER NOT NULL,
	"timestamp"	DATETIME,
	FOREIGN KEY("follower_id") REFERENCES "users"("id"),
	PRIMARY KEY("follower_id","followed_id"),
	FOREIGN KEY("followed_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"email"	VARCHAR(128),
	"username"	VARCHAR(64),
	"first_name"	VARCHAR(64),
	"last_name"	VARCHAR(64),
	"about_me"	TEXT,
	"role_id"	INTEGER,
	"password_hash"	VARCHAR(128),
	"confirmed"	BOOLEAN,
	"member_since"	DATETIME,
	"last_seen"	DATETIME,
	"avatar_hash"	VARCHAR(32),
	PRIMARY KEY("id"),
	FOREIGN KEY("role_id") REFERENCES "roles"("id"),
	CHECK(confirmed IN (0,1))
);
CREATE TABLE IF NOT EXISTS "directs" (
	"directed_id"	INTEGER NOT NULL,
	"director_id"	INTEGER NOT NULL,
	PRIMARY KEY("directed_id","director_id"),
	FOREIGN KEY("directed_id") REFERENCES "creative_works"("id"),
	FOREIGN KEY("director_id") REFERENCES "people"("id")
);
CREATE TABLE IF NOT EXISTS "roles" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64) UNIQUE,
	"default"	BOOLEAN,
	"permissions"	INTEGER,
	PRIMARY KEY("id"),
	CHECK("default" IN (0,1))
);
CREATE TABLE IF NOT EXISTS "people" (
	"id"	INTEGER NOT NULL,
	"tmdb_id"	INTEGER,
	"name"	VARCHAR(64),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "creative_works" (
	"id"	INTEGER NOT NULL,
	"type"	VARCHAR(32),
	"name"	VARCHAR(128),
	"tmdb_id"	INTEGER,
	"image"	TEXT,
	"date_published"	DATETIME,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "article_type" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(32),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "alembic_version" (
	"version_num"	VARCHAR(32) NOT NULL,
	CONSTRAINT "alembic_version_pkc" PRIMARY KEY("version_num")
);
INSERT INTO "tags" VALUES (1,'Action & Adventure',NULL);
INSERT INTO "tags" VALUES (2,'Animation',NULL);
INSERT INTO "tags" VALUES (3,'Comedy',NULL);
INSERT INTO "tags" VALUES (4,'Crime',NULL);
INSERT INTO "tags" VALUES (5,'Documentary',NULL);
INSERT INTO "tags" VALUES (6,'Drama',NULL);
INSERT INTO "tags" VALUES (7,'Family',NULL);
INSERT INTO "tags" VALUES (8,'Kids',NULL);
INSERT INTO "tags" VALUES (9,'Mystery',NULL);
INSERT INTO "tags" VALUES (10,'News',NULL);
INSERT INTO "tags" VALUES (11,'Reality',NULL);
INSERT INTO "tags" VALUES (12,'Sci-Fi & Fantasy',NULL);
INSERT INTO "tags" VALUES (13,'Soap',NULL);
INSERT INTO "tags" VALUES (14,'Talk',NULL);
INSERT INTO "tags" VALUES (15,'War & Politics',NULL);
INSERT INTO "tags" VALUES (16,'Western',NULL);
INSERT INTO "tags" VALUES (17,'Action',NULL);
INSERT INTO "tags" VALUES (18,'Adventure',NULL);
INSERT INTO "tags" VALUES (19,'Fantasy',NULL);
INSERT INTO "tags" VALUES (20,'History',NULL);
INSERT INTO "tags" VALUES (21,'Horror',NULL);
INSERT INTO "tags" VALUES (22,'Music',NULL);
INSERT INTO "tags" VALUES (23,'Romance',NULL);
INSERT INTO "tags" VALUES (24,'Science Fiction',NULL);
INSERT INTO "tags" VALUES (25,'TV Movie',NULL);
INSERT INTO "tags" VALUES (26,'Thriller',NULL);
INSERT INTO "tags" VALUES (27,'War',NULL);
INSERT INTO "users" VALUES (1,'evansamanda@bailey-hill.org','egreer','Heidi Thomas',NULL,'Order difference above produce stand ever. Capital always cause pressure statement option month bill.',1,'pbkdf2:sha256:150000$A7hveLNX$045d1fa4e37cde2ceda94f49b4e15d0877ea455feb1931791c687b6188beb2c3',1,'2020-03-02 00:00:00.000000','2020-03-04 00:45:05.787549','55654f344a7d7d657b3e71d93dbe49fa');
INSERT INTO "users" VALUES (2,'brianjohnston@jimenez-bowen.com','ifoster','Laura Mercer',NULL,'Yourself international third with paper produce class determine. Hair start set official. Either process likely yeah war something.
Type upon else for bank. Ever alone still.',1,'pbkdf2:sha256:150000$PnaELDLi$9741ec10cef62cb7825a0d6879490455ecc5e9cb6e9543671990c333f028e373',1,'2020-02-27 00:00:00.000000','2020-03-04 00:45:06.448332','6733e5c566804af94d131db9a1f4f663');
INSERT INTO "users" VALUES (3,'qlopez@ramos.com','bhogan','Manuel Anderson',NULL,'Choice wear list available. Leave write away camera growth. Democratic medical building begin something.',1,'pbkdf2:sha256:150000$Oc2Uwau2$1a646dcd2c791f3bd01709bc9af70d1e94aad9b1f1341c384cdd606c9f678778',1,'2020-02-27 00:00:00.000000','2020-03-04 00:45:06.573981','f5bb0239d226be41d18813167a3b4b18');
INSERT INTO "users" VALUES (4,'qjones@hotmail.com','rmartin','Deborah Graham',NULL,'Risk major building soldier. Around data good make huge field break. Sister leg Congress office every city hold.
Prevent moment just message quite occur manage close.',1,'pbkdf2:sha256:150000$2clCAW46$9d80837e95f000e699164c762de83aff24ffb91f17d1ebdbba54592ebb41b0fa',1,'2020-03-01 00:00:00.000000','2020-03-04 00:45:06.693054','ab7a102cce43a12cc124c246e0ef5b97');
INSERT INTO "users" VALUES (5,'amberrodriguez@tran.org','harrelljennifer','Corey Myers',NULL,'Middle as east find night west want. Specific one require memory find answer. In feel because.',1,'pbkdf2:sha256:150000$8mwHECwX$08501ebe341841a8ef58b31829e2440d5c6af1e7fe6660ca0ca6d30d36c49944',1,'2020-02-15 00:00:00.000000','2020-03-04 00:45:06.806751','7b7139247540176f04ac4fb2e19f37a0');
INSERT INTO "users" VALUES (6,'brandon71@cisneros.com','kristinsullivan','Susan Salinas',NULL,'Painting wear consumer it answer. College democratic yourself recognize. Major another water what family.',1,'pbkdf2:sha256:150000$pbcaYEKy$0d996a731214dae01a99f8349ab425fe0c51bf687da9b1bb286992e34b39e436',1,'2020-02-22 00:00:00.000000','2020-03-04 00:45:06.924613','c40fe007a15d7007bdc49c1253149ea8');
INSERT INTO "users" VALUES (7,'kpatel@nixon-rogers.info','cheryl47','Elizabeth Rangel',NULL,'Movie theory attack which end away. No set safe focus.
Late situation investment begin. Three happen bank subject get respond.',1,'pbkdf2:sha256:150000$3P8iJehK$b64cb94003d60aa6e41a4a21458068f9641511e18d74e64527e0a76cb62205df',1,'2020-02-17 00:00:00.000000','2020-03-04 00:45:07.048365','76d7fc7c1879dfa28a140770608cba88');
INSERT INTO "users" VALUES (8,'ralph19@yahoo.com','gregorybrian','Michael Day',NULL,'Fast space beyond alone time imagine. Really power minute college team according manage never. Somebody contain easy term alone phone.',1,'pbkdf2:sha256:150000$XBtgxeED$efb18c36708a24967507043a56a2ae5ebe7b4ba1397ab52a08f527fcef3b39d7',1,'2020-02-27 00:00:00.000000','2020-03-04 00:45:07.164024','b81ac000b2c71e4ee44151a1eb3249d8');
INSERT INTO "users" VALUES (9,'robertwagner@gmail.com','williamstafford','Sarah Perez',NULL,'From manager product politics music red. Personal common other best method every.',1,'pbkdf2:sha256:150000$mpQFJeSM$743d5584d4a7e0ba3dac221064040ddb10339cc1cf58a82ca6d6502b28b6efce',1,'2020-02-06 00:00:00.000000','2020-03-04 00:45:07.286146','b6e7f5f3dd184681d0c8571b52e12dcb');
INSERT INTO "users" VALUES (10,'aprilmcgrath@smith.com','kimberly53','Brian Strickland',NULL,'Most inside campaign same create situation. Wear glass chance myself form.
Wrong pass identify another window of. Job ten challenge imagine. Benefit born so sometimes. President rock mind.',1,'pbkdf2:sha256:150000$MRQbZPEN$9cf38fd27e013a3c442d79b91b95f2b1b03e488840d1de55e512a251bb0c15ea',1,'2020-02-06 00:00:00.000000','2020-03-04 00:45:07.414677','04ed1ca80951a862222d82d47c8f2261');
INSERT INTO "users" VALUES (11,'hartmankristine@ruiz.biz','jgarcia','Travis Valdez',NULL,'Professional view art into phone create. Fill a rest economic require. Professional follow another wrong animal else.
Money bed responsibility national group usually way. Officer very computer seat.',1,'pbkdf2:sha256:150000$HUMjAgej$49cc76cfb51e600a2f460e84601c7e2b9bb8d639173eaf2b69f61fd40f31f8a5',1,'2020-03-01 00:00:00.000000','2020-03-04 00:45:07.536316','1325dfe0bcce2fb4ce313113d651c3d7');
INSERT INTO "users" VALUES (12,'ubrown@rose.com','crossdonna','Robin Lowe',NULL,'Ability challenge middle charge small never box lot. Somebody hope including adult manage join. Pull technology set own treatment major.',1,'pbkdf2:sha256:150000$Lecr9dac$4ffed61ef4ed933ec8b20340450db136c3ababf81b1bd5df616cef2e8baf04b8',1,'2020-02-18 00:00:00.000000','2020-03-04 00:45:07.660389','919a680701a13330b55fdcf02c75b7f5');
INSERT INTO "users" VALUES (13,'ishaw@perez.com','thomasblackburn','Traci Henderson',NULL,'This court finally main red probably region eye. Technology answer she friend. So usually least guess agree they.',1,'pbkdf2:sha256:150000$nBUZj3xc$6ff1edea59018329530dcb2cdee34234262de847e88c445c0e61c2c4ccf2c95d',1,'2020-02-06 00:00:00.000000','2020-03-04 00:45:07.779027','25ff5178b0ebce5f182373d4ff45542a');
INSERT INTO "users" VALUES (14,'nburns@chan.com','richard00','Jose Lawrence',NULL,'Within career religious as.
Cause ground pretty push. Almost skill possible.',1,'pbkdf2:sha256:150000$FSJfcQZa$2b5efcb303288c34ae874154cbe8366cb3b077b2b26bdc9c91bda7743c86dda3',1,'2020-02-13 00:00:00.000000','2020-03-04 00:45:07.896672','1baf458914f53cbecc7384493c58a75a');
INSERT INTO "users" VALUES (15,'hclark@gmail.com','sandrabrady','Alan Lambert',NULL,'Music executive left place story too official. Budget second certainly win sea. Game speak not study.',1,'pbkdf2:sha256:150000$wTHviWVA$dfbc34940d03ca14697608aa83a0073c423539cd0844ef40fcfd23a6d6f4cca5',1,'2020-02-15 00:00:00.000000','2020-03-04 00:45:08.019158','a6d0e8a2d87d19593bf850bcc89b4adf');
INSERT INTO "users" VALUES (16,'michaelmitchell@hotmail.com','ecastro','Alan Jackson',NULL,'Project strategy forget message simply adult loss. Authority between oil city. Record suddenly particularly inside he.',1,'pbkdf2:sha256:150000$jq5VXmpL$e7d7ddeea9cdbb6091c605987cfefa03165442b8e17fc8a71de59e930e006151',1,'2020-02-11 00:00:00.000000','2020-03-04 00:45:08.138639','d3e36f2a53e4fdf84228d8124af5f5f6');
INSERT INTO "users" VALUES (17,'steven40@ewing.org','bwalker','Christine Campbell',NULL,'Gun increase dark mother much wall political. Performance turn human official space purpose husband. Hold explain special bit weight.',1,'pbkdf2:sha256:150000$fWRLyAVY$6ef712ca04a8adbdbec262a26b7b535a8d3791421ff835b224c3810747565251',1,'2020-02-04 00:00:00.000000','2020-03-04 00:45:08.258600','d7c5cc6b400bef9621c25f9c91fe6015');
INSERT INTO "users" VALUES (18,'christian33@norton.info','chad76','Luke Martinez',NULL,'Pm worry soldier budget campaign whatever. Business three show apply take. East amount career build state step.',1,'pbkdf2:sha256:150000$HwV7AjxA$04037d0c1238443a2e34f9bc10a454fd4bb3601a4a06daea1d8214b948ec103a',1,'2020-03-01 00:00:00.000000','2020-03-04 00:45:08.390365','94a30bfed4441bcf65a8494ba89d2634');
INSERT INTO "users" VALUES (19,'oliviajackson@hotmail.com','jenniferrichardson','Natalie Wilson',NULL,'Economic lose group this.
Street hand few thought organization often suffer. Bring collection which various show. Company election right west.',1,'pbkdf2:sha256:150000$dYIihqh2$678a2e8e77cba483b7e0955dbcdd10b4a0a4fd25b6bd3d1aea5c5cb9408521be',1,'2020-02-11 00:00:00.000000','2020-03-04 00:45:08.512015','cd74c4e4060e2bd4836f2149cf0cd2c1');
INSERT INTO "users" VALUES (20,'westshane@frost-key.com','robertwhitaker','Andrea Benson',NULL,'Try indeed spring result. Boy detail dream recent.
Protect former more.
Claim measure situation remain able kitchen weight.
Nice car ahead decade. Position heavy party themselves soon where any.',1,'pbkdf2:sha256:150000$mdOKV68m$29736c36c6b3a6006d8d4a238de6888e75b29d3fe44468f2efa577f73b17f847',1,'2020-03-01 00:00:00.000000','2020-03-04 00:45:08.628232','1d74b89ce284cd3517e43aea9c07ee5f');
INSERT INTO "users" VALUES (21,'lopezlaura@davis.com','edward04','Cory Harper',NULL,'Student property gas value party. Call politics audience may rate. Our significant office view his population alone.
Local culture act. Bed behind sense. Another end find development.',1,'pbkdf2:sha256:150000$5PvRAXAt$2ae8ef8d0d0d64d853cb449074a3f78757088e85b8d5cc7dc50845aeba194af7',1,'2020-02-08 00:00:00.000000','2020-03-04 00:45:08.756715','fcd5136b60447443f79bf8e5c4cbef9f');
INSERT INTO "users" VALUES (22,'vobrien@smith-hicks.com','ywaters','Sherry Hunter',NULL,'Ready will cut foot friend. Large set space although glass again almost. Inside either message process fact evidence change.',1,'pbkdf2:sha256:150000$uGr1In24$8af4adbfc6e1264c5b51da0f12bafaf4c5968b337ecd15f4785eb25e094731c1',1,'2020-02-04 00:00:00.000000','2020-03-04 00:45:08.872622','3939b6d1cb9d0b41a94c1f382e32f919');
INSERT INTO "users" VALUES (23,'jayfaulkner@hotmail.com','reneewright','John Hernandez',NULL,'Amount scene fund whom notice indeed. Office federal anything if provide quite money. Few white age ever together bring someone air.
Evening likely analysis case.',1,'pbkdf2:sha256:150000$bUu9zRay$3c6b5ce8bfe75199569d00795eec2e890ae8a084cd197c7c5fde2d0af4416bb6',1,'2020-02-07 00:00:00.000000','2020-03-04 00:45:08.987401','f82cd164a18ca123aa6be1d44073dd12');
INSERT INTO "users" VALUES (24,'ochristensen@james.biz','msullivan','Lauren Arnold PhD',NULL,'Outside industry edge. Writer most capital.
Born stand usually time machine and.
Firm give page.
Company course watch there not. Goal east you order citizen.',1,'pbkdf2:sha256:150000$ft6thkqZ$24f4b069f3a5550fb40ed17cbffadde9ddf59fe8def86de4623546fcb2c94135',1,'2020-02-18 00:00:00.000000','2020-03-04 00:45:09.101727','816a2ecefd63b438d26f8ffd645e2b5a');
INSERT INTO "users" VALUES (25,'melissa55@lee-owen.com','jeffrey77','Samuel Burnett',NULL,'Second despite bit doctor impact else. Food operation bar try. True guy inside.',1,'pbkdf2:sha256:150000$HbRFAE0F$b7a555c0834bd85d140e27ac105df153b24904c7e7a13d60c828075c6381cc4d',1,'2020-02-23 00:00:00.000000','2020-03-04 00:45:09.222985','245d930ac6523149a2479ee45ca56d41');
INSERT INTO "users" VALUES (26,'cherylwilliams@gmail.com','logan55','Alexandra Evans',NULL,'Series act structure camera include amount.
Last college live note number open. Think safe politics be within chance capital. Student program be just rock.',1,'pbkdf2:sha256:150000$cYRwuyvR$bfe00f3bcc39e1fa57d8011c69546dec640bcf393c66a17c656004974e9ae4d8',1,'2020-02-24 00:00:00.000000','2020-03-04 00:45:09.347277','3dfd9b7bc5a62d91f6daa0018d176419');
INSERT INTO "users" VALUES (27,'oacosta@terrell.com','smithrandy','Sierra Johnson',NULL,'Outside somebody point throw society do write. Our onto yourself lose. Where right end many sort down want.',1,'pbkdf2:sha256:150000$DzOssjRC$c7090d631f626dd48b07eb3e22459d0241486eaa0d82e8a390aba4df51bbabb4',1,'2020-02-13 00:00:00.000000','2020-03-04 00:45:09.473624','8451b01040bdd2286b3813a03638d1f0');
INSERT INTO "users" VALUES (28,'sdavis@gmail.com','austin75','Laura Wong',NULL,'Local tax why happy top hundred carry. Move cover no north drive national wide material. Single build people side station. Third possible once time staff far director space.
Miss who red day decide.',1,'pbkdf2:sha256:150000$iBQx1HCI$39c49061f885381a8799c93a10eba3daef7e487e6c9a6c255ef3bdf4d74f42d1',1,'2020-02-17 00:00:00.000000','2020-03-04 00:45:09.592406','19b9137f81c34bf3439c355b352d9c18');
INSERT INTO "users" VALUES (29,'mtorres@luna.com','tnelson','Steven Perez',NULL,'Star prove arrive into public new card. Sell final cold discuss cut child economic. Career source activity magazine she speech myself.',1,'pbkdf2:sha256:150000$ddH1M4zk$679979be6273b3d48947cc233ed02d0362c6eb150e927029e0a5be4eb88a93e4',1,'2020-02-03 00:00:00.000000','2020-03-04 00:45:09.711283','6542f96f8c2af3ac744b13bc15d5a604');
INSERT INTO "users" VALUES (30,'markshah@yahoo.com','lorijohnson','Sean Reed',NULL,'Short particularly person sit decision agree Mr. Explain radio everything language human general real. Card quickly by figure scene audience admit.',1,'pbkdf2:sha256:150000$gLYaUf4w$70cd42b9d784d172187fbb26e5fd52b43a2b0c28742a9d8ec56e8530ee439f2d',1,'2020-02-07 00:00:00.000000','2020-03-04 00:45:09.837487','014f7c768be2ce94566a42fda66b13af');
INSERT INTO "users" VALUES (31,'taylorbrittany@burke.info','krista93','Justin Newman',NULL,'Decide two age pass. Future spend low protect. Enter field practice would as green official collection.
Professor phone case form like. Approach give then concern leave activity each.',1,'pbkdf2:sha256:150000$MZwvsQxh$0c9291de0204692138880a34fca8257cff8953dad8c4f45744296b6a01faf0ba',1,'2020-02-22 00:00:00.000000','2020-03-04 00:45:09.960919','7fcc2948d798881f8e7e5c679c670590');
INSERT INTO "users" VALUES (32,'kristina03@johnson-schneider.com','qdeleon','Belinda Waters',NULL,'Low leave look use. Soldier improve be side difference when.
Trade issue certainly tell. Democrat guy author candidate. Case off identify local feeling.',1,'pbkdf2:sha256:150000$7M9TX2zq$c734d6ccc1f50f357489c3a125c9bf8e51435b2950ec267b80fcbd2d51246bd7',1,'2020-02-09 00:00:00.000000','2020-03-04 00:45:10.084468','e2fb67c3856f88125abc6b552ff96878');
INSERT INTO "users" VALUES (33,'samantha26@price-carter.net','reesekyle','Justin Schwartz',NULL,'Far how west product. Point allow every student wide record future southern.
New human although. Each sea them once public. Election true pull quality father.',1,'pbkdf2:sha256:150000$krDTWZk1$89fd86c403624695d816822678f4117cf1cffd94860acc6b55c61168144a8fe8',1,'2020-03-02 00:00:00.000000','2020-03-04 00:45:10.199763','16114d5c517bd604b65f56ab3425610f');
INSERT INTO "users" VALUES (34,'craigamanda@gmail.com','debra09','Ashley Watkins',NULL,'Now debate war family nation stand. Sea article reveal professor woman by wonder. Large save from million option.',1,'pbkdf2:sha256:150000$rzZ1MneD$3c032784960fe971b13ae55a2bea121cfa645ae92925e81d6a5312ff866077c2',1,'2020-02-17 00:00:00.000000','2020-03-04 00:45:10.318853','3d42c458a0d02fa6bd44093fbcaf5f4a');
INSERT INTO "users" VALUES (35,'audrey73@gmail.com','ibrown','Amy Copeland',NULL,'Sport instead single describe after. Wait form check possible surface thank health opportunity.
Spend trade person whole.
Tree care church age wide. Trip watch somebody every within us.',1,'pbkdf2:sha256:150000$dKNCFlfO$7273248e525746d494c0159013c846bbe000ee5eb9761c84472a89365f8af21a',1,'2020-02-05 00:00:00.000000','2020-03-04 00:45:10.441894','55cc3d3bb8a3b80ad73841995a077bd0');
INSERT INTO "users" VALUES (36,'austinbentley@yahoo.com','mcclainamanda','Stephanie Hoover',NULL,'Present wait Mrs suddenly. Treatment citizen wide pressure. Age available including best stand national.
Affect world not call many agency many. Around news hear big window.',1,'pbkdf2:sha256:150000$mSbcxvQE$5583c7b609cda72c1a8f8319c03e5f32e853f8e111edd28c344f8df31978794c',1,'2020-02-12 00:00:00.000000','2020-03-04 00:45:10.559471','d373731d2b94e51fe91f249056051a2d');
INSERT INTO "users" VALUES (37,'johnsonlucas@martin.net','leah51','Tamara Buckley',NULL,'Those appear month section role. Meeting TV under.
Feeling another similar Congress off. Down camera even nice high character should. Despite join its forget difference production yard.',1,'pbkdf2:sha256:150000$Z6VffNFg$98a13d599859d85071a742d581e2e4cf3cc07133a88ad84e0395ef5b9fb9a995',1,'2020-02-22 00:00:00.000000','2020-03-04 00:45:10.679422','664308c2becfd77d45bd6f374ae5cb9f');
INSERT INTO "users" VALUES (38,'carrheather@yahoo.com','blee','Timothy Lawson',NULL,'Can organization but control skin check wait. Decade this nice fire risk. Watch nice agent sing.
Herself note down anything. According second resource space we gun.',1,'pbkdf2:sha256:150000$VUj5xCls$292c906abe5ed981d720536d432af705c8ccbd1429722aea675dfa9d0e43e7ff',1,'2020-02-12 00:00:00.000000','2020-03-04 00:45:10.798362','b70f3a3a992eabd0d47e7cbc5e0a5677');
INSERT INTO "users" VALUES (39,'whitneysusan@hotmail.com','diana27','Erin Park',NULL,'Thousand grow teach. Above want fill Republican around travel foreign. Cost wonder purpose team.
Our nearly person agent. All third interview subject. Difficult director professional everyone.',1,'pbkdf2:sha256:150000$DIq6rLIc$94fb2fc66d220062b4f9add373e575b9d23ebe2eac05100ed2a626dc24483958',1,'2020-02-07 00:00:00.000000','2020-03-04 00:45:10.928439','bd134b11177e94cb26063f578a10225a');
INSERT INTO "users" VALUES (40,'johnsonannette@waters-adams.com','dthomas','Kristen Oliver',NULL,'Everybody year range defense amount project listen.
Player apply exactly million represent we rise. Talk reflect country there.',1,'pbkdf2:sha256:150000$15SbddgR$25de243f35ef1115bea9de46db8e5a1169122791ed93bbe6c2be8d55e5ba3b1b',1,'2020-02-22 00:00:00.000000','2020-03-04 00:45:11.046405','9d9589210ceed552e82de178d176f85e');
INSERT INTO "users" VALUES (41,'samuel35@bridges.org','cookkayla','David Adkins',NULL,'Direction sense person themselves should. Model community chair color too kid. Also both trip arm there summer.
Until entire stuff popular.',1,'pbkdf2:sha256:150000$kRjeRF2Z$22d673dfae894700552bfb1f84e679e3c9d5b07a6d06212b99d37e373f582f57',1,'2020-02-26 00:00:00.000000','2020-03-04 00:45:11.160685','5467c836a41b2a64914c64deee020d2e');
INSERT INTO "users" VALUES (42,'georgechase@yahoo.com','paynetammy','Brandon Moore',NULL,'Throw both from. Anyone car occur. Tonight building test sea. Single determine majority born moment point.',1,'pbkdf2:sha256:150000$9cjVh1y2$43cd63f210fcfd9133e5bc46ccad5dd2cf70f9300d0d44c7717eb5c3a3a98664',1,'2020-02-27 00:00:00.000000','2020-03-04 00:45:11.275014','d42b0758925e9c70a01428201b471a83');
INSERT INTO "users" VALUES (43,'dwhite@hotmail.com','kwallace','Donna Taylor',NULL,'Table fast movement church task anyone. Perhaps only year pick PM.
Laugh country pattern. Strategy only national machine forget would. Director everyone anything cut.',1,'pbkdf2:sha256:150000$167S9gLa$2588bbaaf92e01dd998609ea6d3aa32be772cf70057ec8dd079c27bec5f87dfc',1,'2020-02-25 00:00:00.000000','2020-03-04 00:45:11.396621','1c77ae3ec980cb37ee485c063347329e');
INSERT INTO "users" VALUES (44,'logantapia@hotmail.com','thorntongregory','Lauren Lowery',NULL,'Office provide on great number talk body. Reason the opportunity American step. Whom seek probably structure never sound.',1,'pbkdf2:sha256:150000$ijERd0Pq$45ba1a8427583d44184061711e5bb6089bd262f905ca6000e34f386bae4069ba',1,'2020-02-13 00:00:00.000000','2020-03-04 00:45:11.522773','0ea7adb2528993eaed026b19d7df5867');
INSERT INTO "users" VALUES (45,'sean61@garza.org','joesherman','Robert Green',NULL,'Card doctor people century garden rise agreement. Edge individual lay everyone chance. Serious worry maintain rise.',1,'pbkdf2:sha256:150000$aTFM8n5q$6a1eea6507bd1c8bc41fe77cbf36980f9d92cfa10cf5a50127660312703c6522',1,'2020-02-11 00:00:00.000000','2020-03-04 00:45:11.646103','2d876b339574e99bb5c5f1d6e574eb55');
INSERT INTO "users" VALUES (46,'albertellis@hotmail.com','nsanders','Rebecca Lee',NULL,'Decision near hear view affect improve push. Try behind baby rate try yet. Marriage expert son language room represent street include. Join range commercial customer.',1,'pbkdf2:sha256:150000$k3ycRfBG$6395e348a83bfc51f5fdbb7f0927bda26349d620327c2f097df2bdc1d3ef91d0',1,'2020-02-12 00:00:00.000000','2020-03-04 00:45:11.763611','04f422f3d6c84f1dd8f76ebc1f7d0a16');
INSERT INTO "users" VALUES (47,'patricksingh@rivers-wilson.com','corey61','Anthony Newton',NULL,'Gun pass how sort themselves interview. In history question technology. Herself news visit particular agree including.',1,'pbkdf2:sha256:150000$5Yf9J5dq$75e35c729144aa002227d134c433528976f1ded48ad3e418923ae8c5eadd3cec',1,'2020-02-03 00:00:00.000000','2020-03-04 00:45:11.886651','d32eaca258cb54b8bf00353682301b0e');
INSERT INTO "users" VALUES (48,'iguerra@mcguire-garcia.org','jeffreycruz','Laura Taylor',NULL,'City everything main evidence. Interview guess decade agency evening.
Idea color energy. Education focus drop happen.',1,'pbkdf2:sha256:150000$D7fsjxOj$ab78942caa4a919c40852b05aef09655b17a6161aa07436a3f846525179e4d69',1,'2020-02-17 00:00:00.000000','2020-03-04 00:45:12.013826','a4479caffb0e08e5449802ad7fd523b1');
INSERT INTO "users" VALUES (49,'annacohen@gmail.com','phammatthew','Judy Charles',NULL,'Subject similar together focus expert believe along. Word bank skill close. Mind nearly enter why material.',1,'pbkdf2:sha256:150000$IH3U8eyr$218141aa677531a2ade45e5123d226df1d411bf647dd44949aa377e5639f912b',1,'2020-02-07 00:00:00.000000','2020-03-04 00:45:12.137250','0470c234303fdb76a77a1e95639bcb43');
INSERT INTO "users" VALUES (50,'olopez@hotmail.com','freed','Calvin Dunn',NULL,'Site training wind some foot. Way good although defense talk despite author. Response point example director nice house agreement policy.
Really marriage doctor they change real.',1,'pbkdf2:sha256:150000$lEDBB31K$70940cba94c56d151660767767b16918c7e29d1d2b54feedb5dd9b517cf8ba98',1,'2020-02-11 00:00:00.000000','2020-03-04 00:45:12.257730','5df1cdfebb7b0648a568651d9e594208');
INSERT INTO "users" VALUES (51,'mnorris@yahoo.com','robert06','Michael Schwartz',NULL,'Many wall although TV. Summer once process might probably live suddenly.
Body heavy amount check around. Could edge model. Fast she population white owner appear. Back against use yard.',1,'pbkdf2:sha256:150000$K4zkvaE9$bbbb34f3a565e563cbc33a25844f83de72aef1c504ee63479d7b230528f3f5fd',1,'2020-02-13 00:00:00.000000','2020-03-04 00:45:12.383651','4fdbd7901cecb5baf82ed5f9be997983');
INSERT INTO "users" VALUES (52,'josephritter@peterson.com','richard57','Sandra Cobb',NULL,'Animal join which course. Foreign then heart century others amount music.
Anyone social degree continue design politics. Ago per Mrs security federal second.',1,'pbkdf2:sha256:150000$GQM3Lsia$d65274cf2e576a3916512ea593318f24eaa53539f7052aaf92e7a8a8eb7f182b',1,'2020-02-08 00:00:00.000000','2020-03-04 00:45:12.501081','9eeb5ecd3dc87a359ed62f5f462aa048');
INSERT INTO "users" VALUES (53,'hernandezjeffrey@mendoza-wiley.biz','aarongarcia','Bethany Thomas',NULL,'Player control push research successful him necessary night. Film during issue magazine stand ability.
Save any certain political ground second do. Current option education.',1,'pbkdf2:sha256:150000$yXdd7wp8$1023314801d1381bdd29172f9df2d46c1729c0d814ed5f51e43a7433d6c49d5d',1,'2020-02-17 00:00:00.000000','2020-03-04 00:45:12.621669','6517da825e0c672787017269452566b2');
INSERT INTO "users" VALUES (54,'kelsey93@gmail.com','thomasanderson','Gabriel Beltran',NULL,'Popular at performance. Probably team tonight yard major school different.
Not late without man suffer act. Operation president our cause we. Arrive kid stuff everyone score fast.',1,'pbkdf2:sha256:150000$gY874BqC$ec05eb5857e07c019cfafe1cc8b221fa9ca51873896f72bd22b30acf2d7526d6',1,'2020-02-24 00:00:00.000000','2020-03-04 00:45:12.744238','7a40959f60203342d2f1c558b702f72e');
INSERT INTO "users" VALUES (55,'pamela51@gmail.com','gbates','Lauren Navarro',NULL,'Career wait finally. Section shake people bad ability story form. Information market put center difficult job international.',1,'pbkdf2:sha256:150000$c1fyO7nT$b633db92d1fa992a9aabf506b8f7b972efdff62dcc928eee44c0f006eb6cdd4c',1,'2020-02-05 00:00:00.000000','2020-03-04 00:45:12.878701','0d20238c78939cdfab40412c13a6b841');
INSERT INTO "users" VALUES (56,'jacobgray@bates.net','gthompson','Kevin Mitchell',NULL,'Table describe policy argue perform. Decade through property none water capital establish. Detail among want television special to.',1,'pbkdf2:sha256:150000$7pCMh1Nz$664bc33c2fb10c139c0107da840ddb4b5401b586296f5e8aaa7245a3bb0df7dc',1,'2020-02-15 00:00:00.000000','2020-03-04 00:45:13.002325','d4a3ca490ed2fdd883e95008c8e920f8');
INSERT INTO "users" VALUES (57,'cwood@yahoo.com','qduncan','Raymond Jackson',NULL,'Score worry stand generation pull region. Other summer business tax join program sea late. Article nature identify coach hope rock. Democratic once address drug lay remember.',1,'pbkdf2:sha256:150000$XEHqCZDO$24ec474f86b28d0ed9f977427040547307822847cc6db6d87d74f95933a25c94',1,'2020-02-21 00:00:00.000000','2020-03-04 00:45:13.142972','e4043ddfe38bb6ca47d703557212cb71');
INSERT INTO "users" VALUES (58,'hmoore@gmail.com','turnermatthew','Brian Thompson',NULL,'List edge suddenly tax middle. Similar usually along difficult. Trial indicate thought his.
Office begin each. Cell laugh realize herself somebody value rest figure. Which chair down.',1,'pbkdf2:sha256:150000$t75EcyZd$dae2bff74824870f77a3c75068ded4416c7bab32df27ad1ff365a1276ac200ea',1,'2020-02-05 00:00:00.000000','2020-03-04 00:45:13.257707','80eef76edf04306492ac37f41ac16725');
INSERT INTO "users" VALUES (59,'derekritter@yahoo.com','jeremydowns','Aaron Mcclure',NULL,'Remember listen parent environmental. Party reduce kid movement of. Nor certainly nearly pretty bad.
Learn up fast opportunity size. Without government them people similar language practice discuss.',1,'pbkdf2:sha256:150000$JNqJgM1f$297413d6a40447d0993e2bbcfa39f9a9275698c52b4a303fecb29354efb3aba4',1,'2020-02-17 00:00:00.000000','2020-03-04 00:45:13.377270','36dd9b7969ff13d872c51555d170d955');
INSERT INTO "users" VALUES (60,'william04@yahoo.com','ecruz','Robert Krause',NULL,'Glass red life appear behavior. Hour well field practice without share store. Story staff scientist edge safe increase wrong.
Law each perhaps similar. Product discover modern son remember.',1,'pbkdf2:sha256:150000$JarySFyk$6e61e4c3185e43e2a55312b681543bcce95dfb8a5f4b0fd4b7fc8d405df07dcd',1,'2020-02-27 00:00:00.000000','2020-03-04 00:45:13.501509','2c347f614c664e4ee529d2ccb3011c0a');
INSERT INTO "users" VALUES (61,'taylorcharles@yahoo.com','gonzalezanthony','Randy Wilkinson',NULL,'Land consider feeling serious. Too reality require catch owner. Use of cup question move prevent.
Arm house what. Than film happy.',1,'pbkdf2:sha256:150000$moLkHSEq$0824de4a2474a5244cc4af3a3fcdb578323dac8931216a1430f2f0fdd3e095e6',1,'2020-02-12 00:00:00.000000','2020-03-04 00:45:13.626487','11942c97df5e3b8a10a96099186d7956');
INSERT INTO "users" VALUES (62,'allison81@gmail.com','jimenezolivia','Stacey Gomez',NULL,'Strategy kitchen small record. Challenge threat record traditional sense. Store artist professor include threat.
Moment friend its special. Court important hold early clearly fish.',1,'pbkdf2:sha256:150000$4hkg3dcX$6778418dbdc76cc1ad219ef877b4f2c8b5cb7a8b3aea435145898ae76f104a31',1,'2020-02-10 00:00:00.000000','2020-03-04 00:45:13.744943','b79679e4f23c85db7e72933d20c47dd6');
INSERT INTO "users" VALUES (63,'jessevaldez@lee-nguyen.com','pscott','Brandon Hernandez',NULL,'Area listen responsibility blood respond adult. Grow base try store suggest without however. Dark kid hundred heavy little ten various.',1,'pbkdf2:sha256:150000$1lOZtK5H$59c25fc35f7bfe0834f8c0a5a8942112fcdb54c8c01ed4adc7b695eedd1bd965',1,'2020-02-11 00:00:00.000000','2020-03-04 00:45:13.861776','d47bff62760f3c4acf65cf2e3dd53c19');
INSERT INTO "users" VALUES (64,'michael24@hotmail.com','qwagner','John Adams',NULL,'Everybody national Congress particular assume. Cultural example without military life enter window.
Call yeah response machine decision. Direction who top the according.',1,'pbkdf2:sha256:150000$TjTeaLiu$cb70d120cffefa0a64cbc9db7eb7737b2c70b5398e0edff137be6ede5bb4f0e6',1,'2020-03-01 00:00:00.000000','2020-03-04 00:45:13.979834','d68b15aef37778f48ab59be605171f64');
INSERT INTO "users" VALUES (65,'sheenanorton@hotmail.com','mklein','Isaiah Dodson',NULL,'Fish card some magazine action sister nature. Company catch reach show student. Act on front affect individual somebody.',1,'pbkdf2:sha256:150000$aLAAer5u$8111e17acba7b4b490ad290a90ca3fc37d5df8bcfb27b19526eeaa71fc20be34',1,'2020-02-21 00:00:00.000000','2020-03-04 00:45:14.097561','8ec24742da3b2a48faab94b8106feaec');
INSERT INTO "users" VALUES (66,'davilakenneth@gmail.com','rebecca83','Justin Abbott',NULL,'Nothing thousand wait training us expect enough.
Culture young your lead out laugh half. Hit hear this bill summer so.
At place foot without military apply. Item staff war television thousand.',1,'pbkdf2:sha256:150000$FFMFGuZw$9a155c760fa95eb5a8b05577be01cfea326ef70001989c27e3cccfb4312d6d1d',1,'2020-02-03 00:00:00.000000','2020-03-04 00:45:14.215762','20f7e38718ca6c9a2dd986270e74aba3');
INSERT INTO "users" VALUES (67,'macdonaldsteven@yahoo.com','mclark','Vanessa Clark',NULL,'College unit painting yes. Feel hold half spring of recognize public condition.
Drop figure charge character. Far individual herself night. Three lead central peace shoulder agency.',1,'pbkdf2:sha256:150000$nPnPECqL$55e4196a308f5be6b9562d5581b9f8e34f8f8e42a26312ba6d7faf6199173da6',1,'2020-02-07 00:00:00.000000','2020-03-04 00:45:14.338976','f87c461c3d45ff9384df16bb63e10f76');
INSERT INTO "users" VALUES (68,'dukekurt@gmail.com','mtucker','Margaret Parks',NULL,'Southern group entire mention such kid save indeed. Foot international player remain college. World my question maybe article human.',1,'pbkdf2:sha256:150000$4lRZxRuz$e491dfd1fafa5ce8eec57f0fd4005d78d15dffa08abe1b5eac57cf62f5ba9884',1,'2020-02-27 00:00:00.000000','2020-03-04 00:45:14.454026','9528994df8a0bc74bf8cb4713b2570db');
INSERT INTO "users" VALUES (69,'hduran@rodriguez.info','kevinking','Joseph Todd',NULL,'Statement appear movie church. Table put itself state hope surface baby front. Poor purpose consider adult.',1,'pbkdf2:sha256:150000$WjHTafmT$a55a041bd147deda9d701f6950425e630c39a7ff6ad009072b45c6da3d7fd94e',1,'2020-02-18 00:00:00.000000','2020-03-04 00:45:14.569926','640252c6324172dd17229ee675bfabfa');
INSERT INTO "users" VALUES (70,'fford@hotmail.com','hurstjohn','Chelsea Rasmussen MD',NULL,'Doctor difference manager. Management party card station training. Various media make take white.',1,'pbkdf2:sha256:150000$tu3FBnO0$ecea78c7801c01fff6aa5260382c143826366c9d0733abf0ede2376b037b7b67',1,'2020-02-13 00:00:00.000000','2020-03-04 00:45:14.691787','e470eb0f022f1276377c55e137ec6b38');
INSERT INTO "users" VALUES (71,'dpatton@gmail.com','gibsonelizabeth','Margaret Bowen',NULL,'Together girl here total design five. Final upon participant reason letter will early.
Size exactly store job. Work protect wish represent do environment. Society low pass goal view.',1,'pbkdf2:sha256:150000$NITiHhOJ$2bcd29cd2ca391757c8f0ff73019a422c8252ffa3ca18cee4260ef69b684549d',1,'2020-02-23 00:00:00.000000','2020-03-04 00:45:14.813892','e3e69e00e4969493d48a5a995f5d566e');
INSERT INTO "users" VALUES (72,'buckleydustin@hotmail.com','uspencer','Brittany Dawson',NULL,'Recent fight side serve. Project sometimes nation even. Professional be up surface. Role pretty interview seat rise.
Remember owner stage pretty. Yourself certain development happen choose bring.',1,'pbkdf2:sha256:150000$LCVjllqR$b3ea80ca0d1fd0a28f31245e86605a1b54dc267cf9022deef9a07642d691504e',1,'2020-02-17 00:00:00.000000','2020-03-04 00:45:14.941647','89f005c67d9abdb39b7446aaba7fde0c');
INSERT INTO "users" VALUES (73,'christine85@ortiz.com','rnelson','Amy Martinez MD',NULL,'Your ask receive big three vote ask husband. Attorney doctor plan force official current.
Step fly represent once sign. Model perform water red professor. Four hour plant.',1,'pbkdf2:sha256:150000$MM2SlF2S$57f87b9140444d388f108f0a8c288a9fbab6a3f7a4e9c78ac1166472d46d77b2',1,'2020-02-04 00:00:00.000000','2020-03-04 00:45:15.066352','93891dc37459123ac11ec36e5abdedeb');
INSERT INTO "users" VALUES (74,'tinaochoa@smith-hogan.com','paula21','Steve Todd',NULL,'Remain create other road south. Anything should continue those director station many.',1,'pbkdf2:sha256:150000$GaiMWDj5$d84800943d4bc926d1eea251eb5c52054aa42956b96cd0d5e53388493377718c',1,'2020-02-14 00:00:00.000000','2020-03-04 00:45:15.193324','e536688cbd1f42683423f7c351b50368');
INSERT INTO "users" VALUES (75,'debrabrady@gmail.com','jessica48','James Lopez',NULL,'Seek itself meet ten. They reflect knowledge support best option break support.',1,'pbkdf2:sha256:150000$ZKt5HvrF$2bd7b41a6b2a8139d5742583d195c506171789c912017b31513d7408bd198131',1,'2020-02-24 00:00:00.000000','2020-03-04 00:45:15.315653','c0c3fb6f538627e7932cfe009b46184c');
INSERT INTO "users" VALUES (76,'tchristensen@yahoo.com','blankenshipcalvin','Jennifer Gray',NULL,'Could can spring check. Personal college business painting full especially program.
Message play it sport we. Research thousand national outside remain able expect sister. Scene already sound occur.',1,'pbkdf2:sha256:150000$1ZtSIEr6$8da45be9339e0dc4dd47e0f1faa251e242fcd68e9fd7b99cf8d777af0ccdb895',1,'2020-02-11 00:00:00.000000','2020-03-04 00:45:15.431638','ca3f844865c93e1b32fd59cca2e54462');
INSERT INTO "users" VALUES (77,'brooke15@yahoo.com','nelsonjohn','Scott Powell',NULL,'Project go Congress lay. Appear soldier person region ability. Tell president energy on cell teacher. Nothing why again company college year.',1,'pbkdf2:sha256:150000$Uwto2vuz$6e4d1c2b1fe34eea34c883ef71a5a1fd4c48e2e8e97787efb8cc57357cadd2ed',1,'2020-02-12 00:00:00.000000','2020-03-04 00:45:15.544853','ec053e2c5bafdbc88dedd4db03c38748');
INSERT INTO "users" VALUES (78,'ryanrobinson@hotmail.com','tgoodman','Jacqueline King',NULL,'Home country miss picture here.
Agreement seat young role. Federal analysis campaign glass mind.
Million possible form woman. Prepare benefit course throw leader report you.',1,'pbkdf2:sha256:150000$OcWwnnF7$eff4473a3da6f8e33b11646a09ae4312511886c850be000d3aa8e5e49a8e6606',1,'2020-03-02 00:00:00.000000','2020-03-04 00:45:15.659200','c7100f78a4e021eba198d11be685f7c1');
INSERT INTO "users" VALUES (79,'melissa28@johnson.biz','ycarr','Erica James',NULL,'Nation skin pretty nice company. Day project around.
Reveal usually fund. Consider fast soon best example. Nation describe hour score physical why sense.',1,'pbkdf2:sha256:150000$pVmjFIHl$a3aa0a70b98272a973c74aa5c500ce798cb78eba3cf572b90283ed385ac5a0b3',1,'2020-02-06 00:00:00.000000','2020-03-04 00:45:15.779412','bc75b274ef61a06868ea0b0f8fd1eca0');
INSERT INTO "users" VALUES (80,'wilsoncindy@brown-nguyen.info','pagekimberly','Steve Gonzalez',NULL,'Increase body church whole.
Until difficult miss for. Such either many mouth among open along.
Agreement call nation contain. Study vote majority third commercial any.
Learn area much more what hand.',1,'pbkdf2:sha256:150000$k3wszWMS$43a9513aaaa0ab62452e56d8ce92e624a7b83572fb17273a55fad3a52c0b9a94',1,'2020-02-09 00:00:00.000000','2020-03-04 00:45:15.915701','20c24af94e1cd13092ca88caf689b598');
INSERT INTO "users" VALUES (81,'nlee@gmail.com','steven43','Thomas Hernandez',NULL,'He reveal production happy majority.
Black international behavior argue early increase no special. Consumer call lead media foreign only.',1,'pbkdf2:sha256:150000$Qj3bjtI0$8c37707532f49645e074de6489965370ab74f6bc7692b4fed2e5a251730ae23c',1,'2020-02-19 00:00:00.000000','2020-03-04 00:45:16.042241','47e2fbec131f13ac4055aa785f5fbf0d');
INSERT INTO "users" VALUES (82,'james68@smith.com','reginald22','Mary Dunn',NULL,'Year ask who goal culture. Nature news ready.
Bring over analysis young. Share than on space friend tree big.',1,'pbkdf2:sha256:150000$CMv4OuTl$46e866bcd5898cc850630e61a96e0417ba43f550821cc428ca15764bb8231c79',1,'2020-02-29 00:00:00.000000','2020-03-04 00:45:16.165335','e82df62861e87b6ce2df300d1677c1ce');
INSERT INTO "users" VALUES (83,'mendezlauren@nelson.com','juanyoung','Scott Fuller',NULL,'Skin next bit officer. Why nearly attention culture.
Significant third able. Party each bad in hot and already. Agree wind time red.',1,'pbkdf2:sha256:150000$InGbOYU3$bce7e29b9d15f7ba87cb4392c5a0b00dd508ea043632281abc20c07ddb28c184',1,'2020-02-17 00:00:00.000000','2020-03-04 00:45:16.291614','efa7d1a2a6d4deca8a89e95a0e494219');
INSERT INTO "users" VALUES (84,'johnsondouglas@hotmail.com','lesliebaker','Preston Rogers',NULL,'Paper southern walk arrive why until value.
North business detail should form door. Full sit right also nor seven hospital.',1,'pbkdf2:sha256:150000$SH1roMxp$52199d11fbc59aec77d398a8fe35927d029ef39b864d5880bc025d7094263de7',1,'2020-02-09 00:00:00.000000','2020-03-04 00:45:16.411977','78c687afc82f52d958493b45f213776c');
INSERT INTO "users" VALUES (85,'rodriguezryan@yahoo.com','nathanturner','Joshua Nelson',NULL,'Analysis sense shake. Until professor else. Road pressure them eight myself test their.
Alone accept lead. Degree material economy order stop.',1,'pbkdf2:sha256:150000$muEnSpmN$e0feafac9cacc7387c95e3aa4ed406abf2afa9e91048169ecc10926e071947ba',1,'2020-02-20 00:00:00.000000','2020-03-04 00:45:16.528229','36ac6301585e3177595715eb70b34eac');
INSERT INTO "users" VALUES (86,'miguel99@yahoo.com','nashgregory','Jessica Roberts',NULL,'Represent believe win tend. Discuss recognize buy society month church deep break.
Hour role word behind. Majority lot choose phone. Nice cold lawyer save.',1,'pbkdf2:sha256:150000$gOdHA5sa$7c9d70b38e6dc4442bf38669c8ef3786fe47d1a3dd1d34b62aa033c6f4b6efc2',1,'2020-02-25 00:00:00.000000','2020-03-04 00:45:16.649052','e5bc1355db3bd4184e32c0b0eccdc092');
INSERT INTO "users" VALUES (87,'catherine77@yahoo.com','avincent','Amy Moore',NULL,'Today painting join along. Painting once three on adult gas himself. Establish growth mission several boy feeling knowledge community.',1,'pbkdf2:sha256:150000$cb4vTWPQ$efb7f02e515d6d60f7e1bf6d98cd0e5a430960490bc284f1f5894484bf8e34e7',1,'2020-02-13 00:00:00.000000','2020-03-04 00:45:16.769217','201dced794ef1f4a59be48c9deafbbfe');
INSERT INTO "users" VALUES (88,'swilkins@watson.com','diazjoshua','Donald Fowler',NULL,'Note each hear they hear mean interest. Party just that fast. Tend institution begin local important.
Teacher present trip nation option prepare.',1,'pbkdf2:sha256:150000$u9mrKeYE$a40311426a5270e24f1faf56611716d14010a0a754c36075ee4ee7040a27adf5',1,'2020-02-23 00:00:00.000000','2020-03-04 00:45:16.900281','2f6052ab065190d8fc7ef59d3d2338aa');
INSERT INTO "users" VALUES (89,'nicolegraves@torres.com','cantukatherine','Robin Hensley',NULL,'Store civil exist claim care present event.
Film hot help third message.
Night season college environment beyond character.',1,'pbkdf2:sha256:150000$JXjO7iPF$e24d077c2831d7858cd7e889e7710ad0a624146d0609b5dbe49b0b25ec014652',1,'2020-02-07 00:00:00.000000','2020-03-04 00:45:17.020339','2fe83aa919957cdb059afbcc26759431');
INSERT INTO "users" VALUES (90,'ecortez@yahoo.com','vanderson','Kelsey Humphrey',NULL,'Course relationship opportunity others check attention. Street name sit believe throw style physical show. Congress himself exist human one several life.',1,'pbkdf2:sha256:150000$pC0orFFo$b694e16da57a52068ada4568c902d5154238ce65255357d00c35c542b8e9a6e5',1,'2020-02-11 00:00:00.000000','2020-03-04 00:45:17.139877','585c1f20ab36769e4e1838d132051dac');
INSERT INTO "users" VALUES (91,'jeremywaters@davidson-johnson.info','chandavid','William Henry MD',NULL,'Cell turn keep suggest our assume note. Modern as discuss his treat right. South brother too.',1,'pbkdf2:sha256:150000$vVgeXgUg$157178cb76959d2bb3bb22dbdffe624ce96b9e86cfd4c2961b1a4232b163b534',1,'2020-02-23 00:00:00.000000','2020-03-04 00:45:17.255790','2671094d72650ca58672b20b7dfd5d9e');
INSERT INTO "users" VALUES (92,'aliciajohnson@stafford-bryan.com','kanethomas','Marie Clark',NULL,'Decision college exist west stage memory security. Pay enjoy analysis pass black may. Coach according water improve claim including. Lead stuff air street hand picture.',1,'pbkdf2:sha256:150000$qj1bJVSu$9bd5bd7e095031fb9689a0acccdce4c674f97582b965109dc057f7af08c3ca7f',1,'2020-02-25 00:00:00.000000','2020-03-04 00:45:17.379041','41f82e63ba772732707d242076302317');
INSERT INTO "users" VALUES (93,'morancraig@gmail.com','breannanewman','Joseph Cooper',NULL,'Suddenly decide it tax sit name possible. Away three guy half rise majority either. On when along listen themselves late.
Finish blue science push for. Political ten it north individual thought end.',1,'pbkdf2:sha256:150000$LH1maPh9$128e5bd13c7eebbdc56eaba25cec76dc963ae234c60df781006ba3e7e53f26d1',1,'2020-02-24 00:00:00.000000','2020-03-04 00:45:17.497289','609eca4d8b5cccc68c864e5650578656');
INSERT INTO "users" VALUES (94,'timothy27@hotmail.com','salastodd','Laura Walker',NULL,'Practice former seem change worry put almost. Determine teach effort trade themselves adult.',1,'pbkdf2:sha256:150000$hiC4IWcH$6c7d44a445b73151d636be9a9237f0b1173f5c46a172f2d944b2c39a790812b9',1,'2020-02-29 00:00:00.000000','2020-03-04 00:45:17.613490','a3a693b5cf7c02d39b7c75804d573752');
INSERT INTO "users" VALUES (95,'eavila@thompson-saunders.com','lamsean','Bernard Hudson',NULL,'Stop heavy cost local actually natural full. Box role trouble body real available pretty six. Explain business next structure.',1,'pbkdf2:sha256:150000$DyQNEuHJ$fededd4a2364c99737e2c46493dd8ee16eed3209405b3e2c06c04bfa92343278',1,'2020-02-07 00:00:00.000000','2020-03-04 00:45:17.733735','d0d11859d0b0f20fea8c396cea2cc461');
INSERT INTO "users" VALUES (96,'nicholas87@beck.com','bradfordlaura','Timothy Frank',NULL,'Site here relationship there past write make improve.
Surface ever set million. Make control treat sometimes.
Baby make arm work account listen social whether. Really when easy.',1,'pbkdf2:sha256:150000$TyRYmCGk$8ac6a50d62207f83174f318d76a3b096182f46952fb1ed56b6475d1bcbb3df18',1,'2020-02-13 00:00:00.000000','2020-03-04 00:45:17.853979','737c50044fcfcc629c814ea62031eab1');
INSERT INTO "users" VALUES (97,'thomasrodriguez@hotmail.com','whitejeffrey','Brenda Stewart',NULL,'Change consumer important foreign cut him. So grow material head phone them commercial. Especially their hope image sister store.
Medical kitchen enough. Building artist throw pressure.',1,'pbkdf2:sha256:150000$44xabMok$ffec6f8f37c20464fb378af9af9f5faf162f59ef7b0505636b99dc693002e422',1,'2020-02-17 00:00:00.000000','2020-03-04 00:45:17.982355','c293426d26960089603437d1e6e21740');
INSERT INTO "users" VALUES (98,'douglasedwards@morales.com','evanscorey','Rodney Smith',NULL,'Discuss me seven sometimes parent popular both. Speak state yes blood school.
Cost the time husband else. Western affect away visit try.',1,'pbkdf2:sha256:150000$fIClaz8J$3b7223ee9922e37402c012680adfd9be492453658d1af352d82b5a8b9ca29f82',1,'2020-02-24 00:00:00.000000','2020-03-04 00:45:18.108419','9a856d8b55be0e0711a75593cd51f332');
INSERT INTO "users" VALUES (99,'hollandjames@gmail.com','ashleysimmons','Rickey Lawrence',NULL,'Something including sound. Can market international on machine seat then. Pm alone second look true here center election.',1,'pbkdf2:sha256:150000$ipTXx1vf$0fdf18fef76ed056e751553482c969b16d3431f089717cf32fbf51954fb11ed7',1,'2020-02-25 00:00:00.000000','2020-03-04 00:45:18.221586','78b80fc2eb5e727910b3fef4845344e4');
INSERT INTO "users" VALUES (100,'roynguyen@robertson-peterson.biz','tunderwood','Hannah Byrd',NULL,'Apply go nor two certainly. Billion together decade effect chance important star. Allow idea particular product her paper list.',1,'pbkdf2:sha256:150000$Qhm5rccw$356b995cdb6affd0c69abe7420c2febd644989971953eabac8fb375594eff49d',1,'2020-02-25 00:00:00.000000','2020-03-04 00:45:18.340499','8eca73d9e22e54092cb96ce995cef0cb');
INSERT INTO "users" VALUES (101,'brokenmind@gmail.com','bentsea','David','Scott','',5,'pbkdf2:sha256:150000$dRfJueii$10de4822ac48b5ab821af2a944a0cc88f59949e8e13cb80612832043f58bd326',1,'2020-03-04 00:46:04.305705','2020-04-22 11:06:45.716245','375215c39004b79434438d506bef07f7');
INSERT INTO "roles" VALUES (1,'User',1,3);
INSERT INTO "roles" VALUES (2,'Writer',0,7);
INSERT INTO "roles" VALUES (3,'Editor',0,15);
INSERT INTO "roles" VALUES (4,'Publisher',0,31);
INSERT INTO "roles" VALUES (5,'Administrator',0,63);
INSERT INTO "article_type" VALUES (1,'Review');
INSERT INTO "article_type" VALUES (2,'Editorial');
INSERT INTO "article_type" VALUES (3,'News');
INSERT INTO "alembic_version" VALUES ('7c567e09ff36');
CREATE INDEX IF NOT EXISTS "ix_articles_title_slug" ON "articles" (
	"title_slug"
);
CREATE INDEX IF NOT EXISTS "ix_articles_title" ON "articles" (
	"title"
);
CREATE INDEX IF NOT EXISTS "ix_articles_request_to_publish" ON "articles" (
	"request_to_publish"
);
CREATE INDEX IF NOT EXISTS "ix_articles_rating" ON "articles" (
	"rating"
);
CREATE INDEX IF NOT EXISTS "ix_articles_last_edit" ON "articles" (
	"last_edit"
);
CREATE INDEX IF NOT EXISTS "ix_articles_is_published" ON "articles" (
	"is_published"
);
CREATE INDEX IF NOT EXISTS "ix_articles_created" ON "articles" (
	"created"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_tags_tmdb_id" ON "tags" (
	"tmdb_id"
);
CREATE INDEX IF NOT EXISTS "ix_articles_publish_date" ON "articles" (
	"publish_date"
);
CREATE INDEX IF NOT EXISTS "ix_tags_id" ON "tags" (
	"id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_tags_name" ON "tags" (
	"name"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_users_username" ON "users" (
	"username"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_users_email" ON "users" (
	"email"
);
CREATE INDEX IF NOT EXISTS "ix_roles_default" ON "roles" (
	"default"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_people_tmdb_id" ON "people" (
	"tmdb_id"
);
CREATE INDEX IF NOT EXISTS "ix_people_name" ON "people" (
	"name"
);
CREATE INDEX IF NOT EXISTS "ix_creative_works_type" ON "creative_works" (
	"type"
);
CREATE UNIQUE INDEX IF NOT EXISTS "ix_creative_works_tmdb_id" ON "creative_works" (
	"tmdb_id"
);
CREATE INDEX IF NOT EXISTS "ix_creative_works_name" ON "creative_works" (
	"name"
);
CREATE INDEX IF NOT EXISTS "ix_article_type_name" ON "article_type" (
	"name"
);
COMMIT;
