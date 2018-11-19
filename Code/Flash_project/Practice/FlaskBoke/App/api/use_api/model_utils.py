from App.models.user_model import BokeUserModel


def get_boke_user(user_ident):

    if not user_ident:
        return None

    # 根据id
    user = BokeUserModel.query.get(user_ident)

    if user:
        return user

    user = BokeUserModel.query.filter(BokeUserModel.u_phone == user_ident).first()

    if user:
        return user

    user = BokeUserModel.query.filter(BokeUserModel.u_email == user_ident).first()

    if user:
        return user

    return None