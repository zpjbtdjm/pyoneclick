# pyoneclick Usage

## Prerequisites

- Proficient use of the `pyoneclick` command requires substantial prior knowledge of Stata. This tutorial will use panel data estimation as an example. We assume that you are proficient in regular Stata commands, including panel estimation commands such as `reghdfe`, `xtlogit`, etc.
- If you are unfamiliar with Stata syntax or the above Stata commands, please use the `help` command in Stata to review the principles of related commands and ensure full mastery of their usage before using this program.
- We provide carefully designed sample data in the file `examples/example.dta`, which contains 31 control variables. You can download the data and try to run the commands.

## Basic Usage

The basic usage of this command is as follows:

```shell
pyoneclick [-h] [-d DATA] [-a ADJUST] [-f FIXED] [-c COMMAND] [-z] [-t THRESHOLD] [--iterations ITERATIONS] [--initial_temperature INITIAL_TEMPERATURE] [--min_temperature MIN_TEMPERATURE] [--cooling_rate COOLING_RATE] [--max_steps MAX_STEPS] [-p]
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

First, please ensure that you have installed the command and correctly set the environment variables in your Windows system. Before running the statistical estimation command for the first time, specify the `.dta` data file to use with the `-d` parameter:

```shell
pyoneclick -d "examples/example.dta"
```

You can also specify the data file at the same time as performing estimation, but note that using the `-d` parameter at any time will update the default data file for all subsequent commands.


### Simple Estimation

The simplest form of estimation. You must specify the Stata command to run via `-c`, explicitly listing all control variables; macros or shorthand notations are not allowed:

```shell
pyoneclick -c "reghdfe y1 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

The model automatically parses the dependent and independent variables and adjusts the significance of target variables by computing an optimal list of control variables.


### Single Statistic Estimation

1. Basic estimation form. The basic method is to provide the `-a` and `-f` arguments to explicitly specify the variable whose significance is to be adjusted and the variables that must be included in the regression.

```shell
pyoneclick -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

2. If the `-a` argument is not provided, the program automatically infers the variable to be adjusted as the first variable following the dependent variable:

```shell
pyoneclick -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

3. If the `-f` argument is not provided, it is assumed that there are no variables that must be included in the command:

```shell
pyoneclick -a "x1" -c "reghdfe y1 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

4. The `-c` argument must never be omitted. Omitting `-c` renders the command meaningless:

```shell
# Wrong!
pyoneclick -a "x1" -f "x2"
```

5. For models fitted via maximum likelihood estimation (e.g., `logit`, `probit`, `poisson`), significance must be tested using z-statistics. In such cases, the `-z` argument must be used to indicate that z-statistics should be used as the basis:

```shell
pyoneclick -a "x1" -f "i.year" -c "xtlogit yb x1 i.year c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, fe" -z
```

6. Supports `if` conditions and any other options:

```shell
pyoneclick -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31 if year > 2014, absorb( stkcd year ) vce(robust)"
```


### Multiple Statistics Estimation

1. Basic estimation format for multiple commands. For each variable requiring significance, the program estimates a separate new command, regardless of whether these commands are identical. In effect, the program estimates a set of commands:

```shell
pyoneclick -a "x2" -f "x1" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

2. Within the same function, when multiple independent variables need to be made significant, a simplified command can be used. Specifically, when `-c` is identical, and different variables are estimated within the same command, `-c` needs to be entered only once. List the `-a` and `-f` parameters to be estimated sequentially; the system will automatically infer them. If a parameter is provided only once, it will be automatically replicated across all other commands to be estimated:

```shell
pyoneclick -a "x2" -f "x1" -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

3. In functions with different dependent variables, the same independent variable may need to be made significant. A concise command can be used at this time. That is, when `-a` or `-f` is the same, meaning estimating the same variables in different commands, `-a` and `-f` can be input once or not at all. If `-a` is not input, the adjustment value from the first command will infer all commands' adjustment values; if `-f` is not input, it means no variables are locked in all commands:

```shell
pyoneclick -a "x1" -c "reghdfe y1 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -c "reghdfe y2 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

4. When estimating multiple variables and needing to set an empty `-f`, use a quoted space `" "` as a placeholder:

```shell
pyoneclick -a "x1" -f "x2" -a "x1" -f " " -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )"
```

5. In multi-command estimation, the significance threshold can be set using `-t`. Setting this parameter helps ensure that all commands achieve the desired level of statistical significance:

```shell
pyoneclick -a "x1" -c "reghdfe y1 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -c "reghdfe y2 x1 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -t 0.05
```

6. In group estimation, using both t-statistics and z-statistics simultaneously is not yet supported:

```shell
# Not yet supported!
pyoneclick -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -a "x1" -f "i.year" -c "xtlogit yb x1 i.year c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, fe" -z 
```


### Advanced Features

1. Set search-related parameters. The search algorithm of this command is based on simulated annealing, so you can configure simulated annealing parameters to optimize the convergence curve:

```shell
pyoneclick -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" --iterations 5 --initial_temperature 1e2 --min_temperature 1e-8 --cooling_rate 0.90 --max_steps 200
```

2. Add the `-p` parameter to print debugging information. The debug output includes the actual parsed components of the command, which helps verify whether the code behaves as expected, for example:

```shell
pyoneclick -a "x1" -f "x2" -c "reghdfe y1 x1 x2 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31, absorb( stkcd year )" -p
```

Sample output:

```shell
Command: 0 |
method: reghdfe | dependent: y1 | adjust: x1 | fixed: x2
control: c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31
others: , absorb( stkcd year )
```
