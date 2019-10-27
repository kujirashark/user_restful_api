/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : user_api

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 27/10/2019 17:05:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for department
-- ----------------------------
DROP TABLE IF EXISTS `department`;
CREATE TABLE `department` (
  `DPT_ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `DPT_NAME` varchar(64) DEFAULT NULL COMMENT '部门名称',
  `SORT` int(11) DEFAULT NULL COMMENT '排序',
  `P_ID` int(11) DEFAULT '0' COMMENT '父ID',
  PRIMARY KEY (`DPT_ID`) USING BTREE,
  KEY `p_id` (`P_ID`) USING BTREE,
  CONSTRAINT `department_ibfk_1` FOREIGN KEY (`P_ID`) REFERENCES `department` (`DPT_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of department
-- ----------------------------
BEGIN;
INSERT INTO `department` VALUES (1, 'XXX有限公司', 1, NULL);
COMMIT;

-- ----------------------------
-- Table structure for inform_message
-- ----------------------------
DROP TABLE IF EXISTS `inform_message`;
CREATE TABLE `inform_message` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TITLE` varchar(128) DEFAULT NULL COMMENT '标题',
  `CREATE_TIME` double DEFAULT NULL COMMENT '创建时间',
  `STATE` int(11) DEFAULT NULL COMMENT '消息状态 0:未读;1:已读',
  `CONTENT` varchar(256) DEFAULT NULL COMMENT '描述信息',
  `TASK_GROUPS` varchar(64) DEFAULT NULL,
  `CREATOR` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `NAME` varchar(128) DEFAULT '' COMMENT '菜单名称',
  `URL` varchar(128) DEFAULT '' COMMENT 'URL',
  `ICON` varchar(128) DEFAULT '' COMMENT '菜单图标',
  `SORT` varchar(11) DEFAULT '' COMMENT '排序',
  `P_ID` int(11) DEFAULT NULL COMMENT '父ID',
  `IS_ROUTER` int(11) DEFAULT NULL COMMENT '是否有路由',
  `ROUTER_PARENT` varchar(128) DEFAULT '' COMMENT '父路由',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for operation
-- ----------------------------
DROP TABLE IF EXISTS `operation`;
CREATE TABLE `operation` (
  `OPER_ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `OPER_TITLE` varchar(255) DEFAULT NULL,
  `OPER_NAME` varchar(128) DEFAULT NULL COMMENT '操作名称',
  `URL` varchar(128) DEFAULT NULL COMMENT 'URL',
  `URLI` varchar(128) DEFAULT NULL COMMENT '类型',
  `SORT` int(11) DEFAULT NULL COMMENT '排序',
  `PARENT_ID` int(11) DEFAULT NULL COMMENT '父ID',
  PRIMARY KEY (`OPER_ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for operation_permission
-- ----------------------------
DROP TABLE IF EXISTS `operation_permission`;
CREATE TABLE `operation_permission` (
  `OPER_ID` int(11) NOT NULL,
  `PERMISSION_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`OPER_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for permission
-- ----------------------------
DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `NAME` varchar(128) DEFAULT NULL COMMENT '权限名称',
  `CREATE_TIME` double DEFAULT NULL COMMENT '创建时间',
  `P_ID` int(11) DEFAULT NULL COMMENT '权限父ID',
  `PERMISSION_TYPE` tinyint(1) DEFAULT '0' COMMENT '权限类型\r\n0:代表普通权限;1:代表数据权限,3,代表grafana权限',
  `GRAFANA_ID` int(11) NOT NULL DEFAULT '0' COMMENT '特殊给grafana权限使用的',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for permission_menu
-- ----------------------------
DROP TABLE IF EXISTS `permission_menu`;
CREATE TABLE `permission_menu` (
  `PERMISSION_ID` int(11) DEFAULT NULL COMMENT '权限ID',
  `MEUN_ID` int(11) DEFAULT NULL COMMENT '菜单ID',
  KEY `permission_id` (`PERMISSION_ID`) USING BTREE,
  KEY `meun_id` (`MEUN_ID`) USING BTREE,
  CONSTRAINT `permission_menu_ibfk_1` FOREIGN KEY (`PERMISSION_ID`) REFERENCES `permission` (`ID`),
  CONSTRAINT `permission_menu_ibfk_2` FOREIGN KEY (`MEUN_ID`) REFERENCES `menu` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `NAME` varchar(64) DEFAULT NULL COMMENT '角色名称',
  `CREATE_TIME` double DEFAULT NULL COMMENT '创建时间',
  `NOTE_INFO` varchar(128) DEFAULT NULL COMMENT '备注信息',
  `TIME_MODIFY` double DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of role
-- ----------------------------
BEGIN;
INSERT INTO `role` VALUES (1, '管理员', 1558316800672, '这是管理员', 1571122452484);
COMMIT;

-- ----------------------------
-- Table structure for roles_permission
-- ----------------------------
DROP TABLE IF EXISTS `roles_permission`;
CREATE TABLE `roles_permission` (
  `PERMISSION_ID` int(11) DEFAULT NULL COMMENT '权限ID',
  `ROLE_ID` int(11) DEFAULT NULL COMMENT '角色ID',
  KEY `permission_id` (`PERMISSION_ID`) USING BTREE,
  KEY `role_id` (`ROLE_ID`) USING BTREE,
  CONSTRAINT `roles_permission_ibfk_1` FOREIGN KEY (`PERMISSION_ID`) REFERENCES `permission` (`ID`),
  CONSTRAINT `roles_permission_ibfk_2` FOREIGN KEY (`ROLE_ID`) REFERENCES `role` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for system_log
-- ----------------------------
DROP TABLE IF EXISTS `system_log`;
CREATE TABLE `system_log` (
  `LOG_KEY` int(11) NOT NULL AUTO_INCREMENT COMMENT '操作日志ID',
  `TITLE` varchar(255) DEFAULT NULL COMMENT '标题',
  `SOURCE` varchar(255) DEFAULT NULL COMMENT '源',
  `IP_ADDRESS` varchar(255) DEFAULT NULL COMMENT 'IP地址',
  `LEVEL` int(8) DEFAULT NULL COMMENT '级别\r\n0：INFO\r\n1：ERROR\r\n2：ALERT\r\n3：FATAL\r\n\r\n',
  `STATUS` int(8) DEFAULT NULL COMMENT '处理状态 0：未处理，1：处理中  2：已处理',
  `OPINION` varchar(2048) DEFAULT NULL COMMENT '处理意见',
  `OPINION_USER` varchar(255) DEFAULT NULL COMMENT '处理人',
  `OPINION_TIME` double DEFAULT NULL COMMENT '处理时间',
  `TIME_CREATE` double DEFAULT NULL COMMENT '时间',
  `DESCRIPTION` varchar(2048) DEFAULT NULL COMMENT '描述信息',
  PRIMARY KEY (`LOG_KEY`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for system_oper_log
-- ----------------------------
DROP TABLE IF EXISTS `system_oper_log`;
CREATE TABLE `system_oper_log` (
  `LOG_KEY` int(11) NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `USER_KEY` int(11) DEFAULT NULL COMMENT '用户ID',
  `IP_ADDRESS` varchar(15) DEFAULT NULL COMMENT 'IP地址',
  `LEVEL` int(11) NOT NULL COMMENT '日志级别\r\n0：INFO\r\n1：ERROR\r\n2：ALERT\r\n3：FATAL\r\n',
  `TIME_CREATE` double DEFAULT NULL COMMENT '创建时间',
  `DESCRIPTION` varchar(640) DEFAULT NULL COMMENT '描述',
  PRIMARY KEY (`LOG_KEY`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for user_group
-- ----------------------------
DROP TABLE IF EXISTS `user_group`;
CREATE TABLE `user_group` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `NAME` varchar(64) DEFAULT NULL COMMENT '用户组名称',
  `DESCRIPTION` varchar(128) DEFAULT NULL COMMENT '用户组描述',
  `CREATE_TIME` double DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for user_group_role
-- ----------------------------
DROP TABLE IF EXISTS `user_group_role`;
CREATE TABLE `user_group_role` (
  `GROUP_ID` int(11) DEFAULT NULL COMMENT '用户组ID',
  `ROLE_ID` int(11) DEFAULT NULL COMMENT '角色ID',
  KEY `group_id` (`GROUP_ID`) USING BTREE,
  KEY `role_id` (`ROLE_ID`) USING BTREE,
  CONSTRAINT `user_group_role_ibfk_1` FOREIGN KEY (`GROUP_ID`) REFERENCES `user_group` (`ID`),
  CONSTRAINT `user_group_role_ibfk_2` FOREIGN KEY (`ROLE_ID`) REFERENCES `role` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for user_roles
-- ----------------------------
DROP TABLE IF EXISTS `user_roles`;
CREATE TABLE `user_roles` (
  `USER_ID` int(11) DEFAULT NULL COMMENT '用户ID',
  `ROLE_ID` int(11) DEFAULT NULL COMMENT '角色ID',
  KEY `user_id` (`USER_ID`) USING BTREE,
  KEY `role_id` (`ROLE_ID`) USING BTREE,
  CONSTRAINT `user_roles_ibfk_1` FOREIGN KEY (`USER_ID`) REFERENCES `users` (`ID`),
  CONSTRAINT `user_roles_ibfk_2` FOREIGN KEY (`ROLE_ID`) REFERENCES `role` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for user_user_group
-- ----------------------------
DROP TABLE IF EXISTS `user_user_group`;
CREATE TABLE `user_user_group` (
  `USER_ID` int(11) DEFAULT NULL COMMENT '用户ID',
  `GROUP_ID` int(11) DEFAULT NULL COMMENT '用户组ID',
  KEY `user_id` (`USER_ID`) USING BTREE,
  KEY `group_id` (`GROUP_ID`) USING BTREE,
  CONSTRAINT `user_user_group_ibfk_1` FOREIGN KEY (`USER_ID`) REFERENCES `users` (`ID`),
  CONSTRAINT `user_user_group_ibfk_2` FOREIGN KEY (`GROUP_ID`) REFERENCES `user_group` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `USER_NAME` varchar(128) DEFAULT NULL COMMENT '账号',
  `USER_SEX` varchar(10) DEFAULT NULL COMMENT '性别',
  `EMAIL` varchar(64) DEFAULT NULL COMMENT '邮箱',
  `PASS_WORD` varchar(256) DEFAULT NULL COMMENT '密码',
  `PHONE` varchar(64) DEFAULT NULL COMMENT '电话',
  `POSITION` varchar(64) DEFAULT NULL COMMENT '职位',
  `CREATE_TIME` double DEFAULT NULL COMMENT '创建时间',
  `NOTE_INFO` varchar(128) DEFAULT NULL COMMENT '备注信息',
  `LOGIN_NAME` varchar(128) DEFAULT NULL COMMENT '姓名',
  `ICON` varchar(255) DEFAULT NULL COMMENT '头像',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES (1, 'super', '1', '124@123.com', 'pbkdf2:sha256:150000$wU6AvaKT$b84ca435628dadf615f4383e0c3c75c23aaa9dc6ba958378061f9a753968e8c0', '13212341222', '超级管理员', 1556523116000, '', '超级管理员', '');
COMMIT;

-- ----------------------------
-- Table structure for users_department
-- ----------------------------
DROP TABLE IF EXISTS `users_department`;
CREATE TABLE `users_department` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `USER_ID` int(11) NOT NULL COMMENT '用户ID',
  `DPT_ID` int(11) NOT NULL COMMENT '部门ID',
  PRIMARY KEY (`ID`) USING BTREE,
  KEY `user_id` (`USER_ID`) USING BTREE,
  KEY `dpt_id` (`DPT_ID`) USING BTREE,
  CONSTRAINT `users_department_ibfk_1` FOREIGN KEY (`USER_ID`) REFERENCES `users` (`ID`),
  CONSTRAINT `users_department_ibfk_2` FOREIGN KEY (`DPT_ID`) REFERENCES `department` (`DPT_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=898 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
