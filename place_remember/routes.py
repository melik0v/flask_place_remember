from flask import (
    redirect,
    url_for,
    render_template,
    request,
    Blueprint,
)

from flask.views import View

from flask_login import (
    current_user,
    login_required,
)
from place_remember.extensions import db
from place_remember.models import Memory
from place_remember.forms import AddMemoryForm

main = Blueprint("main", __name__)


class ListView(View):
    decorators = [login_required]

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        items = {
            "memories": db.session.query(self.model)
            .filter(self.model.user_id == current_user.get_id())
            .all(),
            "user": current_user,
        }
        return render_template(self.template, **items)


class DetailView(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self, id):
        items = {
            "object": self.model.query.get_or_404(id),
            "user": current_user,
        }
        return render_template(self.template, **items)


class UpdateView(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self, id):
        memory = self.model.query.get_or_404(id)
        form = AddMemoryForm(request.form, obj=memory)

        if form.validate_on_submit() and request.method == "POST":
            form.populate_obj(memory)
            db.session.commit()
            return redirect(url_for(".memory_detail", id=id))

        items = {"object": memory, "user": current_user, "memory_form": form}
        return render_template(self.template, **items)


class CreateView(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        form = AddMemoryForm()
        if form.validate_on_submit() and request.method == "POST":
            memory = self.model(
                name=form.name.data,
                description=form.description.data,
                place=form.place.data,
                user_id=current_user.get_id(),
            )
            db.session.add(memory)
            db.session.commit()

            return redirect(url_for(".show_memories"))

        items = {"memory_form": form, "user": current_user}

        return render_template(self.template, **items)


class DeleteView(View):
    decorators = [login_required]

    methods = ["GET", "POST"]

    def __init__(self, model):
        self.model = model

    def dispatch_request(self, id):
        memory = db.session.get(self.model, id)
        db.session.delete(memory)
        db.session.commit()
        return redirect(url_for(".show_memories"))


main.add_url_rule(
    "/memories", view_func=ListView.as_view("show_memories", Memory, "memory_list.html")
)
main.add_url_rule(
    "/memories/<int:id>",
    view_func=DetailView.as_view("memory_detail", Memory, "memory_detail.html"),
)
main.add_url_rule(
    "/memories/<int:id>/edit",
    view_func=UpdateView.as_view("memory_edit", Memory, "memory_form.html"),
)
main.add_url_rule(
    "/memories/<int:id>/delete", view_func=DeleteView.as_view("memory_delete", Memory)
)
main.add_url_rule(
    "/memories/create",
    view_func=CreateView.as_view("create_memory", Memory, "memory_form.html"),
)
