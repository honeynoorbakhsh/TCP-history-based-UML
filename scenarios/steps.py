from scenarios.scn_stuffs import scn_check, monkey_patch, SCNException


def validate_product_data():
    pass


def save_product_to_database():
    pass


def validate_order_data():
    pass


def deduct_inventory():
    pass


def save_order_to_database():
    pass


def retrieve_products_from_database():
    pass


@scn_check("Bearer ...")
def check_credentials():
    pass


#@scn_check("Bearer ...")
def generate_session_token():
    pass


def check_if_user_exists():
    pass


def create_user():
    pass


def send_confirmation_email():
    pass

@scn_check("Bearer ...")
def forbidden():
    pass


def check_two_factor_auth_code():
    pass


def update_failed():
    pass


def update_user_profile():
    pass


def raise_bad_request():
#    raise SCNException()
    pass


def update_inventory():
    pass
