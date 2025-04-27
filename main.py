import re
from argparse import ArgumentParser
from typing import Callable

REPORT_MODES = ["handlers"]
HEADNOTE = ["HANDLER", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def get_target_report(
    filepaths: list[str], target_part: str, get_report: Callable
) -> tuple[dict[str, dict[str, int]], int]:
    """
    Counts total number of all target logs.
    Generates report.

    Args:
        filepaths (list[str]): List of log paths.
        target_part (str): Target part.
        get_report (Callable): Function to get report.

    Returns:
        report (dict[str, dict[str, int]]): Dict of target stuff.
        total_count (int): Total number of target logs.
    """
    report: dict[str, dict[str, int]] = {}
    total_count: int = 0
    for filepath in filepaths:
        try:
            with open(filepath) as file:
                for line in file:
                    if target_part in line:
                        report = get_report(line, report)
                        total_count += 1
        except FileNotFoundError:
            raise FileNotFoundError(f"File with path {filepath} not found")
    return report, total_count


def read_line_for_handler_report(
    line: str, handlers: dict[str, dict[str, int]]
) -> dict[str, dict[str, int]]:
    """
    Adds handler to dict.

    Args:
        line (str): Target log line.
        handlers (dict[str, dict[str, int]]): Dict of handlers.

    Returns:
        handlers (dict[str, dict[str, int]]): Updated dict of handlers.
    """
    handler_name: str = re.findall(r"/.*/", line)[0]
    if handler_name not in handlers:
        handlers[handler_name] = {
            "debug": 0,
            "info": 0,
            "warning": 0,
            "error": 0,
            "critical": 0,
        }
    level: str = re.findall(
        r"debug|info|warning|error|critical", line, flags=re.IGNORECASE
    )[0]
    handlers[handler_name][level.lower()] += 1
    return handlers


def print_handler_report(handlers: dict[str, dict[str, int]], total_count: int) -> None:
    """
    Prints report for handlers in console.

    Args:
        handlers (dict[str, dict[str, int]]): Dict of handlers.
        total_count (int): Total number of log handlers.
    """
    print(f"Total requests: {total_count}")
    print()
    print(
        f"{HEADNOTE[0]:25}{HEADNOTE[1]:10}"
        f"{HEADNOTE[2]:10}{HEADNOTE[3]:10}"
        f"{HEADNOTE[4]:10}{HEADNOTE[5]:10}"
    )
    for handler_name in sorted(list(handlers)):
        print(
            f"{handler_name:25}"
            f"{handlers[handler_name]["debug"]:<10d}"
            f"{handlers[handler_name]["info"]:<10d}"
            f"{handlers[handler_name]["warning"]:<10d}"
            f"{handlers[handler_name]["error"]:<10d}"
            f"{handlers[handler_name]["critical"]:<10d}"
        )


if __name__ == "__main__":
    parser = ArgumentParser(description="Analyzes log files")
    parser.add_argument("filepath", nargs="+", help="Path to log file or files")
    parser.add_argument(
        "-r", "--report", choices=REPORT_MODES, default="handlers", help="Report mode"
    )
    args = parser.parse_args()

    if args.report not in REPORT_MODES:
        raise ValueError(f"Report mode {args.report} is not supported.")
    if args.report == "handlers":
        handlers, total_count = get_target_report(
            args.filepath, "django.request", read_line_for_handler_report
        )
        print_handler_report(handlers, total_count)
