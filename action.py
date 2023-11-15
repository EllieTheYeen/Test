#!/usr/bin/python3
import urllib.request
import argparse
from shlex import quote as q
import json
import csv
import os
import re


def print_and_run(a):
    print(a, flush=True)
    os.system(a)


post_regex = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-.*\.md$")

if __name__ == "__main__":
    pars = argparse.ArgumentParser()
    pars.add_argument("-name", dest="name", required=True)
    pars.add_argument("-username", dest="username", required=True)
    pars.add_argument("-gist", dest="gist", required=True)
    pars.add_argument("-email", dest="email", required=True)
    pars.add_argument("-branch1", dest="branch1", required=True)
    pars.add_argument("-branch2", dest="branch2", required=True)
    pars.add_argument("-instance", dest="instance", required=True)
    pars.add_argument("-blogbase", dest="blogbase", required=True)
    args = pars.parse_args()

    key = os.environ.get("MASTODON_TOKEN")
    gey = os.environ.get("GIST_TOKEN")
    if not key:
        exit(
            "MASTODON_TOKEN not found. Check your secrets and environments config for your repository"
        )

    if not gey:
        exit(
            "GIST_TOKEN not found. Check your secrets and environments config for your repository"
        )

    print(os.getcwd(), flush=True)

    print_and_run(f"git config --global user.name {q(args.name)}")
    print_and_run(f"git config --global user.email {q(args.email)}")
    print_and_run(f"git switch -f -C {q(args.branch2)}")

    post_file = "testposts.csv"
    posts = {}
    try:
        with open(post_file) as f:
            for a in csv.reader(f, dialect="unix"):
                if not a:
                    continue
                posts[a[1]] = a[0]
    except:
        pass

    print_and_run(f"git switch -f -C {q(args.branch1)}")

    found = None
    for a in os.listdir("_posts"):
        if not a:
            continue
        if not post_regex.match(a):
            continue
        a = a.rsplit(".", 1)[0]
        if a not in posts:
            found = a
            break
    else:
        print("No new posts found, exiting", flush=True)
        exit()

    print_and_run(f"git switch -f -C {q(args.branch2)}")
    print_and_run(f"git pull origin {q(args.branch2)} --depth 1")

    msg = (
        f"New post: {found}\n{args.blogbase}/{found.replace('-', '/', 3)}.html"
    )
    print(msg, flush=True)

    a = urllib.request.urlopen(
        urllib.request.Request(
            f"{args.instance}/api/v1/statuses",
            headers={
                "Authorization": "Bearer " + key,
                "Content-Type": "application/json",
            },
        ),
        data=json.dumps(dict(status=msg)).encode("utf-8"),
    )
    d = a.read()
    a.close()
    g = json.loads(d)

    if "id" not in g or "url" not in g:
        print("error when posting", flush=True)
        exit(g)

    print(f"Posted with id {g['id']!r}", flush=True)

    with open(post_file, "a") as f:
        c = csv.writer(f, dialect="unix", quoting=csv.QUOTE_MINIMAL)
        c.writerow([g["id"], found])

    print_and_run(f"git add {q(post_file)}")
    commit_msg = f"Update {post_file} with new post {g['id']}\n{found} {g['url']}"
    print_and_run(f"git commit -m {q(commit_msg)}")
    print_and_run(f"git push origin {q(args.branch2)}")
