from contracts import Advert, User

STORAGE_ADVERTS = {
    1: Advert(
        id=1,
        title="Sell airpods",
        text="Sell white new airpods for 15$",
        author_id=1,
        published=False
    ),
    2: Advert(
        id=2,
        title="Red toyota",
        text="Red toyota, sedan, produced in 2005",
        author_id=1,
        published=False,
        moder_com="Documents are fake"
    )
}

STORAGE_USERS = {
    1: User(
        id=1,
        nickname="Seller",
        email="gooddeal@gmail.com"
    )
}
