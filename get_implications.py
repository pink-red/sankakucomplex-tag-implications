import json
from time import sleep

from aiohttp.client_exceptions import ClientConnectorError
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportServerError


def main():
    with open("config.json") as f:
        config = json.load(f)

    transport = AIOHTTPTransport(
        url="https://capi-v2.sankakucomplex.com/graphql",
        headers={"authorization": f"Bearer {config['auth-token']}"}
    )
    client = Client(transport=transport, execute_timeout=60)

    implications = []

    has_next_page = True
    end_cursor = ""
    while has_next_page:
        query = gql("""
          query TagImplicationConnection(
            $first: Int
            $after: Cursor
            $last: Int
            $before: Cursor
            $lang: String!
            $tagName: [String]
            $order: String
            $userName: String
            $userType: String
            $limit: Int
            $sortBy: String
            $sortDirection: SortDirection
            $status: [Int]
          ) {
            tagImplicationConnection(
              first: $first
              after: $after
              last: $last
              before: $before
              lang: $lang
              tagName: $tagName
              order: $order
              userName: $userName
              userType: $userType
              limit: $limit
              sortBy: $sortBy
              sortDirection: $sortDirection
              status: $status
            ) {
              totalCount
              pageInfo {
                hasNextPage
                hasPreviousPage
                startCursor
                endCursor
              }
              edges {
                node {
                  id
                  predicateTag {
                    id
                    name
                    tagType
                    postCount
                    rating
                  }
                  consequentTag {
                    id
                    name
                    postCount
                    rating
                    tagType
                  }
                  status
                  score
                  creator {
                    id
                    name
                  }
                  reason
                  approvers {
                    id
                    name
                  }
                  commentCount
                  likeStatus
                  requiredNumOfApprovers
                  deletedBy
                }
                cursor
              }
            }
          }
        """)
        variables = {
            "name": "",
            "order": "none",
            "userName": "",
            "userType": "ALL",
            "status": [0, 1, 2, 3],
            "sortBy": "",
            "sortDirection": None,
            "first": 10,
            "after": end_cursor,
            "lang": "en",
            "tagName": []
        }

        for i in range(10):
            try:
                result = client.execute(query, variable_values=variables)
                break
            except (TransportServerError, ClientConnectorError) as e:
                if i < 9:
                    print(424242, e)
                    sleep(10)
                    continue
                else:
                    raise

        has_next_page = result["tagImplicationConnection"]["pageInfo"]["hasNextPage"]
        end_cursor = result["tagImplicationConnection"]["pageInfo"]["endCursor"]

        implications += [x["node"] for x in result["tagImplicationConnection"]["edges"]]
        print(len(implications))
        print(implications[-1])

    with open("implications.json", "w") as f:
        json.dump(implications, f, indent=2)

if __name__ == "__main__":
    main()
