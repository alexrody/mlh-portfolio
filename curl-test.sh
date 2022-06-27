echo "GET TimelinePost"
curl --silent -X GET http://localhost:5000/api/timeline_post | jq .
echo "POST TimelinePost"
curl --silent -X POST http://localhost:5000/api/timeline_post -d "name=Alex&email=alex@mlh.io&content=Never" | jq .
curl --silent -X POST http://localhost:5000/api/timeline_post -d "name=Juan&email=juan@mlh.io&content=gonna" | jq .
curl --silent -X POST http://localhost:5000/api/timeline_post -d "name=Gino&email=gino@mlh.io&content=give" | jq .
curl --silent -X POST http://localhost:5000/api/timeline_post -d "name=Yundi&email=yundi@mlh.io&content=you" | jq .
curl --silent -X POST http://localhost:5000/api/timeline_post -d "name=Emilie&email=emilie@mlh.io&content=up" | jq .
echo "GET TimelinePost"
POSTS=$(curl --silent -X GET http://localhost:5000/api/timeline_post)
echo $POSTS | jq .
echo "DELETE TimelinePost"
echo $POSTS | jq -s ".[].timeline_posts[].id" | xargs -I %id% curl --silent -X DELETE http://localhost:5000/api/timeline_post -d "id=%id%" | jq .
unset POSTS
echo "GET TimelinePost"
curl --silent -X GET http://localhost:5000/api/timeline_post | jq .

