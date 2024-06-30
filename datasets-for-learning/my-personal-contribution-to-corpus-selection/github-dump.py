import os
import aiohttp
import asyncio
import sqlite3

GITHUB_API_URL = "https://api.github.com/graphql"
TOKEN = os.getenv("GH_ACCESS_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# SQL Queries to create tables
CREATE_REPOS_TABLE = """
CREATE TABLE IF NOT EXISTS repositories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    url TEXT,
    description TEXT,
    created_at TEXT,
    updated_at TEXT
);
"""

CREATE_DISCUSSIONS_TABLE = """
CREATE TABLE IF NOT EXISTS discussions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_name TEXT,
    discussion_number INTEGER,
    title TEXT,
    created_at TEXT,
    author TEXT,
    FOREIGN KEY(repo_name) REFERENCES repositories(name)
);
"""

CREATE_COMMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discussion_number INTEGER,
    comment_id TEXT,
    body TEXT,
    created_at TEXT,
    author TEXT,
    FOREIGN KEY(discussion_number) REFERENCES discussions(discussion_number)
);
"""

CREATE_REPLIES_TABLE = """
CREATE TABLE IF NOT EXISTS replies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment_id TEXT,
    reply_id TEXT,
    body TEXT,
    created_at TEXT,
    author TEXT,
    FOREIGN KEY(comment_id) REFERENCES comments(comment_id)
);
"""

CREATE_ISSUES_TABLE = """
CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_name TEXT,
    issue_number INTEGER,
    title TEXT,
    body TEXT,
    created_at TEXT,
    updated_at TEXT,
    author TEXT,
    state TEXT,
    FOREIGN KEY(repo_name) REFERENCES repositories(name)
);
"""

CREATE_PULL_REQUESTS_TABLE = """
CREATE TABLE IF NOT EXISTS pull_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_name TEXT,
    pr_number INTEGER,
    title TEXT,
    body TEXT,
    created_at TEXT,
    updated_at TEXT,
    author TEXT,
    state TEXT,
    FOREIGN KEY(repo_name) REFERENCES repositories(name)
);
"""

REPO_QUERY = """
query($owner: String!, $cursor: String) {
  organization(login: $owner) {
    repositories(first: 100, after: $cursor) {
      totalCount
      edges {
        node {
          name
          url
          description
          createdAt
          updatedAt
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
  user(login: $owner) {
    repositories(first: 100, after: $cursor) {
      totalCount
      edges {
        node {
          name
          url
          description
          createdAt
          updatedAt
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
"""

DISCUSSION_QUERY = """
query($owner: String!, $repo: String!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    discussions(first: 100, after: $cursor) {
      totalCount
      edges {
        node {
          number
          title
          createdAt
          author {
            login
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
"""

COMMENTS_QUERY = """
query($owner: String!, $repo: String!, $discussionNumber: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    discussion(number: $discussionNumber) {
      comments(first: 100, after: $cursor) {
        edges {
          node {
            id
            body
            createdAt
            author {
              login
            }
            replies(first: 100) {
              edges {
                node {
                  id
                  body
                  createdAt
                  author {
                    login
                  }
                }
              }
            }
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
}
"""

ISSUES_QUERY = """
query($owner: String!, $repo: String!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    issues(first: 100, after: $cursor, states: OPEN) {
      totalCount
      edges {
        node {
          number
          title
          body
          createdAt
          updatedAt
          author {
            login
          }
          state
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
"""

PULL_REQUESTS_QUERY = """
query($owner: String!, $repo: String!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequests(first: 100, after: $cursor, states: OPEN) {
      totalCount
      edges {
        node {
          number
          title
          body
          createdAt
          updatedAt
          author {
            login
          }
          state
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
"""

async def fetch_github_data(session, query, variables):
    print(f"Fetching data with variables: {variables}")
    async with session.post(GITHUB_API_URL, json={"query": query, "variables": variables}, headers=HEADERS) as response:
        data = await response.json()
        print(f"Received data: {data}")
        return data

def save_repositories_to_database(conn, repos):
    cursor = conn.cursor()
    for repo in repos:
        cursor.execute("INSERT OR IGNORE INTO repositories (name, url, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                       (repo["name"], repo["url"], repo["description"], repo["createdAt"], repo["updatedAt"]))
    conn.commit()

def save_discussions_to_database(conn, repo, discussions):
    cursor = conn.cursor()
    for discussion in discussions:
        cursor.execute("INSERT OR IGNORE INTO discussions (repo_name, discussion_number, title, created_at, author) VALUES (?, ?, ?, ?, ?)",
                       (repo, discussion["number"], discussion["title"], discussion["createdAt"], discussion["author"]))
    conn.commit()

def save_comments_to_database(conn, discussion_number, comments):
    cursor = conn.cursor()
    for comment in comments:
        cursor.execute("INSERT OR IGNORE INTO comments (discussion_number, comment_id, body, created_at, author) VALUES (?, ?, ?, ?, ?)",
                       (discussion_number, comment['node']['id'], comment['node']['body'], comment['node']['createdAt'], comment['node']['author']['login'] if comment['node']['author'] else "Unknown"))
        for reply in comment['node']['replies']['edges']:
            cursor.execute("INSERT OR IGNORE INTO replies (comment_id, reply_id, body, created_at, author) VALUES (?, ?, ?, ?, ?)",
                           (comment['node']['id'], reply['node']['id'], reply['node']['body'], reply['node']['createdAt'], reply['node']['author']['login'] if reply['node']['author'] else "Unknown"))
    conn.commit()

def save_issues_to_database(conn, repo, issues):
    cursor = conn.cursor()
    for issue in issues:
        cursor.execute(
            "INSERT OR IGNORE INTO issues (repo_name, issue_number, title, body, created_at, updated_at, author, state) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                repo,
                issue["number"],
                issue["title"],
                issue["body"],
                issue["createdAt"],
                issue["updatedAt"],
                issue["author"],
                issue["state"],
            ),
        )
    conn.commit()


def save_pull_requests_to_database(conn, repo, pull_requests):
    cursor = conn.cursor()
    for pr in pull_requests:
        cursor.execute(
            "INSERT OR IGNORE INTO pull_requests (repo_name, pr_number, title, body, created_at, updated_at, author, state) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                repo,
                pr["number"],
                pr["title"],
                pr["body"],
                pr["createdAt"],
                pr["updatedAt"],
                pr["author"],
                pr["state"],
            ),
        )
    conn.commit()


async def get_all_repositories(owner, conn):
    async with aiohttp.ClientSession() as session:
        repos = []
        cursor = None
        total_repos = 0
        while True:
            result = await fetch_github_data(session, REPO_QUERY, {"owner": owner, "cursor": cursor})
            if result["data"]["organization"] is not None:
                repositories = result["data"]["organization"]["repositories"]["edges"]
                total_repos = result["data"]["organization"]["repositories"]["totalCount"]
            else:
                repositories = result["data"]["user"]["repositories"]["edges"]
                total_repos = result["data"]["user"]["repositories"]["totalCount"]
            repos.extend({
                "name": repo["node"]["name"],
                "url": repo["node"]["url"],
                "description": repo["node"]["description"],
                "createdAt": repo["node"]["createdAt"],
                "updatedAt": repo["node"]["updatedAt"]
            } for repo in repositories)
            save_repositories_to_database(conn, [repo for repo in repos])
            print(f"Repositories fetched so far: {len(repos)} / {total_repos} ({len(repos) / total_repos * 100:.2f}%)")
            page_info = result["data"]["organization"]["repositories"]["pageInfo"] if result["data"]["organization"] else result["data"]["user"]["repositories"]["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            cursor = page_info["endCursor"]
        return repos, total_repos


async def get_all_discussions(owner, repo, conn):
    async with aiohttp.ClientSession() as session:
        discussions = []
        cursor = None
        total_discussions = 0
        while True:
            result = await fetch_github_data(session, DISCUSSION_QUERY, {"owner": owner, "repo": repo, "cursor": cursor})
            discussions.extend({
                "number": discussion["node"]["number"],
                "title": discussion["node"]["title"],
                "createdAt": discussion["node"]["createdAt"],
                "author": discussion["node"]["author"]["login"] if discussion["node"]["author"] else "Unknown"
            } for discussion in result["data"]["repository"]["discussions"]["edges"])
            total_discussions = result["data"]["repository"]["discussions"]["totalCount"]
            save_discussions_to_database(conn, repo, discussions)
            if total_discussions > 0:
                print(f"Discussions fetched for {repo} so far: {len(discussions)} / {total_discussions} ({len(discussions) / total_discussions * 100:.2f}%)")
            else:
                print(f"Discussions fetched for {repo} so far: {len(discussions)} / {total_discussions} (N/A)")
            page_info = result["data"]["repository"]["discussions"]["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            cursor = page_info["endCursor"]
        return discussions, total_discussions

async def get_all_comments(owner, repo, discussion_number, conn):
    async with aiohttp.ClientSession() as session:
        comments = []
        cursor = None
        while True:
            result = await fetch_github_data(session, COMMENTS_QUERY, {"owner": owner, "repo": repo, "discussionNumber": discussion_number, "cursor": cursor})
            comments.extend(result["data"]["repository"]["discussion"]["comments"]["edges"])
            save_comments_to_database(conn, discussion_number, result["data"]["repository"]["discussion"]["comments"]["edges"])
            print(f"Comments fetched for discussion {discussion_number} in {repo} so far: {len(comments)}")
            page_info = result["data"]["repository"]["discussion"]["comments"]["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            cursor = page_info["endCursor"]
        return comments

async def get_all_issues(owner, repo, conn):
    async with aiohttp.ClientSession() as session:
        issues = []
        cursor = None
        total_issues = 0
        while True:
            result = await fetch_github_data(
                session, ISSUES_QUERY, {"owner": owner, "repo": repo, "cursor": cursor}
            )
            issues.extend(
                {
                    "number": issue["node"]["number"],
                    "title": issue["node"]["title"],
                    "body": issue["node"]["body"],
                    "createdAt": issue["node"]["createdAt"],
                    "updatedAt": issue["node"]["updatedAt"],
                    "author": issue["node"]["author"]["login"]
                    if issue["node"]["author"]
                    else "Unknown",
                    "state": issue["node"]["state"],
                }
                for issue in result["data"]["repository"]["issues"]["edges"]
            )
            total_issues = result["data"]["repository"]["issues"]["totalCount"]
            save_issues_to_database(conn, repo, issues)
            if total_issues > 0:
                print(
                    f"Issues fetched for {repo} so far: {len(issues)} / {total_issues} ({len(issues) / total_issues * 100:.2f}%)"
                )
            else:
                print(
                    f"Issues fetched for {repo} so far: {len(issues)} / {total_issues} (N/A)"
                )
            page_info = result["data"]["repository"]["issues"]["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            cursor = page_info["endCursor"]
        return issues, total_issues




async def get_all_pull_requests(owner, repo, conn):
    async with aiohttp.ClientSession() as session:
        pull_requests = []
        cursor = None
        total_pull_requests = 0
        while True:
            result = await fetch_github_data(
                session,
                PULL_REQUESTS_QUERY,
                {"owner": owner, "repo": repo, "cursor": cursor},
            )
            pull_requests.extend(
                {
                    "number": pr["node"]["number"],
                    "title": pr["node"]["title"],
                    "body": pr["node"]["body"],
                    "createdAt": pr["node"]["createdAt"],
                    "updatedAt": pr["node"]["updatedAt"],
                    "author": pr["node"]["author"]["login"]
                    if pr["node"]["author"]
                    else "Unknown",
                    "state": pr["node"]["state"],
                }
                for pr in result["data"]["repository"]["pullRequests"]["edges"]
            )
            total_pull_requests = result["data"]["repository"]["pullRequests"]["totalCount"]
            save_pull_requests_to_database(conn, repo, pull_requests)
            if total_pull_requests > 0:
                print(
                    f"Pull requests fetched for {repo} so far: {len(pull_requests)} / {total_pull_requests} ({len(pull_requests) / total_pull_requests * 100:.2f}%)"
                )
            else:
                print(
                    f"Pull requests fetched for {repo} so far: {len(pull_requests)} / {total_pull_requests} (N/A)"
                )
            page_info = result["data"]["repository"]["pullRequests"]["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            cursor = page_info["endCursor"]
        return pull_requests, total_pull_requests



async def fetch_all_data(owner):
    conn = sqlite3.connect(f"{owner}_data.db")
    cursor = conn.cursor()
    cursor.execute(CREATE_REPOS_TABLE)
    cursor.execute(CREATE_DISCUSSIONS_TABLE)
    cursor.execute(CREATE_COMMENTS_TABLE)
    cursor.execute(CREATE_REPLIES_TABLE)
    cursor.execute(CREATE_ISSUES_TABLE)
    cursor.execute(CREATE_PULL_REQUESTS_TABLE)
    conn.commit()

    repos, total_repos = await get_all_repositories(owner, conn)
    all_data = {}
    total_discussions = 0
    fetched_discussions = 0
    for repo in repos:
        repo_name = repo["name"]
        discussions, repo_total_discussions = await get_all_discussions(owner, repo_name, conn)
        total_discussions += repo_total_discussions
        fetched_discussions += len(discussions)
        all_data[repo_name] = {"discussions": {}, "issues": [], "pull_requests": []}
        for discussion in discussions:
            comments = await get_all_comments(owner, repo_name, discussion["number"], conn)
            all_data[repo_name]["discussions"][discussion["number"]] = comments
            print(f"Total discussions fetched so far: {fetched_discussions} / {total_discussions} ({fetched_discussions / total_discussions * 100:.2f}%)")
        issues, total_issues = await get_all_issues(owner, repo_name, conn)
        all_data[repo_name]["issues"] = issues
        pull_requests, total_pull_requests = await get_all_pull_requests(owner, repo_name, conn)
        all_data[repo_name]["pull_requests"] = pull_requests
    conn.close()
    return all_data, total_repos, total_discussions

def main():
    owner = "openai"  # Replace with the actual owner name
    all_data, total_repos, total_discussions = asyncio.run(fetch_all_data(owner))
    print(f"Total repositories fetched: {len(all_data)} / {total_repos} ({len(all_data) / total_repos * 100:.2f}%)")
    for repo, data in all_data.items():
        print(f"Repository: {repo}, Total Discussions: {len(data['discussions'])}, Total Issues: {len(data['issues'])}, Total Pull Requests: {len(data['pull_requests'])}")
        for discussion_number, comments in data["discussions"].items():
            print(f"  Discussion #{discussion_number}, Total Comments: {len(comments)}")
            for comment in comments:
                print(f"    Comment ID: {comment['node']['id']} - {comment['node']['body']}, Total Replies: {len(comment['node']['replies']['edges'])}")

if __name__ == "__main__":
    main()
