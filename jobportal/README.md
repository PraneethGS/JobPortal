**Job Portal (Django) — Project Documentation**

**Overview:**
- **What:** Simple job portal built with Django. Supports two user types (`employer`, `jobseeker`), job posting, applications with text resume and optional file upload, and an employer dashboard to view applicants.
- **Where to look first:** main templates and app folders under the project root.

**Quick Start (development)**
- **Create & activate venv (Windows PowerShell):**
  - `python -m venv .venv`
  - `.\.venv\Scripts\Activate.ps1`
- **Install dependencies:**
  - `pip install -r requirements.txt` (if missing, install Django: `pip install django`)
- **Migrate DB:**
  - `python manage.py migrate`
- **Create superuser (optional):**
  - `python manage.py createsuperuser`
- **Run dev server:**
  - `python manage.py runserver`

**Project Structure (important files)**
- **Project settings & entry:** [jobportal/settings.py](jobportal/settings.py#L1), [manage.py](manage.py)
- **Templates:** global templates are at [templates/](templates/) and app templates under each app (for example [applications/templates/applications/apply_job.html](applications/templates/applications/apply_job.html#L1)).
- **Main base template:** [jobportal/templates/base.html](jobportal/templates/base.html#L1) — contains inline site CSS and header/footer.
- **Applications app:** code lives in [applications/](applications/). Key files:
  - views: [applications/views.py](applications/views.py#L1)
  - models: [applications/models.py](applications/models.py#L1)
  - forms: [applications/forms.py](applications/forms.py#L1)
  - templates: [applications/templates/applications/](applications/templates/applications/)
- **Jobs app:** [jobs/](jobs/) (models, views, templates for job posting and employer dashboard)
- **Users app:** [users/](users/) (custom user model `CustomUser` with `user_type`)

**Key Features & How They Work**
- **Authentication & User Types:** `users.models.CustomUser` extends `AbstractUser` and adds `user_type` with values `employer` or `jobseeker`. Login/registration handled in `users/views.py`.
- **Job Posting:** Employers create jobs via `jobs.create_job`; employer dashboard is at `/jobs/dashboard/` (see [jobs/views.py](jobs/views.py#L1)).
- **Applications:** Jobseekers apply via `/applications/apply/<job_id>/` using `applications.apply_job`. A text resume field (`message`) is stored on the `Application` model and an optional uploaded file is stored to `media/resumes/` using the `resume` FileField.
- **Permissions:** Views check `request.user.user_type` and ownership. Employers can view applicants for their jobs; applicants can view/delete their own applications.

**Database & Migrations**
- SQLite is used by default (`db.sqlite3` in project root). After model changes run:
  - `python manage.py makemigrations`
  - `python manage.py migrate`
- The `resume` FileField was added to `applications.Application`; migrations are created under `applications/migrations/`.

**Static & Media**
- In development, static assets are referenced by `base.html` (inline CSS). If you later move styles to files, update `STATICFILES_DIRS` in [jobportal/settings.py](jobportal/settings.py#L1) and ensure `collectstatic` and `STATIC_ROOT` are set for production.
- Uploaded resumes are served from the `MEDIA_ROOT` directory configured in [jobportal/settings.py](jobportal/settings.py#L1). When `DEBUG=True` Django serves media via `urlpatterns += static(...)`.

**URLs (useful endpoints)**
- Home: `/` (core app) — see [core/urls.py](core/urls.py)
- Jobs list: `/jobs/` — see [jobs/urls.py](jobs/urls.py#L1)
- Employer dashboard: `/jobs/dashboard/`
- Apply to job: `/applications/apply/<job_id>/`
- My applications: `/applications/my/`
- View applicants: `/applications/view/<job_id>/`

**Templates & Styling Notes**
- The site uses a shared `base.html` which includes inline CSS and common header/navigation; update that file to change global styles: [jobportal/templates/base.html](jobportal/templates/base.html#L1).
- Individual app templates use `.card`, `.btn`, and utility classes (defined in `base.html`).

**Admin**
- Register models in admin if you need CRUD via the admin site; `admin/` is available at `/admin/`.

**Testing & Debugging**
- Run Django checks and migrations as described above.
- If an OperationalError appears (e.g. `no such column`), run `makemigrations` and `migrate` — this project previously added the `resume` field and required migration.

**Maintenance / Next Improvements (suggestions)**
- Add file-type and size validation for uploaded resumes (server-side in `ApplicationForm.clean_resume`).
- Current limits: minimum 2 MB and maximum 5 MB. Allowed types: PDF, DOC, DOCX, TXT.
- Move inline CSS to `static/css/style.css` and reference via `{% static %}` for easier maintenance.
- Add pagination for job lists and applicant lists.
- Add email notifications for new applications.

If you'd like, I can generate a more detailed developer README (with commands for testing, CI, and contributions) or add inline examples and screenshots.
