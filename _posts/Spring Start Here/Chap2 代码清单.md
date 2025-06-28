---
title: "Chap2 代码清单"
date: 2024-12-31 11:12:01 +0800
categories: [Spring Start Here]
tags: ['ml', 'java']
---


**清单 2.2 在 `pom.xml` 文件中添加新依赖 **

```XML
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
	/*...*/
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-jdbc</artifactId>
            <version>5.2.6.RELEASE</version>
        </dependency>
    </dependencies>

</project>
```


**清单 2.3 `Parrot` 类 **

```Java
public class Parrot {

    private String name;

    // Omitted getters and setters
}
```


**清单 2.6 创建 Spring 上下文的实例 **

```Java
public class Main {
    public static void main(String[] args) {
        var context =
                new AnnotationConfigApplicationContext();
    }
}
```


**清单 2.7 为项目定义一个配置类 **

```Java
@Configuration
public class ProjectConfig {

}
```


**清单 2.8 定义 `@Bean` 方法 **

```Java
@Configuration
public class ProjectConfig {

    @Bean
    Parrot parrot() {
        var p = new Parrot();
        p.setName("Koko");
        return p;
    }
}
```


**清单 2.9 基于定义的配置类初始化 Spring 上下文**

```Java
public class Main {
    public static void main(String[] args) {
        var context =
                new AnnotationConfigApplicationContext(
                        ProjectConfig.class);
    }
}
```

**清单 2.10 从上下文中引用 `Parrot` 实例**


```Java
public class Main {
    public static void main(String[] args) {
        var context =
                new AnnotationConfigApplicationContext(
                        ProjectConfig.class);

        Parrot p = context.getBean(Parrot.class);
        System.out.println(p.getName());
    }
}
```


**清单 2.11 向上下文中再添加两个 Bean**

```Java
@Configuration
public class ProjectConfig {

    @Bean
    Parrot parrot() {
        var p = new Parrot();
        p.setName("Koko");
        return p;
    }

    @Bean
    String hello() {
        return "Hello";
    }

    @Bean
    Integer ten() {
        return 10;
    }
}
```


**清单 2.12 在控制台打印两个新的 Bean**

```Java
public class Main {
    public static void main(String[] args) {
        var context = new AnnotationConfigApplicationContext(
                ProjectConfig.class);

        Parrot p = context.getBean(Parrot.class);
        System.out.println(p.getName());

        String s = context.getBean(String.class);
        System.out.println(s);

        Integer n = context.getBean(Integer.class);
        System.out.println(n);
    }
}
```


**清单 2.13 向 Spring 上下文中添加多个相同类型的 Bean**

```Java
@Configuration
public class ProjectConfig {

    @Bean
    Parrot parrot1() {
        var p = new Parrot();
        p.setName("Koko");
        return p;
    }

    @Bean
    Parrot parrot2() {
        var p = new Parrot();
        p.setName("Miki");
        return p;
    }

    @Bean
    Parrot parrot3() {
        var p = new Parrot();
        p.setName("Riki");
        return p;
    }
}
```


**清单 2.14 按类型引用一个 `Parrot` 实例**

```Java
public class Main {
    public static void main(String[] args) {
        var context = new
                AnnotationConfigApplicationContext(ProjectConfig.class);

        Parrot p = context.getBean(Parrot.class);
        System.out.println(p.getName());
    }
}
```


**清单 2.15 按其标识符引用一个 Bean**

```Java
public class Main {
    public static void main(String[] args) {
        var context = new
                AnnotationConfigApplicationContext(ProjectConfig.class);

        Parrot p = context.getBean("parrot2", Parrot.class);
        System.out.println(p.getName());
    }
}
```


**清单 2.16 为 `Parrot` 类使用原型注解**

```Java
@Component
public class Parrot {
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```


**清单 2.17 使用 `@ComponentScan` 注解告诉 Spring 在哪里查找**

```Java
@Configuration
@ComponentScan(basePackages = "main")
public class ProjectConfig {

}
```


**清单 2.18 定义 `main` 方法以测试 Spring 配置**

```Java
public class Main {
    public static void main(String[] args) {
        var context = new
                AnnotationConfigApplicationContext(ProjectConfig.class);

        Parrot p = context.getBean(Parrot.class);
        System.out.println(p);
        System.out.println(p.getName());
    }
}
```


**清单 2.19 使用 `registerBean()` 方法向 Spring 上下文添加一个 Bean**

```Java
public class Main {
    public static void main(String[] args) {
        var context =
                new AnnotationConfigApplicationContext(
                        ProjectConfig.class);

        Parrot x = new Parrot();
        x.setName("Kiki");

        Supplier<Parrot> parrotSupplier = () -> x;

        context.registerBean("parrot1",
                Parrot.class, parrotSupplier);

        Parrot p = context.getBean(Parrot.class);
        System.out.println(p.getName());
    }
}
```