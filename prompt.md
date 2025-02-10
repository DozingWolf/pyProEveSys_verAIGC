# Prompt记录
项目中使用到的AI清单，排名不分先后
```
月之暗面 KIMI
字节跳动 Marscode
深度求索 deepseek-v3
qwen2.5-max
```
项目中使用到的工具
```
vscode
    cline插件
cursor
```
## prompt清单
### 后端编写
具体的截图后续会上传，这里提供一份文字版本供大家参考。
**20250110**
1. 你需要扮演一个资深python软件开发工程师。我将逐步叙述我的需求，你不要马上进行代码编写，要等我发出“需求说完了”这个命令后，再根据我所有描述的需求为我编写对应的python代码。
2. 我需要一个http服务，这个http服务有多个restful风格的api接口。这些接口都需要通过认证来进行保护访问的安全性。认证接口希望使用session来实现。请使用flask来实现http服务端的session认证，并编写用于保护接口的装饰器代码。后台的orm请使用sqlalchemy2，数据库请使用sqlite3。
3. 同时，不同用户登录后对api接口有不同的授权，比如A与B用户登录后，A能够访问一部分接口，B却能访问全部接口。此时需要一个权限控制的功能。权限表存储在后台的数据库中，每次普通接口的请求需要先验证人员认证，再进行权限控制。请根据这个需求也写一个权限控制的装饰器。
4. 我需要各个restful api使用flask的blueprint蓝图技术进行管理，版本后追加项目名“prjeventsys”层级。
5. 项目需要使用loguru进行日志记录，日志需要同时在终端和日志文件进行输出。flask的服务端口和debug、数据库的存储路径、日志的level设定请使用配置文件进行。
6. 请同步编写sqlite3数据库中用户表与权限表，权限内容可以先以“api1”、“api2”进行替代。权限需要与api接口相关联，便于与权限控制功能进行配合。
7. 需求说完了
```
AI开始生成
```
8. permissions.py和auth.py这量个文件没有提供，请补充一下
```
AI开始对缺失内容进行补充
```
9.  我尝试运行，有几个问题需要你检查后更正，首先在app/utils/decorators.py文件中，from .models import SessionLocal, Permission语句报错，报错内容“无法解析导入“.models””；其次在这个文件中，user = db.query(User).filter(User.id == user_id).first()语句中的User对象不存在，是否是需要被引用的其他包内的对象？
```
AI开始修正内容
```
10. 第三步3. 更新 __init__.py 文件，这个是哪个目录下的__init__.py？请给我完整的项目下文件路径
11. 在app/api/v1/user_api.py文件中的语句“from ..utils.decorators import login_required, permission_required
from ..models import SessionLocal, User”两句语句报错了，报错内容无法解析导入“..models”，请修改app/api/v1/user_api.py这个文件
```
AI开始修改代码
```
**20250118**

12. 很好，根据以上修改，系统已经成功运行了。接下来我会提出进一步的需求，请接受我的需求，直到我发出“需求说完了”这个指令时，进行新功能编写或对原有代码修改。
13. 现在我要求把配置文件修改为使用通用的conf.ini文件
14. 数据库的用户表不应该存储明文密码，在api接口中传递的报文也不应该使用明文密码。请在数据库侧使用RSA不对称加密，在客户端与服务端的交互中使用AES对称加密。RSA不对称加密的私钥请存储在config.ini文件中。
15. 需求说完了
```
AI开始生成
```
16. 你在app/utils/crypto.py中实现了两种加密方式，但是在app/auth.py中没有如需求要求的实现对AES加密传输的密文密码解密和与RSA存储的密码进行校验这一步，请在auth.py中实现这两个功能，并在app/api/v1路径下生成用户登入系统的接口
```
AI开始生成
```
17. 请修改app/api/v1/user_api.py，这个py文件应该用户编写受到认证和权限保护的业务数据，请模拟一个查询所有User的业务接口，做业务反馈。
```
AI开始修改
```
**20250119**

