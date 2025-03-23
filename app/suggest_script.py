import os
import re
import subprocess

print("****Inside Suggest Script****")
def remove_ansi_escape_sequences(text):
    """
    Removes ANSI terminal escape sequences from LLM output (e.g., spinners, colors).
    """
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def clean_llm_output(output):
    """
    Clean terminal spinner characters, backticks, and unnecessary formatting.
    Return only the actual script starting from mbo lines.
    """
    # Remove unnecessary characters or weird terminal sequences
    output = re.sub(r'[⠁-⣿]+', '', output)
    output = re.sub(r"```.*?\n", "", output)
    output = output.replace("```", "")

    # Strip leading/trailing whitespace again after cleanup
    output = output.strip()

    # Extract from first mbo-relevant line
    lines = output.split("\n")
    for i, line in enumerate(lines):
        if 'mbo.' in line or line.strip().startswith("if mbo"):
            return "\n".join(lines[i:]).strip()
    return output

def is_valid_maximo_script(script_text):
    must_have_keywords = ['mbo.', 'mbo.getString(', 'mbo.setValue(', 'mbo.getMboSet(']
    return any(keyword in script_text for keyword in must_have_keywords)

def suggest_script(user_prompt):
    system_prompt = f"""
    You are an expert in IBM Maximo Automation Scripting
    Always return ONLY the script code in Jython.
    Never include markdown, comments, explanation, or blank lines.
    Use Maximo MBO API like mbo.getString(), mbo.setValue(), etc.
    You need to generate automation script. Refer to examples given below to understand how to generate proper script.
    Examples:
    Prompt: When Work Type is CM, make failurecode mandatory.
    Script:
    if mbo.getString("WORKTYPE") == "CM":
        if not mbo.getString("FAILURECODE"):
            errorkey = "missing_failurecode"
            errorgroup = "custom"
            params = ["FAILURECODE"]
            raise MXApplicationException(errorgroup, errorkey, params)

    Prompt: When Service Request's location starts with 'PLT', set siteid as 'PLANT'.
    Script:
    location = mbo.getString("LOCATION")
    if location.startswith("PLT"):
        mbo.setValue("SITEID", "PLANT",11L)

    Prompt: Propulate Priroity of Asset to Work Order Prirotiy.
    Script:
    assetSet=mbo.getMboSet("ASSET")
    if !assetSet.isEmpty():
        asset_priority=mbo.getString("PRIORITY")
        mbo.setValue("WOPRIORITY",asset_priority,11L)
    Now Prompt to generate automation script: {user_prompt.strip()}
    """

    try:
        # Log prompt to file
        log_dir = os.path.join(os.path.dirname(__file__), "../data")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "prompt_log.txt")
        print(log_path)

        with open(log_path, "a") as logf:
            logf.write(user_prompt.strip() + "\n")
            logf.write("\n==== New Prompt Sent to LLM ====\n")
            logf.write(system_prompt.strip() + "\n")

        model_name = "mistral:latest"
        response = subprocess.check_output(
            ["ollama", "run", model_name, system_prompt],
            stderr=subprocess.STDOUT
        )

        script_output = response.decode("utf-8").strip()
        script_output = remove_ansi_escape_sequences(script_output)
        clean_output= clean_llm_output(script_output)

        # Optional validation
        if is_valid_maximo_script(clean_output):
            print(clean_output)
            return clean_output
        else:
            return "❌ LLM generated output doesn't look like a valid Maximo Automation Script."

    except subprocess.CalledProcessError as e:
        return "❌ LLM call failed:\n" + remove_ansi_escape_sequences(e.output.decode("utf-8"))
