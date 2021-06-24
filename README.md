# Document structure
** I'll explain as plainly as I can, so ask your questions if you feel confused!**

```shell
.
├── __pycache__
├── algorithm
├── apps
│   ├── FT
│   └── MOT
├── assets
│   ├── imgs
│   └── js
├── components
│   ├── __pycache__
│   ├── display
│   │   └── __pycache__
│   ├── input
│   │   └── __pycache__
│   ├── nav
│   │   └── __pycache__
│   └── upload
│       └── __pycache__
├── app.py
├── index.py
└── defer-load-js

# Ignore these pycache files, they are just caches
```
CN : 设想一下我们搭建的网页是一个大型乐高积木玩具。那么components文件中放置的是乐高最小的积木块(类似于前端的导航栏，输入栏这些)。那么apps文件中将放置由components文件中搭建的你们的个人应用。例如 FT的应用就放在FT文件夹下，MOT的就放MOT下。algorithm文件夹则存放一些数据处理算法，例如傅立叶方程。。。

ENG : Imagine that the web page we build is a giant Lego block toy. Then the components file contains the smallest LEGO blocks (similar to the front-end navigation bar, input fields, etc.). Then the apps file will hold your applications built from the components file. For example, FT applications will be placed in the FT folder and MOT applications will be placed in the MOT folder. The algorithm folder holds data processing algorithms such as Fourier's equation.

# Multi-apps
** This part of the demo I made is still buggy and needs to be checked. **

CN : 由于我们的文件相当于当个页面的集合。我在和components同目录的文件下设置了app.py 和 index.py的文件。其中index.py负责url映射，获取你们对应的页面。

ENG : Since our files are equivalent to a collection of pages, I have set up the files app.py and index.py under the same directory as the components where index.py is responsible for URL mapping and getting your corresponding pages.