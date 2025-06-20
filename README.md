# React-Django-Boilerplate

Web Application for Sports Leagues to generate balanced teams.

---

## 📦 Project Structure

```
react-django-boilerplate/
├── backend/         # Django project
├── frontend/        # React + Vite app
├── env/             # Python virtual environment (not tracked)
└── README.md
```

---

## 🛠️ Setup Instructions

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/tylerrubino/react-django-boilerplate.git
cd react-django-boilerplate
```

---

### 🐍 2. Backend (Django)

> ⚠️ Python 3.10+ recommended

#### Create and activate virtual environment

```bash
python -m venv env
env\Scripts\activate  # On Windows
# source env/bin/activate  # On macOS/Linux
```

#### Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Run Django server

```bash
python manage.py migrate
python manage.py runserver
```

By default: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### ⚛️ 3. Frontend (React + Vite)

> ⚠️ Node.js 18+ recommended

```bash
cd ../frontend
npm install
npm run dev
```

By default: [http://localhost:5173/](http://localhost:5173/)

---

## 🧾 Notes

- Be sure to create a `.env` file in both `/backend` and `/frontend` if needed.
- `.env` is needed in the `backend\` folder, add the following in it:
  - SECRET_KEY=some_secret_key -> make one here: https://djecrety.ir/
  - DEBUG=True
- The virtual environment folder (`env/`) and `node_modules/` are ignored via `.gitignore`.

---

## 🤝 Contributing

1. Fork the repo
2. Create a new branch using the naming convention:  
   `projectname-<issueNumber>-<task-name>`  
   Example:
   ```bash
   git checkout -b projectname-12-add-some-api
   ```
3. Commit and push (`git commit -m 'Add your feature'`)
4. Push your branch (`git push -u origin projectname-<issueNumber>-<task-name>`)
5. Open a Pull Request to main!

---

## 🚧 Working on Tasks & Issues

We use [GitHub Projects](https://github.com/your-org/projectname/projects) to manage tasks across the team.

### 🧠 Task Workflow

1. **Pick a task from the `To do` column** in the [ProjectName GitHub Project board](https://github.com/users/tylerrubino/projects/1).
2. **Assign yourself** to the task.
3. **Move the task to `In progress`** to indicate you're working on it.
4. **Create a new branch** using the correct naming convention:

   ```bash
   git checkout -b projectname-<issueNumber>-<task-name>
   # Example:
   git checkout -b projectname-12-add-new-api
   ```

5. Make your changes, commit, and push to your branch:

   ```bash
   git commit -m "Add new API endpoint"
   git push -u origin projectname-12-add-new-api
   ```

6. Open a **Pull Request (PR)** to `main`, referencing the issue:

   - Name the PR `projectname#12 - add new api`
   - Add `Closes #12` at the bottom of your description to auto-link and close the issue on merge.

7. After opening your PR:

   - **Move the task to `Code review`**
   - **Unassign yourself** to indicate it’s ready for peer review

8. In the issues comment section add a comment with some test instructions for the code reviewer to test with and gain context.

9. Once reviewed and merged, the task will be closed automatically.

### 🛠️ Creating Issues

If you come across an issue that you want worked on, do the following:

- go to https://github.com/users/vladachini/projects/1
- click `+ Add item` under Todo and click the `+` that comes up at the bottom
- click `Create new issue`
- add a short title
- explain what the issue/task is

---
