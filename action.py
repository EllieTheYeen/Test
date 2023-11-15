#!/usr/bin/python3
import urllib.request
import argparse
import shlex
import json
import csv
import os
import re


def print_and_run(a):
    print(a)
    os.system(a)


post_regex = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-.*\.md$")

if __name__ == "__main__":
    pars = argparse.ArgumentParser()
    pars.add_argument("-name", dest="name", required=True)
    pars.add_argument("-username", dest="username", required=True)
    pars.add_argument("-gist", dest="gist", required=True)
    pars.add_argument("-email", dest="email", required=True)
    pars.add_argument("-branch", dest="branch", required=True)
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

    print(os.getcwd())

    print_and_run(f"git config --global user.name {shlex.quote(args.name)}")
    print_and_run(f"git config --global user.email {shlex.quote(args.email)}")
    print_and_run(f"git checkout -m {shlex.quote(args.branch)}")

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

    found = None
    for a in os.listdir("/_posts"):
        if not a:
            continue
        if not post_regex.match(a):
            continue
        a = a.rsplit(".", 1)[0]
        if a not in posts:
            found = a
            break
    else:
        print("No new posts found, exiting")
        exit()

    msg = (
        f"New post: {args.blogbase}/{found.replace('-', '/', 3).rsplit('.', 1)[0]}.html"
    )
    print(msg)

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
        print("error when posting")
        exit(g)

    print(f"Posted with id {g['id']!r}")

    with open(post_file, "a") as f:
        c = csv.writer(f, dialect="unix", quoting=csv.QUOTE_MINIMAL)
        c.writerow([g["id"], found])

    print_and_run(f"git add {shlex.quote(post_file)}")
    commit_msg = f"Update {post_file} with post {shlex.quote(g['url'])}"
    print_and_run(f"git commit -m {shlex.quote(commit_msg)}")
    print_and_run(f"git push origin {shlex.quote(args.branch)}")
