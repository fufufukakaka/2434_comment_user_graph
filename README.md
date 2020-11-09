# 2434_comment_user_graph

にじさんじの配信についたコメントのユーザを取得して、ユーザがどの配信者の動画にコメントしたかによってエッジをはったとみなす。

- Get video list and comment data
- extract user id in comments
- Using commented user id data, construct graph data(node; channel, edge; commented user id)

https://qiita.com/fufufukakaka/items/9f73389e0ea0ba95307c

本リポジトリはこのqiita記事に対応しています。prefixで番号が振っており、記事中で言及している処理の順番と概ね対応しています。
