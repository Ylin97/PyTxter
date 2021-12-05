## 简介  
这是一个基于 [Python](https://www.python.org/) 和 [PyQt5](https://pypi.org/project/PyQt5/) 的 txt文本/小说编辑器。它不仅提供了记事本的所有功能，同时还提供了章节目录的支持。此外，它还为 txt 小说编辑和格式化加入了**一键格式化**、**清除空白行**、**章节名格式化**、**中英标点纠正**、**屏蔽字替换**等特色功能。   

软件截图：  

![image-20211205132308301](https://ylin-typora01.oss-cn-shenzhen.aliyuncs.com/images/image-20211205132308301.png)

## 工具栏介绍  

![image-20211205134129152](https://ylin-typora01.oss-cn-shenzhen.aliyuncs.com/images/image-20211205134129152.png)

## 功能介绍   

### 一键格式化  
一键格式化用于对排版混乱的txt小说文本进行排版整理，使之适合手机阅读。此功能特别适合于那些从网上复制的、未分好段落的文本，以及其他从网上下载的排版混乱的txt小说文本。    
此功能可以选择**强制自动分段**（默认判断界限为 100 字符）。当然它最终是根据句子结尾的标点符号来执行分段的，所以即使当前段的总字符数超过了 100，只要遍历器还没有碰到可作为分段的标点，那也不会自动分段。  

一键格式化功能演示：   

![click2format](https://ylin-typora01.oss-cn-shenzhen.aliyuncs.com/images/一键格式化演示2.gif)

### 清除空白行  
顾名思义，就是清除文本中的空白行。   

### 中英标点纠正  
此功能会尝试对中英标点进行纠正，具体替换类型如下：   
| 英文标点 | 中文标点 |
| :------: | :------: |
|  ``,``   |  ``，``  |
|  ``.``   |  ``。``  |
|  ``!``   |  ``！``  |
|  ``?``   |  ``？``  |

## 功能截图   

打开文件和点击目录跳转功能演示：   

![](https://ylin-typora01.oss-cn-shenzhen.aliyuncs.com/images/打开文件和目录跳转.gif)

文本格式化功能演示：   

![](https://ylin-typora01.oss-cn-shenzhen.aliyuncs.com/images/格式化功能演示.gif)

## 待完善功能   

- [ ] 目录项自动定位到光标位置所对应的章节名  
- [ ] 实现"屏蔽字替换功能"  
- [ ] 为 Sigil 导入提供格式优化  
