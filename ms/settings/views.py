from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from ms.db import db_api
from ms.db.forms import OrganisationForm, UnitForm
from ms.db.models import Organisation, Unit, db

settings = Blueprint("settings", __name__)


@settings.route("setup", methods=["POST"])
def add_organisation():

    form = OrganisationForm(request.form)

    if form.validate():

        # this method is only allowed if no entry is there
        if Organisation.query.get(1):
            flash("setup already made", category="warning")
            abort(404)

        data = form.data
        del data["csrf_token"]
        db_api.add_org(data)

        flash(f"Viel erfolg beim möhrenschleudern, {data['name']}!", category="primary")
        return redirect(url_for("settings.settings_view"), 302)

    flash("setup already made", category="warning")
    return redirect(url_for("settings.settings_view"), 302)


@settings.route("/", methods=["POST", "GET"])
def settings_view():

    organisation = Organisation.query.get(1)

    if not organisation:

        form = OrganisationForm()
        return render_template("settings/setup.html", form=form)

    form = OrganisationForm(request.form, obj=organisation)

    if request.method == "POST" and form.validate():

        # Handle file upload if present
        # Use direct request.files access instead of form.logo.data to avoid WTForms file handling issues
        if 'logo' in request.files and request.files['logo'] and request.files['logo'].filename:
            file = request.files['logo']
            
            # Validate file is actually an image
            if file and allowed_file(file.filename):
                # Resize and encode the image to base64
                base64_string = resize_and_encode_image(file.stream, max_width=500, max_height=500)
                
                # Store the base64 string in the database
                organisation.logo = base64_string
                flash("Logo erfolgreich hochgeladen", category="success")
            else:
                flash("Ungültiger Dateityp für Logo", category="error")
        elif 'logo' in request.files:
            # File was submitted but no filename (empty upload)
            # Don't show warning for empty uploads when form is submitted with other changes
            pass
        
        # Update other fields from form data, excluding logo
        # This avoids conflicts with manual logo assignment
        form_data = form.data
        # Remove the logo field from form data to prevent conflicts
        if 'logo' in form_data:
            del form_data['logo']
        
        # Manually populate non-logo fields to avoid conflicts with logo field
        for field_name, value in form_data.items():
            if hasattr(organisation, field_name):
                setattr(organisation, field_name, value)
        
        db.session.commit()

        return redirect(url_for("settings.settings_view"), 302)

    units = Unit.query.all()

    return render_template("settings/settings.html", units=units, form=form)


@settings.route("/units/new", methods=["GET", "POST"])
def add_unit():

    form = UnitForm(request.form)

    if request.method == "POST" and form.validate():

        data = form.data
        del data["csrf_token"]
        db_api.add(Unit, data)

        return redirect(url_for("settings.settings_view"), 302)

    return render_template("settings/add_unit.html", form=form)


@settings.route("/unit/<int:unit_id>/edit", methods=["GET", "POST"])
def edit_unit(unit_id):

    unit = Unit.query.get_or_404(unit_id)
    unit.by_piece = str(unit.by_piece)  # dirty workaround #12
    form = UnitForm(request.form, obj=unit)
    form.populate_obj(unit)

    if request.method == "POST" and form.validate():

        db.session.commit()

        return redirect(url_for("settings.settings_view"), 302)

    return render_template("settings/edit_unit.hx.html", unit=unit, form=form)


def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def resize_and_encode_image(stream, max_width=500, max_height=500):
    """Resize image and encode to base64 string"""
    from PIL import Image
    import io
    import base64
    try:
        # Read the image from stream
        image = Image.open(stream)
        
        # Convert to RGB if necessary (handles PNG with transparency)
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        
        # Calculate new dimensions preserving aspect ratio
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Save to memory buffer
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        
        # Encode to base64
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Return as data URL
        return f"data:image/jpeg;base64,{base64_string}"
    except Exception as e:
        print(f"Error processing image: {e}")
        raise
