import io
import requests
import pdfplumber
import re
from typing import List, Dict
from datetime import datetime

from utils.utils import find_date_in_line, generate_motion_id, generate_subject_id, generate_vote_id

def clean_member_name(name: str) -> str:
    """
    Removes titles like "Mayor", "Mayor Pro Tempore", and "Council Member" 
    from the name.
    """
    # Regex to remove titles
    name = re.sub(r"Mayor\s+Pro\s+Tempore\s+", "", name)
    name = re.sub(r"Mayor\s+", "", name)
    name = re.sub(r"Council\s+Members?\s+", "", name)
    name = name.rstrip(".")
    return name.strip()

def split_vote_list(vote_string: str) -> list:
    """
    Splits a vote string into individual member names. Handles names separated by commas
    or 'and' (Oxford comma or not).
    
    Parameters:
    - vote_string: A string containing the names of council members.
    
    Returns:
    - A list of member names.
    """
    # First, replace "and" with a comma to standardize splitting
    vote_string = vote_string.replace(", and ", ", ")
    vote_string = vote_string.replace(" and ", ", ")
    
    # Now split by comma
    members = [clean_member_name(name.strip()) for name in vote_string.split(",")]
    return members

def parse_votes(motion_text: str, motion_id: str, meeting_date: datetime):
    """
    Parses the list of vote lines to extract member names for Ayes, Noes, and Absent categories.
    Assumes the vote information spans multiple lines.
    """
    votes = []
    
    # Regex to capture Ayes, Noes, and Absent information from the motion text
    ayes_pattern = r"Ayes:\s*(.*?)(?=\s*Noes:|\s*Absent:|$)"
    noes_pattern = r"Noes:\s*(.*?)(?=\s*Absent:|$)"
    absent_pattern = r"Absent:\s*(.*?)(?=\.)"

    # Extract Ayes
    ayes_match = re.search(ayes_pattern, motion_text)
    if ayes_match:
        ayes_members = split_vote_list(ayes_match.group(1))
        for name in ayes_members:
            if name.lower() != "none":
                votes.append({"id": generate_vote_id(motion_id, name, meeting_date), "motion_id": motion_id, "vote": "Aye", "member": name, "created_at": datetime.now().isoformat()})

    # Extract Noes
    noes_match = re.search(noes_pattern, motion_text)
    if noes_match:
        noes_members = split_vote_list(noes_match.group(1))
        for name in noes_members:
            if name.lower() != "none":
                votes.append({"id": generate_vote_id(motion_id, name, meeting_date), "motion_id": motion_id, "vote": "No", "member": name, "created_at": datetime.now().isoformat()})

    # Extract Absent
    absent_match = re.search(absent_pattern, motion_text)
    if absent_match:
        absent_members = split_vote_list(absent_match.group(1))
        for name in absent_members:
            if name.lower() != "none":
                votes.append({"id": generate_vote_id(motion_id, name, meeting_date), "motion_id": motion_id, "vote": "Absent", "member": name, "created_at": datetime.now().isoformat()})

    return votes


def parse_minutes(lines: List[str]):
    subjects = []
    motions = []
    votes = []

    meeting_date = None
    current_subject = None
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # meeting date
        if find_date_in_line(line) and not meeting_date:
            meeting_date = find_date_in_line(line)

        # SUBJECT block — capture only all-caps title and extract PR #
        if line.startswith("SUBJECT:"):
            subject_lines = [line.replace("SUBJECT:", "").strip()]
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                # Check if the next line starts with all caps (the title portion)
                if next_line.isupper():
                    subject_lines.append(next_line)
                else:
                    break
                i += 1

            # Join the all caps lines as the subject title
            subject_text = " ".join(subject_lines)
            # # Check for PR # pattern in the text
            # pr_match = re.search(r"PR #(\d+)", subject_text)
            # if pr_match:
            #     pr_id = int(pr_match.group(1))  # Extract PR #
            subject_id = generate_subject_id(subject_text)

            current_subject = {
                "id": subject_id, # Include PR # as ID
                "title": subject_text,
                "created_at": datetime.now().isoformat()
            }
            subjects.append(current_subject)
            continue  # i already moved forward

        # MOTION
        elif line.startswith("MOTION by"):
            if current_subject:
              motion_lines = [line]
              i += 1
              while i < len(lines):
                  next_line = lines[i].strip()
                  if next_line.startswith("MOTION by") or next_line.startswith("SUBJECT:") or re.match(r"\[.*\]", next_line):
                      break
                  motion_lines.append(next_line)
                  i += 1
              full_motion_text = " ".join(motion_lines)
              motion_id = generate_motion_id(current_subject["title"] if current_subject else None, full_motion_text, meeting_date)
              motions.append({
                  "id": motion_id,
                  "subject_id": current_subject["id"] if current_subject else None,
                  "motion_text": full_motion_text,
                  "meeting_date": meeting_date,
                  "created_at": datetime.now().isoformat()
              })

              votes.extend(parse_votes(full_motion_text, motion_id, meeting_date))

              continue  # i already moved forward

        i += 1

    return {
        "subjects": subjects,
        "motions": motions,
        "votes": votes
    }


def extract_contents(url):
  response = requests.get(url)
  file = io.BytesIO(response.content)

  with pdfplumber.open(file) as pdf:
      full_text = "\n".join(page.extract_text() for page in pdf.pages)

  lines = full_text.split('\n')

  data = parse_minutes(lines)

  return data


# print([vote for vote in extract_contents("https://www.durhamnc.gov/AgendaCenter/ViewFile/Minutes/_01212025-2971")['votes'] if vote['member'] == ''])
