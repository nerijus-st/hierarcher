# Hierarcher

Hierarcher is a simple CLI application written in Python. It reads input from stdin or json/yaml file and prints company hierarchy tree with total salary. See examples in usage for more details.

## Installation

Clone repo first, activate virtual environment and install dependencies:
```bash
git clone https://github.com/nerijus-st/hierarcher.git
cd hierarcher
python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage
Hierarcher application accepts either valid json format from stdin or json/yaml file. To read from stdin pass json with -t ar --text argument:
```bash
./hierarcher.py -t '{"employer": {"name": "Kobe", "salary": 100000, "reports": [{"employer": {"name": "Lebron", "salary": 80000, "reports": []}}]}}'
```

output:
```bash
Kobe
Employees of: Kobe
    Lebron
Total salary: $180,000.00
```

Sample file examples are provided under /samples. If you want to pass a file use -f or --file argument:
```bash
./hierarcher.py -f samples/input3.json
```

output2:
```bash
Jeff
Employees of: Jeff
    Cory
    Dave
    Employees of: Dave
        Anna
        Zach
Total salary: $385,000.00
```

Employees will be sorted alphabetically.

Application is covered with tests. To run them execute the following command:
```bash
python3 -m unittest -v
```

## Limitations / TODO
This was just a coding exercise and program has a bunch of limitations. Program is not validating json schema, but blindly expects that all required keys are defined.
Input format must be the following:
```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "employer": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "salary": {
          "type": "integer"
        },
        "reports": {
          "type": "array",
          "items": {}
        }
      },
      "required": [
        "name",
        "salary",
        "reports"
      ]
    }
  },
  "required": [
    "employer"
  ]
}
```
