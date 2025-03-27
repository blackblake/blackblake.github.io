---
title: "SpringBoot"
date: 2025-03-27 03:39:16 +0800
categories: [JavaWeb]
tags: [spring]     # TAG names should always be lowercase
---

异常处理
---
---
打开浏览器，输入 http://localhost:8080/hello 后发现显示如下：

>Whitelabel Error Page This application has no explicit mapping for /error, so you are seeing this as a fallback. 
> Tue Mar 27 16:26:02 CST 2025 There was an unexpected error (type=Not Found, status=404). No message available

stack overflow上的解释：
  
>Make sure that your main class is in a root package above other classes.
>
>When you run a Spring Boot Application, (i.e. a class annotated with @SpringBootApplication), Spring will only scan the classes below your main class package.
>

```plaintext
com
+- APP
+- Application.java  <--- your main class should be here, above your controller classes
|
+- model
|   +- user.java
+- controller
+- UserController.java
```


Tomcat
---
---

### 到底有什么用？

Tomcat 是一个广泛使用的 **Web 服务器** 和 **Servlet 容器**，它的核心作用可以简单理解为：**运行 Java 编写的网站或 Web 应用**。下面用通俗易懂的方式解释它的用途和工作原理：

---

#### 1. **Tomcat 是什么？**
- **本质**：一个用 Java 编写的开源软件，由 Apache 基金会维护。
- **核心功能**：
  - **Web 服务器**：能接收用户的 HTTP 请求（比如浏览器访问网址），并返回网页或数据。
  - **Servlet 容器**：能执行 Java 代码（Servlet/JSP），动态生成网页内容（比如用户登录、数据库查询等）。

---

#### 2. **为什么需要 Tomcat？**
- **静态网站 vs 动态网站**：
  - 静态网站（如纯 HTML）可以直接用 Nginx 等服务器提供。
  - **动态网站**（如淘宝、银行系统）需要根据用户请求实时生成内容（比如显示你的订单），这时就需要 Tomcat 这类容器运行 Java 代码来处理逻辑。

- **Java Web 应用的“运行环境”**：
  - 你写的 Java 代码（Servlet/JSP）不能直接运行，需要 Tomcat 加载、管理它们的生命周期（启动、调用、销毁）。

---

#### 3. **Tomcat 的具体作用**
##### （1）处理 HTTP 请求
- 当用户通过浏览器访问 `http://example.com/login` 时：
  1. Tomcat 接收请求，分析 URL。
  2. 找到对应的 Java 类（Servlet）处理登录逻辑（比如验证用户名密码）。
  3. 将结果生成 HTML 或 JSON 返回给浏览器。

##### （2）管理 Servlet/JSP
- **Servlet**：Java 类，专门处理业务逻辑（比如计算、数据库操作）。
- **JSP**：类似 HTML，但能嵌入 Java 代码动态生成页面。
- Tomcat 负责调用这些组件，确保它们正确响应请求。

##### （3）提供共享资源
- 多个用户访问时，Tomcat 可以管理共享资源（如数据库连接池），避免重复创建。

---

#### 4. **类比理解**
- **Tomcat 像“餐厅服务员”**：
  - 你（用户）点菜（HTTP 请求） → 服务员（Tomcat）把订单交给厨房（Servlet） → 厨房做菜（业务逻辑） → 服务员上菜（返回响应）。
- **对比其他服务器**：
  - Nginx：只负责“端菜”（静态内容），不会“做菜”（动态逻辑）。
  - Tomcat：既能“端菜”也能“做菜”。

#### 5. **本地性**

Tomcat 像一家“本地餐馆”​：
你在厨房（Tomcat）做好了菜（Java Web 应用），
你自己（localhost）可以吃，邻居（同一局域网）也可以来吃（通过输入你的本地ip localhost）。
但外地人（外网）想吃到你的菜，需要你“开门迎客”（配置网络权限或公网映射）。

#### 6. **我的理解**
所以我用tomcat的时候，tomcat相当于一个位于我的计算机本地的服务器，而网络需要从它——也就是我的本地服务器来请求一些东西，tomcat会回应浏览器的请求。
