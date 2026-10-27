# user_restful_api

一个基于 **Flask + Flask-RESTful + MySQL** 的通用用户管理后台 RESTful API，提供用户、部门、角色、权限、用户组的完整管理能力，使用 JWT 进行认证。

---

## 1. 需求背景

企业内部应用普遍需要一套统一的组织与账号体系，本项目的目标是提供一套**通用、可复用**的用户管理 API，供各个业务系统接入，避免每个系统重复开发账号/权限功能。

### 1.1 功能需求

| 模块   | 功能点                                                       |
| ------ | ------------------------------------------------------------ |
| 登录   | 账号密码登录，签发 JWT Token；支持超级管理员标识              |
| 用户   | 用户列表（分页/搜索）、新建、修改、删除、修改密码、重置密码、修改基本信息 |
| 部门   | 部门树（支持父子层级）增删改查、部门成员管理                  |
| 角色   | 角色增删改查、给角色分配权限                                  |
| 权限   | 权限节点查询                                                  |
| 用户组 | 用户组增删改查、组成员管理、用户组与角色绑定                  |
| 通用   | 接口版本控制、统一响应格式与错误码、操作日志、JSON / XML 双格式支持 |

### 1.2 非功能需求

- 认证：无状态 JWT Token，不依赖 Session
- 权限：区分普通用户与超级管理员（user_key == 1）
- 数据库：使用连接池，避免频繁建连
- 可观测：按模块记录运行日志与操作日志
- 兼容：支持 JSON 与 XML 两种数据交换格式

---

## 2. 系统设计

### 2.1 总体架构（分层设计）

```
客户端请求
    │
    ▼
┌─────────────────┐
│  api/  接口层    │  ← 路由注册、参数校验、鉴权装饰器、组织响应
├─────────────────┤
│ common/ 通用层   │  ← 请求/响应统一处理、错误码、枚举、日志
├─────────────────┤
│ core/  核心层    │  ← 业务封装（Singleton 类，隔离接口层与数据层）
├─────────────────┤
│ db/  数据访问层  │  ← 各模块 DB Manager，纯 SQL 操作
├─────────────────┤
│ MySQL（连接池）  │  ← DBUtils PooledDB + PyMySQL
└─────────────────┘
```

调用链路：`api（接口层）→ core（业务层）→ db（数据层）`，接口层不直接操作数据库。

### 2.2 认证设计（JWT）

- 登录接口校验用户名密码后签发 JWT（HS256，密钥为 `config.py` 中的 `SECRET_KEY`），payload 中携带 `user_key` 与登录时间
- Token 有效期控制见 `utils/auth_helper.py`（当前取消了对 exp 的强制校验，可按需打开）
- 请求头携带 Token，`Auth.identify()` 解析并还原用户身份，写入 Flask 的 `g.user_key`
- 两个鉴权装饰器位于 `common/common_login_helper.py`：
  - `@login_required`：校验 Token，未通过返回 401
  - `@login_super`：只允许超级管理员（g.user_key == 1），未通过返回 403

### 2.3 接口版本控制

- URL 中显式携带版本：`/li-boss/<version>/...`
- 通过 `@api_version` 装饰器统一校验版本合法性，合法版本在 `common/common_api_version.py` 中以枚举定义（当前支持 `v1`、`v2`）
- 新增版本只需扩展枚举，接口实现保持兼容

### 2.4 统一请求/响应设计

- 请求参数经 `common/common_request_process.py` 统一解析：默认 JSON；URL 加 `?format=xml` 时自动将 XML 请求体转换为 JSON，并按 `common/common_model_enum.py` 中定义的 root/body 标签结构取参
- 响应由 `response_result_process` 统一包装输出，自动支持 JSON/XML 两种格式
- 错误码集中在 `common/common_response_code.py` / `utils/status_code.py`，见下文错误码表

### 2.5 日志设计

