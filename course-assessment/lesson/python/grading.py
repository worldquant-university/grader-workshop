from grading_tools.checkers import check_submission
from grading_tools.utils import get_fixture_path, nested_get, nested_set


def fix_fixture_paths(defaults: dict) -> dict:
    """Change paths for fixtures specified in grader definition.

    Parameters
    ----------
    defaults: dict
        The dictionary associated with the ``"defaults"`` key in the grader definition.
    """
    if ("loaders" not in defaults) or ("fixtures_loaded" in defaults):
        return defaults

    for loader in defaults["loaders"]:
        # Make sure the key are there
        for key in ["file_key", "method"]:
            if key not in loader:
                raise KeyError(f"Loaders is missing a '{key}' key.")

        if nested_get(loader, ["kwargs", "fixture_path"], True):
            # Get filename
            fn_keys = loader["file_key"].split("__")
            fn = nested_get(defaults, fn_keys)

            # Get absolute path
            fn = get_fixture_path(fn)

            # Assign new path to `defaults` dict
            nested_set(defaults, fn_keys, fn)

    return defaults


def grade(defaults, submission):
    defaults = fix_fixture_paths(defaults)
    feedback = check_submission(defaults, submission)
    return feedback
