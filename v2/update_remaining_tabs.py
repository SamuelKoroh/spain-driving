#!/usr/bin/env python3
"""Automatically add tab system to remaining section HTML files."""
import re
from pathlib import Path

sections = {
    6: ("Traffic signs", "Regulatory signs, stop/yield signs, lane control, one-way streets, road markings, warning signs, traffic calming signs, and level crossings"),
    7: ("Traffic lights", "Traffic signals meaning, turning at lights, pedestrian signals, hand signals by drivers and cyclists"),
    8: ("Speed limits", "Two-second rule, speed limits for roads and vehicles, stopping distances, and speeding penalties"),
    9: ("Junctions", "Safe approach to junctions, yellow box junctions, roundabouts, and dual carriageway procedures"),
    10: ("Parking", "Legal parking places, disabled parking, permit zones, parking restrictions, and never leaving engines running"),
    11: ("Motorways", "General motorway rules, speed limits, joining/exiting, lane discipline, rest areas, breakdowns, tunnels"),
    12: ("Assisting Gardaí", "Traffic signals, instructions, priority, emergency service vehicle procedures"),
    13: ("Safe driving", "Alcohol limits (20mg for learners), drugs, tiredness, fatigue, road rage, and aggressive driving"),
    14: ("Accidents", "Actions at accident scenes, emergency procedures, dangerous goods, and insurance claims"),
    15: ("Penalty points", "Penalty points offences, fixed charges, totting up, and disqualification thresholds"),
    16: ("Motorcyclists", "Motorcycle licence, insurance, protective equipment, riding tactics, and safety measures"),
    17: ("Cyclists", "Bicycle maintenance, protective clothing, trailers, cycling rules, and roundabout procedures"),
}

section_files = {
    6: "section6_traffic_signs.html",
    7: "section7_traffic_lights.html",
    8: "section8_speed_limits.html",
    9: "section9_junctions.html",
    10: "section10_parking.html",
    11: "section11_motorways.html",
    12: "section12_assisting_garda.html",
    13: "section13_safe_driving.html",
    14: "section14_accidents.html",
    15: "section15_penalty_points.html",
    16: "section16_motorcyclists.html",
    17: "section17_cyclists.html",
}

for sec_num, (title, notes) in sections.items():
    file_path = Path(section_files[sec_num])
    
    if not file_path.exists():
        print(f"✗ {file_path} not found")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has tabs
    if '<div class="tab-bar">' in content:
        print(f"← {file_path.name} already has tabs")
        continue
    
    # Add tab bar and notes before quiz section
    tab_html = f'''<div class="tab-bar"><button class="tab-btn active" onclick="showTab('notes')">Study Notes</button><button class="tab-btn" onclick="showTab('quiz')">Practice Quiz</button></div><div class="content"><div id="notes-section" class="tab-content active"><div class="notes-content">{notes}</div></div>
      <div id="quiz-section" class="tab-content">'''
    
    content = content.replace('<div class="content">\n  <div class="quiz-header">', tab_html + '<div class="quiz-header">')
    
    # Close divs before script
    showTab_fn = '''function showTab(tab) { 
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active')); 
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active')); 
  document.getElementById(tab + '-section').classList.add('active'); 
  document.querySelector(`[onclick="showTab('${tab}')"]`).classList.add('active'); 
}
'''
    
    content = content.replace('    </div>\n  </div>\n</div>\n<script>\nlet qCur=0,qScore=0,qAnswered=false;', 
                            '    </div>\n  </div>\n</div></div></div>\n<script>\n' + showTab_fn + 'let qCur=0,qScore=0,qAnswered=false;')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ {file_path.name}")

print("\n✅ All sections updated!")
