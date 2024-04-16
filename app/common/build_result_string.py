import logging
import pprint
import threading
from typing import List, cast
from collections import OrderedDict
import json

from colorama import init

from nornir.core.task import AggregatedResult, MultiResult, Result


LOCK = threading.Lock()


init(autoreset=True, strip=True)


def print_title(title: str) -> None:
    """
    Helper function to print a title.
    """
    msg = "**** {} ".format(title)
    print(msg + "*" * (80 - len(msg)))


def _get_color(result: Result, failed: bool) -> str:
    """
    Returns an empty string since color output is disabled.
    """
    return ""


def _build_individual_result_string(
    result: Result,
    attrs: List[str],
    failed: bool,
    severity_level: int,
    task_group: bool = False,
    print_host: bool = False,
) -> str:
    if result.severity_level < severity_level:
        return ""


    # color = _get_color(result, failed)  <- Commented out or removed this line
    subtitle = (
        "" if result.changed is None else " ** changed : {} ".format(result.changed)
    )
    level_name = logging.getLevelName(result.severity_level)
    symbol = "v" if task_group else "-"
    host = (
        f"{result.host.name}: "
        if (print_host and result.host and result.host.name)
        else ""
    )
    msg = "{} {}{}{}".format(symbol * 4, host, result.name, subtitle)
    result_line = (
        msg + " " + level_name  # Replaced color-related formatting with a simple concatenation
    )

    attr_strings = []
    for attribute in attrs:
        x = getattr(result, attribute, "")
        if isinstance(x, BaseException):
            # for consistency between py3.6 and py3.7
            attr_strings.append(f"{x.__class__.__name__}{x.args}")
        elif x and not isinstance(x, str):
            if isinstance(x, OrderedDict):
                attr_strings.append(json.dumps(x, indent=2))
            else:
                attr_strings.append(pprint.pformat(x, indent=2))
        elif x:
            attr_strings.append(str(x))

    return "\n".join([result_line] + attr_strings)


def _build_result_string(
    result: Result,
    attrs: List[str] = None,
    failed: bool = False,
    severity_level: int = logging.INFO,
    print_host: bool = False,
) -> str:
    attrs = attrs or ["diff", "result", "stdout"]
    if isinstance(attrs, str):
        attrs = [attrs]

    if isinstance(result, AggregatedResult):
        title_line = result.name + "*" * (80 - len(result.name))  # Removed color-related formatting
        host_data_strings = [
            _build_result_string(host_data, attrs, failed, severity_level)
            for host, host_data in sorted(result.items())
        ]
        return "\n".join([title_line] + host_data_strings)

    elif isinstance(result, MultiResult):
        if result[0].name == "write_file":
            # Skip processing the "write_file" task results

            return ""
        task_group_string = _build_individual_result_string(
            result[0],
            attrs,
            failed,
            severity_level,
            task_group=True,
            print_host=print_host,
        )
        sub_result_strings = [
            _build_result_string(r, attrs, failed, severity_level)
            for r in result[1:]
        ]
        end_marker = (
            "^^^^ END " + result[0].name + "^" * (80 - len("^^^^ END " + result[0].name))
            if result[0].severity_level >= severity_level
            else ""
        )
        return "\n".join([task_group_string] + sub_result_strings + [end_marker])

    elif isinstance(result, Result):
        if result.name == "write_file":
            # Skip processing the "write_file" task results

            return ""
        return _build_individual_result_string(
            result, attrs, failed, severity_level, print_host=print_host
        )


def build_result_string(
    result: Result,
    vars: List[str] = None,
    failed: bool = False,
    severity_level: int = logging.INFO,
) -> str:
    """
    Builds a string representation of a `nornir.core.task.Result` object.

    Arguments:
      result: from a previous task
      vars: Which attributes you want to include in the string
      failed: if ``True`` assume the task failed
      severity_level: Include only errors with this severity level or higher
    """
    return _build_result_string(result, vars, failed, severity_level, print_host=True)