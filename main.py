import re
from argparse import ArgumentParser
from multiprocessing import managers, Manager, Process
from typing import Callable

HEADNOTE = ["HANDLER", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def run_multiprocessing(
    filepaths: list[str], target_part: str, read_line: Callable, concatenate: Callable
) -> tuple[dict[str, dict[str, int]], int]:
    """
    Runs new process and generates report
    for each file, concatenates result.

    Args:
    filepaths (list[str]): List of filepaths.
    target_part (str): Target part of app.
    read_line (Callable): Read line function.
    concatenate (Callable): Concatenate function.

    Returns:
        report (dict[str, dict[str, int]]): Ready report.
        total_count (int): Total count of target lines.
    """
    with Manager() as manager:
        return_dict: managers.DictProxy = manager.dict()
        processes: list[Process] = [
            Process(
                target=get_target_report,
                args=[
                    filepath,
                    target_part,
                    read_line,
                    return_dict,
                ],
            )
            for filepath in filepaths
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join()
        try:
            error = return_dict["error"]
            raise error[0](error[1])
        except KeyError:
            pass
        return concatenate_data(return_dict.values(), concatenate)


def get_target_report(
    filepath: str,
    target_part: str,
    get_report: Callable,
    return_dict: managers.DictProxy,
) -> None:
    """
    Counts total number of all target logs in one
    target file. Generates report for this file.

    Args:
        filepath (str): Log path.
        target_part (str): Target part of app.
        get_report (Callable): Function to get report.
        return_dict (DictProxy): Return dictionary.
    """
    report: dict[str, dict[str, int]] = {
        "total": {
            "debug": 0,
            "info": 0,
            "warning": 0,
            "error": 0,
            "critical": 0,
        }
    }
    total_count: int = 0
    try:
        with open(filepath) as file:
            for line in file:
                if target_part in line:
                    report = get_report(line, report)
                    total_count += 1
    except FileNotFoundError:
        return_dict["error"] = [
            FileNotFoundError,
            f"File with path {filepath} not found",
        ]
    return_dict[filepath] = [report, total_count]


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
    handlers["total"][level.lower()] += 1
    return handlers


def concatenate_data(
    data: list[list[dict[str, dict[str, int]], int]], concatenate: Callable
) -> tuple[dict[str, dict[str, int]], int]:
    """
    Concatenates data into one dictionary.

    Args:
        data (list[list[dict[str, dict[str, int]]], int]): List of data.
        concatenate (Callable): Concatenate function.

    Returns:
        data (tuple[dict[str, dict[str, int]], int]): Concatenated data.
    """
    return concatenate(data)


def concatenate_handlers(
    data: list[list[dict[str, dict[str, int]], int]],
) -> tuple[dict[str, dict[str, int]], int]:
    """
    Concatenate functions for handlers.

    Args:
    data (list[list[dict[str, dict[str, int]]], int]): List of data.

    Returns:
        handlers (dict[str, dict[str, int]]): Updated dict of handlers.
        total_count (int): Total count of target lines.
    """
    handlers: dict[str, dict[str, int]] = data[0][0]
    total_count: int = data[0][1]
    data.pop(0)
    for file in data:
        for key, value in file[0].items():
            handlers[key]["debug"] += value["debug"]
            handlers[key]["info"] += value["info"]
            handlers[key]["warning"] += value["warning"]
            handlers[key]["error"] += value["error"]
            handlers[key]["critical"] += value["critical"]
        total_count += file[1]
    return handlers, total_count


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
            f"{"" if handler_name == "total" else handler_name:25}"
            f"{handlers[handler_name]["debug"]:<10d}"
            f"{handlers[handler_name]["info"]:<10d}"
            f"{handlers[handler_name]["warning"]:<10d}"
            f"{handlers[handler_name]["error"]:<10d}"
            f"{handlers[handler_name]["critical"]:<10d}"
        )


REPORT_MODES = {
    "handlers": {
        "target_part": "django.request",
        "read_line": read_line_for_handler_report,
        "concatenate": concatenate_handlers,
        "print_report": print_handler_report,
    },
}

if __name__ == "__main__":
    parser = ArgumentParser(description="Analyzes log files")
    parser.add_argument("filepath", nargs="+", help="Path to log file or files")
    parser.add_argument(
        "-r",
        "--report",
        choices=REPORT_MODES.keys(),
        default="handlers",
        help="Report mode",
    )
    args = parser.parse_args()

    if args.report in REPORT_MODES.keys():
        report, total_count = run_multiprocessing(
            args.filepath,
            REPORT_MODES[args.report]["target_part"],
            REPORT_MODES[args.report]["read_line"],
            REPORT_MODES[args.report]["concatenate"],
        )
        REPORT_MODES[args.report]["print_report"](report, total_count)
    else:
        raise ValueError(f"Report mode {args.report} is not supported.")
