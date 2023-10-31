# SPM-T6
Software Project Management T6

# Development

## Running the Project

### Prerequisites

[Python](https://www.python.org/downloads/) >= 3.10
[Node.js](https://nodejs.org/en/download) >= 16.17.0

### On Windows

Start Frontend (Make sure you are on project root folder)

```shell
cd frontend
npm install
npm run serve
```
Before running the backend app, you need to install the required Python packages. Navigate to the project root directory and run:
```shell
 pip install -r requirements.txt
```

Start Backend (Make sure you are on project root folder)

```shell
 cd revamped_backend
 start_all.bat
```

The [`start_all.bat`](start_all.bat) script is used to run all backend services.

### On OSX/WSL/Linux (Unix-based)

Start Frontend (Make sure you are on project root folder)

```shell
cd frontend
npm install
npm run serve
```
Before running the backend app, you need to install the required Python packages. Navigate to the project root directory and run:

```shell
 pip install -r requirements.txt
```

Start Backend (Make sure you are on project root folder)

```shell
cd revamped_backend
./start_all.sh
```

## Repository Structure

```
~/spm-t6 main*
❯ tree .
.
├── README.md
├── frontend
│   ├── ...
│   └── README.md
├── requirements.txt
└── revamped_backend
    ├── ...
    └── README.md
```