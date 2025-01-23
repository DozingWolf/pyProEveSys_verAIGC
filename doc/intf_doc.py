import pandas as pd

# 定义所有接口数据
interfaces = {
    # 查询接口（支持分页和多条件查询）
    "QueryUser": {
        "接口用途说明": "查询用户信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/QueryUser",
        "方法": "GET",
        "入参": {
            "empcode": "0001",
            "empname": "John",
            "sex": 1,
            "mobile": "1234567890",
            "status": 0,
            "admin": 1,
            "page": 1,
            "pageSize": 10
        },
        "出参": {
            "code": 2000,
            "msg": "success",
            "data": [
                {
                    "empid": 1,
                    "empcode": "0001",
                    "empname": "John Doe",
                    "sex": 1,
                    "mobile": "1234567890",
                    "weticket": "wechat_ticket",
                    "status": 0,
                    "admin": 1
                }
            ],
            "pagination": {
                "page": 1,
                "pageSize": 10,
                "total": 100
            }
        }
    },
    "QueryDepartment": {
        "接口用途说明": "查询部门信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/QueryDepartment",
        "方法": "GET",
        "入参": {
            "deptcode": "D001",
            "deptname": "HR",
            "status": 0,
            "page": 1,
            "pageSize": 10
        },
        "出参": {
            "code": 2000,
            "msg": "success",
            "data": [
                {
                    "deptid": 1,
                    "deptcode": "D001",
                    "deptname": "HR Department",
                    "deptlocation": "New York",
                    "status": 0
                }
            ],
            "pagination": {
                "page": 1,
                "pageSize": 10,
                "total": 100
            }
        }
    },
    "QueryCompany": {
        "接口用途说明": "查询公司信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/QueryCompany",
        "方法": "GET",
        "入参": {
            "compcode": "C001",
            "compname": "Tech",
            "status": 0,
            "page": 1,
            "pageSize": 10
        },
        "出参": {
            "code": 2000,
            "msg": "success",
            "data": [
                {
                    "compid": 1,
                    "compcode": "C001",
                    "compname": "Tech Corp",
                    "compadd": "Silicon Valley",
                    "uscicode": "123456789",
                    "status": 0
                }
            ],
            "pagination": {
                "page": 1,
                "pageSize": 10,
                "total": 100
            }
        }
    },
    "QueryMenu": {
        "接口用途说明": "查询菜单信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/QueryMenu",
        "方法": "GET",
        "入参": {
            "menucode": "M001",
            "mununame": "Dashboard",
            "status": 0,
            "page": 1,
            "pageSize": 10
        },
        "出参": {
            "code": 2000,
            "msg": "success",
            "data": [
                {
                    "menuid": 1,
                    "menucode": "M001",
                    "mununame": "Dashboard",
                    "subject": "MST",
                    "level": 1,
                    "sortid": 1,
                    "status": 0
                }
            ],
            "pagination": {
                "page": 1,
                "pageSize": 10,
                "total": 100
            }
        }
    },
    "QueryPermissionGroup": {
        "接口用途说明": "查询权限组信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/AUT/QueryPermissionGroup",
        "方法": "GET",
        "入参": {
            "pgroupcode": "PG001",
            "pgroupname": "Admin",
            "status": 0,
            "page": 1,
            "pageSize": 10
        },
        "出参": {
            "code": 2000,
            "msg": "success",
            "data": [
                {
                    "pgroupid": 1,
                    "pgroupcode": "PG001",
                    "pgroupname": "Admin Group",
                    "desc": "Administrator permissions",
                    "status": 0
                }
            ],
            "pagination": {
                "page": 1,
                "pageSize": 10,
                "total": 100
            }
        }
    },
    "QueryProject": {
        "接口用途说明": "查询项目信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/BUS/QueryProject",
        "方法": "GET",
        "入参": {
            "prjcode": "P001",
            "prjname": "New Project",
            "status": 0,
            "page": 1,
            "pageSize": 10
        },
        "出参": {
            "code": 2000,
            "msg": "success",
            "data": [
                {
                    "prjid": 1,
                    "prjcode": "P001",
                    "prjname": "New Project",
                    "cstid": 1,
                    "ownerid": 1,
                    "sponsorid": 1,
                    "desc": "Project description",
                    "goal": "Project goal",
                    "status": 0
                }
            ],
            "pagination": {
                "page": 1,
                "pageSize": 10,
                "total": 100
            }
        }
    },
    "QueryEvent": {
        "接口用途说明": "查询事件信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/BUS/QueryEvent",
        "方法": "GET",
        "入参": {
            "eventid": 1,
            "reporter": 1,
            "status": 0,
            "page": 1,
            "pageSize": 10
        },
        "出参": {
            "code": 2000,
            "msg": "success",
            "data": [
                {
                    "eventid": 1,
                    "reporter": 1,
                    "reportertime": "2023-01-01T00:00:00Z",
                    "desc": "Event description",
                    "status": 0
                }
            ],
            "pagination": {
                "page": 1,
                "pageSize": 10,
                "total": 100
            }
        }
    },
    # 其他接口（非查询接口）
    "CreateUser": {
        "接口用途说明": "创建用户",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/CreateUser",
        "方法": "POST",
        "入参": {
            "empcode": "0001",
            "empname": "John Doe",
            "passwd": "encrypted_password",
            "sex": 1,
            "mobile": "1234567890",
            "weticket": "wechat_ticket",
            "admin": 1
        },
        "出参": {
            "code": 2000,
            "msg": "user created successfully"
        }
    },
    "EditUser": {
        "接口用途说明": "修改用户信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/EditUser",
        "方法": "POST",
        "入参": {
            "empid": 1,
            "empname": "Jane Doe",
            "passwd": "new_encrypted_password",
            "sex": 0,
            "mobile": "0987654321",
            "weticket": "new_wechat_ticket",
            "admin": 0
        },
        "出参": {
            "code": 2000,
            "msg": "user updated successfully"
        }
    },
    "CreateDepartment": {
        "接口用途说明": "创建部门",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/CreateDepartment",
        "方法": "POST",
        "入参": {
            "deptcode": "D001",
            "deptname": "HR Department",
            "deptlocation": "New York"
        },
        "出参": {
            "code": 2000,
            "msg": "department created successfully"
        }
    },
    "EditDepartment": {
        "接口用途说明": "修改部门信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/EditDepartment",
        "方法": "POST",
        "入参": {
            "deptid": 1,
            "deptname": "Finance Department",
            "deptlocation": "San Francisco"
        },
        "出参": {
            "code": 2000,
            "msg": "department updated successfully"
        }
    },
    "CreateCompany": {
        "接口用途说明": "创建公司",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/CreateCompany",
        "方法": "POST",
        "入参": {
            "compcode": "C001",
            "compname": "Tech Corp",
            "compadd": "Silicon Valley",
            "uscicode": "123456789"
        },
        "出参": {
            "code": 2000,
            "msg": "company created successfully"
        }
    },
    "EditCompany": {
        "接口用途说明": "修改公司信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/EditCompany",
        "方法": "POST",
        "入参": {
            "compcode": "new_compcode",
            "compname": "Tech Corp Inc.",
            "compadd": "San Francisco",
            "uscicode": "987654321"
        },
        "出参": {
            "code": 2000,
            "msg": "company updated successfully"
        }
    },
    "CreateMenu": {
        "接口用途说明": "创建菜单",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/CreateMenu",
        "方法": "POST",
        "入参": {
            "menucode": "M001",
            "mununame": "Dashboard",
            "subject": "MST",
            "level": 1,
            "sortid": 1
        },
        "出参": {
            "code": 2000,
            "msg": "menu created successfully"
        }
    },
    "EditMenu": {
        "接口用途说明": "修改菜单信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/MST/EditMenu",
        "方法": "POST",
        "入参": {
            "menuid": 1,
            "mununame": "Main Dashboard",
            "subject": "MST",
            "level": 1,
            "sortid": 1
        },
        "出参": {
            "code": 2000,
            "msg": "menu updated successfully"
        }
    },
    "CreatePermissionGroup": {
        "接口用途说明": "创建权限组",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/AUT/CreatePermissionGroup",
        "方法": "POST",
        "入参": {
            "pgroupcode": "PG001",
            "pgroupname": "Admin Group",
            "desc": "Administrator permissions"
        },
        "出参": {
            "code": 2000,
            "msg": "permission group created successfully"
        }
    },
    "EditPermissionGroup": {
        "接口用途说明": "修改权限组信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/AUT/EditPermissionGroup",
        "方法": "POST",
        "入参": {
            "pgroupid": 1,
            "pgroupname": "Super Admin Group",
            "desc": "Super Administrator permissions"
        },
        "出参": {
            "code": 2000,
            "msg": "permission group updated successfully"
        }
    },
    "GrantPermissiontoUser": {
        "接口用途说明": "赋予人员权限",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/AUT/GrantPermissiontoUser",
        "方法": "POST",
        "入参": {
            "empid": 1,
            "pgroupid": 1
        },
        "出参": {
            "code": 2000,
            "msg": "permission granted successfully"
        }
    },
    "RevokePermissiontoUser": {
        "接口用途说明": "取消人员权限",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/AUT/RevokePermissiontoUser",
        "方法": "POST",
        "入参": {
            "empid": 1,
            "pgroupid": 1
        },
        "出参": {
            "code": 2000,
            "msg": "permission revoked successfully"
        }
    },
    "CreateProject": {
        "接口用途说明": "创建项目",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/BUS/CreateProject",
        "方法": "POST",
        "入参": {
            "prjcode": "P001",
            "prjname": "New Project",
            "cstid": 1,
            "ownerid": 1,
            "sponsorid": 1,
            "desc": "Project description",
            "goal": "Project goal"
        },
        "出参": {
            "code": 2000,
            "msg": "project created successfully"
        }
    },
    "EditProject": {
        "接口用途说明": "修改项目信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/BUS/EditProject",
        "方法": "POST",
        "入参": {
            "prjid": 1,
            "prjname": "Updated Project",
            "cstid": 1,
            "ownerid": 1,
            "sponsorid": 1,
            "desc": "Updated project description",
            "goal": "Updated project goal"
        },
        "出参": {
            "code": 2000,
            "msg": "project updated successfully"
        }
    },
    "AddProjectMember": {
        "接口用途说明": "添加项目参与者",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/BUS/AddProjectMember",
        "方法": "POST",
        "入参": {
            "prjid": 1,
            "empid": 1
        },
        "出参": {
            "code": 2000,
            "msg": "project member added successfully"
        }
    },
    "RemoveProjectMember": {
        "接口用途说明": "移除项目参与者",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/BUS/RemoveProjectMember",
        "方法": "POST",
        "入参": {
            "prjid": 1,
            "empid": 1
        },
        "出参": {
            "code": 2000,
            "msg": "project member removed successfully"
        }
    },
    "CreateEvent": {
        "接口用途说明": "创建事件",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/BUS/CreateEvent",
        "方法": "POST",
        "入参": {
            "reporter": 1,
            "reportertime": "2023-01-01T00:00:00Z",
            "desc": "Event description"
        },
        "出参": {
            "code": 2000,
            "msg": "event created successfully"
        }
    },
    "EditEvent": {
        "接口用途说明": "修改事件信息",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/BUS/EditEvent",
        "方法": "POST",
        "入参": {
            "eventid": 1,
            "reporter": 1,
            "reportertime": "2023-01-01T00:00:00Z",
            "desc": "Updated event description"
        },
        "出参": {
            "code": 2000,
            "msg": "event updated successfully"
        }
    },
    "AddEventtoProject": {
        "接口用途说明": "将事件添加至项目",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/BUS/AddEventtoProject",
        "方法": "POST",
        "入参": {
            "prjid": 1,
            "eventid": 1
        },
        "出参": {
            "code": 2000,
            "msg": "event added to project successfully"
        }
    },
    "LoginbyWechat": {
        "接口用途说明": "微信鉴权",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/AUT/LoginbyWechat",
        "方法": "POST",
        "入参": {
            "weticket": "wechat_ticket"
        },
        "出参": {
            "code": 2000,
            "msg": "login success"
        }
    },
    "LoginbyDing": {
        "接口用途说明": "钉钉鉴权",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/AUT/LoginbyDing",
        "方法": "POST",
        "入参": {
            "dingticket": "ding_ticket"
        },
        "出参": {
            "code": 2000,
            "msg": "login success"
        }
    },
    "Login": {
        "接口用途说明": "普通鉴权",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/AUT/Login",
        "方法": "POST",
        "入参": {
            "empcode": "0001",
            "passwd": "encrypted_password",
            "verifycode": "bcnx"
        },
        "出参": {
            "code": 2000,
            "msg": "login success"
        }
    },
    "Logout": {
        "接口用途说明": "退出系统",
        "url": "http://[your_owner_ip_or_domain]:[set_port]/api/v1.0/AUT/Logout",
        "方法": "POST",
        "入参": {
            "Cookie": "some_session_item"
        },
        "出参": {
            "code": 2000,
            "msg": "logout success"
        }
    }
}

# 创建Excel文件
with pd.ExcelWriter("接口设计.xlsx") as writer:
    for sheet_name, data in interfaces.items():
        # 创建DataFrame
        df = pd.DataFrame([
            ["接口用途说明", data["接口用途说明"]],
            ["url", data["url"]],
            ["方法", data["方法"]],
            ["入参", ""],
            ["报文Header", ""],
            ["报文", data["入参"]],
            ["入参说明", ""],
            *[[key, value] for key, value in data["入参"].items()],
            ["", ""],
            ["出参", ""],
            ["报文Header", ""],
            ["报文", data["出参"]],
            ["出参说明", ""],
            *[[key, value] for key, value in data["出参"].items()]
        ])

        # 写入Excel
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

print("Excel文件生成成功！")