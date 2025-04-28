# log_analysis

## How to add new report

- write function to read line for report, function to
  concatenate report data from different files and 
  function to print report:
```python
def read_line_for_new_report(line, report):
    ...

def concatenate_new_report(data):
    ...

def print_new_report(report, total_count):
    ...
```

- add report name and info to REPORT_MODES list:
```python
REPORT_MODES = {
    ...
    "new_report": {
        "target_part": "target_part_of_app",
        "read_line": read_line_for_new_report,
        "concatenate": concatenate_new_report,
        "print_report": print_new_report,
    }
}
```
