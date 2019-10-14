from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from findit import db
from findit.models import Vacancy
from findit.vacancies.forms import VacancyForm

vacancies = Blueprint('vacancies', __name__)


@vacancies.route("/vacancy/new", methods=['GET', 'vacancy'])
@login_required
def new_vacancy():
    form = VacancyForm()
    if form.validate_on_submit():
        vacancy = Vacancy(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(vacancy)
        db.session.commit()
        flash('Your vacancy has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_vacancy.html', title='New vacancy',
                           form=form, legend='New vacancy')


@vacancies.route("/vacancy/<int:vacancy_id>")
def vacancy(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)
    return render_template('vacancy.html', title=vacancy.title, vacancy=vacancy)


@vacancies.route("/vacancy/<int:vacancy_id>/update", methods=['GET', 'vacancy'])
@login_required
def update_vacancy(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)
    if vacancy.author != current_user:
        abort(403)
    form = VacancyForm()
    if form.validate_on_submit():
        vacancy.title = form.title.data
        vacancy.content = form.content.data
        db.session.commit()
        flash('Your vacancy has been updated!', 'success')
        return redirect(url_for('vacancies.vacancy', vacancy_id=vacancy.id))
    elif request.method == 'GET':
        form.title.data = vacancy.title
        form.content.data = vacancy.content
    return render_template('create_vacancy.html', title='Update Vacancy',
                           form=form, legend='Update Vacancy')


@vacancies.route("/vacancy/<int:vacancy_id>/delete", methods=['vacancy'])
@login_required
def delete_vacancy(vacancy_id):
    vacancy = Vacancy.query.get_or_404(vacancy_id)
    if vacancy.author != current_user:
        abort(403)
    db.session.delete(vacancy)
    db.session.commit()
    flash('Your vacancy has been deleted!', 'success')
    return redirect(url_for('main.home'))
