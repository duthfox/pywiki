from flask_admin import BaseView, expose

class ItemView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/item.html')