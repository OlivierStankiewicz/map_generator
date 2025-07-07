# Heroes of Might and Magic III Procedural Map Generator

This project implements procedural content generation for map creation in **Heroes of Might and Magic III**.

---

## Project Structure

```
map_generator/
│
├── example_maps/                  # Example maps in .json and .h3m formats used for development
│
├── generated_maps/
│   ├── manually_generated/        # Maps generated using test scripts
│   └── automatially_generated/    # Maps generated from the main script
│
├── src/
│   ├── classes/                   # All classes used to represent map objects
│   ├── generation/                # Map generation logic
│   ├── test_scripts/              # Scripts for testing map generation and conversion
│   └── main.py                    # Main script for map generation
│
├── Readme.md
├── .gitignore
├── h3mtxt.exe                     # Script used for converting .json files representing valid maps to .h3m
└── requirements.txt
```

---

## Folder Descriptions

- **example_maps/**  
  Contains example maps in `.json` and `.h3m` formats used as references during development.

- **generated_maps/manually_generated/**  
  Maps generated using test scripts.

- **generated_maps/automatially_generated/**  
  Maps generated from the main script.

- **src/classes/**  
  Contains all classes used to represent the map as an object.  
  Each class provides:

  - A standard constructor
  - A no-argument constructor (creates an object with default values)
  - A function that returns the dictionary representation of the object

- **src/generation/**  
  Contains map generation logic.  
  Each class has its own file.  
  For now, most classes just create objects with default values, but `map` and `tile` already have more complex generation functions.

- **src/test_scripts/**  
  Contains two scripts:

  - Generation of a `.json` file representing a default map of all Water 22 sprite tiles
  - Conversion from any valid `.json` file to `.h3m`

- **src/main.py**  
  The main script for map generation.  
  Currently, it generates a map of all terrain types with all of their known sprites (more sprite numbers have to be tested).

---

## Usage

- Use the scripts in `src/test_scripts/` for separately testing map .json representation generation and conversion to .h3m.
- Run `src/main.py` to generate maps using the main procedural logic.

---

**Note:**  
This project is under active development. More features and improvements are
