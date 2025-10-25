# Math-Data

A project to crawl, collect, and organize unsolved problems in mathematics from Wikipedia and other sources.

## Overview

This repository contains tools and data related to unsolved mathematical problems. It crawls mathematical problems from Wikipedia, particularly focusing on unsolved problems in mathematics, and organizes them in a structured format for further analysis or research.

The project collects information about famous conjectures, hypotheses, and open problems in various fields of mathematics, making it easier to explore and study these challenging problems.

## Data Structure

The repository contains the following data:

1. `data/unsolved_problems.json` - A structured JSON file containing unsolved mathematical problems organized by categories
2. `data/problems/` - A directory containing individual HTML files for specific mathematical problems
3. `data/List of unsolved problems in mathematics - Wikipedia.html` - The source Wikipedia page

## Scripts

- `crawl_math_problems.py` - Extracts unsolved problems from the main Wikipedia page and organizes them by category
- `crawl_individual_problems.py` - Crawls individual problem pages from Wikipedia to create a more detailed dataset

## Installation

To set up the project, you need to install the required dependencies:

```bash
pip install -e .
```

Or for development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

1. To extract problems from the main Wikipedia page:
   ```bash
   python crawl_math_problems.py
   ```

2. To crawl individual problem pages:
   ```bash
   python crawl_individual_problems.py
   ```

## Dependencies

- beautifulsoup4: For HTML parsing
- playwright: For web crawling
- requests: For HTTP requests
- tqdm: For progress bars

## Data Format

The `unsolved_problems.json` file contains an array of objects, each with:
- `category`: The category or grouping of problems
- `problems`: An array of problem descriptions in that category

## Examples of Collected Problems

Some of the well-known mathematical problems included in this dataset:
- Millennium Prize Problems (including the Riemann Hypothesis, P versus NP problem, etc.)
- Various conjectures in algebra, number theory, geometry, and other fields
- Problems from mathematical notebooks and collections

## License

This project is licensed under the MIT License - see the LICENSE file for details.