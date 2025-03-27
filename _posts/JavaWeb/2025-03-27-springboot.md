---
title: "SpringBoot"
date: 2025-03-27 03:39:16 +0800
categories: [JavaWeb]
tags: [spring]     # TAG names should always be lowercase
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
