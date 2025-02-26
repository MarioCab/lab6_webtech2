from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from model.categories_table import CategoriesTable

class AddCategoryForm(FlaskForm):
    name = StringField("Name:")
    submit = SubmitField("Add Category")

    def validate_name(form, field):
        valid, message = CategoriesTable.validate_name(field.data)
        if not valid:
            raise ValidationError(message)


class DeleteCategoryButton(FlaskForm):
    category_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Delete")
