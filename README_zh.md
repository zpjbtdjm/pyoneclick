# pyoneclick

该 Python 工具能够自动筛选控制变量以调整特定变量的显著性，类似于 Stata 的 `oneclick` 命令但提供更强大的功能。

- English: [README.md](https://github.com/zpjbtdjm/pyoneclick/blob/master/README.md)

## 简介

### 洞见

本研究的开发基于以下见解：

1. 要做时间与最优解的权衡。在筛选控制变量的过程中，当控制变量过多时，筛选最优解在时间上是不可接受的。很多时候我们只需要快速得出一个能用的结果，即一个接近最优解的结果，而不是所有能用的结果。

2. 要解决按下葫芦浮起瓢的问题。很多时候一个变量在特定命令中显著了，另一个变量或者另一条命令中的同一个变量又不显著了，因此用于筛选的命令需要解决这类需要同时显著的问题。

### 命令特点

相对 Stata 中的 oneclick 命令，本命令加入了许多新的特性。本命令具有以下特性：

1. 筛选更加高效。本命令基于模拟退火算法而非枚举，在搜索可用控制变量过程中具有较低的时间复杂度。

2. 逻辑更加清晰。在执行命令过程中可以直接传入 Stata 的原生代码，无需改变代码习惯，命令可读性更高。

3. 功能范围更广。支持多命令联合估计，支持同时对多个变量或多条命令的显著性进行调整。

## 使用

### 需求

在正式使用之前，我们需要具备以下条件：

1. 拥有有效的许可证的 Stata 软件。软件版本必须为 Stata 17 及以上。

2. 合适的 Python 3 环境。建议为 Python 3.8 及以上版本。

### 安装

1. 首先需要在 Windows 控制面板中设置系统环境变量，变量名为 `STATA_PATH`。变量的值设定为 Stata 安装路径加上版本号。以 64 位电脑上 Stata 18 的 MP 版本为例，系统默认安装路径以下所示：
```
STATA_PATH=C:\Program Files\Stata18\StataMP-64.exe
```

2. 安装 `pyoneclick` 命令：
```shell
pip install pyoneclick
```

### 简单开始

1. 指定数据。首先请确保您已经安装该命令并在 Windows 系统中正确设定了环境变量。在第一次执行统计估计命令之前，请使用参数指定要使用的 `.dta` 数据文件：

```shell
pyoneclick -d "examples/example.dta" 
```

也可以在进行估计的同时指定数据，但请注意在任何时候使用 `-d` 参数会更新后续所有命令的默认数据文件。

2. 简单估计。必须通过 `-c` 指定要运行的 stata 命令，显式列出所有控制变量列表，不能使用宏定义或简写：

```shell
pyoneclick -c "reghdfe y1 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

模型会自动解析因变量与自变量，并通过计算最优控制变量列表实现待调整变量的显著性调节。

`pyoneclick` 命令的完整功能较为复杂，完整掌握可能需要一定时间。
- 我们提供了详细的使用说明，以帮助用户快速上手：[查看详细使用说明](https://github.com/zpjbtdjm/pyoneclick/blob/master/docs/USAGE_zh.md)

## 致谢

本项目的开发受到了 [StataOneClick](https://github.com/ShutterZor/StataOneClick) 项目的启发，在此我们向该项目的作者致以诚挚的感谢。作者的卓越工作为我们的项目提供了宝贵的思路，并成为了本项目开发的重要基础。

## 第三方库

本项目使用了以下开源库：
- [stata-setup](https://pypi.org/project/stata-setup/)：遵循 [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) 许可协议。

