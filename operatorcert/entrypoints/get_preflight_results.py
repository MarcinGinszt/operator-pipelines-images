import argparse
import logging

from operatorcert import get_preflight_result
from operatorcert.utils import store_results


def setup_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Get the test results and logs from the CI pipeline")
    parser.add_argument(
        "--pyxis-url",
        default="https://pyxis.engineering.redhat.com",
        help="Base URL for Pyxis container metadata API",
    )
    parser.add_argument(
        "--cert-project-id", help="Certification project ID", required=True
    )
    parser.add_argument(
        "--certification-hash", help="Certification bundle hash", required=True
    )
    parser.add_argument(
        "--operator-package-name", help="Operator package name", required=True
    )
    parser.add_argument(
        "--operator-package-version", help="Operator package version", required=True
    )
    parser.add_argument(
        "--cert-path", help="Path to the auth certificate (Pyxis access)", required=True
    )
    parser.add_argument(
        "--key-path", help="Path to the private auth key (Pyxis access)", required=True
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    return parser


def main() -> None:
    # Args
    parser = setup_argparser()
    args = parser.parse_args()

    # Logging
    log_level = "INFO"
    if args.verbose:
        log_level = "DEBUG"
    logging.basicConfig(level=log_level)

    # Logic
    for resource in ["test-results", "artifacts"]:
        success = get_preflight_result(args, resource)
        if not success:
            break

    # Store results
    store_results({"results_exists": str(success)})


if __name__ == "__main__":
    main()