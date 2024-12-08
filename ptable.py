def format_table(benchmarks: [str], algos: [str], results: [[int]]) -> str:
    header = "Benchmark"
    column_width = list(map(lambda x: x + 2,
                            [max(len(_) for _ in [header] + benchmarks)] + [
                                max(len(_) for _ in [algos[i]] + [str(results[j][i]) for j in range(len(benchmarks))])
                                for i in range(len(algos))]))
    first_row = f"| {header}".ljust(column_width[0] + 1) + '|'
    for i in range(len(algos)):
        first_row += f" {algos[i]}".ljust(column_width[i + 1]) + '|'
    second_row = "|" + "-" * (sum(column_width) + len(column_width) - 1) + "|"
    other_rows = []
    for j in range(len(benchmarks)):
        tmp = "| " + benchmarks[j].ljust(column_width[0] - 1) + '|'
        for k in range(len(algos)):
            tmp += f" {results[j][k]}".ljust(column_width[k + 1]) + '|'
        other_rows.append(tmp)
    return "\n".join([first_row, second_row, *other_rows])


if __name__ == "__main__":
    print(format_table(["best case", "worst case"], ["quick sort", "merge sort", "bubble sort"],
                       [[1.23, 1.56, 2.0], [3.3, 2.9, 3.9]]))
    print()
    print(format_table(["best case", "the worst case"], ["quick sort", "merge sort", "bubble sort"],
                       [[1.23, 1.56, 2.0], [3.3, 2.9, 3.9]]))
    print()
    print(format_table(['best case', 'worst case', 'middle case'],
                       ['quick sort', 'merge sort', 'bubble sort', 'bogo sort'],
                       [[1.23, 1.56, 2.0, float("inf")], [3.3, 2.9, 4., float("inf")], [3.3, 2.9, 3.9, float("inf")]]))
    print()
    print(format_table(["b", "w"], ["quick sort", "merge sort", "bubble sort"],
                       [[1.23123123123123123, 1.56, 2.0], [3.3, 2.9, 3.9]]))