- `utils/log_helper.py` 初始化日志框架并输出到 `var/log/user_api.log`
- 业务侧通过 `@operation_log`（`common/common_log.py`）记录操作日志

### 2.6 数据模型

数据库初始化脚本：`dbsql/user_api.sql`，核心表：

| 表                      | 说明                     |
| ----------------------- | ------------------------ |
| `department`            | 部门表（P_ID 构成树形结构、自增主键、外键自引用） |
| `db_user` / 用户相关表  | 用户账号信息             |
| `role`                  | 角色表                   |
| `permission`            | 权限节点表               |
| 用户组相关表            | 用户组、组成员、组角色   |

> 初始化后内置超级管理员账号：`super` / `123456`

---

## 3. 技术实现

### 3.1 技术栈

| 组件           | 版本   | 用途                     |
| -------------- | ------ | ------------------------ |
| Flask          | 1.1.1  | Web 框架                 |
| Flask-RESTful  | 0.3.7  | RESTful 接口组织         |
| Flask-Cors     | 3.0.8  | 跨域支持                 |
| PyJWT          | 1.4.2  | Token 签发与校验         |
| PyMySQL        | 0.9.3  | MySQL 驱动               |
| DBUtils        | 1.3    | 数据库连接池（PooledDB） |
| xmltodict      | 0.12.0 | XML / JSON 互转          |

### 3.2 关键机制实现

- **连接池**：`db/connection_pool.py` 中 `MysqlConn` 使用 DBUtils `PooledDB`（mincached=1, maxcached=10, maxconnections=100），配置来自 `config.ini` 的 `[DB]` 段，默认返回 `DictCursor`
- **配置读取**：`config.py` 的 `Configuration` 类封装 `configparser` 读取 `config.ini`；SQLAlchemy 风格的环境配置类（development/testing/production/default）控制 `DEBUG` 与 `SECRET_KEY`，`start.py` 通过环境变量 `FLASK_CONFIG` 选择，默认 `default`
- **参数校验**：`requestProcess` 提供 must 字段校验、参数类型校验，校验失败返回对应错误码
- **应用工厂**：`api/__init__.py` 的 `create_app()` 完成 CORS、配置加载、日志初始化、路由注册

### 3.3 路由注册

统一在 `api/resource.py` 中注册，路由前缀 `/li-boss/<version>/`：

| 模块     | 路径                                                           | 支持的方法          |
| -------- | -------------------------------------------------------------- | ------------------- |
| 登录     | `/li-boss/<version>/login`                                     | POST                |
| 部门     | `/li-boss/<version>/department`、`.../<dpt_id>`                | GET / POST / PUT / DELETE |
| 部门成员 | `/li-boss/<version>/department/staff/<dpt_id>`                 | GET / POST / DELETE |
| 用户     | `/li-boss/<version>/user`、`.../<user_id>`                     | GET / POST / PUT / DELETE |
| 密码     | `/li-boss/<version>/user/<user_id>/password`                   | POST / PUT          |
| 基本信息 | `/li-boss/<version>/user/<user_id>/base/info`                  | PUT                 |
| 角色     | `/li-boss/<version>/role`、`.../<role_id>`                     | GET / POST / PUT / DELETE |
| 角色权限 | `/li-boss/<version>/role/<role_id>/permission`                 | GET / POST          |
| 权限     | `/li-boss/<version>/permission`                                | GET                 |
| 用户组   | `/li-boss/<version>/user/group`、`.../<group_id>`              | GET / POST / PUT / DELETE |
| 组成员   | `/li-boss/<version>/user/group/<group_id>/staff`               | GET / POST / DELETE |
| 组角色   | `/li-boss/<version>/user/group/<group_id>/role`                | GET / POST / DELETE |

### 3.4 统一响应格式

```json
{ "code": 200, "msg": "操作成功", "data": {} }
```

常见错误码（完整见 `common/common_response_code.py`）：

