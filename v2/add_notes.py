#!/usr/bin/env python3
"""
Extract study notes from Rules-of-the-road.txt and add to HTML pages.
"""
import re
from pathlib import Path

# Read the full text file
txt_file = Path('Rules-of-the-road.txt')
with open(txt_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by sections - match "Section X:" followed by actual section content
sections_dict = {}

# Find all section starts with their line numbers
pattern = r'Section (\d+):'
matches = list(re.finditer(pattern, content))

for i, match in enumerate(matches):
    section_num = match.group(1)
    start = match.start()
    
    # End is the start of the next section or end of file
    if i + 1 < len(matches):
        end = matches[i + 1].start()
    else:
        end = len(content)
    
    section_text = content[start:end]
    
    # Extract just the content after the section title line
    lines = section_text.split('\n')
    title_line = lines[0]  # "Section X: Title"
    
    # Get the title from the first line
    title_match = re.match(r'Section \d+:\s*(.*)', title_line)
    title = title_match.group(1) if title_match else f'Section {section_num}'
    
    # The notes are everything after the title, cleaned up
    notes_lines = lines[1:]
    notes = '\n'.join(notes_lines).strip()
    
    # Remove page number markers and extra whitespace
    notes = re.sub(r'\s*\d+\s*\n', '\n', notes)
    notes = re.sub(r'\n\s*\n\s*\n+', '\n\n', notes)
    notes = re.sub(r'[^a-zA-Z0-9\s\n\.,;:\(\)\-\'/]', '', notes)  # Remove special chars
    
    sections_dict[int(section_num)] = {
        'title': title,
        'notes': notes[:2000]  # Limit to 2000 chars for readability
    }

# Now update the HTML files
section_files = [
    ('section1_driving_licences.html', 1),
    ('section2_learner_driver.html', 2),
    ('section3_driving_test.html', 3),
    ('section4_vehicle_safety.html', 4),
    ('section5_good_driving_practice.html', 5),
    ('section6_traffic_signs.html', 6),
    ('section7_traffic_lights.html', 7),
    ('section8_speed_limits.html', 8),
    ('section9_junctions.html', 9),
    ('section10_parking.html', 10),
    ('section11_motorways.html', 11),
    ('section12_assisting_garda.html', 12),
    ('section13_safe_driving.html', 13),
    ('section14_accidents.html', 14),
    ('section15_penalty_points.html', 15),
    ('section16_motorcyclists.html', 16),
    ('section17_cyclists.html', 17),
]

for html_file, sec_num in section_files:
    html_path = Path(html_file)
    
    if not html_path.exists():
        print(f"⚠️ {html_file} not found, skipping")
        continue
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Check if file already has the tab system (section1 was already updated)
    if '<div class="tab-bar">' not in html_content:
        # Add the CSS for tabs if not present
        if '.tab-bar{' not in html_content:
            css_injection = '''.tab-bar{display:flex;margin-bottom:24px;border-bottom:1px solid var(--border)}.tab-btn{background:none;border:none;padding:12px 24px;font-family:'Syne',sans-serif;font-size:14px;font-weight:600;color:var(--text-muted);cursor:pointer;border-bottom:2px solid transparent;transition:color .15s,border-color .15s}.tab-btn.active{color:var(--navy);border-bottom-color:var(--gold)}.tab-content{display:none}.tab-content.active{display:block}.notes-content{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);padding:24px;font-size:14px;line-height:1.6;white-space:pre-wrap}
      '''
            html_content = html_content.replace('@media (max-width: 768px) {', css_injection + '@media (max-width: 768px) {')
        
        # Add the HTML structure for tabs after <div class="content">
        notes_text = sections_dict.get(sec_num, {}).get('notes', 'Study notes for this section.')
        notes_html = f'<div class="tab-bar"><button class="tab-btn active" onclick="showTab(\'notes\')">Study Notes</button><button class="tab-btn" onclick="showTab(\'quiz\')">Practice Quiz</button></div><div class="content"><div id="notes-section" class="tab-content active"><div class="notes-content">{notes_text}</div></div>'
        
        html_content = html_content.replace('<div class="content">', notes_html)
        
        # Wrap the quiz section
        html_content = html_content.replace(
            '<div class="quiz-header">',
            '<div id="quiz-section" class="tab-content"><div class="quiz-header">'
        )
        
        # Close the quiz-section div before the script tag
        html_content = html_content.replace(
            '</div>\n    <script>',
            '</div></div></div>\n    <script>'
        )
        
        # Add the showTab function to JavaScript
        js_function = '''function showTab(tab) { 
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active')); 
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active')); 
      document.getElementById(tab + '-section').classList.add('active'); 
      document.querySelector(`[onclick="showTab('${tab}')"]`).classList.add('active'); 
    }
'''
        html_content = html_content.replace(
            '<script>',
            '<script>\n    ' + js_function,
            1
        )
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ Updated {html_file}")
    else:
        print(f"← {html_file} already has tabs")

print("\n✅ All files updated!")
