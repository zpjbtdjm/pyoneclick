# pyoneclick Usage

## Prerequisites

- Proficient use of the `pyoneclick` command requires substantial prior knowledge of Stata. This tutorial will use panel data estimation as an example. We assume that you are proficient in regular Stata commands, including panel estimation commands such as `reghdfe`, `xtlogit`, etc.
- If you are unfamiliar with Stata syntax or the above Stata commands, please use the `help` command in Stata to review the principles of related commands and ensure full mastery of their usage before using this program.
- We provide carefully designed sample data in the file `examples/example.dta`, which contains 31 control variables. You can download the data and try to run the commands.

## Basic Usage

The basic usage of this command is as follows:

```shell
pyoneclick [-h] -d DATA [-a ADJUST] [-f FIXED] -c COMMAND [-z] [-t THRESHOLD] [--iterations ITERATIONS] [--initial_temperature INITIAL_TEMPERATURE] [--min_temperature MIN_TEMPERATURE] [--cooling_rate COOLING_RATE] [--max_steps MAX_STEPS] [-p]
```

The parameters of this command can be grouped into four categories: data source, command execution, search strategy, and information output.

### Data Source
- `-d` or `--data`: Specifies the path to the data source.

### Command Execution
These are some Stata-based command parameters that allow specification of the following:
- `-a` or `--adjust`: Variables for which significance needs adjustment.
- `-f` or `--fixed`: Variables that must be included in the regression.
- `-c` or `--command`: The complete Stata regression command.
- `-z` or `--z_statistic`: Specifies regression methods using z-statistics.
- `-t` or `--threshold`: Desired significance level for the regression.

### Search Strategy
These are parameters based on the simulated annealing algorithm, used to set the search strategy:
- `--iterations`: Number of repetitions of the simulated annealing algorithm (default is 5).
- `--initial_temperature`: Initial temperature for simulated annealing (default is 1e2).
- `--min_temperature`: Minimum temperature for simulated annealing (default is 1e-8).
- `--cooling_rate`: Cooling rate for simulated annealing (default is 0.90).
- `--max_steps`: Maximum number of steps for a single simulated annealing run (default is 200).

### Information Output
- `-p` or `--print_commands`: Print command information.

## Command Examples

### Presets

First, ensure that you have installed the command and set the environment variables. To run these examples, navigate to the `examples` directory first and then execute the `pyoneclick` command:

```shell
cd ../examples
```

### Single Statistic Estimation

1. Basic estimation form. All control variable lists must be explicitly listed in the `-c` command; macro definitions or abbreviations cannot be used:

```shell
pyoneclick -d "example.dta" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

2. If the `-a` parameter is not provided, the program will automatically infer the variable to be adjusted as the first variable after the dependent variable:

```shell
pyoneclick -d "example.dta" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

3. If the `-f` parameter is not provided, it means there are no variables that must be included in the regression:

```shell
pyoneclick -d "example.dta" -a "x1" -c "reghdfe y1 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

4. Clearly, the `-c` parameter cannot be omitted. If `-c` is omitted, the code will lose its meaning:

```shell
# Wrong!
pyoneclick -d "example.dta" -a "x1" -f "x2"
```

5. For models fitted using maximum likelihood estimation (such as `logit`, `probit`, `poisson`), z-statistics must be used to test significance. In this case, specify using the `-z` parameter based on z-statistics:

```shell
pyoneclick -d "example.dta" -a "x1" -f "i.year" -c "xtlogit yb x1 i.year c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, fe" -z
```

6. Supports `if` conditions and any other options:

```shell
pyoneclick -d "example.dta" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31 if year > 2014, absorb( stkcd year ) vce(robust)"
```

### Multiple Statistics Estimation

1. Basic multi-command estimation form. For each statistic to be significant, the program will estimate a new command separately, regardless of whether these commands are the same or different. The entire program will actually estimate a group of commands:

```shell
pyoneclick -d "example.dta" -a "x2" -f "x1" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

2. Within the same function, different independent variables may need to be made significant. A concise command can be used at this time. That is, when `-c` is the same, estimating different variables in the same command can only require inputting `-c` once. List the `-a` and `-f` parameters to be estimated sequentially, and the system will automatically infer. If the input count of a certain item is once, that parameter will be automatically copied to other commands to be estimated:

```shell
pyoneclick -d "example.dta" -a "x2" -f "x1" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

3. In functions with different dependent variables, the same independent variable may need to be made significant. A concise command can be used at this time. That is, when `-a` or `-f` is the same, meaning estimating the same variables in different commands, `-a` and `-f` can be input once or not at all. If `-a` is not input, the adjustment value from the first command will infer all commands' adjustment values; if `-f` is not input, it means no variables are locked in all commands:

```shell
pyoneclick -d "example.dta" -a "x1" -c "reghdfe y1 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -c "reghdfe y2 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

4. If you need to set empty `-f` in multiple variable estimations, use a space `" "` enclosed in quotes as a placeholder:

```shell
pyoneclick -d "example.dta" -a "x1" -f "x2" -a "x1" -f " " -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

5. When estimating multiple commands, you can set the significance threshold through `-t`. Setting this parameter helps achieve the desired significant results for all commands:

```shell
pyoneclick -d "example.dta" -a "x1" -c "reghdfe y1 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -c "reghdfe y2 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -t 0.05
```

6. In group estimation, t-statistics and z-statistics cannot be mixed:

```shell
# Wrong!
pyoneclick -d "example.dta" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -a "x1" -f "i.year" -c "xtlogit yb x1 i.year c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, fe" -z 
```


### Advanced Features

1. Set search-related parameters. The search algorithm of this command is based on simulated annealing, so you can set relevant parameters of simulated annealing to optimize the convergence curve:

```shell
pyoneclick -d "example.dta" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" --iterations 5 --initial_temperature 1e2 --min_temperature 1e-8 --cooling_rate 0.90 --max_steps 200
```

2. Add the `-p` parameter to print debugging information. The debugging information contains the actual splitting effect of the command, helping to determine whether the code has achieved the expected effect:

```shell
pyoneclick -d "example.dta" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -p
```