#!/usr/bin/env python3
import argparse
import subprocess
import sys

SUPPORTED_ROLES = ['default-common','timedatectl','prometheus','node-exporter','grafana','nginx']

def main():
    parser = argparse.ArgumentParser(
        description="Run Ansible Playbook or adhoc ping test"
    )
    parser.add_argument("inventory", help="Path to inventory file")
    parser.add_argument(
        "--ping",
        action="store_true",
        help="Run adhoc ping test against all hosts",
    )
    parser.add_argument(
        "--target-role",
        default="all",
        help="Target role to run (default: all)\nSupported roles: {}".format(", ".join(SUPPORTED_ROLES)),
    )
    parser.add_argument(
        "--extra-vars",
        dest="extra_vars",
        default=None,
        help="Extra vars to pass to ansible-playbook",
    )

    args = parser.parse_args()

    if args.ping:
        cmd = [
            "ansible",
            "all",
            "-i",
            args.inventory,
            "-m",
            "ping",
        ]
    else:
        cmd = [
            "ansible-playbook",
            "playbook.yml",
            "-i",
            args.inventory,
        ]

        if args.target_role and args.target_role != "all":
            target_roles = args.target_role.split(",")
            for role in target_roles:
                if role not in SUPPORTED_ROLES:
                    print(f"[ERROR] Invalid role: {role}")
                    sys.exit(1)
            cmd.extend(
                [
                    "--extra-vars",
                    "roles_to_run=[{}].format(''.join(target_roles))",
                ]
            )

        if args.extra_vars:
            cmd.extend(["--extra-vars", args.extra_vars])

    print("Executing:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