| code | 含义             |
| ---- | ---------------- |
| 200  | 请求成功         |
| 400  | 请求参数错误     |
| 403  | 无权限           |
| 404  | 资源不存在       |
| 1001 | 用户名或密码错误 |
| 1005 | 登录失败         |
| 1007 | 用户不存在       |
| 1010 | 记录已存在       |
| 1018 | 请求参数缺失     |
| 1019 | 请求参数格式错误 |

---

## 4. 项目结构

```
user_restful_api
├── start.py                    # 启动入口
├── config.ini                  # 运行配置（服务端口、数据库连接）
├── config.py                   # 配置读取类 Configuration + Flask 环境配置
├── requirements.txt            # 依赖清单
├── dbsql/user_api.sql          # 数据库初始化脚本
│
├── api/                        # 接口层
│   ├── resource.py             # 路由注册（add_resource）
│   ├── login/                  # 登录接口
│   ├── user/                   # 用户 / 密码 / 基本信息
│   ├── department/             # 部门 / 部门成员
│   ├── role/                   # 角色 / 角色权限 / 权限
│   └── user_group/             # 用户组 / 组成员 / 组角色
│
├── common/                     # 通用处理层
│   ├── common_api_version.py   # API 版本枚举
│   ├── common_log.py           # 操作日志装饰器
│   ├── common_login_helper.py  # login_required / login_super 装饰器
│   ├── common_model_enum.py    # 各模块 XML root/body 结构枚举
│   ├── common_request_process.py   # 请求解析与参数校验
│   ├── common_response_code.py # 错误码定义
│   ├── common_response_log.py  # 响应日志
│   └── common_response_process.py  # 统一响应输出
│
├── core/                       # 核心业务层（Singleton 模式）
│   ├── user_singleton.py
│   ├── department_singleton.py
│   ├── role_permission_singleton.py
│   └── user_group_singleton.py
│
├── db/                         # 数据访问层
│   ├── connection_pool.py      # DBUtils 连接池
│   ├── base.py                 # 游标封装
│   ├── logger/db_log_mgr.py    # 日志表访问
│   ├── user/db_user_mgr.py     # 用户表访问
│   ├── department/db_department_mgr.py
│   ├── role/db_role_permission_mgr.py
│   └── user_group/db_group_mgr.py
│
├── utils/                      # 工具层
│   ├── auth_helper.py          # JWT 签发 / 校验 / 用户认证
│   ├── api_version_verify.py   # api_version 装饰器
│   ├── log_helper.py           # 日志初始化
│   ├── status_code.py          # 响应码
│   ├── xml_json_process.py     # XML/JSON 转换
│   └── fun_name_to_enum.py     # 函数名转枚举工具
│
└── var/log/                    # 日志输出目录
```

---

## 5. 快速开始（本地开发）

### 5.1 环境要求

- Python 3.5+（建议 3.6 ~ 3.7，依赖版本较老）
- MySQL 5.7+

### 5.2 初始化数据库

将 `dbsql/user_api.sql` 导入 MySQL（默认库名 `user_api`）：

```bash
mysql -uroot -p < dbsql/user_api.sql
```

内置超级管理员：用户名 `super`，密码 `123456`。

### 5.3 修改配置

编辑 `config.ini`：

```ini
# 服务启动配置
[IPCONFIG]
host = 0.0.0.0
port = 8099
debug = True

# 数据库配置
[DB]
type = mysql
user = root
pwd = 123456
host = 127.0.0.1
port = 3306
name = user_api
```

### 5.4 安装依赖并启动

```bash
pip install -r requirements.txt
python start.py
```

服务运行在 `http://127.0.0.1:8099`，可先测试登录：

```bash
curl -X POST http://127.0.0.1:8099/li-boss/v1/login \
  -H "Content-Type: application/json" \
  -d '{"login_name": "super", "login_password": "123456"}'
```

---

## 6. 开发注意事项

### 6.1 新增接口的标准流程

