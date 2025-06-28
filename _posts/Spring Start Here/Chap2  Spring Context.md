---
title: "第二章 Spring 上下文：定义 Bean"
date: 2025-06-28 11:12:01 +0800
categories: [Spring Start Here]
tags: ['java']
---


### 第二章 Spring 上下文：定义 Bean

本章的核心是学习 Spring 框架的基石：**Spring 上下文（Spring Context）**，以及如何将我们自己定义的对象实例作为 **Bean** 添加到上下文中，从而让 Spring 框架来管理它们。

#### 1. Spring 上下文概述

- **什么是 Spring 上下文？** 你可以把它想象成一个存在于应用内存中的“容器”或“桶”。这个容器负责创建、配置和管理我们应用中的对象实例（即 Beans）。
- **为什么需要它？** Spring 只有对自己上下文中存在的 Bean 才拥有控制权，才能为它们提供诸如依赖注入（DI）、事务管理等强大的功能。默认情况下，Spring 对我们应用中的任何对象都一无所知，因此我们必须手动将它们添加到上下文中。
- **如何实例化上下文？** 在现代的 Spring 配置中，我们通常使用 `AnnotationConfigApplicationContext` 类来创建上下文的实例。

#### 2. 将 Bean 添加到上下文的三种主要方法

---

##### **方法一：使用 `@Bean` 注解**

这是最直接、最灵活的方法，尤其适用于那些我们无法直接修改其源代码的类（例如，来自第三方库的类）。

**步骤：**

1. **创建配置类 (Configuration Class)**：
    
    - 创建一个普通的 Java 类，并在其上方添加 `@Configuration` 注解。这个注解告诉 Spring，这个类包含了 Bean 的定义信息。
2. **定义 Bean 创建方法**：
    
    - 在配置类中，定义一个方法，该方法的返回类型就是你想要添加到上下文中的对象类型。
    - 在这个方法上方添加 `@Bean` 注解。Spring 会在初始化上下文时调用这个方法，并将返回的对象实例注册为一个 Bean。
    - **命名规则**：默认情况下，方法名就是这个 Bean 的名字（ID）。例如，一个名为 `parrot()` 的方法会创建一个名为 "parrot" 的 Bean。
3. **关联配置类与上下文**：
    
    - 在创建 `AnnotationConfigApplicationContext` 实例时，将配置类的 `.class` 对象作为参数传入，例如：`new AnnotationConfigApplicationContext(ProjectConfig.class)`。

**处理多个同类型 Bean 的情况：**

- **歧义问题**：如果你定义了多个相同类型的 Bean，仅通过类型 `context.getBean(Parrot.class)` 获取会抛出 `NoUniqueBeanDefinitionException` 异常，因为 Spring 不知道该选择哪一个。
- **解决方案**：
    - **按名称获取**：在 `getBean()` 方法中同时提供 Bean 的名称和类型，例如 `context.getBean("parrot2", Parrot.class)`。
    - **使用 `@Primary` 注解**：在一个 `@Bean` 方法上添加 `@Primary` 注解，将其标记为该类型的“首选”或“默认” Bean。当 Spring 遇到多个同类型 Bean 且未指定名称时，会优先选择被 `@Primary` 标记的那个。

---

##### **方法二：使用原型注解 (Stereotype Annotations)**

这种方法代码更简洁，当你需要将自己项目中的类注册为 Bean 时，这是首选方式。

**步骤：**

1. **标记组件类**：
    
    - 在你想要注册为 Bean 的类（例如 `Parrot` 类）的上方，直接添加原型注解，最常用的是 `@Component`。
2. **启用组件扫描 (Component Scan)**：
    
    - 仅有 `@Component` 是不够的，你还需要告诉 Spring 去哪里寻找这些被标记的类。
    - 在你的 `@Configuration` 配置类上添加 `@ComponentScan` 注解，并通过 `basePackages` 属性指定要扫描的包名，例如 `@ComponentScan(basePackages = "main")`。Spring 会自动扫描这些包及其子包下的所有 `@Component` 类，并为它们创建 Bean。

**初始化逻辑：**

- **使用 `@PostConstruct`**：当你使用 `@Component` 时，你无法像 `@Bean` 方法那样在创建实例时立即执行配置逻辑（如设置名字）。为了解决这个问题，你可以在组件类中定义一个方法，并用 `@PostConstruct` 注解标记它。Spring 会在构造函数执行完毕后、Bean 完全初始化之前调用这个方法，让你可以在此执行初始化任务。

---

##### **方法三：编程方式注册 Bean**

这是一种高度灵活的方式，允许你在应用运行时根据特定逻辑动态地向上下文中添加 Bean。

**步骤：**

1. **调用 `registerBean()` 方法**：
    - 获取 `ApplicationContext` 的实例。
    - 调用其 `registerBean()` 方法来注册一个新的 Bean。
    - 这个方法的主要参数包括：
        - `beanName`：Bean 的名称。
        - `beanClass`：Bean 的类型。
        - `supplier`：一个供给型接口 (`Supplier`)，它的实现逻辑负责返回真正的 Bean 实例。
        - `customizers` (可选)：用于对 Bean 定义进行更细致的配置，例如将其设置为主 Bean (`setPrimary(true)`)。

#### 总结对比

|            |                                       |                                                           |
| ---------- | ------------------------------------- | --------------------------------------------------------- |
| **特性**     | **@Bean 注解**                          | **原型注解 (@Component)**                                     |
| **控制力**    | **完全控制**：你可以在方法体内完全控制实例的创建和配置过程。      | **间接控制**：Spring 负责创建实例，你只能通过 `@PostConstruct` 等方式在事后进行干预。 |
| **适用对象**   | **任何类**：可以为项目内外的任何类（包括第三方库的类）创建 Bean。 | **仅限项目内可修改的类**：因为你需要在类的源码上添加注解。                           |
| **代码量**    | 相对较多，每个 Bean 都需要一个独立的方法。              | 代码非常简洁，只需一个注解。                                            |
| **同类型多实例** | **支持**：可以轻松定义多个同类型的 Bean。             | **不支持**：一个类默认只能创建一个 Bean。                                 |

总的来说，本章为你打下了使用 Spring 的基础，让你明白了如何将普通的对象交给 Spring 管理，这是后续学习所有 Spring 高级功能的先决条件。