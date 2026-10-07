SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


/*The table structure for grades */
DROP TABLE IF EXISTS grades;
CREATE TABLE grades (
  sno varchar(15) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  math int(5) NULL DEFAULT NULL,
  english int(5) NULL DEFAULT NULL,
  python int(5) NULL DEFAULT NULL,
  INDEX sno(sno) USING BTREE,
  CONSTRAINT grades_ibfk_1 FOREIGN KEY (sno) REFERENCES students(sno) 
  ON DELETE RESTRICT ON UPDATE RESTRICT) 
 ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;


/* The records of six students' grades */
INSERT INTO grades VALUES ('002020', 90, 91, 87);
INSERT INTO grades VALUES ('002021', 86, 69, 82);
INSERT INTO grades VALUES ('002022', 88, 82, 80);
INSERT INTO grades VALUES ('002023', 70, 76, 93);
INSERT INTO grades VALUES ('002024', 78, 86, 73);
INSERT INTO grades VALUES ('002025', 90, 73, 97);

/* The table structure for students */
DROP TABLE IF EXISTS students;
CREATE TABLE students (
   sno varchar(15) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
   sname varchar(80) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
   sex varchar(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
   birthday date NULL DEFAULT NULL,
   PRIMARY KEY (sno) USING BTREE) 
 ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;


/* The records of six students */
INSERT INTO students VALUES ('002020', 'LiGangren', 'male', '2003-12-26');
INSERT INTO students VALUES ('002021', 'YuDabao', 'female', '2004-09-03');
INSERT INTO students VALUES ('002022', 'Mark', 'male', '2005-03-27');
INSERT INTO students VALUES ('002023', 'ZhenZheng', 'male', '2002-04-18');
INSERT INTO students VALUES ('002024', 'LiXuexi', 'female', '2005-08-09');
INSERT INTO students VALUES ('002025', 'SunKe', 'male', '2004-08-30');

SET FOREIGN_KEY_CHECKS = 1;

