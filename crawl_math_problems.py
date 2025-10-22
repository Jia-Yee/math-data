import json
import os
from bs4 import BeautifulSoup

def extract_unsolved_problems(html_content):
    """
    Extract unsolved problems from the Wikipedia page
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    problems = []
    
    # Find the main content area
    content = soup.find('div', {'id': 'mw-content-text'})
    if not content:
        print("Main content area not found")
        return problems
    
    # Find all ul elements in the content
    lists = content.find_all('ul')
    print(f"Found {len(lists)} lists")
    
    for ul in lists:
        # Check if this list has list items with substantial content
        list_items = ul.find_all('li')
        section_problems = []
        
        for item in list_items:
            problem_text = item.get_text().strip()
            if problem_text and len(problem_text) > 10:
                section_problems.append(problem_text)
        
        # If we found problems, we need to associate them with a heading
        if section_problems:
            # Find the preceding heading
            category_name = "Uncategorized"
            prev_element = ul.find_previous()
            heading_types = ['h2', 'h3', 'h4']
            
            # Look backwards for the closest heading
            while prev_element:
                if prev_element.name in heading_types:
                    category_name = prev_element.get_text().strip()
                    break
                prev_element = prev_element.find_previous()
            
            # Skip generic sections
            skip_sections = ['see also', 'references', 'external links', 'notes', 'further reading']
            if any(skip in category_name.lower() for skip in skip_sections):
                continue
                
            problems.append({
                'category': category_name,
                'problems': section_problems
            })
            print(f"Added category '{category_name}' with {len(section_problems)} problems")
    
    # Merge categories with the same name
    merged_problems = {}
    for item in problems:
        category = item['category']
        if category in merged_problems:
            merged_problems[category]['problems'].extend(item['problems'])
        else:
            merged_problems[category] = item
    
    return list(merged_problems.values())

def crawl_math_unsolved_problems():
    """
    Crawl the main unsolved problems page and extract problems
    """
    # Check if we already have the page content
    file_path = 'data/List of unsolved problems in mathematics - Wikipedia.html'
    
    if not os.path.exists(file_path):
        print("Wikipedia page not found!")
        return []
    else:
        print("Using existing Wikipedia page...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    
    # Extract problems
    problems = extract_unsolved_problems(content)
    
    # Save to JSON file
    output_file = 'data/unsolved_problems.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    
    print(f"\nExtracted {len(problems)} categories of unsolved problems")
    total_problems = sum(len(category['problems']) for category in problems)
    print(f"Total problems extracted: {total_problems}")
    
    # Print a summary
    for category in problems:
        print(f"- {category['category']}: {len(category['problems'])} problems")
        # Print first few problems as examples
        for i, problem in enumerate(category['problems'][:3]):
            print(f"  {i+1}. {problem[:60]}{'...' if len(problem) > 60 else ''}")
        if len(category['problems']) > 3:
            print(f"  ... and {len(category['problems']) - 3} more")
    
    return problems

if __name__ == "__main__":
    # Extract problems from the main page
    problems = crawl_math_unsolved_problems()
    
    print("\nCrawling complete! Data saved to 'data/unsolved_problems.json'")