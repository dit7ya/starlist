from gql import gql, Client, AIOHTTPTransport
import json

import os

GITHUB_TOKEN = os.environ.get("GH_TOKEN")

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(
    url="https://api.github.com/graphql",
    headers={"Authorization": "bearer {}".format(GITHUB_TOKEN)},
)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)


edges = []

# Provide a GraphQL query
query = gql(
    """
    query getStarredRepos
        {
          user(login: "dit7ya") {
            starredRepositories(first: 100) {
                pageInfo {
                        hasNextPage
                        endCursor
                    }
              edges {
                starredAt
                node {
                  id
                  descriptionHTML
                  description
                  name
                  nameWithOwner
                  stargazerCount
                  url
                  updatedAt
                    primaryLanguage {
                                name
                            }
                            repositoryTopics(first: 30) {
                                nodes {
                                topic {
                                    name
                                }
                                }
                            }
                }
              }
            }
          }
        }
"""
)

# Execute the query on the transport
result = client.execute(query)  # this is a python dictionary

# Append the edges from the result to the edges list

edges += result["user"]["starredRepositories"]["edges"]

# Get the last edge's cursor

# last_edges_cursor = result["user"]["starredRepositories"]["edges"][-1]["cursor"]
endCursor = result["user"]["starredRepositories"]["pageInfo"]["endCursor"]
hasNextPage = result["user"]["starredRepositories"]["pageInfo"]["hasNextPage"]

while hasNextPage:

    query = gql(
        """
        query getStarredRepos($cur: String!)
            {
            user(login: "dit7ya") {
                starredRepositories(after: $cur) {
                    pageInfo {
                            hasNextPage
                            endCursor
                        }
                edges {
                    starredAt
                    node {
                    id
                    descriptionHTML
                    description
                    name
                    nameWithOwner
                    stargazerCount
                    url
                    updatedAt
                    primaryLanguage {
                                name
                            }
                            repositoryTopics(first: 30) {
                                nodes {
                                topic {
                                    name
                                }
                                }
                            }
                    }
                }
                }
            }
            }
    """
    )
    # print(query)

    result = client.execute(query, {"cur": endCursor})

    # print(len(result["user"]["starredRepositories"]["edges"]))
    # print("running")

    edges += result["user"]["starredRepositories"]["edges"]

    endCursor = result["user"]["starredRepositories"]["pageInfo"]["endCursor"]
    hasNextPage = result["user"]["starredRepositories"]["pageInfo"]["hasNextPage"]

# Flatten the dictionaries inside the edges list

for edge in edges:
    edge.update(**edge["node"])
    edge.pop("node")
    edge["linkHTML"] = '<a href="{}">{}</a>'.format(
        edge["url"], edge["nameWithOwner"]
    )  # Add this key to the dict


with open("edges.json", "w") as f:
    json.dump(edges, f)
