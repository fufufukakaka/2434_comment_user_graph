# 2434_comment_user_graph

にじさんじの配信についたコメントのユーザを取得して、ユーザがどの配信者の動画にコメントしたかによってエッジをはったとみなす。

- Get video list and comment data
- extract user id in comments
- Using commented user id data, construct graph data(node; channel, edge; commented user id)