18. 我学习了一些新知识，发现我们之前的设计存在不安全的地方。我接下来会叙述我对于接口认证加密和密码存储的新需求。请等待我发出“需求说完了”指令后，根据需求内容进行编码。
19. 数据库用户表中存储的密码应该使用加盐加密，每次用户登陆的认证请求应该使用一个校验函数来进行比对而不是直接比对两组密码文字的差异。请修改一下。
20. 考虑安全性，请把前端传输至后端的密码使用RSA2048加密。请实现一个密码服务类，类中包括前面叙述的加盐加密的生成和密码校验功能，以及现在说明的RSA加密与解密功能。
21. 除此之外，请再帮我定义一个自定义错误类，用于处理系统内各种业务错误内容。比如，密码错误、数据值错误等。这个错误需要包含一个错误代码，一个出现错误的模块名，一个字段用于展现出现错误时的入参，一个字段用于展现具体错误内容。错误代码请使用四位数字表示。
22. 请使用Crypto来实现密码服务类，不要使用bcrypt
```
此处AI开始生成，出现了突破关键词的情况
```
23. 请在密码服务类中使用werkzeug.security的generate_password_hash, check_password_hash两个方法
```
AI开始修改
```
24. 请参考我上传的这份表设计更新model和其他需要更新的py文件。这份文件的使用方法为“表设计”sheet中的tablename字段对应后续每一个sheet，通过表设计sheet可以获得表的说明和业务分类，后续的sheet为表字段的具体定义和说明。（此处上传了[表结构文件](doc/表设计.xlsx)）
```
AI开始生成
```
25. 请问当根据表结构修改了model.py后我是否需要更新auth.py和permission.py这两个py文件？
```
AI开始修改
```
26. 根据你编写的代码，我尝试运行后发现了两个问题：问题1，auth.py文件中session["user_id"] = user.empid这一行代码报错显示“未定义“session””；问题2，permission.py文件中user = db.query(User).filter(User.empid == user_id).first()这一行代码报错“未定义“User””。请帮我看一下，是什么原因，并且帮我修正一下代码。
```
AI开始修改代码
```
27. 好的，请帮我检查一下，app/utils/decorators.py文件是否需要对应更新代码？
```
AI开始修改
```
### 根据数据库设计创建接口设计
**20250123**
1. 1.对[表设计.xlsx](doc/表设计.xlsx)“表设计.xlsx”文档的说明如下：表设计sheet中列明了这个系统总共有多少个表，表设计sheet中tablename字段描述某个表的表名；desc字段描述这个表是做什么的；业务分类字段描述这个表属于哪一种类型的定义。每一个tablename都可以在后续的sheet中找到对应的sheet名，这个sheet名就是这个表的详细定义。详细定义sheet中，column字段表示表内部的字段名称；type字段表示数据类型；PK字段表示这个字段是否是主键，如有Y则为主键，为空则是普通字段；default字段表示这个表字段的默认值，其中sysdate标记是oracle数据库中取当前时间的书写方法；desc字段表示这个字段的简要说明。ER sheet中描述了各个表之间的主要关联关系。2.对[接口设计.xlsx](doc/接口设计.xlsx)“接口设计.xlsx”文档的说明如下：接口设计sheet记录了所有的接口清单。其中，业务分类字段表示这个接口属于哪种业务；业务分类代码字段记录这个业务的代码编号；接口名字段记录这个接口的中文名称；接口方法记录这个接口调用时需要使用的方法；说明字段记录这个接口的简要描述和说明；name字段记录这个接口在调用url中的调用名。后续的C、U、R、D几个字段分别代表CURD中的Create、Update、Read、Delete这几个动作。这几个字段中填充的数据是该接口涉及操作的表，表与表之间用半角逗号分开。如果这个接口不涉及某个动作，使用“/”符号进行填充。3.请结合这两个文档，根据接口设计.xlsx文档中接口设计sheet的设计要求设计一套接口，这套接口需要遵循restful api的设计规范。设计中url中使用[your_owner_ip_or_domain]作为请求IP的占位符，使用[set_port]作为请求端口的占位符。接口请求url格式为api/[版本号]/[业务分类代码]/[接口名]。请使用json格式进行入参、出参的设计，入参、出参中需要对每个参数进行说明。每个接口都有的公共参数请在一开始就优先说明。出参与入参的命名，请与表设计中相关字段的命名保持一致。
```
AI开始生成
```
```
我根据AI的反馈逐步补全接口设计文档
```
### 根据接口设计文档要求创建接口代码
**20250207**
**注意，这里我开始使用vscode的插件cline和cursor，使用这两个工具后文件都是可以直接关联的**
1. 请根据 @models.py 中的Company类生成用于创建新公司的接口。接口使用marshmallow进行校验，schema对应的代码存储在 @schemas 中，api存储在 @v1 中，需要通过 @decorators.py 中login_required进行保护。接口需要使用blueprint进行管理，注册在 @__init__.py 中，url_prefix为"/api/v1.0/MST"。
2. 请根据 @models.py 中的Company类生成用于查询公司情况的接口。接口使用marshmallow进行校验，schema对应的代码存储在 @schemas 中，api存储在 @v1 中，需要通过 @decorators.py 中login_required进行保护。允许的查询条件是compcode、compname、compadd、uscicode、createuser、createdate、status。允许些查询条件组合使用。其中createdate创建时间应允许进行时间范围查询，compcode、compname、compadd应允许模糊查询。接口需要使用blueprint进行管理，注册在 @__init__.py 中，url_prefix为"/api/v1.0/MST"。
3. 请根据 @models.py 中的Project类生成用于修改项目信息的接口。接口使用marshmallow进行校验，schema对应的代码存储在 @schemas 中，api存储在 @v1 中，且需要通过 @decorators.py 中login_required进行保护。允许修改的字段为ownerid、sponsorid、desc、goal、expectedtime、status。接口需要使用blueprint进行管理，注册在 @__init__.py 中
**20250210**
4. 请根据 @models.py 中Project类生成用于查询项目概况的接口。接口使用marshmallow进行校验，schema对应的代码存储在 @schemas 中，api存储在 @v1 中，需要通过 @decorators.py 中login_required进行保护。允许的查询条件是prjcode、prjname、ownerid、sponsorid、approvetime、expectedtime、status。允许这些查询条件组合使用。其中prjname允许模糊查询，approvetime、expectedtime应允许进行事件范围查询。接口需要使用blueprint进行管理，注册在 @__init__.py 中。
5. 请根据 @models.py 中的Event类生成用于修改事件信息的接口。接口使用marshmallow进行校验，schema对应的代码存储在 @schemas 中，api存储在 @v1 中，且需要通过 @decorators.py 中login_required进行保护。允许修改的字段为event、status。modifyuser使用session中当前用户信息进行填充，modifytime使用当前时间进行填充。 接口使用blueprint进行管理，注册在 @__init__.py 中。
6. 请根据 @models.py 中的Event类生成用于查询事件信息的接口。接口使用marshmallow进行校验，schema对应的代码存储在 @schemas 中，api存储在 @v1 中，且需要通过 @decorators.py 中login_required进行保护。允许的查询条件是reporter、reportertime、status，允许这些查询条件组合使用。其中reportertime允许进行时间范围查询。接口需要使用blueprint进行管理。reportertime的结束时间若前端未传值请使用当前时间作为结束时间进行查询。
7. 根据 @models.py 中ProjectMember类，创建一个新增项目成员接口。接口使用marshmallow进行校验，schema对应的代码存储在 @schemas 中，api存储在 @v1 中，需要通过 @decorators.py 中login_required进行保护。新增成员执行前请校验prjid和empid是否存在，如不存在要求报错。createuser使用session中当前用户进行填充，createdate使用当前时间进行填充。
8. 根据 @models.py 中ProjectMember类，创建一个移除或停用项目成员接口。接口使用marshmallow进行校验，schema对应的代码存储在 @schemas 中，api存储在 @v1 中，需要通过 @decorators.py 中login_required进行保护。使用更新项目成员status的方法进行逻辑删除，并需要使用operation_log装饰器进行日志的记录。接口需要使用blueprint进行管理。http方法应该是POST，不要使用DELETE方法。
9.  根据remove_project_member新增的逻辑，add_project_member需要做一些修改，insert数据前需要判断人员是否已存在，如果人员曾经加入过项目，后续移除，最后又需要加入项目，此时add_project_member中应该将项目下人员状态置为0。请修改一下这段业务逻辑。
10. 根据 @models.py 中ProjectMember类、Project类、User类，创建一个查询项目参与者的接口。这三个类之间的关系为，ProjectMember.prjid = Project.prjid，关系是n:1；ProjectMember.empid = User.empid，关系是n:1。一个人员可以参与多个项目，一个项目中有多位不重复的人员。允许的查询条件是User.empcode、User.empname、Project.prjcode、Project.prjname，允许这些查询条件组合使用。接口使用marshmallow进行校验，schema对应的代码存储在 @schemas 中，api存储在 @v1 中，且需要通过 @decorators.py 中login_required进行保护。接口需要使用blueprint进行管理。
11. 根据 @models.py 中Project类、Event类、ProjectEvent类生成一个将事件增加至项目的接口。这三个类之间的关联关系为ProjectEvent.prjid = Project.prjid、ProjectEvent.eventid = Event.eventid。ProjectEvent.leafid为主键，ProjectEvent.parentid为用户选择的与上级事件的ProjectEvent.leafid，ProjectEvent.depth为用户选择的上级事件的depth+1。ProjectEvent.depth默认为0。用户输入信息为：prjid、eventid、parentid。接口使用marshmallow进行校验，schema对应的代码存储在 @schemas 中，api存储在 @v1 中，需要通过 @decorators.py 中login_required进行保护，通过operation_log装饰器进行日志的记录。接口需要使用blueprint进行管理。

