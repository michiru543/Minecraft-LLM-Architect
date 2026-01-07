import time
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from chains.model_style import get_style_description
from chains.model_modules import generate_module_names
from chains.model_furniture import generate_furniture
from chains.model_layout import generate_layout
from chains.model_connections import generate_connections
from chains.model_structure_json import generate_structure_json
from chains.model_code import generate_code_and_save
from utils.load_functions import load_material_map
from utils.save_log import save_raw_response

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-pro")

INPUT_PRICE_PER_1M = 1.25
OUTPUT_PRICE_PER_1M = 10.00

step_logs = []

def calculate_cost(input_tokens, output_tokens):
    input_cost = (input_tokens / 1_000_000) * INPUT_PRICE_PER_1M
    output_cost = (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_1M
    return input_cost + output_cost

def log_step(step_name, duration, usage_data):
    if not usage_data:
        usage_data = {'input_tokens': 0, 'output_tokens': 0}

    input_tokens = usage_data.get('input_tokens', 0)
    output_tokens = usage_data.get('output_tokens', 0)

    cost = calculate_cost(input_tokens, output_tokens)

    log_entry = {
        "name": step_name,
        "duration": duration,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cost": cost
    }
    step_logs.append(log_entry)

    print(
        f"[{step_name}] Time: {duration:.2f}s | Real Tokens: In {input_tokens} / Out {output_tokens} | Cost: ${cost:.5f}")
    return log_entry

def run_task_with_timing(func, *args):
    start = time.perf_counter()
    try:
        content, usage = func(*args)
    except ValueError:
        content = func(*args)
        usage = {}
        print(f"Warning: {func.__name__} did not return usage data.")

    end = time.perf_counter()
    duration = end - start

    return (content, usage), duration


if __name__ == "__main__":
    materials_map = load_material_map("materials/materials.txt")
    material_list = ",".join(materials_map.values())

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_save_path = f"generated/log_{timestamp}.txt"
    code_save_path = f"generated/code_{timestamp}.py"

    user_input = input("Please enter a description of the building:\n> ").strip()
    if not user_input:
        user_input = None

    use_image = input("Upload image? (y/n):\n> ").strip().lower()
    image_path = None
    if use_image == "y":
        while True:
            path_input = input("Image path:\n> ").strip()
            if path_input.lower() == 'q': break
            if os.path.exists(path_input):
                image_path = path_input
                break
            else:
                print("Error: Image not found.")

    if image_path:
        print(f"Image set: {image_path}")

    input_log = f"Model: {MODEL_NAME}\nPrompt: {user_input}\nImage: {image_path}"
    save_raw_response(input_log, log_save_path, "--- Input Settings ---")

    print("\n" + "=" * 60)
    print(f"   STARTING GENERATION (Real Token Tracking)   ")
    print("=" * 60 + "\n")

    total_start_time = time.perf_counter()

    # --- Step 1: Style ---
    (style, style_usage), dur = run_task_with_timing(get_style_description, user_input, material_list, image_path)
    save_raw_response(style, log_save_path, "\nBuilding Style:")
    log_step("Style Generation", dur, style_usage)

    # --- Step 2: Modules ---
    (modules, modules_usage), dur = run_task_with_timing(generate_module_names, style)
    save_raw_response(modules, log_save_path, "\n\nModule Name:")
    log_step("Module Definition", dur, modules_usage)

    # --- Step 3 & 4: Furniture & Layout ---
    print("\n>>> Starting Parallel Execution (Furniture & Layout)...")
    parallel_start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_furn = executor.submit(run_task_with_timing, generate_furniture, style, modules, material_list)
        future_layout = executor.submit(run_task_with_timing, generate_layout, style, modules)

        (furniture, furn_usage), dur_furn = future_furn.result()
        (layout, layout_usage), dur_layout = future_layout.result()

    parallel_dur = time.perf_counter() - parallel_start
    print(f">>> Parallel block finished in {parallel_dur:.2f}s\n")

    save_raw_response(furniture, log_save_path, "\n\nModule Furniture:")
    log_step("Furniture Gen", dur_furn, furn_usage)

    save_raw_response(layout, log_save_path, "\n\nModule Layout:")
    log_step("Layout Gen", dur_layout, layout_usage)

    # --- Step 5: Connections ---
    (connections, conn_usage), dur = run_task_with_timing(generate_connections, layout)
    save_raw_response(connections, log_save_path, "\n\nModule Connections:")
    log_step("Connection Logic", dur, conn_usage)

    # --- Step 6: JSON ---
    (structure_json, json_usage), dur = run_task_with_timing(generate_structure_json, style, modules, layout,
                                                             connections, furniture, material_list)
    save_raw_response(structure_json, log_save_path, "\n\nStructure Layout(JSON):")
    log_step("JSON Construction", dur, json_usage)

    # --- Step 7: Code ---
    (code_gen, code_usage), dur = run_task_with_timing(generate_code_and_save, layout, structure_json, code_save_path)
    save_raw_response(code_gen, log_save_path, "\n\nCode Generation:")
    log_step("Code Writing", dur, code_usage)

    # --- Cost Info ---
    total_elapsed = time.perf_counter() - total_start_time
    total_cost = sum(item['cost'] for item in step_logs)
    total_tokens_in = sum(item['input_tokens'] for item in step_logs)
    total_tokens_out = sum(item['output_tokens'] for item in step_logs)

    print("\n" + "=" * 70)
    print(f"          FINAL PERFORMANCE REPORT ({MODEL_NAME})          ")
    print("=" * 70)

    report_lines = []
    report_lines.append(f"\nModel Used: {MODEL_NAME}")
    report_lines.append(f"Price: Input ${INPUT_PRICE_PER_1M}/1M | Output ${OUTPUT_PRICE_PER_1M}/1M")
    report_lines.append("\n--- Detailed Breakdown ---")

    header = f"{'Step Name':<20} | {'Time(s)':<8} | {'In Tok':<8} | {'Out Tok':<8} | {'Cost($)':<10}"
    print(header)
    print("-" * 70)
    report_lines.append(header)
    report_lines.append("-" * 70)

    for log in step_logs:
        line = f"{log['name']:<20} | {log['duration']:<8.2f} | {log['input_tokens']:<8} | {log['output_tokens']:<8} | {log['cost']:<10.5f}"
        print(line)
        report_lines.append(line)

    print("-" * 70)
    report_lines.append("-" * 70)

    summary = f"TOTAL               | {total_elapsed:<8.2f} | {total_tokens_in:<8} | {total_tokens_out:<8} | ${total_cost:.5f}"
    print(summary)
    report_lines.append(summary)

    save_raw_response("\n".join(report_lines), log_save_path, "")

    print(f"\nLog saved to: {log_save_path}")

    print(f"Code saved to: {code_save_path}")

