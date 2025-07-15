# Learning-Fastapi-Basics
Absolutely! 🎉 Here’s your complete **`README.md`** file in **one ready-to-copy block**.
Just select it all, paste it into your `README.md`, commit, and push. 🚀

---

```markdown
# 🩺 Patient Management System API with FastAPI

This is a fully-featured **Patient Management System API** built using **FastAPI**.  
It allows you to create, update, view, sort, and delete patient records, while also automatically calculating and reporting on BMI and health status.

---

## 🚀 Features

✅ CRUD operations for patient records  
✅ Automatically computes **BMI** and gives a health **verdict**  
✅ Sort patients by height, weight, BMI, age, or name in ascending/descending order  
✅ Data persisted in a local JSON file (`patients.json`)  
✅ Robust validation using **Pydantic models with computed fields**

---

## 🏗️ Tech Stack

- **Python 3.10+**
- **FastAPI** 🚀 for building APIs
- **Pydantic** for data validation and computed fields
- **JSON** for local data persistence

---

## 📂 Project Structure

```

.
├── main.py          # FastAPI application
├── patients.json    # Local data storage (created automatically)
├── requirements.txt # Python dependencies
└── README.md

````

---

## 🔌 API Endpoints

### Root & Info
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/`      | Returns welcome message |
| GET    | `/about` | Information about this API |

### CRUD Operations
| Method | Endpoint               | Description                   |
|--------|-------------------------|-------------------------------|
| GET    | `/view`                 | View all patient records |
| GET    | `/patient/{patient_id}` | View a single patient by ID |
| POST   | `/create`               | Create a new patient |
| PUT    | `/update/{patient_id}`  | Update an existing patient |
| DELETE | `/delete/{patient_id}`  | Delete a patient by ID |

### Sorting
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/sort?sort_by=bmi&order=asc` | Sort patients by height, weight, bmi, age, or name |

---

## 📝 Example Patient JSON

When creating a patient (`POST /create`), supply data like:

```json
{
    "id": "P001",
    "name": "Ram Bahadur",
    "city": "Kathmandu",
    "age": 30,
    "gender": "male",
    "height": 175.0,
    "weight": 70.0
}
````

Response will include computed fields:

```json
{
  "message": "Patient created successfully",
  "patient": {
    "id": "P001",
    "name": "Ram Bahadur",
    "city": "Kathmandu",
    "age": 30,
    "gender": "male",
    "height": 175.0,
    "weight": 70.0,
    "bmi": 22.86,
    "verdict": "Normal weight"
  }
}
```

---

## 🚀 How to Run

1️⃣ Clone the repo

```bash
git clone https://github.com/Bishal-Somare/Learning-Fastapi-Basics.git
cd Learning-Fastapi-Basics
```

2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

3️⃣ Start the server

```bash
uvicorn main:app --reload
```

API will be available at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔍 Testing API

Use **Swagger UI** (auto docs by FastAPI):
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Or use curl / Postman to test endpoints.

---

## 🎯 Improvements & Ideas

* Switch to a real database (SQLite or PostgreSQL)
* Add authentication for secure access
* Implement pagination for `/view` or `/sort`
* Deploy with Docker or on a cloud platform (Heroku, Render)

---

## 💡 Author

👤 **Bishal Somare**
📬 [https://github.com/Bishal-Somare](https://github.com/Bishal-Somare)

---

## 📜 License

This project is open source under the MIT License.

---

🚀 Happy coding! If you like this project, consider starring ⭐ the repo.

````

---

✅ **That’s it!**  
You can literally paste this into `README.md`, then run:

```bash
git add README.md
git commit -m "Add detailed README"
git push
````

and your GitHub page will look 🔥.

---

Need a **`.gitignore`**, **`requirements.txt`** or a small **badge section** for GitHub?
Just tell me, I’ll whip them up for you in seconds! 💪
