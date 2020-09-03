import argparse
import os
import subprocess
import sys


class BaseCommand:
    docker_repo_slug = "dullage/gunicorn"
    alpine_version = "3.12"
    python_version = "3.8"
    gunicorn_version = "20.0"

    def __init__(self, arch):
        self.arch = arch

    def build_tag(self, alpine, arch):
        return "-".join(
            item
            for item in [
                self.gunicorn_version,
                f"python{self.python_version}",
                f"alpine{self.alpine_version}" if alpine is True else None,
                arch,
            ]
            if item is not None
        )

    def build_image_name(self, alpine, arch, latest=False):
        return ":".join(
            [
                self.docker_repo_slug,
                self.build_tag(alpine=alpine, arch=arch)
                if latest is False
                else "latest",
            ]
        )

    @classmethod
    def docker_login(cls):
        command = [
            "docker",
            "login",
            "-u",
            os.environ["DOCKER_CREDENTIALS_USR"],
            "--password-stdin",
        ]
        subprocess.run(
            command,
            input=os.environ["DOCKER_CREDENTIALS_PSW"].encode("utf-8"),
            stderr=sys.stderr,
            stdout=sys.stdout,
            check=True,
        )

    def subprocess_run(self, command):
        subprocess.run(
            command, stderr=sys.stderr, stdout=sys.stdout, check=True,
        )


class BuildCommand(BaseCommand):
    dockerfile_path = os.environ["WORKSPACE"]

    def base_image_tag(self, alpine):
        if alpine is True:
            return f"{self.python_version}-alpine{self.alpine_version}"
        else:
            return self.python_version

    def command(self, alpine):
        return [
            "docker",
            "build",
            "--build-arg",
            f"BASE_IMAGE_TAG={self.base_image_tag(alpine=alpine)}",
            "--build-arg",
            f"GUNICORN_VERSION={self.gunicorn_version}.*",
            "-t",
            self.build_image_name(alpine=alpine, arch=self.arch),
            self.dockerfile_path,
        ]

    def run(self):
        self.subprocess_run(self.command(alpine=False))
        self.subprocess_run(self.command(alpine=True))


class DeployCommand(BaseCommand):
    def command(self, alpine):
        return [
            "docker",
            "push",
            self.build_image_name(alpine=alpine, arch=self.arch),
        ]

    def run(self):
        self.docker_login()
        self.subprocess_run(self.command(alpine=False))
        self.subprocess_run(self.command(alpine=True))


class ManifestsCommand(BaseCommand):
    def manifest_list(self, alpine):
        return [
            self.build_image_name(alpine=alpine, arch=arch)
            for arch in self.arch
        ]

    def manifest_create(self, manifest, images):
        return ["docker", "manifest", "create", manifest] + images

    def manifest_push(self, manifest):
        return [
            "docker",
            "manifest",
            "push",
            "--purge",
            manifest,
        ]

    def run(self):
        self.docker_login()

        manifests = {
            self.build_image_name(alpine=True, arch=None): self.manifest_list(
                alpine=True
            ),
            self.build_image_name(alpine=False, arch=None): self.manifest_list(
                alpine=False
            ),
            self.build_image_name(
                alpine=True, arch=None, latest=True
            ): self.manifest_list(alpine=True),
        }

        for manifest, manifest_list in manifests.items():
            self.subprocess_run(self.manifest_create(manifest, manifest_list))
            self.subprocess_run(self.manifest_push(manifest))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument(
        "architecure",
        metavar="architecure",
        type=str,
        help="The architecure tag to use.",
    )

    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument(
        "architecure",
        metavar="architecure",
        type=str,
        help="The architecure tag to use.",
    )

    manifest_parser = subparsers.add_parser("manifest")
    manifest_parser.add_argument(
        "architecures",
        metavar="architecures",
        nargs="+",
        type=str,
        help="The architecure tags to use.",
    )
    args = parser.parse_args()

    if args.action == "build":
        command = BuildCommand(arch=args.architecure)
    elif args.action == "deploy":
        command = DeployCommand(arch=args.architecure)
    else:  # args.action == "manifest"
        command = ManifestsCommand(arch=args.architecures)
    command.run()
