import os
from flask import Flask, render_template, redirect, url_for, flash, request,session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.orm import relationship
from flask_session import Session
from wtforms import PasswordField




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/staff_management'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db = SQLAlchemy(app)

# Staff Table
class StaffModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_name = db.Column(db.String(250), nullable=False)
    mobile = db.Column(db.String(10), nullable=False)
    mail = db.Column(db.String(250), nullable=False)
    experience = db.Column(db.String(250), nullable=False)
    staff_status = db.Column(db.String(20), default="Available", nullable=False)

# Subject Table
class SubjectModel(db.Model):
    subid = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(250), nullable=False)
    sub_status = db.Column(db.String(20), default="ACTIVE", nullable=False)

# Schedule Table
class ScheduleModel(db.Model):
    schedule_id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff_model.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject_model.subid'), nullable=False)
    schedule_status = db.Column(db.String(20), default="ACTIVE", nullable=False)
    staff = relationship('StaffModel', backref='schedules')
    subject = relationship('SubjectModel', backref='schedules')
# Staff Form
class StaffForm(FlaskForm):
    staff_name = StringField('Staff Name', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=10, max=10)])
    mail = StringField('Mail', validators=[DataRequired(), Length(max=250)])
    experience = StringField('Experience', validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('Add Staff')

# Subject Form
class SubjectForm(FlaskForm):
    s_name = StringField('Subject Name', validators=[DataRequired()])
    submit = SubmitField('Add Subject')

# Schedule Form
class SchedulefForm(FlaskForm):
    staff_id = SelectField('Staff', coerce=int, validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Schedule')

def get_staff_choices():
    return [(staff.id, staff.staff_name) for staff in StaffModel.query.all()]

def get_subject_choices():
    return [(subject.subid, subject.s_name) for subject in SubjectModel.query.all()]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    form = StaffForm()

    if form.validate_on_submit():
        new_staff = StaffModel(
            staff_name=form.staff_name.data,
            mobile=form.mobile.data,
            mail=form.mail.data,
            experience=form.experience.data
        )

        db.session.add(new_staff)
        db.session.commit()

        flash('Staff added successfully', 'success')
        return redirect(url_for('home'))

    return render_template('add_staff.html', form=form)

@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    form = SubjectForm()

    if form.validate_on_submit():
        new_sub = SubjectModel(
            s_name=form.s_name.data
        )

        db.session.add(new_sub)
        db.session.commit()

        flash('Subject added successfully', 'success')
        return redirect(url_for('home'))

    return render_template('add_subject.html', form=form)

@app.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    form = SchedulefForm()
    form.staff_id.choices = get_staff_choices()
    form.subject_id.choices = get_subject_choices()

    if form.validate_on_submit():
        schedule = ScheduleModel(
            staff_id=form.staff_id.data,
            subject_id=form.subject_id.data
        )

        db.session.add(schedule)
        db.session.commit()

        flash('Schedule added successfully', 'success')
        return redirect(url_for('home'))

    return render_template('add_schedule.html', form=form)

@app.route('/view_staff')
def view_staff():
    staff_records = StaffModel.query.all()
    return render_template('view_staff.html', staff_records=staff_records)
# ... other imports
@app.route('/view_subject')
def view_subject():
    sub_records = SubjectModel.query.all()
    return render_template('Subject.html', staff_records=sub_records)

class EditStaffForm(FlaskForm):
    staff_name = StringField('Staff Name')
    mobile = StringField('Mobile')
    mail = StringField('Mail')
    experience = StringField('Experience')
    submit = SubmitField('Update Staff')

@app.route('/edit_staff/<int:staff_id>', methods=['GET', 'POST'])
def edit_staff(staff_id):
    staff = StaffModel.query.get_or_404(staff_id)
    form = EditStaffForm(obj=staff)

    if form.validate_on_submit():
        staff.staff_name = form.staff_name.data
        staff.mobile = form.mobile.data
        staff.mail = form.mail.data
        staff.experience = form.experience.data

        db.session.commit()

        flash('Staff updated successfully', 'success')
        return redirect(url_for('view_staff'))

    return render_template('edit_staff.html', form=form)
# ... other imports

@app.route('/delete_staff/<int:staff_id>', methods=['GET', 'POST'])
def delete_staff(staff_id):
    staff = StaffModel.query.get_or_404(staff_id)

    if request.method == 'POST':
        db.session.delete(staff)
        db.session.commit()

        flash('Staff deleted successfully', 'success')
        return redirect(url_for('view_staff'))

    return render_template('delete_staff.html', staff=staff,form=FlaskForm())
# Edit Subject
class EditSubjectForm(FlaskForm):
    s_name = StringField('Subject Name', validators=[DataRequired()])
    submit = SubmitField('Update Subject')

@app.route('/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):
    subject = SubjectModel.query.get_or_404(subject_id)
    form = EditSubjectForm(obj=subject)

    if form.validate_on_submit():
        subject.s_name = form.s_name.data
        db.session.commit()

        flash('Subject updated successfully', 'success')
        return redirect(url_for('view_subject'))

    return render_template('edit_subject.html', form=form)

# Delete Subject
@app.route('/delete_subject/<int:subject_id>', methods=['GET', 'POST'])
def delete_subject(subject_id):
    subject = SubjectModel.query.get_or_404(subject_id)

    if request.method == 'POST':
        db.session.delete(subject)
        db.session.commit()

        flash('Subject deleted successfully', 'success')
        return redirect(url_for('view_subject'))

    return render_template('delete_subject.html', subject=subject, form=FlaskForm())
@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    flash('Logout successful', 'success')
    # Redirect to the home page or any other desired page
    return redirect(url_for('home'))
@app.route('/view_schedule')
def view_schedule():
    schedule_records = ScheduleModel.query.all()
    return render_template('view_schedule.html', schedule_records=schedule_records)
# Assuming you have defined your delete_schedule form
class DeleteScheduleForm(FlaskForm):
    submit = SubmitField('Delete Schedule')
@app.route('/delete_schedule/<int:schedule_id>', methods=['GET', 'POST'])
def delete_schedule(schedule_id):
    schedule = ScheduleModel.query.get_or_404(schedule_id)
    form = DeleteScheduleForm()

    if form.validate_on_submit():
        # Perform deletion
        db.session.delete(schedule)
        db.session.commit()

        flash('Schedule deleted successfully', 'success')
        return redirect(url_for('view_schedule'))  # Redirect to the schedule view page

    return render_template('delete_schedule.html', schedule=schedule, form=form)

# AdminLoginForm
class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Admin Login route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()

    if form.validate_on_submit():
        # Check the admin credentials
        if form.username.data == "admin" and form.password.data == "1234":
            # Hardcoded credentials, replace with your actual authentication logic
            # Redirect to the admin dashboard or home page on successful login
            flash('Login successful', 'success')
            return redirect(url_for('admin_home'))  # Replace 'admin_dashboard' with your actual route
        else:
            # Invalid credentials, flash an error message
            flash('Invalid credentials', 'danger')

    return render_template('admin_login.html', form=form)
@app.route('/admin_home')
def admin_home():
    # Your admin home logic here
    return render_template('admin_home.html')
class StaffLoginForm(FlaskForm):
    staff_name = StringField('Staff Name', validators=[DataRequired()])
    mobile = PasswordField('Mobile', validators=[DataRequired()])
    submit = SubmitField('Login')
@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    form = StaffLoginForm()

    if form.validate_on_submit():
        staff_name = form.staff_name.data
        mobile = form.mobile.data

        # Check the staff credentials
        staff = StaffModel.query.filter_by(staff_name=staff_name, mobile=mobile).first()

        if staff:
            name = staff.staff_name
            staff_id = staff.id
            session['uname'] = name
            session['uid'] = staff_id
            # Staff login successful, you can redirect to the staff dashboard or home page
            flash('Login successful', 'success')
            return redirect(url_for('staff_home'))  # Replace 'staff_dashboard' with your actual route
        else:
            # Invalid credentials, flash an error message
            flash('Invalid credentials', 'danger')

    return render_template('staff_login.html', form=form)
@app.route('/staff_home')
def staff_home():
    # Your Staff home logic here
    return render_template('staff_home.html')
@app.route('/view_profile')
def view_profile():
    # Retrieve staff details from the session
    staff_name = session.get('uname')
    staff_id = session.get('uid')
    staff = StaffModel.query.filter_by(id=staff_id).first()

    # Pass staff details to the profile template
    return render_template('profile.html', staff=staff)
# API to view staff schedule
@app.route('/view_Staff_schedule')
def view_Staff_schedule():
    staff_id = session.get('uid')
    schedule_records = ScheduleModel.query.filter_by(staff_id=staff_id).all()
    return render_template('view_Staff_schedule.html', schedule_records=schedule_records)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