## 从AI处学习到的知识
1. @company_api.py 在这个文件中，你编写的create_company、edit_company函数都没有使用use_kwargs这个装饰器，但是query_companies函数却使用了use_kwargs这个装饰器，请帮我解释一下这是什么原因？那种方式更好？

``` 
这是一个很好的问题。这两种方式都是处理请求参数的常见方法，它们各有优缺点，我来详细解释一下：

1. **不使用use_kwargs（create_company和edit_company的方式）**：
   - 手动调用schema.load()来验证和加载数据
   - 优点：
     * 更直观，代码流程清晰可见
     * 可以更灵活地处理异常情况
     * 可以在验证前后添加自定义逻辑
   - 缺点：
     * 代码量稍多
     * 需要手动处理验证错误

2. **使用use_kwargs（query_companies的方式）**：
   - 自动处理请求参数的验证和加载
   - 优点：
     * 代码更简洁
     * 自动处理验证错误，返回400响应
     * 参数直接作为函数参数传入，使用更方便
   - 缺点：
     * 对参数处理的控制较弱
     * 需要额外导入webargs库

**哪种方式更好？**

这取决于具体场景：
- 对于简单的查询接口（如query_companies），使用use_kwargs更合适，因为它：
  * 代码更简洁
  * 自动处理验证错误
  * 参数直接作为函数参数传入，使用更方便

- 对于创建/修改接口（如create_company和edit_company），手动验证可能更好，因为：
  * 通常需要更复杂的业务逻辑
  * 可能需要处理额外的上下文信息（如session中的用户ID）
  * 需要更灵活的错误处理

**建议的统一方案：**


python:app/api/v1/company_api.py
# 对于查询类接口
@company_bp.route("/query_companies", methods=["POST"])
@login_required
@use_kwargs(CompanyQuerySchema)
def query_companies(**kwargs):
    # 直接使用kwargs中的已验证参数
    pass

# 对于创建/修改类接口
@company_bp.route("/create_company", methods=["POST"])
@login_required
def create_company():
    try:
        data = request.json
        validated_data = CompanyCreateSchema().load(data)
        # 手动处理业务逻辑
    except ValidationError as e:
        return jsonify({"error": "参数验证失败", "details": e.messages}), 400

这种混合使用的方式可以兼顾代码简洁性和灵活性，是当前比较推荐的做法。
```