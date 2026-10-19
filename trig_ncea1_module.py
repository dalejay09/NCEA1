import streamlit as st
import random
import math
import io
import json
import os
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
from pydantic import BaseModel, Field

# --- Import our Universal AI Marking Suite ---
import ai_marking_component

# --- AI Output Schemas ---
class SolutionRow(BaseModel):
    q_num: int = Field(description="The question number (1 to 20)")
    steps: str = Field(description="Step-by-step solving method using valid LaTeX formatting")

class AIWorksheetSolutions(BaseModel):
    solutions: list[SolutionRow]

class WordProblemOutput(BaseModel):
    problem_text: str = Field(description="The problem statement text")
    target_variable: str = Field(description="The target variable name")

# --- Math Engine: TRIGONOMETRY (Graphical) ---
def generate_trig_problem(topic_setting, level="1"):
    if topic_setting == "Both":
        topic = random.choice(["Pythagoras", "Trigonometry"])
    else:
        topic = topic_setting

    base_a, base_b = random.randint(4, 12), random.randint(4, 12)
    hyp_real = math.hypot(base_a, base_b)
    angle_rad = math.atan2(base_a, base_b)
    angle_deg = round(math.degrees(angle_rad))
    
    opp_val = round(base_a, 1) if base_a % 1 != 0 else base_a
    adj_val = round(base_b, 1) if base_b % 1 != 0 else base_b
    hyp_val = round(hyp_real, 1) if hyp_real % 1 != 0 else int(hyp_real)

    side_var = random.choice(['x', 'y', 'z', 'a', 'b', 'c', 'h', 'p', 'q'])
    angle_var = random.choice([r'\theta', r'\alpha', r'\beta', r'\gamma', r'\phi', 'x', 'y'])

    labels = {'opp': '', 'adj': '', 'hyp': '', 'angle': ''}
    ans = 0
    text_desc = ""
    target_var = ""
    rule_key = ""
    sub_type = ""

    if topic == "Pythagoras":
        rule_key = "Pythagoras"
        target = random.choice(['hyp', 'leg1', 'leg2'])
        target_var = side_var
        if target == 'hyp':
            sub_type = "hyp"
            labels['opp'], labels['adj'], labels['hyp'] = opp_val, adj_val, side_var
            ans, text_desc = hyp_val, f"Legs {opp_val}, {adj_val}. Find hyp {side_var}."
        elif target == 'leg1':
            sub_type = "leg"
            labels['opp'], labels['adj'], labels['hyp'] = side_var, adj_val, hyp_val
            ans, text_desc = opp_val, f"Hyp {hyp_val}, Leg {adj_val}. Find leg {side_var}."
        else:
            sub_type = "leg"
            labels['opp'], labels['adj'], labels['hyp'] = opp_val, side_var, hyp_val
            ans, text_desc = adj_val, f"Hyp {hyp_val}, Leg {opp_val}. Find leg {side_var}."
    else:
        base_rule = random.choice(["Sine", "Cosine", "Tangent"])
        find_angle = random.choice([True, False])
        
        if find_angle:
            rule_key = f"{base_rule} Inverse"
            sub_type = "angle"
        else:
            rule_key = base_rule
            sub_type = random.choice(["side_opp", "side_hyp"])
            
        if base_rule == "Sine":
            if find_angle:
                target_var = angle_var
                labels['opp'], labels['hyp'], labels['angle'] = opp_val, hyp_val, angle_var
                ans, text_desc = angle_deg, f"Opp {opp_val}, Hyp {hyp_val}. Find angle {angle_var}."
            else:
                target_var = side_var
                if random.choice([True, False]):
                    labels['opp'], labels['hyp'], labels['angle'] = side_var, hyp_val, f"{angle_deg}^\\circ"
                    ans, text_desc = opp_val, f"Angle {angle_deg}, Hyp {hyp_val}. Find Opp {side_var}."
                else:
                    labels['opp'], labels['hyp'], labels['angle'] = opp_val, side_var, f"{angle_deg}^\\circ"
                    ans, text_desc = hyp_val, f"Angle {angle_deg}, Opp {opp_val}. Find Hyp {side_var}."
        elif base_rule == "Cosine":
            if find_angle:
                target_var = angle_var
                labels['adj'], labels['hyp'], labels['angle'] = adj_val, hyp_val, angle_var
                ans, text_desc = angle_deg, f"Adj {adj_val}, Hyp {hyp_val}. Find angle {angle_var}."
            else:
                target_var = side_var
                if random.choice([True, False]):
                    labels['adj'], labels['hyp'], labels['angle'] = side_var, hyp_val, f"{angle_deg}^\\circ"
                    ans, text_desc = adj_val, f"Angle {angle_deg}, Hyp {hyp_val}. Find Adj {side_var}."
                else:
                    labels['adj'], labels['hyp'], labels['angle'] = adj_val, side_var, f"{angle_deg}^\\circ"
                    ans, text_desc = hyp_val, f"Angle {angle_deg}, Adj {adj_val}. Find Hyp {side_var}."
        elif base_rule == "Tangent":
            if find_angle:
                target_var = angle_var
                labels['opp'], labels['adj'], labels['angle'] = opp_val, adj_val, angle_var
                ans, text_desc = angle_deg, f"Opp {opp_val}, Adj {adj_val}. Find angle {angle_var}."
            else:
                target_var = side_var
                if random.choice([True, False]):
                    labels['opp'], labels['adj'], labels['angle'] = side_var, adj_val, f"{angle_deg}^\\circ"
                    ans, text_desc = opp_val, f"Angle {angle_deg}, Adj {adj_val}. Find Opp {side_var}."
                else:
                    labels['opp'], labels['adj'], labels['angle'] = adj_val, side_var, f"{angle_deg}^\\circ"
                    ans, text_desc = adj_val, f"Angle {angle_deg}, Opp {opp_val}. Find Adj {side_var}."

    l2_type = None
    l2_label = ""
    if level == "2" and topic != "Pythagoras":
        if find_angle:
            l2_type = random.choice(['parallel_Z', 'vertical_opp'])
            l2_label = f"{angle_var}"
        else:
            l2_type = random.choice(['complement', 'supplementary', 'parallel_Z', 'vertical_opp'])
            if l2_type == 'complement':
                l2_label = f"{90 - angle_deg}^\\circ"
            elif l2_type == 'supplementary':
                l2_label = f"{180 - angle_deg}^\\circ"
            elif l2_type == 'parallel_Z':
                l2_label = f"{angle_deg}^\\circ"
            elif l2_type == 'vertical_opp':
                l2_label = f"{angle_deg}^\\circ"
        labels['angle'] = ""

    return labels, rule_key, ans, text_desc, (opp_val, adj_val), target_var, sub_type, hyp_real, angle_deg, l2_type, l2_label

