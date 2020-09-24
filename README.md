<h1 align="center">Welcome to arida 👋</h1>
<p>
  <a href="https://www.npmjs.com/package/arida" target="_blank">
    <img alt="Version" src="https://img.shields.io/npm/v/arida.svg">
  </a>
  <a href="暂无" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="暂无" target="_blank">
    <img alt="License: 暂无" src="https://img.shields.io/badge/License-暂无-yellow.svg" />
  </a>
</p>

> 基于`FastAPI`实现的`Frida-RPC`工具，只需开发好相对应app的`Frida-Js`脚本，即可自动生成相应的基于`FastAPI`的`Frida-RPC`工具

### 🏠 [Homepage](暂无)

### ✨ [Demo](暂无)

Do By You Self！

## 实现原理

`Python`执行`PyexecJs`通过`Js的AST树`结构获取`Frida-Js`脚本中`rpc.exports`的方法以及对应方法的参数个数，根据方法名和参数个数通过`types.FunctionDef`从`Python AST字节码`来动态生成新的`Function对象`，并且结合`pydantic`的`create_model`自动生成的参数模型注册到`FastAPI的路由系统`中，实现`Frida-RPC`的功能。

## 核心功能

1. 对接多个`App`的`RPC接口暴露`

2. 自动转化`Js export`方法变成接口

3. 自动生成接口文档

## Install

```sh
1. git clone git@github.com:lateautumn4lin/arida.git

2. conda create -n arida python==3.8

3. conda install --yes --file requirements.txt
```

## Usage

```sh
1. uvicorn main:app --reload

2. watch 127.0.0.1:8000/docs 
```
eg:

![生成的fastapi的api结构图](https://github.com/lateautumn4lin/arida/blob/master/source/fastapi_docs.png)

![对应api的参数图](https://github.com/lateautumn4lin/arida/blob/master/source/post_body_hints.png)

## 如何开发自己的接口呢？

1. `Config`文件中写入自己的`App信息`

2. `Apps`目录写开发相应的`Frida-Js`脚本，可参考其他两个文件

## Run tests

```sh
uvicorn main:app --reload

测试Apk地址：

1. https://www.wandoujia.com/apps/6612700

2. https://www.wandoujia.com/apps/7666802
```
eg:

![测试图](https://github.com/lateautumn4lin/arida/blob/master/source/test.png)

## 参考资料

1. https://www.cnblogs.com/olivetree123/p/5067685.html（python动态创建函数）

2. http://blog.soliloquize.org/2016/07/06/Python%E5%8A%A8%E6%80%81%E5%88%9B%E5%BB%BA%E5%87%BD%E6%95%B0/

3. https://zhuanlan.zhihu.com/p/103665038（python字节码）

4. https://www.jianshu.com/p/2006a8c75bb2（FastAPI动态建模） 

5. https://github.com/xonsh/xonsh/pull/3304/files（python AST解析参考）

## Author

👤 **Lateautumn4lin**

* Website: https://cloudcrawler.club/
* Github: [@Lateautumn4lin](https://github.com/Lateautumn4lin)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](暂无). You can also take a look at the [contributing guide](暂无).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2020 [Lateautumn4lin](https://github.com/Lateautumn4lin).<br />
This project is [暂无](暂无) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