1. 在 `api/<模块>/` 下实现 `Resource` 类，其 `get/post/put/delete` 方法需挂 `@api_version` 装饰器
2. 请求参数用 `req.request_process(request, xml, modelEnum.<模块>.value)` 解析，再用 `req.verify_all_param_must` 做必填校验
3. 数据持久化一律通过对应模块的 db manager（必要时经 core Single 类），不要在接口层写 SQL
4. 路由最后在 `api/resource.py` 中 `api.add_resource(...)` 注册
5. 响应必须用 `response_result_process(data, xml=xml)` 统一格式输出

### 6.2 鉴权

- 需要登录才能访问的接口加 `@login_required`；仅超管可操作的加 `@login_super`
- 当前业务用户身份从 `g.user_key` 获取
- Token 密钥 `SECRET_KEY` 写在 `config.py` 的 `Config` 类中，生产环境务必修改，且不要提交到代码库

### 6.3 一般注意点

- **编码**：所有源码使用 UTF-8；`app.config['JSON_AS_ASCII'] = False` 保证中文正常输出
- **跨域**：已在 `create_app` 中全局开启 CORS（`supports_credentials=True`）
- **请求只接受 JSON 对象**：请求体为 JSON 数组会被判定为格式错误；XML 格式需按 `common_model_enum` 中定义的 root/body 结构组织
- **错误码**：所有 `response_code` 属性均为 `@property` 取值方式（`response_code.SUCCESS` 即可），不要用 callable 调用
- **新增版本**：在 `common/common_api_version.py` 的枚举中登记，否则 `@api_version` 会拦截请求
- **数据库**：使用连接池后，请求结束记得调用 `MysqlConn` 的 `close()` 释放连接；新增 SQL 注意消除 SQL 注入（使用占位符）
- **配置文件**：`Configuration.set_option` 会直接写回 `config.ini`，注意并发场景与文件备份
- **依赖版本较老**（Flask 1.1.1 / PyJWT 1.4.2 等）：请勿随意升级依赖，Python 3.8+ 环境可能出现兼容性问题，需实测

---

## 7. 部署

### 7.1 部署前检查

- `config.ini` 中数据库改为生产库信息，`debug = False`（关闭调试模式）
- `config.py` 中 `SECRET_KEY` 修改为随机强密钥
- 生产日志目录 `var/log/` 可写
- 数据库允许应用所在机器远程访问

### 7.2 Linux（gunicorn）

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:8099 start:app
```

> 注意：`start.py` 中的 `app.run()` 仅在直接执行时生效，gunicorn 引入 `start:app` 不走 `__main__`，是安全的。

### 7.3 Windows（waitress）

```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=8099 start:app
```

### 7.4 反向代理（Nginx 示例）

```nginx
location / {
    proxy_pass http://127.0.0.1:8099;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

### 7.5 进程托管

建议用 systemd（Linux）或 NSSM/任务计划（Windows）守护进程，示例 systemd 单元：

```ini
[Unit]
Description=user api service
After=network.target mysql.service

[Service]
WorkingDirectory=/opt/user_restful_api
ExecStart=/opt/user_restful_api/venv/bin/gunicorn -w 2 -b 0.0.0.0:8099 start:app
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 8. 接口示例

```bash
# 1. 登录
curl -X POST "http://127.0.0.1:8099/li-boss/v1/login" \
  -H "Content-Type: application/json" \
  -d '{"login_name":"super","login_password":"123456"}'

# 2. 查询用户列表（携带 Token）
curl "http://127.0.0.1:8099/li-boss/v1/user" \
  -H "Authorization: <token>"

# 3. XML 格式请求（url 加 format 参数，body 用 XML 结构）
curl -X POST "http://127.0.0.1:8099/li-boss/v1/login?format=xml" \
  -H "Content-Type: application/xml" \
  -d "<root><login><login_name>super</login_name><login_password>123456</login_password></login></root>"
```

> Token 具体传递方式以 `utils/auth_helper.py` 的 `Auth.identify()` 实现为准。
