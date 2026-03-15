# 🎓 CampusLife - 校园一站式数字化服务平台

> **最后更新时间**: 2026-02-04

**CampusLife** 是一个现代化的全栈 Web 应用，旨在模拟真实的校园综合信息系统。它打通了从静态数据展示到动态交互的壁垒，采用前后端分离架构，实现了学生档案管理、教务信息查询、体质健康监测以及智慧图书馆服务的一体化解决方案。

---

## 🛠️ 技术栈 (Tech Stack)

本项目坚持使用原生前端技术栈以展示对 Web 底层原理的掌握，同时引入现代化的 Python 后端框架保障性能。

### **前端 (Frontend)**
* **核心语言**: HTML5, JavaScript (ES6+ Vanilla JS) - *无依赖，零构建工具*
* **UI 框架**: **Tailwind CSS** (通过 CDN 引入) - *实现完全响应式的现代化界面*
* **图标库**: Phosphor Icons
* **数据交互**: Native Fetch API (Async/Await)

### **后端 (Backend)**
* **核心框架**: **Python 3.9+**, **FastAPI** - *高性能异步 Web 框架*
* **服务器**: Uvicorn (ASGI Server)
* **ORM**: **SQLAlchemy** - *处理对象关系映射*
* **数据验证**: Pydantic Schemas

### **数据库 (Database)**
* **数据库**: **SQLite** - *轻量级、无需配置的关系型数据库*
* **数据持久化**: 包含自动化 ETL 脚本 (`seed.py`)，负责清洗并将复杂的嵌套 JSON 数据迁移至数据库。

### **外部集成 (Integrations)**
* **Open Library API**: 用于智慧图书馆页面的书籍检索与元数据获取。

---

## 🖥️ 核心功能 (Features)

### 1. 🏠 校园首页 (`index.html`)
* **动态欢迎致辞**：根据当前登录用户身份（如学生会主席、普通学生），从后端获取个人化问候与头像。
* **实时新闻轮播**：基于数据库驱动的新闻发布系统。
* **身份无缝切换**：内置全局用户切换器，可模拟不同角色的视角。

### 2. 🗂️ 档案检索中心 (`archive_search.html`)
* **全局模糊搜索**：支持通过姓名或学号（Real ID）检索学生数据库。
* **多分类档案展示**：
    * **📚 学术档案**：各阶段考试成绩、年级排名趋势及各科得分明细表。
    * **🏥 体质健康**：可视化呈现体检报告（BMI、视力、肺活量等核心指标）。
    * **🏆 荣誉记录**：学生获得的奖项、处分及社会实践经历。
* **交互式详情卡片**：悬停展开与折叠动画效果。

### 3. 📖 智慧图书馆 (`library.html`)
* **Open Library 集成**：对接全球最大的开放图书馆 API，支持实时检索书名、作者或 ISBN。
* **我的借阅看板**：从后端数据库拉取当前用户的真实借阅状态（在借、即将到期、已逾期），并动态计算剩余天数。
* **热度排行榜**：展示校园热门借阅书籍。

---

## 📦 项目结构 (Project Structure)

- **CampusLife/**: 项目根目录
  - 📄 **index.html**: **首页** - 负责展示新闻轮播与导航入口
  - 📄 **archive_search.html**: **档案检索页** - 提供成绩查询与健康报告可视化
  - 📄 **library.html**: **智慧图书馆** - 集成借阅看板与 Open Library API 检索
  - 🐍 **main.py**: **后端核心** - FastAPI 应用入口与 API 路由逻辑
  - ⚙️ **database.py**: **数据库配置** - SQLAlchemy 连接与 Session 管理
  - 🗃️ **models.py**: **ORM 模型** - 定义数据库表结构 (User, Archive, News)
  - ✅ **schemas.py**: **数据验证** - Pydantic Schema 定义
  - 🌱 **seed.py**: **初始化脚本** - 清洗数据并写入 SQLite 数据库
  - 💾 **campuslife_data.db**: **数据库文件** - 自动生成的 SQLite 文件
  - 📝 **README.md**: 项目说明文档
 
---

## 🚀 使用指南 (Usage Guide)


使用指南 (Usage Guide)

### 1. 环境准备
* **确保您的电脑已安装 Python 3.9+ 和 Git：**
  执行以下命令检查版本：
  python --version
  git --version

### 2. 克隆项目
* **将项目代码从 GitHub 下载到本地：**
  git clone https://github.com/你的用户名/edu-space.git
  cd edu-space

### 3. 创建并激活虚拟环境 (推荐)
* **Windows 系统操作：**
  python -m venv venv
  .\venv\Scripts\activate

* **macOS / Linux 系统操作：**
  python3 -m venv venv
  source venv/bin/activate

### 4. 安装后端依赖
* **安装 FastAPI、SQLAlchemy 等核心库：**
  pip install fastapi uvicorn sqlalchemy pydantic requests

### 5. 初始化数据库 (ETL)
* **运行数据种子脚本，生成本地 SQLite 数据库：**
  python seed.py
  (执行后文件夹内应出现 edu_space.db 文件)

### 6. 启动后端服务
* **运行主程序启动 Uvicorn 服务器：**
  python main.py
  (看到 "Uvicorn running on http://127.0.0.1:8000" 表示成功)

### 7. 访问应用
* **打开浏览器查看前端效果：**
  1. 推荐在 VS Code 中安装 "Live Server" 插件。
  2. 在项目根目录右键点击 "index.html"，选择 "Open with Live Server"。
  3. 或者直接在浏览器地址栏输入文件路径访问。
