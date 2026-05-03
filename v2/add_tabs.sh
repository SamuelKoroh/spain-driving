#!/bin/bash

# Add tab system to sections 5-17

sections=(
  "5|Good driving practice|Moving off, positioning, lane changes, overtaking, reversing, U-turns, stopping, towing, night driving, horn use, and other essential driving manoeuvres"
  "6|Traffic signs|Regulatory signs, stop/yield signs, lane control, one-way streets, road markings, warning signs, traffic calming signs, special signs for buses/trams/rail, and level crossings"
  "7|Traffic lights|Red, amber, green lights, turning at lights, pedestrian signals, hand signals by drivers and cyclists, safe signal communication"
  "8|Speed limits|Two-second rule, appropriate speed limits for roads and vehicles, stopping distances, speeding offences and penalties"
  "9|Junctions|Approaching junctions safely, yellow box junctions, dual carriageways, and roundabout procedures"
  "10|Parking|Legal and illegal parking, permit zones, disabled parking, parking near schools, never leaving engine running"
  "11|Motorways|General rules, speed limits, joining/leaving, lane discipline, rest areas, breakdowns, tunnels"
  "12|Assisting Garda|Traffic signals, following instructions, emergency vehicle procedures, priority"
  "13|Safe driving|Alcohol limits (20mg for learners), drugs, tiredness, fatigue, road rage, aggressive driving"
  "14|Accidents|What to do at accident scenes, emergency contact, dangerous goods, insurance claims"
  "15|Penalty points|Points offences, fixed charges, totting up, disqualification thresholds"
  "16|Motorcyclists|Licence requirements, insurance, tax, protective equipment, riding tactics"
  "17|Cyclists|Bicycle maintenance, protective clothing, trailers, cycling safely, cycle track rules"
)

for section_info in "${sections[@]}"; do
  IFS='|' read -r sec_num sec_title sec_notes <<< "$section_info"
  
  # Determine filename
  case $sec_num in
    5) file="section5_good_driving_practice.html" ;;
    6) file="section6_traffic_signs.html" ;;
    7) file="section7_traffic_lights.html" ;;
    8) file="section8_speed_limits.html" ;;
    9) file="section9_junctions.html" ;;
    10) file="section10_parking.html" ;;
    11) file="section11_motorways.html" ;;
    12) file="section12_assisting_garda.html" ;;
    13) file="section13_safe_driving.html" ;;
    14) file="section14_accidents.html" ;;
    15) file="section15_penalty_points.html" ;;
    16) file="section16_motorcyclists.html" ;;
    17) file="section17_cyclists.html" ;;
  esac
  
  if [ -f "$file" ]; then
    if ! grep -q '<div class="tab-bar">' "$file"; then
      # Add tab bar and notes before quiz
      sed -i "s|<div class=\"content\">|<div class=\"tab-bar\"><button class=\"tab-btn active\" onclick=\"showTab('notes')\">Study Notes</button><button class=\"tab-btn\" onclick=\"showTab('quiz')\">Practice Quiz</button></div><div class=\"content\"><div id=\"notes-section\" class=\"tab-content active\"><div class=\"notes-content\">$sec_notes</div></div>\n      <div id=\"quiz-section\" class=\"tab-content\">|" "$file"
      
      # Close divs before script
      sed -i 's|</div>\n<script>|</div></div></div>\n<script>|' "$file"
      
      # Add showTab function
      sed -i 's|<script>|<script>\nfunction showTab(tab) { \n  document.querySelectorAll('\''.tab-content'\'').forEach(el => el.classList.remove('\'active'\')); \n  document.querySelectorAll('\''.tab-btn'\'').forEach(el => el.classList.remove('\'active'\')); \n  document.getElementById(tab + '\''-section'\'').classList.add('\'active'\''); \n  document.querySelector(`[onclick="showTab('\''${tab}'\'')"]\`).classList.add('\'active'\''); \n}|' "$file"
      
      echo "✓ Updated $file"
    else
      echo "← $file already has tabs"
    fi
  else
    echo "✗ $file not found"
  fi
done

echo "Done!"
