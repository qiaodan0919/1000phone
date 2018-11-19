from movie_user.models import MovieUser


def get_movie_user(user_ident):

    if not user_ident:
        return None

    # 根据id
    if isinstance(user_ident, int):
        user = MovieUser.objects.filter(id=user_ident).first()

        if user:
            return user

    user = MovieUser.objects.filter(phone=user_ident).first()

    if user:
        return user

    user = MovieUser.objects.filter(username=user_ident).first()

    if user:
        return user

    return None