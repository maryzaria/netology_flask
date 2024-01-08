from views import AdvertisementView

from flask import Flask


app = Flask("app")

advertisements_view = AdvertisementView.as_view("advertisements")

app.add_url_rule("/advertisements",
                 view_func=advertisements_view,
                 methods=["POST"])
app.add_url_rule("/advertisements/<int:advertisement_id>",
                 view_func=advertisements_view,
                 methods=["GET", "PATCH", "DELETE"])

if __name__ == '__main__':
    app.run()