# --- Equations Generator ---
def build_equations(problem_data, topic_setting):
    labels, rule_key, ans, text_desc, (opp_val, adj_val), target_var, sub_type, hyp_real, angle_deg, l2_type, l2_label = problem_data
    hyp_val = round(hyp_real, 1) if hyp_real % 1 != 0 else int(hyp_real)
    t_disp = target_var.replace(r'\theta', 'θ').replace(r'\alpha', 'α').replace(r'\beta', 'β').replace(r'\gamma', 'γ').replace(r'\phi', 'ϕ')

    if rule_key == "Pythagoras":
        if sub_type == "hyp":
            correct = f"{t_disp} = √({opp_val}² + {adj_val}²)"
            distractor1 = f"{t_disp} = √({opp_val}² - {adj_val}²)"
            if topic_setting == "Both":
                trig_fn = random.choice(["sin", "cos", "tan"])
                distractor2 = f"{t_disp} = {opp_val} / {trig_fn}({angle_deg}°)"
            else:
                distractor2 = f"{t_disp} = {opp_val}² + {adj_val}²"
        else:
            other_side = adj_val if labels['opp'] == target_var else opp_val
            correct = f"{t_disp} = √({hyp_val}² - {other_side}²)"
            distractor1 = f"{t_disp} = √({hyp_val}² + {other_side}²)"
            if topic_setting == "Both":
                trig_fn = random.choice(["sin", "cos", "tan"])
                distractor2 = f"{t_disp} = {other_side} × {trig_fn}({angle_deg}°)"
            else:
                distractor2 = f"{t_disp} = {hyp_val}² - {other_side}²"
    else:
        base = rule_key.replace(" Inverse", "")
        fn = "sin" if base == "Sine" else ("cos" if base == "Cosine" else "tan")
        wrong_fn_map = {"sin": "cos", "cos": "tan", "tan": "sin"}
        w_fn = wrong_fn_map[fn]
        
        if "Inverse" in rule_key:
            num = opp_val if base == "Sine" else (adj_val if base == "Cosine" else opp_val)
            den = hyp_val if base != "Tangent" else adj_val
            inv_fn = "sin⁻¹" if fn == "sin" else ("cos⁻¹" if fn == "cos" else "tan⁻¹")
            w_inv_fn = "sin⁻¹" if w_fn == "sin" else ("cos⁻¹" if w_fn == "cos" else "tan⁻¹")
            correct = f"{t_disp} = {inv_fn}({num} / {den})"
            distractor1 = f"{t_disp} = {w_inv_fn}({num} / {den})"
            distractor2 = f"{t_disp} = {inv_fn}({den} / {num})"
        else:
            if labels['opp'] == target_var or labels['adj'] == target_var:
                known_side = hyp_val if base != "Tangent" else (adj_val if base == "Sine" else opp_val)
                correct = f"{t_disp} = {known_side} × {fn}({angle_deg}°)"
                distractor1 = f"{t_disp} = {known_side} × {w_fn}({angle_deg}°)"
                distractor2 = f"{t_disp} = {known_side} / {fn}({angle_deg}°)"
            else:
                known_side = opp_val if base == "Sine" else (adj_val if base == "Cosine" else opp_val)
                correct = f"{t_disp} = {known_side} / {fn}({angle_deg}°)"
                distractor1 = f"{t_disp} = {known_side} / {w_fn}({angle_deg}°)"
                distractor2 = f"{t_disp} = {known_side} × {fn}({angle_deg}°)"

    return correct, distractor1, distractor2

# --- Word Problem Engine ---
def generate_word_problem(level):
    from google import genai
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    
    if level == "1":
        prompt_choices = [
            "Act as an NCEA Level 1 Mathematics assessment writer. Generate a single right-angled triangle word problem involving either an angle of elevation, an angle of depression, or a leaning ladder. Randomize the real-world context, side lengths, and angle values.",
            "Act as an NCEA Level 1 Mathematics assessment writer. Generate a 'Shared Wall' back-to-back right-angled triangle word problem (e.g., a surveyor measuring angles to two separate towers from a central point, or a roof truss split by a central support pillar). Random