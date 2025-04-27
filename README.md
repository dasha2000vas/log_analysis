# log_analysis

## How to add new report

- add report name to REPORT_MODES list:
```python
REPORT_MODES = ["handlers", "new_report"]
```

- write function to read line for report and function to print report:
```python
def read_line_for_new_report(line, report):
    ...

def print_new_report(report, total_count):
    ...
```

- add in  ```if __name__ == "__main__"``` block:

```python
if args.report == "handlers":
    ...
elif args.report == "new_report":
    report, total_count = get_target_report(
        args.filepath, "target_part", read_line_for_new_report
    )
    print_new_report(report, total_count)
```
