# Pythia

Personal clone I have been working on with raylib and python
Done out of spite to prove a certain developer wrong

## Build Instructions
After you made your own venv, run this command

### Windows
```
pyinstaller src/main.py --onefile --add-data ".venv/Lib/site-packages/fleep/data.json:fleep"
```
### Linux
```
pyinstaller src/main.py --onefile --add-data ".venv/lib/python3.13/site-packages/fleep/data.json:fleep"
```

For those using pyright, put this in the repo folder
```json
// pyrightconfig.json
{
  "venvPath": "./",
  "venv": ".venv"
}
```
