import pandas as pd
from pathlib import Path
from collections import Counter
from collections import defaultdict
import statistics
import re


ROOT = Path(__file__).resolve().parent.parent

dataset_path = ROOT / "data" / "dr-tulu-sft-cleaned" / "deep-research-tulu-sft-data-cleaned.parquet"

df = pd.read_parquet(dataset_path)


# 1 Uzd:

def data_showcase(kiekis):
    print("\n1 uzduotis\n")
    print("Dataset dydis:")
    print(df.shape)

    print("\nTop-level laukai:")
    print(df.columns.tolist())

    print("\nPilni 2 irasu laukai:")
    for i in range(kiekis):
        for key, value in df.iloc[i].to_dict().items():
            if key != "conversations":
                print(f"{key}: {value}\n")

        for item in df.iloc[i]['conversations']:
            print(f"ROLE: {item['role']}")
            print(f"CONTENT: {item['content']}")
            print("-" * 50)




# 2 Uzd:
def count_tool_calls():
    print("\n2 uzduotis\n")

    tool_counts = Counter()

    for conversations in df['conversations']:
        for item in conversations:
            if item['role'] == 'tool_call':
                content = item['content']

                # suranda name reikšmę
                match = re.search(r'"name":\s*"([^"]+)"', content)

                if match:
                    tool_name = match.group(1)
                    tool_counts[tool_name] += 1

    print("Naudojami irankiai")
    for tool, count in tool_counts.most_common():
        print(f"\n{tool}: {count}")





# 3 Uzd:

def detect_type(value):

    value = value.strip()

    # string
    if value.startswith('"') and value.endswith('"'):
        return "str", value.strip('"')

    # bool
    if value.lower() == "true":
        return "bool", True

    if value.lower() == "false":
        return "bool", False

    # null
    if value.lower() == "null":
        return "null", None

    # int
    if re.fullmatch(r"-?\d+", value):
        return "int", int(value)

    # float
    if re.fullmatch(r"-?\d+\.\d+", value):
        return "float", float(value)

    # list
    if value.startswith("[") and value.endswith("]"):
        return "list", value

    # dict
    if value.startswith("{") and value.endswith("}"):
        return "dict", value

    return "unknown", value



def extract_tool_arguments():

    print("\n3 uzduotis\n")


    tools_args = {}


    for conversations in df['conversations']:

        for item in conversations:


            if item['role'] == 'tool_call':

                content = item['content']


                # Surandame tool pavadinimą
                tool_match = re.search(
                    r'"name":\s*"([^"]+)"',
                    content
                )


                if tool_match:

                    tool_name = tool_match.group(1)


                    # Sukuriame vietą tool jei dar nėra
                    if tool_name not in tools_args:
                        tools_args[tool_name] = {}


                    # Surandame arguments
                    args_match = re.search(
                        r'"arguments":\s*\{(.*?)\}',
                        content,
                        re.DOTALL
                    )


                    if args_match:

                        args_text = args_match.group(1)


                        args = re.findall(
                            r'"([^"]+)":\s*("(?:[^"\\]|\\.)*"|\[[^\]]*\]|\{[^\}]*\}|true|false|null|-?\d+\.\d+|-?\d+)',
                            args_text
                        )


                        for arg, value in args:


                            value_type, value = detect_type(value)


                            # Sukuriame vietą argumentui
                            if arg not in tools_args[tool_name]:
                                tools_args[tool_name][arg] = []


                            # Pridedame rastą tipą ir pavyzdį
                            tools_args[tool_name][arg].append({
                                "type": value_type,
                                "example": value
                            })


    # Sukuriame lentelę
    rows = []


    for tool, args in tools_args.items():

        for arg, values in args.items():

            types = []
            examples = []


            for item in values:

                if item["type"] not in types:
                    types.append(item["type"])

                if len(examples) < 2:
                    examples.append(item["example"])


            rows.append({
                "Tool": tool,
                "Argumentas": arg,
                "Tipai": ", ".join(types),
                "Pavyzdziai": examples
            })


    table = pd.DataFrame(rows)


    print(table.to_string(index=False))






# 4 Uzd:

def analyze_tool_calls():
    print("\n4 uzduotis\n")


    tool_calls_per = []

    for conversations in df['conversations']:

        count = 0

        for item in conversations:
            if item['role'] == 'tool_call':
                count += 1

        tool_calls_per.append(count)


    print("Trajektoriju statistika:")
    print(f"Min: {min(tool_calls_per)}")
    print(f"Max: {max(tool_calls_per)}")
    print(f"Mediana: {statistics.median(tool_calls_per)}")

    # Vieno ir daugiažingsnių grandinių skaičius

    single_step = 0
    multi_step = 0

    for x in tool_calls_per:
        if x == 1:
            single_step += 1

    for x in tool_calls_per:
        if x > 1:
            multi_step += 1


    print("\nGrandiniu iskvietimai:")
    print(f"Vienas irankio iskvietimas: {single_step}")
    print(f"Daugiaizngsnes grandines (>1): {multi_step}")




# 5 Uzd:
def analyze_answers():
    print("\n5 uzduotis\n")

    i = 0

    for conversations in df['conversations']:
        for item in conversations:
            if item['role'] == 'answer':
                i += 1

                content = item['content']

                if len(content) > 500:
                    content = content[:998] + "... </answer>"

                print(f"\n{content}")

                if i >= 2:
                    return



# 6 uzd

def analyze_broken_trajectories():
    print("\n6 uzduotis\n")

    broken_json = 0
    empty_answers = 0
    broken_trajectory = 0

    for conversations in df["conversations"]:

        has_tool_call = False
        has_tool_output = False
        has_answer = False

        for item in conversations:

            role = item["role"]
            content = item["content"]

            # tikrinam tool_call formatą
            if role == "tool_call":
                has_tool_call = True

                if not re.search(r'"name"\s*:\s*".+?"', content):
                    broken_json += 1

                if not re.search(r'"arguments"\s*:\s*\{.*\}', content, re.DOTALL):
                    broken_json += 1


            # tikrinam atsakymus
            if role == "answer":
                has_answer = True

                if not content.strip():
                    empty_answers += 1


            if role == "tool_output":
                has_tool_output = True


        # jei yra tool_call, bet nėra rezultato arba atsakymo
        if has_tool_call and (not has_tool_output or not has_answer):
            broken_trajectory += 1


    print(f"Luze JSON argumentai: {broken_json}")
    print(f"Tusti atsakymai: {empty_answers}")
    print(f"Nutrukusios trajektorijos: {broken_trajectory}")



if __name__ == "__main__":

    # 1 uzd
    data_showcase(2)

    # 2 uzd
    count_tool_calls()

    # 3 uzd
    extract_tool_arguments()

    # 4 uzd
    analyze_tool_calls()

    # 5 uzd
    analyze_answers()

    # 6 uzd
    analyze_broken_trajectories()