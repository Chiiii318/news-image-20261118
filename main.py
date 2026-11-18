#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261118 bounty.

The infographic (entry.png, shipped in this repository) is a pre-made,
byte-fixed asset: this program simply copies it into the grader's output
directory as entry.png. It never generates, downloads or alters the image,
so two runs always produce byte-identical output. The image itself was
designed and rendered beforehand by generate_image.py, which is kept in
the repository for provenance only and is not run by the grader.
"""
import os
import shutil


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
