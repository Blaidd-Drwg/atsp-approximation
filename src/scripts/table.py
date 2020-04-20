from csv import DictReader
import sys
import os

# Script to generate a Latex table of the multibeta results

step_size = 2
columns = 4
table_x_sep = '0.64mm'
table_y_stretch = '1.1'

instances = ['ft53', 'ft70', 'ftv170', 'ftv33', 'ftv35', 'ftv38', 'ftv44', 'ftv47', 'ftv55',
             'ftv64', 'ftv70', 'kro124p', 'p43', 'rbg323', 'rbg358', 'rbg403', 'rbg443', 'ry48p']
data_points = columns * step_size
tab_begin = r'''
\bgroup
\aboverulesep=0ex
\belowrulesep=0ex
\renewcommand{\arraystretch}{1.1}
\setlength\tabcolsep{0.64mm}
\begin{table}[htbp]
\centering
\begin{tabu}
'''
tab_end = r'''
\end{tabu}
\end{table}
\egroup
'''


def main():
    if len(sys.argv) == 1:
        print("Usage: python3 table.py resultdir")
        print("This script creates a Latex table displaying the results of multibeta experiments. The input filenames are hardcoded as '{resultdir}/{instance}.atsp.{c/t}'. The table code is printed to stdout.")
        exit()

    directory = sys.argv[1]

    substrings = []
    substrings += [tab_begin]

    substrings += ['{@{}c|']
    for _ in range(0, data_points + 2, step_size):
        substrings += ['c']
    substrings += ['|[1pt]']
    for _ in range(0, data_points + 1, step_size):
        substrings += ['c']
    substrings += ['@{}}']
    substrings += [r'\toprule']
    substrings += ['\n']

    substrings += [f'& \\multicolumn{{5}}{{c|[1pt]}}{{\\ezlk}} & \\multicolumn{{5}}{{c}}{{\\avtwo}} \\\\']
    substrings += ['\n']
    for i in list(range(data_points))[::step_size]:
        percent = round(100 * (1/2**i), 2)
        substrings += [f'&{percent:g}\\%']
    substrings += [f'& 0\\%']
    for i in list(range(data_points))[::step_size]:
        percent = round(100 * (1/2**i), 2)
        substrings += [f'&{percent:g}\\%']
    substrings += [f'& {{0\\%}}']
    substrings += [r'\\ \midrule']
    substrings += ['\n']

    for instance in instances:
        substrings += [f'{{{instance}}}']

        t_substrings = []
        c_substrings = []
        t_data, t_zero = algo_data(os.path.join(directory, f'{instance}.atsp.t'))
        c_data, c_zero = algo_data(os.path.join(directory, f'{instance}.atsp.c'))
        for a, e in zip(t_data, c_data):
            if a['tour_cost'] < e['tour_cost']:
                a['tour_cost'] = f'\\textbf{{{a["tour_cost"]:.2f}}}'
                e['tour_cost'] = f'{e["tour_cost"]:.2f}'
            elif e['tour_cost'] < a['tour_cost']:
                e['tour_cost'] = f'\\textbf{{{e["tour_cost"]:.2f}}}'
                a['tour_cost'] = f'{a["tour_cost"]:.2f}'
            else:
                a['tour_cost'] = f'{a["tour_cost"]:.2f}'
                e['tour_cost'] = f'{e["tour_cost"]:.2f}'

            if a['kernel_size'] < e['kernel_size']:
                a['kernel_size'] = f'\\textbf{{{a["kernel_size"]}}}'
            elif e['kernel_size'] < a['kernel_size']:
                e['kernel_size'] = f'\\textbf{{{e["kernel_size"]}}}'

            t_substrings += [f' & {a["kernel_size"]}/{a["tour_cost"]}']
            c_substrings += [f' & {e["kernel_size"]}/{e["tour_cost"]}']

        if t_zero['tour_cost'] < c_zero['tour_cost']:
            t_zero['tour_cost'] = f'\\textbf{{{t_zero["tour_cost"]:.2f}}}'
            c_zero['tour_cost'] = f'{c_zero["tour_cost"]:.2f}'
        elif c_zero['tour_cost'] < t_zero['tour_cost']:
            c_zero['tour_cost'] = f'\\textbf{{{c_zero["tour_cost"]:.2f}}}'
            t_zero['tour_cost'] = f'{t_zero["tour_cost"]:.2f}'
        else:
            t_zero['tour_cost'] = f'{t_zero["tour_cost"]:.2f}'
            c_zero['tour_cost'] = f'{c_zero["tour_cost"]:.2f}'

        substrings += c_substrings
        substrings += [f' & {c_zero["tour_cost"]}']
        substrings += t_substrings
        substrings += [f' & {t_zero["tour_cost"]}']
        substrings += ['\n']
        substrings += [r' \\']
        substrings += ['\n']
    substrings += [r'\bottomrule']
    substrings += [tab_end]

    if len(sys.argv) >= 3 and sys.argv[2] == '--doc':
        print(r' \documentclass[11pt]{article} \usepackage{multirow} \usepackage{makecell} \usepackage{tabu} \usepackage{booktabs} \newcommand{\ezlk}{EZLK} \newcommand{\avtwo}{Tree Based Approximation} \begin{document}')
        print(''.join(substrings))
        print(r'\end{document}')
    else:
        print(''.join(substrings))


def algo_data(algo_file):
    with open(algo_file) as f:
        all_data = list(DictReader(f, delimiter=',', skipinitialspace=True))[:-1]
    opt = all_data[0]
    zero = all_data[-1]

    all_data = all_data[1:]
    all_data = all_data[:data_points]
    all_data += [zero] * (data_points - len(all_data))  # pad all_data with zero
    all_data = all_data[::step_size]

    for data in all_data:
        data['tour_cost'] = round(int(data["tour_cost"]) / int(opt["tour_cost"]), 2)
        data['kernel_size'] = int(data["kernel_size"])
    zero['tour_cost'] = round(int(zero["tour_cost"]) / int(opt["tour_cost"]), 2)
    return all_data, zero


if __name__ == '__main__':
    main()
