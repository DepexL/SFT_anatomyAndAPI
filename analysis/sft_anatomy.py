import pandas as pd
from pathlib import Path
from collections import Counter
import re

ROOT = Path(__file__).resolve().parent.parent

dataset_path = ROOT / "data" / "dr-tulu-sft-cleaned" / "deep-research-tulu-sft-data-cleaned.parquet"

df = pd.read_parquet(dataset_path)


# 1 Uzd:
print("\n1 užduotis\n")
print("Dataset dydis:")
print(df.shape)

print("\nTop-level laukai:")
print(df.columns.tolist())


print("\nPilni 2 įrašų laukai:")
for i in range(2):

    for key, value in df.iloc[i].to_dict().items():
        if key != "conversations":
            print(f"{key}: {value}\n")

    for item in df.iloc[i]['conversations']:
        print(f"ROLE: {item['role']}")
        print(f"CONTENT: {item['content']}")
        print("-" * 50) 


# 2 Uzd:

print("\n2 užduotis\n")

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

print("Naudojami įrankiai")
for tool, count in tool_counts.most_common():
    print(f"\n{tool}: {count}")


# 3 Uzd: