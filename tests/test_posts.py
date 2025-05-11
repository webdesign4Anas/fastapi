from app import schemas
def test_all_posts(authorized_client,test_posts):
    res=authorized_client.get("/posts")
    def validate(post):
        return schemas.PostOut(**post)
    post_map=map(validate,res.json())
    posts=list(post_map)
    print(posts)

def test_unauthorize_all_posts(client,test_posts):
    res=client.get("/posts")
    assert res.status_code==401

def test_unauthorize_one_posts(client,test_posts):
    res=client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code==401

            
def test_one_post_not_exist(authorized_client,test_posts):
    res=authorized_client.get("/posts/50000")
    assert res.status_code==404

def test_authorize_one_posts(authorized_client,test_posts):
    res=authorized_client.get(f"/posts/{test_posts[0].id}")
    post=schemas.PostOut(**res.json())
    assert res.status_code==200
    assert post.post.title==test_posts[0].title


def test_create_post(authorized_client,test_posts):
    res=authorized_client.post("/posts",json={"title":"forth","content":"forthh","published":"True"})
    new_post=schemas.Post(**res.json())
    assert res.status_code==201
    assert new_post.id==4

def test_create_post_default_published_true(authorized_client,test_posts,test_user):
    res=authorized_client.post("/posts",json={"title":"forth","content":"forthh"})
    new_post=schemas.Post(**res.json())
    assert res.status_code==201
    assert new_post.id==4
    assert new_post.published==True
    assert new_post.owner.id==test_user['id']

def test_un_authorized_create_post(client,test_posts):
    res=client.post("/posts",json={"title":"forth","content":"forthh","published":"True"})
    assert res.status_code==401
    


def test_un_authorized_delete_post(client,test_posts):
    res=client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code==401


def test_authorized_delete_post(authorized_client,test_posts):
    res=authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code==204


def test_delete_post_not_exist(authorized_client):
    res=authorized_client.delete("/posts/50")
    assert res.status_code==404