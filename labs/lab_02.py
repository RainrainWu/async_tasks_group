import logging


eg_timeout = ExceptionGroup(
    "exception group timeout",
    [
        TimeoutError("timeout error 1"),
        TimeoutError("timeout error 2"),
    ],
)

eg_value = ExceptionGroup(
    "exception group value",
    [
        ValueError("value error 1"),
        ValueError("value error 2"),
    ],
)

eg_overall = ExceptionGroup(
    "exception group overall",
    [eg_timeout, eg_value],
)

def exceptions_raised():

    raise eg_overall

def exceptions_handled():

    try:
        raise eg_overall
    except* TimeoutError as eg_timeout:
        logging.error(f"catch timeout errors {eg_timeout.exceptions}")
    except* ValueError as eg_value:
        logging.error(f"catch value errors {eg_value.exceptions}")

if __name__ == "__main__":

    # exceptions_raised()
    exceptions_handled()
