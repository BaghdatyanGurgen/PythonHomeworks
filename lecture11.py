import requests

def get_posts():
    r = requests.get(url + "posts")
    if r.status_code == 200:
        data = r.json()
        res = []
        for post in data:
            words_in_title = len(post['title'].split())
            if words_in_title <= 6:
                body_lines = len(post['body'].split('\n'))
                if body_lines <= 3:
                    res.append(post)
        return res
    return []

def create():
    post = {
        "title": "Test Title",
        "body": "This is a new post content",
        "userId": 1
    }
    r = requests.post(url + "posts", json=post)
    if r.status_code == 201:
        print("Created: ", r.json())
    else:
        print("Error creating post")

def update(post_id):
    post_update = {
        "title": "New Title",
        "body": "Updated body content for the post",
        "userId": 1
    }
    r = requests.put(url + f"posts/{post_id}", json=post_update)
    if r.status_code == 200:
        print("Updated: ", r.json())
    else:
        print(f"Failed to update post {post_id}")

def delete(post_id):
    r = requests.delete(url + f"posts/{post_id}")
    if r.status_code == 200:
        print(f"Post {post_id} deleted")
    else:
        print(f"Failed to delete post {post_id}")


url = "https://jsonplaceholder.typicode.com/"
filtered = get_posts()
if filtered:
    for p in filtered:
        print(f"Title: {p['title']}, Body: {p['body']}\n")
else :
  print("List is empty")

create()
update(1)
delete(1)
