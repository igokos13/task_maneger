from flask import Blueprint, abort, redirect, render_template, request, url_for

from models.categories import (
    count_category_tasks,
    create_category,
    delete_category,
    get_category,
    list_categories,
    update_category,
)
from views.helpers import read_category_form, validate_category

categories_bp = Blueprint('categories_bp', __name__, template_folder='../templates')


@categories_bp.route('/categories')
def index():
    return render_template('categories.html', categories=list_categories(), error='')


@categories_bp.route('/categories/new', methods=['GET', 'POST'])
def create():
    category = {"name": ""}
    error = ''

    if request.method == 'POST':
        category = read_category_form()
        error = validate_category(category, list_categories())

        if not error:
            create_category(category)
            return redirect(url_for('categories_bp.index'))

    return render_template('category_form.html', category=category, error=error,
                           heading='Новая категория')


@categories_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def edit(category_id: int):
    category = get_category(category_id)
    if category is None:
        abort(404)

    error = ''

    if request.method == 'POST':
        category = read_category_form()
        error = validate_category(category, list_categories(), category_id)

        if not error:
            update_category(category_id, category)
            return redirect(url_for('categories_bp.index'))

    return render_template('category_form.html', category=category, error=error,
                           heading='Редактирование категории')


@categories_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
def delete(category_id: int):
    if get_category(category_id) is None:
        abort(404)

    if count_category_tasks(category_id) > 0:
        error = "Нельзя удалить категорию, пока в ней есть задачи."
        return render_template('categories.html', categories=list_categories(), error=error), 400

    delete_category(category_id)
    return redirect(url_for('categories_bp.index'))