
# 使用方法

## 使用前须知

- 本教程将以面板数据的估计为例。我们默认您精通 stata 常规命令操作，含面板估计的命令 `reghdfe`、`xtlogit` 等。
- 如果您对 stata 语法或者以上 stata 命令不熟悉，请在 stata 中使用 `help` 命令查看相关命令的原理，并确保您完整掌握相关命令的使用方式之后再使用本程序。

## 基本使用方法

```shell
pyoneclick [-h] -d DATA [-a ADJUST] [-f FIXED] -c COMMAND [-z] [-t THRESHOLD] [--iterations ITERATIONS] [--initial_temperature INITIAL_TEMPERATURE] [--min_temperature MIN_TEMPERATURE] [--cooling_rate COOLING_RATE] [--max_steps MAX_STEPS] [-p]
```

这一命令的参数分为四类功能：

### 数据来源
- `-d` 或  `--data`：指定数据的来源路径。

### 命令执行
这是一些基于 stata 的命令参数，可以指定以下内容：
- `-a` 或 `--adjust`：待调整显著性的变量。
- `-f` 或 `--fixed`：在回归中必须加入的锁定变量。
- `-c` 或 `--command`：完整的回归命令。
- `-z` 或 `--z_statistic`：指定使用 z 值统计量的回归方式。
- `-t` 或 `--threshold`：回归希望达到的显著性水平。

### 策略搜索
这是一些基于模拟退火算法的参数，用于设置搜索策略：
- `--iterations`：重复进行模拟退火算法的次数。
- `--initial_temperature`：模拟退火初始温度。
- `--min_temperature`：模拟退火最低温度。
- `--cooling_rate`：模拟退火冷却速率。
- `--max_steps`：单次模拟退火的最大步数。

### 信息打印
- `-p` 或 `--print_commands`：打印命令的信息。

## 命令示例

### 单个统计量估计

1. 基本估计形式。`-c` 的命令中必须显式列出所有控制变量列表，不能使用宏定义或简写。

```shell
pyoneclick -d "example.dta" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

2. 如果未提供 `-a` 参数，程序会自动将待调整的变量推断为因变量之后的第一个变量。

```shell
pyoneclick -d "example.dta" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

3. 如果未提供 `-f` 参数，则视为没有需要锁定的变量。

```shell
pyoneclick -d "example.dta" -a "x1" -c "reghdfe y1 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

4. 显然，`-c` 参数不可省略。如果省略 `-c`，代码将失去意义。

```shell
# Wrong!
pyoneclick -d "example.dta" -a "x1" -f "x2"
```

5. 对于基于最大似然估计拟合的模型（如 `logit`、`probit`、`poisson`），必须使用 z 值统计量来检验显著性。此时需通过 `-z` 参数指定以 z 值统计量为基准。

```shell
pyoneclick -d "example.dta" -a "x1" -f "i.year" -c "xtlogit yb x1 i.year c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, fe" -z
```

6. 支持 `if` 条件以及任意其他选项。

```shell
pyoneclick -d "example.dta" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31 if year > 2014, absorb( stkcd year ) vce(robust)"
```


### 多个统计量估计

1. 多命令的基本估计形式。对于每个需要显著的统计量，程序会单独估计一条新命令，无论这些命令是否相同。整个程序将估计一组命令。

```shell
pyoneclick -d "example.dta" -a "x2" -f "x1" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

2. 在同一个函数中，可能需要使不同的自变量都显著，此时可以采用简略写法。即当 `-c` 相同时，在相同的命令中估计不同变量时，可以仅输入一次 `-c`。依次列出待估计的 `-a` 和 `-f` 参数，系统会自动推断。如果某项输入次数为一次，则该参数将被自动复制到其他待估计命令中。

```shell
pyoneclick -d "example.dta" -a "x2" -f "x1" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

3. 在不同因变量的函数中，可能需要使同一个自变量显著，此时可以采用简略写法。即当 `-a` 或 `-f` 相同时，也就是在不同命令中估计相同变量时，可以仅输入一次 `-a` 和 `-f`，或者不输入。如果未输入 `-a`，则依据第一条命令的待调整值推断所有命令的待调整值；如果未输入 `-f`，则表示所有命令中不锁定任何变量。

```shell
pyoneclick -d "example.dta" -a "x1" -c "reghdfe y1 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -c "reghdfe y2 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

4. 如果需要在多个变量估计时设置空的 `-f`，请使用引号包裹的空格 `" "` 进行占位。

```shell
pyoneclick -d "example.dta" -a "x1" -f "x2" -a "x1" -f " " -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

5. 在多命令估计时，可以通过 `-t` 设置显著性阈值。设置该参数有助于尽量使所有命令都达到期望的显著结果。

```shell
pyoneclick -d "example.dta" -a "x1" -c "reghdfe y1 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -c "reghdfe y2 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -t 0.05
```

6. 在组估计中，不能混合使用 t 值和 z 值的统计量。

```shell
# Wrong!
pyoneclick -d "example.dta" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -a "x1" -f "i.year" -c "xtlogit yb x1 i.year c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, fe" -z 
```


### 高级功能

1. 设置搜索相关参数。本命令的搜索算法基于模拟退火，因此可以设置模拟退火的相关参数以优化收敛曲线。

```shell
pyoneclick -d "example.dta" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" --iterations 5 --initial_temperature 1e2 --min_temperature 1e-8 --cooling_rate 0.90 --max_steps 200
```

2. 添加 `-p` 参数以打印调试信息，包含命令的实际拆分效果。

```shell
pyoneclick -d "example.dta" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -p
```
