def main():
    with open("02-Red-Nosed-Reports.txt") as f:
        file_lines = f.readlines()
    
    # parse the lines
    reports = [[int(level) for level in report.split(" ")] for report in file_lines]
    print(reports)

    #safe_reports = part_1(reports)
    #print(safe_reports)

    safe_reports = part_2(reports)
    print(safe_reports)

def is_report_safe(report: list[int], problem_dampener=False, problem_dampener_index=-1) -> bool:
    scoped_report = report
    if problem_dampener and problem_dampener_index >= 0:
        if problem_dampener_index > len(scoped_report):
            return False
        scoped_report = report[:problem_dampener_index] + report[problem_dampener_index+1:]
    
    increase = scoped_report[0] < scoped_report[1]
    for i, level in enumerate(scoped_report):
        if i+1 >= len(scoped_report):
            break
        diff = level - scoped_report[i+1]
        failed = False
        if increase and not diff < 0:
            failed = True
        if not increase and not diff > 0:
            failed = True
        if not 1 <= abs(diff) <= 3:
            failed = True

        if failed:
            if problem_dampener:
                return is_report_safe(report, problem_dampener=True, problem_dampener_index=problem_dampener_index+1)
            return False
    return True

def get_safe_reports(reports: list[list[int]], problem_dampener=False) -> list[list[int]]:
    return [report for report in reports if is_report_safe(report, problem_dampener)]

def part_1(reports: list[list[int]]) -> int:
    safe_reports = get_safe_reports(reports)
    return len(safe_reports)


def part_2(reports: list[list[int]]) -> int:
    safe_reports = get_safe_reports(reports, problem_dampener=True)
    return len(safe_reports)



if __name__ == "__main__":
    main()
