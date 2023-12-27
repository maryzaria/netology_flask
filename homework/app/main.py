from app import app
from views import AdvertisementView, LoginView, UserView

advertisements_view = AdvertisementView.as_view("advertisements")


app.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=["POST"])
app.add_url_rule(
    "/user",
    view_func=UserView.as_view("user"),
    methods=["GET", "POST", "PATCH", "DELETE"],
)
app.add_url_rule("/advertisements", view_func=advertisements_view, methods=["POST"])
app.add_url_rule(
    "/advertisements/<int:adv_id>",
    view_func=advertisements_view,
    methods=["GET", "PATCH", "DELETE"],
)


if __name__ == "__main__":
    app.run()
