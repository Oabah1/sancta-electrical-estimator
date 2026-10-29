
from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
    flash,
    abort,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "sancta-tech-local-development-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import (
        Project,
        Room,
        ElectricalPoint,
        Circuit,
        Cable,
        BOQItem,
        MaterialPrice,
        ProjectMaterial,
        ProjectCableEstimate,
    )

    @app.route("/")
    def home():
        stats = {
            "projects": Project.query.count(),
            "rooms": Room.query.count(),
            "circuits": Circuit.query.count(),
            "cables": Cable.query.count(),
            "boq_items": BOQItem.query.count(),
        }

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Dashboard | Sancta Tech</title>
            <style>
                * { box-sizing: border-box; }
                body {
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background: #0b1120;
                    color: #e5edf8;
                }
                .layout { display: flex; min-height: 100vh; }
                .sidebar {
                    width: 250px;
                    flex-shrink: 0;
                    padding: 28px 18px;
                    background: #111c32;
                    border-right: 1px solid #26344b;
                }
                .brand {
                    padding: 0 12px 26px;
                    border-bottom: 1px solid #26344b;
                }
                .brand h1 { margin: 0 0 8px; font-size: 23px; }
                .brand p { margin: 0; color: #9aabc4; font-size: 12px; line-height: 1.5; }
                .nav-title {
                    margin: 25px 12px 10px;
                    color: #8194b1;
                    font-size: 11px;
                    text-transform: uppercase;
                    letter-spacing: 1.5px;
                }
                .nav a {
                    display: block;
                    padding: 12px;
                    margin: 5px 0;
                    color: #c7d4e8;
                    text-decoration: none;
                    border-radius: 8px;
                    font-size: 14px;
                }
                .nav a.active, .nav a:hover {
                    color: white;
                    background: #1d3a68;
                }
                .nav a.active { border-left: 3px solid #60a5fa; }
                .main { flex: 1; min-width: 0; }
                .topbar {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 16px;
                    padding: 22px 32px;
                    border-bottom: 1px solid #26344b;
                    background: #101827;
                }
                .topbar span { color: #9aabc4; font-size: 13px; }
                .workspace { max-width: 1250px; margin: auto; padding: 34px 32px; }
                .eyebrow {
                    color: #60a5fa;
                    font-size: 12px;
                    text-transform: uppercase;
                    letter-spacing: 1.5px;
                }
                h2 { margin: 10px 0; font-size: 29px; }
                .intro { color: #9aabc4; line-height: 1.7; }
                .cards {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
                    gap: 18px;
                    margin-top: 28px;
                }
                .card {
                    padding: 23px;
                    background: #172338;
                    border: 1px solid #2a3951;
                    border-radius: 13px;
                }
                .card-label { color: #a8b7cc; font-size: 13px; }
                .number { margin-top: 18px; font-size: 34px; font-weight: bold; }
                .card-note { margin-top: 8px; color: #8295b1; font-size: 12px; }
                .section {
                    margin-top: 28px;
                    padding: 25px;
                    background: #172338;
                    border: 1px solid #2a3951;
                    border-radius: 13px;
                }
                .section h3 { margin-top: 0; }
                .quick-links {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
                    gap: 14px;
                }
                .quick-link {
                    display: block;
                    padding: 18px;
                    background: #202e45;
                    border: 1px solid #34445d;
                    border-radius: 9px;
                    color: #e5edf8;
                    text-decoration: none;
                }
                .quick-link:hover { border-color: #60a5fa; }
                .quick-link strong { display: block; margin-bottom: 8px; }
                .quick-link span { color: #9aabc4; font-size: 12px; line-height: 1.5; }
                .status {
                    display: inline-block;
                    padding: 6px 10px;
                    border-radius: 20px;
                    background: #143b37;
                    color: #6ee7b7;
                    font-size: 12px;
                }
                footer { padding: 24px 32px; color: #8194b1; font-size: 12px; }
                @media (max-width: 720px) {
                    .layout { display: block; }
                    .sidebar { width: 100%; padding: 18px; }
                    .brand { padding-bottom: 16px; }
                    .nav-title { margin-top: 16px; }
                    .nav { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px; }
                    .topbar { padding: 18px; }
                    .workspace { padding: 24px 18px; }
                    h2 { font-size: 24px; }
                }
            </style>
        </head>
        <body>
            <div class="layout">
                <aside class="sidebar">
                    <div class="brand">
                        <h1>⚡ Sancta Tech</h1>
                        <p>Electrical Installation<br>Design &amp; Estimation</p>
                    </div>
                    <div class="nav-title">Workspace</div>
                    <nav class="nav">
                        <a class="active" href="{{ url_for('home') }}">▦ &nbsp; Dashboard</a>
                        <a href="{{ url_for('projects') }}">▤ &nbsp; Projects</a>
                        <a href="{{ url_for('projects') }}">⌂ &nbsp; Building Design</a>
                        <a href="{{ url_for('circuits') }}">ϟ &nbsp; Circuits</a>
<a href="{{ url_for('materials') }}">▧ &nbsp; Materials</a>
<a href="{{ url_for('reports') }}">▥ &nbsp; Reports</a>
                    </nav>
                    <div class="nav-title">Company</div>
                    <nav class="nav">
                        <a href="{{ url_for('projects') }}">Project Management</a>
                    </nav>
                </aside>

                <div class="main">
                    <header class="topbar">
                        <strong>Engineering Workspace</strong>
                        <span>Sancta Tech Electrical Engineering Services</span>
                    </header>

                    <main class="workspace">
                        <div class="eyebrow">Overview</div>
                        <h2>Dashboard</h2>
                        <p class="intro">
                            Welcome to your electrical project workspace.
                            Manage projects and prepare for detailed building design and estimation.
                        </p>

                        <section class="cards">
                            <div class="card">
                                <div class="card-label">Total Projects</div>
                                <div class="number">{{ stats.projects }}</div>
                                <div class="card-note">Projects recorded</div>
                            </div>
                            <div class="card">
                                <div class="card-label">Rooms Added</div>
                                <div class="number">{{ stats.rooms }}</div>
                                <div class="card-note">Rooms across all projects</div>
                            </div>
                            <div class="card">
                                <div class="card-label">Total Circuits</div>
                                <div class="number">{{ stats.circuits }}</div>
                                <div class="card-note">Circuits recorded</div>
                            </div>
                            <div class="card">
                                <div class="card-label">Cable Types</div>
                                <div class="number">{{ stats.cables }}</div>
                                <div class="card-note">Cable types in the system</div>
                            </div>
                            <div class="card">
                                <div class="card-label">BOQ Items</div>
                                <div class="number">{{ stats.boq_items }}</div>
                                <div class="card-note">Bill of quantities entries</div>
                            </div>
                        </section>

                        <section class="section">
                            <h3>Quick Actions</h3>
                            <div class="quick-links">
                                <a class="quick-link" href="{{ url_for('projects') }}">
                                    <strong>Manage Projects →</strong>
                                    <span>Create projects, review project details and manage rooms.</span>
                                </a>
                                <a class="quick-link" href="{{ url_for('projects') }}">
                                    <strong>Building Design →</strong>
                                    <span>Open project details to continue setting up rooms.</span>
                                </a>
                            </div>
                        </section>

                        <section class="section">
                            <h3>System Status</h3>
                            <p><span class="status">Dashboard Online</span></p>
                            <p class="intro">Circuit analysis, materials and reporting links will be connected as those sections are implemented.</p>
                        </section>
                    </main>
                    <footer>© Sancta Tech Electrical Engineering Services</footer>
                </div>
            </div>
        </body>
        </html>
        """, stats=stats)

    @app.route("/projects", methods=["GET", "POST"])
    def projects():
        if request.method == "POST":
            project_name = request.form.get("project_name", "").strip()
            customer_name = request.form.get("customer_name", "").strip()
            location = request.form.get("location", "").strip()
            building_type = request.form.get("building_type", "").strip()
            floors_text = request.form.get("number_of_floors", "").strip()

            if not all([
                project_name,
                customer_name,
                location,
                building_type,
                floors_text,
            ]):
                flash("Please complete all project fields.")
                return redirect(url_for("projects"))

            try:
                floors = int(floors_text)
                if not 1 <= floors <= 200:
                    raise ValueError
            except ValueError:
                flash("Number of floors must be between 1 and 200.")
                return redirect(url_for("projects"))

            project = Project(
                project_name=project_name,
                customer_name=customer_name,
                location=location,
                building_type=building_type,
                number_of_floors=floors,
            )

            try:
                db.session.add(project)
                db.session.commit()
                flash("Project saved successfully.")
            except Exception:
                db.session.rollback()
                app.logger.exception("Unable to save project")
                flash("The project could not be saved. Check the application logs.")

            return redirect(url_for("projects"))

        all_projects = Project.query.order_by(
            Project.created_at.desc()
        ).all()

        return render_template(
            "projects.html",
            projects=all_projects,
        )

    @app.route("/projects/<int:project_id>")
    def project_detail(project_id):
        project = db.session.get(Project, project_id)

        if project is None:
            abort(404)

        rooms = Room.query.filter_by(
            project_id=project.id
        ).order_by(Room.id.asc()).all()

        electrical_points = ElectricalPoint.query.filter_by(
            project_id=project.id
        ).order_by(ElectricalPoint.id.asc()).all()

        piping_materials = ProjectMaterial.query.filter_by(
            project_id=project.id
        ).order_by(ProjectMaterial.id.asc()).all()

        piping_total = sum(item.amount for item in piping_materials)

        from app.services.cable_service import calculate_coils

        project_cable_estimates = ProjectCableEstimate.query.filter_by(
            project_id=project.id
        ).order_by(ProjectCableEstimate.id.asc()).all()

        available_cables = Cable.query.order_by(
            Cable.cable_type.asc(),
            Cable.size.asc(),
            Cable.colour.asc(),
        ).all()

        cable_estimate_rows = []
        cable_total = 0

        for estimate in project_cable_estimates:
            calculation = calculate_coils(
                estimate.required_metres,
                estimate.coil_length,
            )
            amount = calculation["number_of_coils"] * estimate.unit_price
            cable_total += amount

            cable_estimate_rows.append({
                "estimate": estimate,
                "number_of_coils": calculation["number_of_coils"],
                "supplied_metres": calculation["supplied_metres"],
                "spare_metres": calculation["spare_metres"],
                "amount": amount,
            })

        return render_template(
            "project_detail.html",
            project=project,
            rooms=rooms,
            electrical_points=electrical_points,
            piping_materials=piping_materials,
            piping_total=piping_total,
            available_cables=available_cables,
            cable_estimate_rows=cable_estimate_rows,
            cable_total=cable_total,
        )

    @app.route(
        "/projects/<int:project_id>/cable-estimates",
        methods=["POST"],
    )
    def add_project_cable_estimate(project_id):
        project = db.session.get(Project, project_id)
        if project is None:
            abort(404)

        try:
            required = float(request.form.get("required_metres", ""))
            mode = request.form.get("entry_mode", "catalogue")
            cable = None

            if mode == "catalogue":
                cable_id = int(request.form.get("cable_id", ""))
                cable = db.session.get(Cable, cable_id)
                if cable is None:
                    raise ValueError("Select a valid catalogue cable.")

                cable_type = cable.cable_type.strip()
                brand = (cable.brand or "").strip()
                size = cable.size.strip()
                colour = cable.colour.strip()
                function = (cable.function or "").strip()
                conductor_material = (cable.conductor_material or "").strip()
                insulation = (cable.insulation or "").strip()
                coil_length = float(cable.coil_length)
                price = float(cable.unit_price or 0)
            else:
                cable_type = request.form.get("manual_cable_type", "").strip()
                brand = request.form.get("manual_brand", "").strip()
                size = request.form.get("manual_size", "").strip()
                colour = request.form.get("manual_colour", "").strip()
                function = request.form.get("manual_function", "").strip()
                conductor_material = request.form.get("manual_conductor_material", "").strip()
                insulation = request.form.get("manual_insulation", "").strip()
                coil_length = float(request.form.get("manual_coil_length", ""))
                price = float(request.form.get("manual_unit_price", "0") or 0)

            if required <= 0 or coil_length <= 0 or price < 0:
                raise ValueError("Metres and coil length must be positive; price cannot be negative.")
            if not cable_type or not size or not colour:
                raise ValueError("Cable type, size and colour are required.")

            estimate = ProjectCableEstimate(
                project_id=project.id,
                cable_id=cable.id if cable else None,
                cable_type=cable_type,
                brand=brand or None,
                size=size,
                colour=colour,
                function=function or None,
                conductor_material=conductor_material or None,
                insulation=insulation or None,
                required_metres=required,
                coil_length=coil_length,
                unit_price=price,
            )
            db.session.add(estimate)
            db.session.commit()
            flash("Cable estimate added successfully.")

        except (TypeError, ValueError) as exc:
            db.session.rollback()
            flash(str(exc) or "Enter valid cable details.")
        except Exception:
            db.session.rollback()
            app.logger.exception("Unable to add project cable estimate")
            flash("Could not save the cable estimate.")

        return redirect(url_for("project_detail", project_id=project.id))


    @app.route(
        "/projects/<int:project_id>/cable-estimates/<int:estimate_id>/edit",
        methods=["POST"],
    )
    def edit_project_cable_estimate(project_id, estimate_id):
        project = db.session.get(Project, project_id)
        if project is None:
            abort(404)

        estimate = db.session.get(ProjectCableEstimate, estimate_id)
        if estimate is None or estimate.project_id != project.id:
            abort(404)

        try:
            required = float(request.form.get("required_metres", ""))
            mode = request.form.get("entry_mode", "manual")
            cable = None

            if mode == "catalogue":
                cable_id = int(request.form.get("cable_id", ""))
                cable = db.session.get(Cable, cable_id)
                if cable is None:
                    raise ValueError("Select a valid catalogue cable.")

                cable_type = cable.cable_type.strip()
                brand = (cable.brand or "").strip()
                size = cable.size.strip()
                colour = cable.colour.strip()
                function = (cable.function or "").strip()
                conductor_material = (cable.conductor_material or "").strip()
                insulation = (cable.insulation or "").strip()
                coil_length = float(cable.coil_length)
                price = float(cable.unit_price or 0)
            else:
                cable_type = request.form.get("manual_cable_type", "").strip()
                brand = request.form.get("manual_brand", "").strip()
                size = request.form.get("manual_size", "").strip()
                colour = request.form.get("manual_colour", "").strip()
                function = request.form.get("manual_function", "").strip()
                conductor_material = request.form.get("manual_conductor_material", "").strip()
                insulation = request.form.get("manual_insulation", "").strip()
                coil_length = float(request.form.get("manual_coil_length", ""))
                price = float(request.form.get("manual_unit_price", "0") or 0)

            if required <= 0 or coil_length <= 0 or price < 0:
                raise ValueError("Metres and coil length must be positive; price cannot be negative.")
            if not cable_type or not size or not colour:
                raise ValueError("Cable type, size and colour are required.")

            estimate.cable_id = cable.id if cable else None
            estimate.cable_type = cable_type
            estimate.brand = brand or None
            estimate.size = size
            estimate.colour = colour
            estimate.function = function or None
            estimate.conductor_material = conductor_material or None
            estimate.insulation = insulation or None
            estimate.required_metres = required
            estimate.coil_length = coil_length
            estimate.unit_price = price
            db.session.commit()
            flash("Cable estimate updated successfully.")

        except (TypeError, ValueError) as exc:
            db.session.rollback()
            flash(str(exc) or "Enter valid cable details.")
        except Exception:
            db.session.rollback()
            app.logger.exception("Unable to update project cable estimate")
            flash("Could not update the cable estimate.")

        return redirect(url_for("project_detail", project_id=project.id))


    @app.route(
        "/projects/<int:project_id>/cable-estimates/<int:estimate_id>/delete",
        methods=["POST"],
    )
    def delete_project_cable_estimate(project_id, estimate_id):
        project = db.session.get(Project, project_id)
        if project is None:
            abort(404)

        estimate = db.session.get(ProjectCableEstimate, estimate_id)
        if estimate is None or estimate.project_id != project.id:
            abort(404)

        try:
            db.session.delete(estimate)
            db.session.commit()
            flash("Cable estimate deleted successfully.")
        except Exception:
            db.session.rollback()
            app.logger.exception("Unable to delete project cable estimate")
            flash("Could not delete the cable estimate.")

        return redirect(url_for("project_detail", project_id=project.id))


    @app.route(
        "/projects/<int:project_id>/piping-materials",
        methods=["POST"],
    )
    def add_piping_material(project_id):
        project = db.session.get(Project, project_id)

        if project is None:
            abort(404)

        material_name = request.form.get("material_name", "").strip()
        unit = request.form.get("unit", "").strip()
        category = request.form.get("category", "Piping").strip() or "Piping"
        notes = request.form.get("notes", "").strip()

        try:
            quantity = float(request.form.get("quantity", ""))
            unit_price = float(request.form.get("unit_price", ""))

            if not material_name or not unit:
                raise ValueError("Material name and unit are required.")
            if quantity <= 0 or unit_price < 0:
                raise ValueError("Quantity must be positive and price cannot be negative.")

            item = ProjectMaterial(
                project_id=project.id,
                material_name=material_name,
                unit=unit,
                quantity=quantity,
                unit_price=unit_price,
                amount=round(quantity * unit_price, 2),
                category=category,
                notes=notes or None,
            )
            db.session.add(item)
            db.session.commit()
            flash("Piping material added successfully.")

        except (ValueError, TypeError):
            db.session.rollback()
            flash("Enter a material name, unit, positive quantity, and valid non-negative price.")
        except Exception:
            db.session.rollback()
            app.logger.exception("Unable to save piping material")
            flash("Could not save the piping material.")

        return redirect(url_for("project_detail", project_id=project.id))


    @app.route(
        "/projects/<int:project_id>/piping-materials/<int:item_id>/edit",
        methods=["POST"],
    )
    def edit_piping_material(project_id, item_id):
        project = db.session.get(Project, project_id)
        if project is None:
            abort(404)

        item = db.session.get(ProjectMaterial, item_id)
        if item is None or item.project_id != project.id:
            abort(404)

        material_name = request.form.get("material_name", "").strip()
        unit = request.form.get("unit", "").strip()
        category = request.form.get("category", "Piping").strip() or "Piping"
        notes = request.form.get("notes", "").strip()

        try:
            quantity = float(request.form.get("quantity", ""))
            unit_price = float(request.form.get("unit_price", ""))

            if not material_name or not unit:
                raise ValueError
            if quantity <= 0 or unit_price < 0:
                raise ValueError

            item.material_name = material_name
            item.unit = unit
            item.category = category
            item.notes = notes or None
            item.quantity = quantity
            item.unit_price = unit_price
            item.amount = round(quantity * unit_price, 2)

            db.session.commit()
            flash("Piping material updated successfully.")

        except (ValueError, TypeError):
            db.session.rollback()
            flash("Enter a material name, unit, positive quantity, and valid non-negative price.")
        except Exception:
            db.session.rollback()
            app.logger.exception("Unable to update piping material")
            flash("Could not update the piping material.")

        return redirect(url_for("project_detail", project_id=project.id))


    @app.route(
        "/projects/<int:project_id>/piping-materials/<int:item_id>/delete",
        methods=["POST"],
    )
    def delete_piping_material(project_id, item_id):
        project = db.session.get(Project, project_id)
        if project is None:
            abort(404)

        item = db.session.get(ProjectMaterial, item_id)
        if item is None or item.project_id != project.id:
            abort(404)

        try:
            db.session.delete(item)
            db.session.commit()
            flash("Piping material deleted successfully.")
        except Exception:
            db.session.rollback()
            app.logger.exception("Unable to delete piping material")
            flash("Could not delete the piping material.")

        return redirect(url_for("project_detail", project_id=project.id))


    @app.route(
        "/projects/<int:project_id>/rooms",
        methods=["POST"],
    )
    def add_room(project_id):
        project = db.session.get(Project, project_id)

        if project is None:
            abort(404)

        room_name = request.form.get("name", "").strip()
        room_type = request.form.get("room_type", "").strip()

        if not room_name or not room_type:
            flash("Please enter a room name and room type.")
            return redirect(
                url_for("project_detail", project_id=project.id)
            )

        def get_dimension(field):
            value = request.form.get(field, "").strip()
            if not value:
                return None
            number = float(value)
            if number <= 0:
                raise ValueError
            return number

        try:
            length = get_dimension("length")
            width = get_dimension("width")
            height = get_dimension("height")
        except ValueError:
            flash("Dimensions must be positive numbers or left blank.")
            return redirect(
                url_for("project_detail", project_id=project.id)
            )

        room = Room(
            project_id=project.id,
            name=room_name,
            room_type=room_type,
            length=length,
            width=width,
            height=height,
        )

        try:
            db.session.add(room)
            db.session.commit()
            flash("Room added successfully.")
        except Exception:
            db.session.rollback()
            app.logger.exception("Unable to save room")
            flash("The room could not be saved.")

        return redirect(
            url_for("project_detail", project_id=project.id)
        )


    @app.route(
        "/projects/<int:project_id>/electrical-points",
        methods=["POST"],
    )
    def add_electrical_point(project_id):
        project = db.session.get(Project, project_id)
        if project is None:
            abort(404)

        room_id_text = request.form.get("room_id", "").strip()
        point_type = request.form.get("point_type", "").strip()
        quantity_text = request.form.get("quantity", "1").strip()
        description = request.form.get("description", "").strip()
        load_text = request.form.get("load_watts", "").strip()

        try:
            room_id = int(room_id_text)
            room = db.session.get(Room, room_id)
            if room is None or room.project_id != project.id:
                raise ValueError

            quantity = int(quantity_text)
            if quantity < 1:
                raise ValueError

            load_watts = None
            if load_text:
                load_watts = float(load_text)
                if load_watts < 0:
                    raise ValueError

            if not point_type:
                raise ValueError

        except (ValueError, TypeError):
            flash("Check the room, point type, quantity, and load values.")
            return redirect(
                url_for("project_detail", project_id=project.id)
            )

        point = ElectricalPoint(
            project_id=project.id,
            room_id=room.id,
            point_type=point_type,
            quantity=quantity,
            description=description or None,
            load_watts=load_watts,
        )

        try:
            db.session.add(point)
            db.session.commit()
            flash("Electrical point added successfully.")
        except Exception:
            db.session.rollback()
            app.logger.exception("Unable to save electrical point")
            flash("The electrical point could not be saved.")

        return redirect(
            url_for("project_detail", project_id=project.id)
        )


    @app.route("/circuits", methods=["GET", "POST"])
    def circuits():
        projects_list = Project.query.order_by(Project.project_name.asc()).all()

        if request.method == "POST":
            try:
                project_id = int(request.form.get("project_id", ""))
                project = db.session.get(Project, project_id)
                circuit_name = request.form.get("circuit_name", "").strip()
                circuit_type = request.form.get("circuit_type", "").strip()
                cable_size = request.form.get("cable_size", "").strip()
                protection_rating = request.form.get("protection_rating", "").strip()

                connected_load = float(request.form.get("connected_load", "0"))
                route_text = request.form.get("route_length", "").strip()
                route_length = float(route_text) if route_text else None
                design_load_text = request.form.get("design_load", "").strip()
                design_load = float(design_load_text) if design_load_text else connected_load

                if project is None:
                    raise ValueError("Select a valid project.")
                if not circuit_name or not circuit_type:
                    raise ValueError("Circuit name and circuit type are required.")
                if connected_load < 0 or design_load < 0:
                    raise ValueError("Loads cannot be negative.")
                if route_length is not None and route_length < 0:
                    raise ValueError("Route length cannot be negative.")

                # Preliminary single-phase estimate at 230 V and power factor 1.0.
                # This is not a substitute for verified electrical design.
                design_current = design_load / 230.0

                circuit = Circuit(
                    project_id=project.id,
                    circuit_name=circuit_name,
                    circuit_type=circuit_type,
                    connected_load=connected_load,
                    design_load=design_load,
                    design_current=design_current,
                    cable_size=cable_size or None,
                    protection_rating=protection_rating or None,
                    route_length=route_length,
                )
                db.session.add(circuit)
                db.session.commit()
                flash("Circuit created successfully.")
                return redirect(url_for("circuits"))

            except (ValueError, TypeError) as exc:
                db.session.rollback()
                flash(str(exc) or "Please check the circuit details.")
            except Exception:
                db.session.rollback()
                app.logger.exception("Unable to save circuit")
                flash("The circuit could not be saved. Check the application log.")

        circuits_list = (
            db.session.query(Circuit, Project)
            .join(Project, Circuit.project_id == Project.id)
            .order_by(Circuit.id.desc())
            .all()
        )

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Circuits | Sancta Tech</title>
            <style>
                * { box-sizing: border-box; }
                body { margin: 0; padding: 28px; font-family: Arial, sans-serif; background: #0b1120; color: #e5e7eb; }
                main { max-width: 1200px; margin: auto; }
                h1 { margin-bottom: 8px; }
                p, .hint { color: #a8b3c7; }
                a { color: #60a5fa; }
                .panel { margin-top: 24px; padding: 20px; background: #151f32; border: 1px solid #29364d; border-radius: 12px; overflow-x: auto; }
                .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; }
                label { display: block; margin-bottom: 7px; font-weight: bold; }
                input, select { width: 100%; padding: 11px; border: 1px solid #40516b; border-radius: 6px; background: #0b1120; color: #e5e7eb; }
                button { margin-top: 16px; padding: 11px 16px; border: 0; border-radius: 6px; background: #2563eb; color: white; cursor: pointer; }
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 13px; text-align: left; border-bottom: 1px solid #29364d; white-space: nowrap; }
                th { color: #93c5fd; }
                .empty { padding: 22px 0; }
                .message { padding: 12px; margin: 12px 0; background: #142d46; border-left: 4px solid #0b7285; }
            </style>
        </head>
        <body>
            <main>
                <a href="{{ url_for('home') }}">← Back to Dashboard</a>
                <h1>Circuit Management</h1>
                <p>Create circuits for a project and review saved circuit details.</p>

                {% with messages = get_flashed_messages() %}
                    {% for message in messages %}
                        <div class="message">{{ message }}</div>
                    {% endfor %}
                {% endwith %}

                <section class="panel">
                    <h2>Create Circuit</h2>
                    {% if projects_list %}
                    <form method="POST" action="{{ url_for('circuits') }}">
                        <div class="form-grid">
                            <div>
                                <label for="project_id">Project *</label>
                                <select id="project_id" name="project_id" required>
                                    <option value="">Select project</option>
                                    {% for project in projects_list %}
                                    <option value="{{ project.id }}">{{ project.project_name }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div>
                                <label for="circuit_name">Circuit Name *</label>
                                <input id="circuit_name" name="circuit_name" required placeholder="e.g. Ground Floor Lighting">
                            </div>
                            <div>
                                <label for="circuit_type">Circuit Type *</label>
                                <select id="circuit_type" name="circuit_type" required>
                                    <option value="">Select type</option>
                                    <option>Lighting</option>
                                    <option>Socket Outlet</option>
                                    <option>Air Conditioning</option>
                                    <option>Water Heater</option>
                                    <option>Cooker</option>
                                    <option>Other</option>
                                </select>
                            </div>
                            <div>
                                <label for="connected_load">Connected Load (W)</label>
                                <input id="connected_load" name="connected_load" type="number" min="0" step="0.1" value="0">
                            </div>
                            <div>
                                <label for="design_load">Design Load (W)</label>
                                <input id="design_load" name="design_load" type="number" min="0" step="0.1" placeholder="Defaults to connected load">
                            </div>
                            <div>
                                <label for="route_length">Route Length (m)</label>
                                <input id="route_length" name="route_length" type="number" min="0" step="0.1" placeholder="Optional">
                            </div>
                            <div>
                                <label for="cable_size">Cable Size</label>
                                <input id="cable_size" name="cable_size" placeholder="e.g. 2.5 mm²">
                            </div>
                            <div>
                                <label for="protection_rating">Protection Rating</label>
                                <input id="protection_rating" name="protection_rating" placeholder="e.g. 20 A">
                            </div>
                        </div>
                        <p class="hint">Preliminary current estimate = design load ÷ 230 V, assuming single-phase supply and power factor 1.0. Confirm cable capacity, installation method, voltage drop, fault protection and protective-device coordination before using this for an installation.</p>
                        <button type="submit">Save Circuit</button>
                    </form>
                    {% else %}
                    <p>No projects exist yet. <a href="{{ url_for('projects') }}">Create a project first.</a></p>
                    {% endif %}
                </section>

                <section class="panel">
                    <h2>Saved Circuits</h2>
                    {% if circuits_list %}
                    <table>
                        <thead>
                            <tr><th>Project</th><th>Circuit</th><th>Type</th><th>Connected Load (W)</th><th>Design Current (A)</th><th>Cable Size</th><th>Protection</th><th>Route (m)</th></tr>
                        </thead>
                        <tbody>
                            {% for circuit, project in circuits_list %}
                            <tr>
                                <td>{{ project.project_name }}</td>
                                <td>{{ circuit.circuit_name }}</td>
                                <td>{{ circuit.circuit_type }}</td>
                                <td>{{ "%.2f"|format(circuit.connected_load or 0) }}</td>
                                <td>{{ "%.2f"|format(circuit.design_current or 0) }}</td>
                                <td>{{ circuit.cable_size or "Not specified" }}</td>
                                <td>{{ circuit.protection_rating or "Not specified" }}</td>
                                <td>{{ circuit.route_length if circuit.route_length is not none else "—" }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    {% else %}
                    <div class="empty"><h3>No circuits found yet</h3><p>Use the form above to create your first circuit.</p></div>
                    {% endif %}
                </section>
            </main>
        </body>
        </html>
        """, circuits_list=circuits_list, projects_list=projects_list)


    @app.route("/materials", methods=["GET", "POST"])
    def materials():
        from datetime import datetime

        if request.method == "POST":
            action = request.form.get("action", "")

            try:
                if action == "add_cable":
                    cable_type = request.form.get("cable_type", "").strip()
                    brand = request.form.get("brand", "").strip() or None
                    conductor_material = request.form.get("conductor_material", "").strip() or None
                    insulation = request.form.get("insulation", "").strip() or None
                    size = request.form.get("size", "").strip()
                    colour = request.form.get("colour", "").strip()
                    function = request.form.get("function", "").strip()
                    coil_length = float(request.form.get("coil_length", ""))
                    price_text = request.form.get("unit_price", "").strip()
                    stock = float(request.form.get("stock_quantity", ""))
                    price = float(price_text) if price_text else None

                    if not all([cable_type, size, colour, function]):
                        flash("Cable type, size, colour and function are required.")
                    elif coil_length <= 0:
                        flash("Coil length must be greater than zero.")
                    elif price is not None and price < 0:
                        flash("Cable price cannot be negative.")
                    elif stock < 0:
                        flash("Stock quantity cannot be negative.")
                    else:
                        cable = Cable(
                            cable_type=cable_type,
                            brand=brand,
                            conductor_material=conductor_material,
                            insulation=insulation,
                            size=size,
                            colour=colour,
                            function=function,
                            coil_length=coil_length,
                            unit_price=price,
                            stock_quantity=stock,
                        )
                        db.session.add(cable)
                        db.session.commit()
                        flash("New cable registered successfully.")
                        return redirect(url_for("materials"))

                elif action == "add_material":
                    name = request.form.get("material_name", "").strip()
                    unit = request.form.get("unit", "").strip()
                    supplier = request.form.get("supplier", "").strip()
                    price = float(request.form.get("current_price", ""))

                    if not name or not unit:
                        flash("Material name and unit are required.")
                    elif price < 0:
                        flash("Price cannot be negative.")
                    else:
                        item = MaterialPrice(
                            material_name=name,
                            unit=unit,
                            current_price=price,
                            supplier=supplier or None,
                            updated_at=datetime.utcnow(),
                        )
                        db.session.add(item)
                        db.session.commit()
                        flash("Material registered successfully.")
                        return redirect(url_for("materials"))

                elif action == "update_cable":
                    cable_id = int(request.form.get("cable_id", ""))
                    cable = db.session.get(Cable, cable_id)

                    if cable is None:
                        flash("Cable record not found.")
                    else:
                        cable_type = request.form.get("cable_type", "").strip()
                        brand = request.form.get("brand", "").strip() or None
                        conductor_material = request.form.get("conductor_material", "").strip() or None
                        insulation = request.form.get("insulation", "").strip() or None
                        size = request.form.get("size", "").strip()
                        colour = request.form.get("colour", "").strip()
                        function = request.form.get("function", "").strip()
                        price_text = request.form.get("unit_price", "").strip()
                        length = float(request.form.get("coil_length", ""))
                        stock = float(request.form.get("stock_quantity", ""))

                        price = float(price_text) if price_text else None

                        if not all([cable_type, size, colour, function]):
                            flash("Cable type, size, colour and function are required.")
                        elif length <= 0:
                            flash("Coil length must be greater than zero.")
                        elif price is not None and price < 0:
                            flash("Cable price cannot be negative.")
                        elif stock < 0:
                            flash("Stock quantity cannot be negative.")
                        else:
                            cable.cable_type = cable_type
                            cable.brand = brand
                            cable.conductor_material = conductor_material
                            cable.insulation = insulation
                            cable.size = size
                            cable.colour = colour
                            cable.function = function
                            cable.coil_length = length
                            cable.unit_price = price
                            cable.stock_quantity = stock
                            db.session.commit()
                            flash("Cable details, price and stock updated successfully.")
                            return redirect(url_for("materials"))

                elif action == "update_price":
                    item_id = int(request.form.get("material_id", ""))
                    item = db.session.get(MaterialPrice, item_id)

                    if item is None:
                        flash("Material record not found.")
                    else:
                        price = float(request.form.get("current_price", ""))
                        supplier = request.form.get("supplier", "").strip()

                        if price < 0:
                            flash("Price cannot be negative.")
                        else:
                            item.current_price = price
                            item.supplier = supplier or None
                            item.updated_at = datetime.utcnow()
                            db.session.commit()
                            flash("Material price updated successfully.")
                            return redirect(url_for("materials"))
                else:
                    flash("Unknown materials action.")

            except (ValueError, TypeError):
                db.session.rollback()
                flash("Please enter a valid price and material ID.")
            except Exception:
                db.session.rollback()
                app.logger.exception("Materials operation failed")
                flash("Could not save the material change. Please try again.")

        cables = Cable.query.order_by(Cable.cable_type, Cable.size).all()
        material_prices = MaterialPrice.query.order_by(
            MaterialPrice.material_name
        ).all()

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Materials | Sancta Tech</title>
            <style>
                * { box-sizing: border-box; }
                body {
                    margin: 0; padding: 28px;
                    font-family: Arial, sans-serif;
                    background: #0b1120; color: #e5e7eb;
                }
                main { max-width: 1200px; margin: auto; }
                h1 { margin-bottom: 8px; }
                h2 { margin-top: 0; color: #bfdbfe; }
                p { color: #a8b3c7; }
                a { color: #60a5fa; }
                .panel {
                    margin-top: 24px; padding: 20px;
                    background: #151f32; border: 1px solid #29364d;
                    border-radius: 12px; overflow-x: auto;
                }
                table { width: 100%; border-collapse: collapse; }
                th, td {
                    padding: 12px; text-align: left;
                    border-bottom: 1px solid #29364d;
                }
                th { color: #93c5fd; }
                .empty { padding: 12px 0; }
                .back { display: inline-block; margin-bottom: 10px; }
                .form-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                    gap: 14px;
                }
                label { display: block; margin-bottom: 6px; color: #cbd5e1; }
                input {
                    width: 100%; padding: 10px; border-radius: 6px;
                    border: 1px solid #475569; background: #0b1120;
                    color: #e5e7eb;
                }
                button {
                    padding: 10px 14px; border: 0; border-radius: 6px;
                    background: #2563eb; color: white; cursor: pointer;
                }
                .notice {
                    margin: 14px 0; padding: 12px; border-radius: 6px;
                    background: #1e3a5f; color: #dbeafe;
                }
                .update-form { min-width: 230px; display: grid; gap: 8px; }
            </style>
        </head>
        <body>
            <main>
                <a class="back" href="{{ url_for('home') }}">← Back to Dashboard</a>
                <h1>Materials Management</h1>
                <p>Review cable specifications, prices and available stock.</p>

                {% with messages = get_flashed_messages() %}
                    {% for message in messages %}
                    <div class="notice">{{ message }}</div>
                    {% endfor %}
                {% endwith %}

                <section class="panel">
                    <h2>Register New Material</h2>
                    <form method="post" action="{{ url_for('materials') }}">
                        <input type="hidden" name="action" value="add_material">
                        <div class="form-grid">
                            <div>
                                <label for="material_name">Material name *</label>
                                <input id="material_name" name="material_name" required maxlength="150"
                                       placeholder="e.g. 13A socket outlet">
                            </div>
                            <div>
                                <label for="unit">Unit *</label>
                                <input id="unit" name="unit" required maxlength="50"
                                       placeholder="e.g. pcs, length, pack">
                            </div>
                            <div>
                                <label for="new_price">Price (₦) *</label>
                                <input id="new_price" name="current_price" type="number"
                                       min="0" step="0.01" required placeholder="0.00">
                            </div>
                            <div>
                                <label for="new_supplier">Supplier (optional)</label>
                                <input id="new_supplier" name="supplier" maxlength="150"
                                       placeholder="Supplier name">
                            </div>
                        </div>
                        <p><button type="submit">Register Material</button></p>
                    </form>
                </section>

                <section class="panel">
                    <h2>Register New Cable</h2>
                    <form method="post" action="{{ url_for('materials') }}">
                        <input type="hidden" name="action" value="add_cable">
                        <div class="form-grid">
                            <div>
                                <label for="new_cable_type">Cable type *</label>
                                <input id="new_cable_type" name="cable_type"
                                       maxlength="100" required
                                       placeholder="e.g. Single Core PVC Copper">
                            </div>
                            <div>
                                <label for="new_cable_brand">Brand / manufacturer</label>
                                <input id="new_cable_brand" name="brand" maxlength="100"
                                       placeholder="e.g. Comester, Coman, Lagos Star">
                            </div>
                            <div>
                                <label for="new_cable_material">Conductor material</label>
                                <input id="new_cable_material" name="conductor_material" maxlength="100"
                                       placeholder="e.g. Copper, Aluminium">
                            </div>
                            <div>
                                <label for="new_cable_insulation">Insulation</label>
                                <input id="new_cable_insulation" name="insulation" maxlength="100"
                                       placeholder="e.g. PVC">
                            </div>
                            <div>
                                <label for="new_cable_size">Size (mm²) *</label>
                                <input id="new_cable_size" name="size"
                                       maxlength="50" required
                                       placeholder="e.g. 2.5">
                            </div>
                            <div>
                                <label for="new_cable_colour">Colour *</label>
                                <input id="new_cable_colour" name="colour"
                                       maxlength="50" required
                                       placeholder="e.g. Red">
                            </div>
                            <div>
                                <label for="new_cable_function">Function *</label>
                                <input id="new_cable_function" name="function"
                                       maxlength="50" required
                                       placeholder="e.g. Live">
                            </div>
                            <div>
                                <label for="new_cable_length">Coil length (m) *</label>
                                <input id="new_cable_length" name="coil_length"
                                       type="number" min="0.01" step="0.01"
                                       required placeholder="e.g. 100">
                            </div>
                            <div>
                                <label for="new_cable_price">Unit price (₦)</label>
                                <input id="new_cable_price" name="unit_price"
                                       type="number" min="0" step="0.01"
                                       placeholder="Leave blank if unknown">
                            </div>
                            <div>
                                <label for="new_cable_stock">Stock quantity (coils) *</label>
                                <input id="new_cable_stock" name="stock_quantity"
                                       type="number" min="0" step="0.01"
                                       value="0" required>
                            </div>
                        </div>
                        <p><button type="submit">Register New Cable</button></p>
                    </form>
                </section>

                <section class="panel">
                    <h2>Cable Inventory</h2>
                    {% if cables %}
                    <table>
                        <thead>
                            <tr>
                                <th>Cable Type</th>
                                <th>Brand</th>
                                <th>Conductor</th>
                                <th>Insulation</th>
                                <th>Size</th>
                                <th>Colour</th>
                                <th>Function</th>
                                <th>Coil Length (m)</th>
                                <th>Unit Price</th>
                                <th>Stock</th>
                                <th>Edit Cable</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for cable in cables %}
                            <tr>
                                <td>{{ cable.cable_type }}</td>
                                <td>{{ cable.brand or "—" }}</td>
                                <td>{{ cable.conductor_material or "—" }}</td>
                                <td>{{ cable.insulation or "—" }}</td>
                                <td>{{ cable.size }}</td>
                                <td>{{ cable.colour }}</td>
                                <td>{{ cable.function }}</td>
                                <td>{{ "%.2f"|format(cable.coil_length) }}</td>
                                <td>
                                    {% if cable.unit_price is not none %}
                                    ₦{{ "{:,.2f}".format(cable.unit_price) }}
                                    {% else %}Not set{% endif %}
                                </td>
                                <td>{{ cable.stock_quantity if cable.stock_quantity is not none else 0 }}</td>
                                <td>
                                    <form class="update-form" method="post"
                                          action="{{ url_for('materials') }}">
                                        <input type="hidden" name="action" value="update_cable">
                                        <input type="hidden" name="cable_id" value="{{ cable.id }}">

                                        <label for="cable-type-{{ cable.id }}">Cable type</label>
                                        <input id="cable-type-{{ cable.id }}" name="cable_type"
                                               maxlength="100" value="{{ cable.cable_type }}" required>

                                        <label for="cable-brand-{{ cable.id }}">Brand / manufacturer</label>
                                        <input id="cable-brand-{{ cable.id }}" name="brand"
                                               maxlength="100" value="{{ cable.brand or '' }}">

                                        <label for="cable-material-{{ cable.id }}">Conductor material</label>
                                        <input id="cable-material-{{ cable.id }}" name="conductor_material"
                                               maxlength="100" value="{{ cable.conductor_material or '' }}">

                                        <label for="cable-insulation-{{ cable.id }}">Insulation</label>
                                        <input id="cable-insulation-{{ cable.id }}" name="insulation"
                                               maxlength="100" value="{{ cable.insulation or '' }}">

                                        <label for="cable-size-{{ cable.id }}">Size (mm²)</label>
                                        <input id="cable-size-{{ cable.id }}" name="size"
                                               maxlength="50" value="{{ cable.size }}" required>

                                        <label for="cable-colour-{{ cable.id }}">Colour</label>
                                        <input id="cable-colour-{{ cable.id }}" name="colour"
                                               maxlength="50" value="{{ cable.colour }}" required>

                                        <label for="cable-function-{{ cable.id }}">Function</label>
                                        <input id="cable-function-{{ cable.id }}" name="function"
                                               maxlength="50" value="{{ cable.function }}" required>

                                        <label for="cable-length-{{ cable.id }}">Coil length (m)</label>
                                        <input id="cable-length-{{ cable.id }}" name="coil_length"
                                               type="number" min="0.01" step="0.01"
                                               value="{{ cable.coil_length }}" required>

                                        <label for="cable-price-{{ cable.id }}">Unit price (₦)</label>
                                        <input id="cable-price-{{ cable.id }}" name="unit_price"
                                               type="number" min="0" step="0.01"
                                               value="{{ cable.unit_price if cable.unit_price is not none else '' }}"
                                               placeholder="Enter price">

                                        <label for="cable-stock-{{ cable.id }}">Stock quantity (coils)</label>
                                        <input id="cable-stock-{{ cable.id }}" name="stock_quantity"
                                               type="number" min="0" step="0.01"
                                               value="{{ cable.stock_quantity if cable.stock_quantity is not none else 0 }}"
                                               required>
                                        <button type="submit">Save Changes</button>
                                    </form>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    {% else %}
                    <p class="empty">No cable records found yet.</p>
                    {% endif %}
                </section>

                <section class="panel">
                    <h2>Material Price List</h2>
                    {% if material_prices %}
                    <table>
                        <thead>
                            <tr>
                                <th>Material</th>
                                <th>Unit</th>
                                <th>Current Price</th>
                                <th>Supplier</th>
                                <th>Last Updated</th>
                                <th>Update Price</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in material_prices %}
                            <tr>
                                <td>{{ item.material_name }}</td>
                                <td>{{ item.unit }}</td>
                                <td>₦{{ "{:,.2f}".format(item.current_price) }}</td>
                                <td>{{ item.supplier or "Not specified" }}</td>
                                <td>
                                    {% if item.updated_at %}
                                    {{ item.updated_at.strftime("%d %b %Y") }}
                                    {% else %}Not available{% endif %}
                                </td>
                                <td>
                                    <form class="update-form" method="post"
                                          action="{{ url_for('materials') }}">
                                        <input type="hidden" name="action" value="update_price">
                                        <input type="hidden" name="material_id" value="{{ item.id }}">
                                        <label for="price-{{ item.id }}">New price (₦)</label>
                                        <input id="price-{{ item.id }}" name="current_price"
                                               type="number" min="0" step="0.01"
                                               value="{{ item.current_price }}" required>
                                        <label for="supplier-{{ item.id }}">Supplier</label>
                                        <input id="supplier-{{ item.id }}" name="supplier"
                                               maxlength="150" value="{{ item.supplier or '' }}"
                                               placeholder="Supplier name">
                                        <button type="submit">Save Price</button>
                                    </form>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    {% else %}
                    <p class="empty">No material price records found yet.</p>
                    {% endif %}
                </section>
            </main>
        </body>
        </html>
        """, cables=cables, material_prices=material_prices)


    @app.route("/reports")
    def reports():
        projects_count = Project.query.count()
        rooms_count = Room.query.count()
        circuits_count = Circuit.query.count()
        cables_count = Cable.query.count()
        material_prices_count = MaterialPrice.query.count()
        boq_count = BOQItem.query.count()

        boq_total = db.session.query(
            db.func.coalesce(db.func.sum(BOQItem.amount), 0)
        ).scalar()

        project_totals = db.session.query(
            Project.project_name,
            db.func.coalesce(db.func.sum(BOQItem.amount), 0)
        ).outerjoin(
            BOQItem, BOQItem.project_id == Project.id
        ).group_by(
            Project.id, Project.project_name
        ).order_by(
            Project.project_name
        ).all()

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Reports | Sancta Tech</title>
            <style>
                * { box-sizing: border-box; }
                body {
                    margin: 0; padding: 28px;
                    font-family: Arial, sans-serif;
                    background: #0b1120; color: #e5e7eb;
                }
                main { max-width: 1200px; margin: auto; }
                h1 { margin-bottom: 8px; }
                h2 { color: #bfdbfe; }
                p { color: #a8b3c7; }
                a { color: #60a5fa; }
                .cards {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
                    gap: 16px; margin-top: 24px;
                }
                .card, .panel {
                    padding: 20px; border-radius: 12px;
                    background: #151f32; border: 1px solid #29364d;
                }
                .card h2 { margin: 0 0 12px; font-size: 14px; }
                .number { font-size: 30px; font-weight: bold; }
                .panel { margin-top: 24px; overflow-x: auto; }
                table { width: 100%; border-collapse: collapse; }
                th, td {
                    text-align: left; padding: 13px;
                    border-bottom: 1px solid #29364d;
                }
                th { color: #93c5fd; }
                .total { font-size: 24px; font-weight: bold; }
            </style>
        </head>
        <body>
            <main>
                <a href="{{ url_for('home') }}">← Back to Dashboard</a>
                <h1>Estimation Reports</h1>
                <p>A summary of the records currently saved in Sancta Tech.</p>

                <section class="cards">
                    <div class="card">
                        <h2>Total Projects</h2>
                        <div class="number">{{ projects_count }}</div>
                    </div>
                    <div class="card">
                        <h2>Total Rooms</h2>
                        <div class="number">{{ rooms_count }}</div>
                    </div>
                    <div class="card">
                        <h2>Total Circuits</h2>
                        <div class="number">{{ circuits_count }}</div>
                    </div>
                    <div class="card">
                        <h2>Cable Records</h2>
                        <div class="number">{{ cables_count }}</div>
                    </div>
                    <div class="card">
                        <h2>Material Price Records</h2>
                        <div class="number">{{ material_prices_count }}</div>
                    </div>
                    <div class="card">
                        <h2>BOQ Items</h2>
                        <div class="number">{{ boq_count }}</div>
                    </div>
                </section>

                <section class="panel">
                    <h2>Overall Estimated BOQ Value</h2>
                    <div class="total">₦{{ "{:,.2f}".format(boq_total) }}</div>
                    <p>This is the sum of saved BOQ item amounts, not a new quotation.</p>
                </section>

                <section class="panel">
                    <h2>BOQ Value by Project</h2>
                    {% if project_totals %}
                    <table>
                        <thead>
                            <tr><th>Project</th><th>Estimated BOQ Value</th></tr>
                        </thead>
                        <tbody>
                            {% for project_name, total in project_totals %}
                            <tr>
                                <td>{{ project_name }}</td>
                                <td>₦{{ "{:,.2f}".format(total) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    {% else %}
                    <p>No projects have been created yet.</p>
                    {% endif %}
                </section>
            </main>
        </body>
        </html>
        """,
        projects_count=projects_count,
        rooms_count=rooms_count,
        circuits_count=circuits_count,
        cables_count=cables_count,
        material_prices_count=material_prices_count,
        boq_count=boq_count,
        boq_total=boq_total,
        project_totals=project_totals)

    return app
