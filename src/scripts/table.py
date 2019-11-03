from csv import DictReader
import sys
import os

# Script to generate a Latex table of the multibeta results, TODO adapt to changed output format

step_size = 2
columns = 4
table_x_sep = '0.64mm'
table_y_stretch = '1.1'

fieldnames = ['beta', 'k', 'cost']
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

        a_substrings = []
        e_substrings = []
        a_data, a_zero = algo_data(os.path.join(directory, f'{instance}.atsp.a'))
        e_data, e_zero = algo_data(os.path.join(directory, f'{instance}.atsp.e'))
        for a, e in zip(a_data, e_data):
            if a['cost'] < e['cost']:
                a['cost'] = f'\\textbf{{{a["cost"]:.2f}}}'
                e['cost'] = f'{e["cost"]:.2f}'
            elif e['cost'] < a['cost']:
                e['cost'] = f'\\textbf{{{e["cost"]:.2f}}}'
                a['cost'] = f'{a["cost"]:.2f}'
            else:
                a['cost'] = f'{a["cost"]:.2f}'
                e['cost'] = f'{e["cost"]:.2f}'

            if a['k'] < e['k']:
                a['k'] = f'\\textbf{{{a["k"]}}}'
            elif e['k'] < a['k']:
                e['k'] = f'\\textbf{{{e["k"]}}}'

            a_substrings += [f' & {a["k"]}/{a["cost"]}']
            e_substrings += [f' & {e["k"]}/{e["cost"]}']

        if a_zero['cost'] < e_zero['cost']:
            a_zero['cost'] = f'\\textbf{{{a_zero["cost"]:.2f}}}'
            e_zero['cost'] = f'{e_zero["cost"]:.2f}'
        elif e_zero['cost'] < a_zero['cost']:
            e_zero['cost'] = f'\\textbf{{{e_zero["cost"]:.2f}}}'
            a_zero['cost'] = f'{a_zero["cost"]:.2f}'
        else:
            a_zero['cost'] = f'{a_zero["cost"]:.2f}'
            e_zero['cost'] = f'{e_zero["cost"]:.2f}'

        substrings += e_substrings
        substrings += [f' & {e_zero["cost"]}']
        substrings += a_substrings
        substrings += [f' & {a_zero["cost"]}']
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
        all_data = list(DictReader(f, fieldnames=fieldnames, delimiter=' '))[:-1]
    opt = all_data[0]
    zero = all_data[-1]

    all_data = all_data[1:]
    all_data = all_data[:data_points]
    all_data += [zero] * (data_points - len(all_data))  # pad all_data with zero
    all_data = all_data[::step_size]

    for data in all_data:
        data['cost'] = round(int(data["cost"]) / int(opt["cost"]), 2)
        data['k'] = int(data["k"])
    zero['cost'] = round(int(zero["cost"]) / int(opt["cost"]), 2)
    return all_data, zero


if __name__ == '__main__':
    main()
